"""
Automatic blog-post generator for elearningfrcpath.in.

Sources a topic from Google Trends (rising queries around FRCPath /
NEET-SS seed terms), asks Groq (Llama 3.3 70B) to write a full post
following .claude/instructions.md, and saves + commits it locally.

This script does NOT push. Review `git log` / `git diff` and run
`git push` yourself once you're happy with a generated post.

Requires GROQ_API_KEY to be set as an environment variable — never
hardcode it here or commit it anywhere.
"""

import os
import re
import random
import subprocess
from datetime import date

from groq import Groq
from pytrends.request import TrendReq

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTRUCTIONS_FILE = os.path.join(REPO, ".claude", "instructions.md")
USED_FILE = os.path.join(REPO, "scripts", "used_topics.txt")
BLOG_DIR = os.path.join(REPO, "content", "blog")

MODEL = "llama-3.3-70b-versatile"
MIN_WORDS = 1500
MAX_RETRIES = 3  # 1 initial attempt + 2 retries with failure feedback
BODY_MAX_TOKENS = 5500   # body-only generation, no schema — fits free-tier TPM
SCHEMA_MAX_TOKENS = 2000  # schema-only generation is short

FORMATS = [
    "case-based",
    "comparison",
    "MCQ-heavy",
    "news-update",
    "deep-dive",
    "mnemonic-focused",
]

TREND_SEEDS = [
    "FRCPath",
    "NEET SS pathology",
    "histopathology",
    "WHO 5th edition pathology",
    "NEET INI CET pathology",
]

FALLBACK_TOPIC = "High-yield pathology topic for FRCPath and NEET-SS"

# (label, detection/sanitize regex, replacement text)
FORBIDDEN_PATTERNS = [
    ("delve", r"\bdelv\w*\s+into\b", "look into"),
    ("delve", r"\bdelv\w*\b", "explore"),
    ("crucial", r"\bcrucial\w*\b", "important"),
    ("it's important to note", r"\bit'?s important to note(?: that)?\b", ""),
    ("it is worth noting", r"\bit is worth noting(?: that)?\b", ""),
    ("in conclusion", r"\bin conclusion,?\b", "Overall,"),
    ("comprehensive guide", r"\bcomprehensive\s+guide\w*\b", "guide"),
    ("in the realm of", r"\bin the realm of\b", "in"),
]


def get_used() -> set:
    if not os.path.exists(USED_FILE):
        return set()
    with open(USED_FILE, encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_used(topic: str) -> None:
    os.makedirs(os.path.dirname(USED_FILE), exist_ok=True)
    with open(USED_FILE, "a", encoding="utf-8") as f:
        f.write(topic + "\n")


def get_trending_topics() -> list:
    topics = []
    try:
        pt = TrendReq(hl="en-IN", tz=330)
        pt.build_payload(TREND_SEEDS, geo="IN", timeframe="today 1-m")
        related = pt.related_queries()
        for kw in TREND_SEEDS:
            data = related.get(kw, {}).get("rising")
            if data is not None:
                topics += data["query"].tolist()
    except Exception as e:
        print("pytrends failed:", e)
    return topics


def pick_topic() -> str:
    used = get_used()
    candidates = [t for t in get_trending_topics() if t not in used]
    if not candidates:
        candidates = [FALLBACK_TOPIC]
    return random.choice(candidates)


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")[:60]


def split_front_matter(content: str):
    """Return (front_matter_text, body_text) for a '---\\n...\\n---\\n' post."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return "", content
    return match.group(1), match.group(2)


def normalize_front_matter(content: str, topic: str) -> tuple:
    """Force date to today and slug to match a deterministic filename.

    Returns (fixed_content, filename_slug). Model output for these two
    fields is unreliable (wrong dates, slug/filename drift), so they are
    corrected deterministically rather than relying on a retry.
    """
    front, body = split_front_matter(content)
    if not front:
        return content, slugify(topic)

    today_str = date.today().isoformat()
    filename_slug = slugify(topic)

    if re.search(r"^date:\s*.*$", front, re.MULTILINE):
        front = re.sub(r"^date:\s*.*$", f"date: {today_str}", front, flags=re.MULTILINE)
    else:
        front += f"\ndate: {today_str}"

    if re.search(r'^slug:\s*.*$', front, re.MULTILINE):
        front = re.sub(r'^slug:\s*.*$', f'slug: "{filename_slug}"', front, flags=re.MULTILINE)
    else:
        front += f'\nslug: "{filename_slug}"'

    fixed = f"---\n{front.strip()}\n---\n{body}"
    return fixed, filename_slug


def validate_body(content: str) -> list:
    """Check the generated post body (no schema yet) against instructions.md.

    Returns a list of human-readable violations; empty list means pass.
    """
    errors = []
    front, body = split_front_matter(content)

    if not front:
        errors.append("Missing YAML front matter block (--- ... ---).")

    if "draft: false" not in front:
        errors.append('Front matter must set "draft: false".')

    if not re.search(r"^cover:\s*$", front, re.MULTILINE) or "image:" not in front:
        errors.append("Front matter must include a cover.image URL.")

    word_count = len(re.findall(r"\b\w+\b", body))
    if word_count < MIN_WORDS:
        errors.append(f"Body is only ~{word_count} words; needs at least {MIN_WORDS}.")

    for label, pattern, _ in FORBIDDEN_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f'Contains forbidden phrase: "{label}".')

    mcq_count = len(re.findall(r"\*\*Q\d+\.\*\*", body))
    if mcq_count < 3:
        errors.append(f"Found {mcq_count} MCQs; needs at least 3 (format: **Q1.**).")

    details_count = len(re.findall(r"<details>", body, re.IGNORECASE))
    if details_count < mcq_count:
        errors.append("Not every MCQ has an expandable <details> answer block.")

    if "elearningfrcpath.com" not in body:
        errors.append("Missing internal link(s) to elearningfrcpath.com.")

    return errors


def validate_schema(schema_block: str) -> list:
    """Check a standalone JSON-LD <script> block for required schema types."""
    errors = []

    if not re.search(r'<script type="application/ld\+json">', schema_block):
        errors.append('Missing <script type="application/ld+json"> schema block.')
        return errors

    for schema_type in ('"@type": "Article"', '"@type": "FAQPage"', '"@type": "BreadcrumbList"'):
        if schema_type not in schema_block:
            errors.append(f"JSON-LD schema is missing {schema_type}.")

    question_count = schema_block.count('"@type": "Question"')
    if question_count < 5:
        errors.append(f"FAQPage schema has {question_count} questions; needs at least 5.")

    return errors


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set. "
            "Set it with: setx GROQ_API_KEY \"your-new-key\" (then restart the shell)."
        )
    return Groq(api_key=api_key)


def sanitize_forbidden_phrases(text: str) -> str:
    """Deterministically swap out forbidden filler phrases the model keeps using.

    Retrying on this alone wastes tokens/attempts against a model that
    reliably reaches for these words regardless of instructions, so fix
    them the same way date/slug drift is fixed: directly, not by asking
    the model to try again.
    """
    for _, pattern, replacement in FORBIDDEN_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


INTERNAL_LINKS = [
    ("https://elearningfrcpath.com/", "the eLearning FRCPath homepage"),
    ("https://elearningfrcpath.com/frcpath-part-1-histopathology-course", "the FRCPath Part 1 histopathology course at eLearning FRCPath"),
    ("https://elearningfrcpath.com/neet-ss-pathology", "the NEET-SS pathology course at eLearning FRCPath"),
    ("https://elearningfrcpath.com/pathology-mcq-2026", "the pathology MCQ bank at elearningfrcpath.com"),
    ("https://elearningfrcpath.com/frcpath-exam-guide-2026", "the FRCPath exam guide at eLearning FRCPath"),
]


def ensure_internal_link(body: str) -> str:
    """Guarantee at least one elearningfrcpath.com link, matching the
    instructions.md requirement, without spending a retry on it."""
    if "elearningfrcpath.com" in body:
        return body

    url, anchor = random.choice(INTERNAL_LINKS)
    sentence = f"\nFor structured, exam-focused revision on this topic, see [{anchor}]({url}).\n"
    marker = "\n## Key Takeaways"
    if marker in body:
        return body.replace(marker, sentence + marker, 1)
    return body.rstrip() + "\n" + sentence


def _run_with_retries(client, system_prompt, user_prompt, max_tokens, validator, label, fixup=None):
    """Call Groq, validate, retry once with failure feedback, else raise."""
    last_errors = []
    for attempt in range(1, MAX_RETRIES + 1):
        # Messages are rebuilt fresh each attempt (not appended) to stay
        # under the provider's tokens-per-minute rate limit on retries.
        prompt = user_prompt
        if last_errors:
            prompt += (
                "\n\nYour previous attempt violated these rules — fix every "
                "one of them this time:\n" + "\n".join(f"- {e}" for e in last_errors)
            )

        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        content = resp.choices[0].message.content
        if fixup:
            content = fixup(content)
        errors = validator(content)

        if not errors:
            return content

        print(f"{label} attempt {attempt} failed validation:")
        for e in errors:
            print(f"  - {e}")
        last_errors = errors

    raise RuntimeError(
        f"{label} failed validation after {MAX_RETRIES} attempts; "
        "not saved or committed. Last errors:\n" + "\n".join(f"- {e}" for e in last_errors)
    )


def generate_body(client: Groq, topic: str, fmt: str) -> str:
    with open(INSTRUCTIONS_FILE, encoding="utf-8") as f:
        system_prompt = f.read()
    system_prompt += (
        f"\n\nWrite this post in a '{fmt}' style/format, distinct from a "
        "standard listicle. Output ONLY the front matter and body Markdown "
        "(everything up to and including the 'Cover image: ...' credit "
        "line) — do NOT include the JSON-LD schema block, it will be "
        "generated separately. No extra commentary before or after. "
        f"Today's date is {date.today().isoformat()}; use it verbatim as the "
        "front matter 'date' field."
    )
    user_prompt = (
        f"Write a full blog post on: {topic}\n\n"
        f"The body (excluding front matter) must be at least {MIN_WORDS} words. "
        "Write full paragraphs with real explanatory depth for every section "
        "(mechanism, morphology, IHC, molecular updates, differential "
        "diagnosis, exam pearls, mnemonic, high-yield table, 3 MCQs with "
        "explanations, 5 FAQs with 50-150 word answers, key takeaways) — "
        "do not stop early or pad with short bullet points to reach length."
    )

    def fixup(content: str) -> str:
        # Forbidden phrases can show up in the title/description too, so
        # sanitize the whole document, not just the body.
        content = sanitize_forbidden_phrases(content)
        front, body = split_front_matter(content)
        if not front:
            return content
        body = ensure_internal_link(body)
        return f"---\n{front.strip()}\n---\n{body}"

    content = _run_with_retries(
        client, system_prompt, user_prompt, BODY_MAX_TOKENS, validate_body, "Body", fixup=fixup
    )
    content, _ = normalize_front_matter(content, topic)
    return content


def generate_schema(client: Groq, topic: str, body_content: str, filename_slug: str) -> str:
    permalink = f"https://elearningfrcpath.in/blog/{filename_slug}/"
    system_prompt = (
        "You generate JSON-LD structured data for a Hugo blog post at "
        "elearningfrcpath.in. Given the post's Markdown content, output "
        "ONLY a single <script type=\"application/ld+json\"> block "
        "containing an @graph array with exactly three entries: an "
        "Article, a FAQPage (pull the actual FAQ questions/answers from "
        "the '## FAQs' section of the post — at least 5 of them, exact "
        "text), and a BreadcrumbList (Home -> Blog -> this post). Use "
        f"\"{permalink}\" as the post URL. No commentary, no markdown "
        "fences, just the raw <script> tag and its contents."
    )
    user_prompt = f"Generate the JSON-LD schema for this post:\n\n{body_content}"

    return _run_with_retries(
        client, system_prompt, user_prompt, SCHEMA_MAX_TOKENS, validate_schema, "Schema"
    )


def generate_post(topic: str, fmt: str) -> str:
    client = _get_client()
    body_content = generate_body(client, topic, fmt)
    _, filename_slug = normalize_front_matter(body_content, topic)
    schema_block = generate_schema(client, topic, body_content, filename_slug)
    return body_content.rstrip() + "\n\n" + schema_block.strip() + "\n"


def save_and_commit(topic: str, content: str) -> str:
    _, filename_slug = normalize_front_matter(content, topic)
    filepath = os.path.join(BLOG_DIR, f"{filename_slug}.md")
    os.makedirs(BLOG_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    save_used(topic)

    subprocess.run(["git", "add", filepath, USED_FILE], cwd=REPO, check=True)
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"Add blog post: {topic} — FRCPath/NEET-SS {date.today().year}\n\n"
            "Generated by scripts/auto_blog.py — review before pushing.",
        ],
        cwd=REPO,
        check=True,
    )
    return filepath


def main():
    topic = pick_topic()
    fmt = random.choice(FORMATS)
    print(f"Selected topic: {topic!r} (format: {fmt})")
    content = generate_post(topic, fmt)
    filepath = save_and_commit(topic, content)
    print(f"Committed: {filepath}")
    print("Review the diff, then run `git push` yourself to publish.")


if __name__ == "__main__":
    main()
