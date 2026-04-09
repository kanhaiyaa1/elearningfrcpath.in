+++
date = '2026-04-08T08:49:04+05:30'
draft = false
title = 'Contact'
description = "Get in touch with the ElearningFRCPath team for queries about FRCPath and NEET SS Pathology courses"
+++

<style>
/* ── Contact Page Layout ─────────────────────────────────────── */
.cf-wrap {
  display: grid;
  grid-template-columns: 1fr 1.8fr;
  gap: 40px;
  max-width: 1000px;
  margin: 40px auto 0;
  align-items: start;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
@media (max-width: 720px) {
  .cf-wrap { grid-template-columns: 1fr; gap: 28px; margin-top: 24px; }
}

/* ── Info Panel ──────────────────────────────────────────────── */
.cf-info {
  background: linear-gradient(160deg, #1a365d 0%, #2b4c7e 60%, #319795 100%);
  border-radius: 16px;
  padding: 36px 28px;
  color: #fff;
}
.cf-info-title {
  font-size: 1.4rem;
  font-weight: 800;
  margin: 0 0 8px;
  color: #fff;
}
.cf-info-sub {
  font-size: 0.9rem;
  color: rgba(255,255,255,0.72);
  line-height: 1.6;
  margin: 0 0 32px;
}
.cf-info-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 22px;
}
.cf-info-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  background: rgba(255,255,255,0.15);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.cf-info-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.55);
  margin-bottom: 3px;
}
.cf-info-value {
  font-size: 0.93rem;
  color: rgba(255,255,255,0.92);
  line-height: 1.4;
}
.cf-info-value a { color: #81e6d9; text-decoration: none; }
.cf-info-value a:hover { text-decoration: underline; }
.cf-response-note {
  margin-top: 28px;
  padding: 14px 16px;
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.18);
  font-size: 0.84rem;
  color: rgba(255,255,255,0.8);
  line-height: 1.55;
}

/* ── Form Panel ──────────────────────────────────────────────── */
.cf-form-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 36px 32px;
  box-shadow: 0 4px 24px rgba(26,54,93,0.08);
}
[data-theme="dark"] .cf-form-card {
  background: #1e293b;
  border-color: #334155;
}
.cf-form-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1a365d;
  margin: 0 0 24px;
}
[data-theme="dark"] .cf-form-title { color: #93c5fd; }

.cf-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 520px) { .cf-row { grid-template-columns: 1fr; } }

.cf-field { margin-bottom: 18px; }
.cf-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 6px;
  letter-spacing: 0.02em;
}
[data-theme="dark"] .cf-label { color: #94a3b8; }
.cf-label span { color: #e53e3e; margin-left: 2px; }

.cf-input, .cf-select, .cf-textarea {
  width: 100%;
  padding: 11px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #2d3748;
  background: #f8fafc;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
  box-sizing: border-box;
}
[data-theme="dark"] .cf-input,
[data-theme="dark"] .cf-select,
[data-theme="dark"] .cf-textarea {
  background: #0f172a;
  border-color: #334155;
  color: #e2e8f0;
}
.cf-input:focus, .cf-select:focus, .cf-textarea:focus {
  border-color: #319795;
  box-shadow: 0 0 0 3px rgba(49,151,149,0.15);
  background: #fff;
}
[data-theme="dark"] .cf-input:focus,
[data-theme="dark"] .cf-select:focus,
[data-theme="dark"] .cf-textarea:focus {
  background: #1e293b;
}
.cf-input::placeholder, .cf-textarea::placeholder { color: #a0aec0; }
[data-theme="dark"] .cf-input::placeholder,
[data-theme="dark"] .cf-textarea::placeholder { color: #475569; }

.cf-textarea { resize: vertical; min-height: 130px; line-height: 1.6; }

/* Submit button */
.cf-submit {
  width: 100%;
  padding: 13px 24px;
  background: linear-gradient(135deg, #1a365d, #319795);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: opacity 0.2s, transform 0.15s;
  margin-top: 6px;
  font-family: inherit;
}
.cf-submit:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.cf-submit:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }

/* Alerts */
.cf-alert {
  padding: 14px 18px;
  border-radius: 8px;
  font-size: 0.92rem;
  font-weight: 500;
  margin-top: 16px;
  display: none;
  align-items: center;
  gap: 10px;
  line-height: 1.5;
}
.cf-alert.show { display: flex; }
.cf-alert-success {
  background: #f0fff4;
  border: 1px solid #9ae6b4;
  color: #276749;
}
.cf-alert-error {
  background: #fff5f5;
  border: 1px solid #feb2b2;
  color: #c53030;
}
[data-theme="dark"] .cf-alert-success { background: #14532d; border-color: #166534; color: #86efac; }
[data-theme="dark"] .cf-alert-error   { background: #450a0a; border-color: #7f1d1d; color: #fca5a5; }

/* Spinner */
.cf-spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: cf-spin 0.7s linear infinite;
  display: none;
}
.cf-submit.loading .cf-spinner { display: block; }
.cf-submit.loading .cf-btn-text { opacity: 0.7; }
@keyframes cf-spin { to { transform: rotate(360deg); } }
</style>

<div class="cf-wrap">

  <!-- ── Left: Info ── -->
  <div class="cf-info">
    <h2 class="cf-info-title">Get in Touch</h2>
    <p class="cf-info-sub">Have a question about our courses, study material, or exam preparation? We typically respond within 24 hours.</p>

    <div class="cf-info-item">
      <div class="cf-info-icon">📧</div>
      <div>
        <div class="cf-info-label">Email</div>
        <div class="cf-info-value"><a href="mailto:info@elearningfrcpath.in">info@elearningfrcpath.in</a></div>
      </div>
    </div>

    <div class="cf-info-item">
      <div class="cf-info-icon">🎓</div>
      <div>
        <div class="cf-info-label">Courses</div>
        <div class="cf-info-value">FRCPath Part 1 &amp; 2 · NEET-SS · INI-SS</div>
      </div>
    </div>

    <div class="cf-info-item">
      <div class="cf-info-icon">🌐</div>
      <div>
        <div class="cf-info-label">Main Platform</div>
        <div class="cf-info-value"><a href="https://elearningfrcpath.com" target="_blank">elearningfrcpath.com</a></div>
      </div>
    </div>

    <div class="cf-info-item">
      <div class="cf-info-icon">🕐</div>
      <div>
        <div class="cf-info-label">Response Time</div>
        <div class="cf-info-value">Within 24–48 hours (Mon–Sat)</div>
      </div>
    </div>

    <div class="cf-response-note">
      💡 For course access issues or payment queries, please mention your registered email in the message for faster resolution.
    </div>
  </div>

  <!-- ── Right: Form ── -->
  <div class="cf-form-card">
    <h3 class="cf-form-title">Send Us a Message</h3>

    <form id="contactForm">
      <!-- Web3Forms access key — get yours free at https://web3forms.com -->
      <input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
      <input type="hidden" name="subject" id="formSubjectHidden" value="New Contact Form Submission — ElearningFRCPath">
      <input type="hidden" name="from_name" value="ElearningFRCPath Contact Form">
      <input type="checkbox" name="botcheck" style="display:none">

      <div class="cf-row">
        <div class="cf-field">
          <label class="cf-label" for="cf-name">Full Name <span>*</span></label>
          <input class="cf-input" type="text" id="cf-name" name="name" placeholder="Dr. Priya Sharma" required>
        </div>
        <div class="cf-field">
          <label class="cf-label" for="cf-phone">Phone Number</label>
          <input class="cf-input" type="tel" id="cf-phone" name="phone" placeholder="+91 98765 43210">
        </div>
      </div>

      <div class="cf-field">
        <label class="cf-label" for="cf-email">Email Address <span>*</span></label>
        <input class="cf-input" type="email" id="cf-email" name="email" placeholder="you@example.com" required>
      </div>

      <div class="cf-field">
        <label class="cf-label" for="cf-subject">I'm interested in</label>
        <select class="cf-select" id="cf-subject" name="interest">
          <option value="">— Select a topic —</option>
          <option>FRCPath Part 1 Preparation</option>
          <option>FRCPath Part 2 Preparation</option>
          <option>NEET-SS Pathology Course</option>
          <option>INI-SS Pathology Preparation</option>
          <option>MCQ Bank / Mock Tests</option>
          <option>Course Access / Technical Issue</option>
          <option>Other</option>
        </select>
      </div>

      <div class="cf-field">
        <label class="cf-label" for="cf-message">Message <span>*</span></label>
        <textarea class="cf-textarea" id="cf-message" name="message" placeholder="Tell us how we can help you…" required></textarea>
      </div>

      <button type="submit" class="cf-submit" id="cf-submit-btn">
        <div class="cf-spinner"></div>
        <span class="cf-btn-text">✉️ Send Message</span>
      </button>

      <div class="cf-alert cf-alert-success" id="cf-success">
        ✅ Message sent! We'll get back to you within 24–48 hours.
      </div>
      <div class="cf-alert cf-alert-error" id="cf-error">
        ❌ Something went wrong. Please email us directly at info@elearningfrcpath.in
      </div>
    </form>
  </div>

</div>

<script>
document.getElementById('contactForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const btn    = document.getElementById('cf-submit-btn');
  const success = document.getElementById('cf-success');
  const error   = document.getElementById('cf-error');

  // Update hidden subject with selected interest
  const interest = document.getElementById('cf-subject').value;
  document.getElementById('formSubjectHidden').value =
    interest ? `[${interest}] Contact Form — ElearningFRCPath` : 'New Contact Form Submission — ElearningFRCPath';

  btn.disabled = true;
  btn.classList.add('loading');
  success.classList.remove('show');
  error.classList.remove('show');

  try {
    const formData = new FormData(this);
    const res = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    if (data.success) {
      success.classList.add('show');
      this.reset();
    } else {
      error.classList.add('show');
    }
  } catch (err) {
    error.classList.add('show');
  } finally {
    btn.disabled = false;
    btn.classList.remove('loading');
  }
});
</script>
