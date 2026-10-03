# Auto Blog Generator

Generates a new FRCPath/NEET-SS blog post every run using Groq (Llama 3.3 70B),
following `.claude/instructions.md` as the system prompt. Saves the post to
`content/blog/` and commits it locally — **it does not push**. Review the
generated post and run `git push` yourself.

## One-time setup

```powershell
pip install -r scripts/requirements.txt
setx GROQ_API_KEY "your-new-groq-key"
```

`setx` sets a persistent user environment variable so Task Scheduler picks it
up too. Restart your terminal (and re-open PowerShell) after running it once
for the variable to take effect. Never put the key in a script or commit it.

## Manual run

```powershell
python scripts\auto_blog.py
```

Then:

```powershell
git log -1 -p        # review the generated post
git push              # publish — this triggers the GitHub Actions deploy
```

If a generated post is unusable, undo the local commit without losing the
working tree: `git reset --soft HEAD~1`, delete the bad file under
`content/blog/`, and remove its line from `scripts/used_topics.txt` so the
topic can be retried later.

## Scheduling with Windows Task Scheduler (every 2 days, 9 AM)

Run once from an elevated PowerShell prompt (adjust the Python path if needed):

```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" `
  -Argument "C:\lance\elearningfrcpath.in\scripts\auto_blog.py" `
  -WorkingDirectory "C:\lance\elearningfrcpath.in"

$trigger = New-ScheduledTaskTrigger -Daily -DaysInterval 2 -At 9am

Register-ScheduledTask -TaskName "FRCPath-AutoBlog" `
  -Action $action -Trigger $trigger -Description "Generate a draft FRCPath/NEET-SS blog post"
```

Because the script only commits (never pushes), each scheduled run leaves a
new commit sitting locally for you to review and push at your convenience —
nothing reaches the live site unattended.

To remove the task later: `Unregister-ScheduledTask -TaskName "FRCPath-AutoBlog" -Confirm:$false`

## Notes

- Topic sourcing uses Google Trends (`pytrends`) seeded from FRCPath/NEET-SS
  terms only — no RSS feed is wired in. Add one later if you have a real
  PubMed saved-search RSS URL.
- `scripts/used_topics.txt` tracks topics already covered so they aren't
  repeated; it's created automatically on first run.
- The LLM output is not guaranteed to satisfy every rule in
  `instructions.md` (word count, MCQ/FAQ counts, schema correctness) —
  always read the generated post before pushing.
