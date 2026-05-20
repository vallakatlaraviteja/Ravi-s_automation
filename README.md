# Ravi's Job Automation System

**One JSON file. Drop your resume URL. Jobs found, scored, and emailed to recruiters — automatically, every day, for $0.**

---

## The Main File

```
workflow/ENHANCED-MASTER-workflow.json
```

This is the **only file you import into n8n**. Everything else in this repo is documentation and deployment config.

**Import URL (paste directly into n8n):**
```
https://raw.githubusercontent.com/vallakatlaraviteja/Ravi-s_automation/main/workflow/ENHANCED-MASTER-workflow.json
```

---

## How It Works (The Complete Flow)

```
YOU DO ONCE (30 min setup):
  1. Upload resume PDF to Google Drive (public link)
  2. Fill your details in the User Config node
  3. Connect credentials (Gmail x4, Groq x4, Sheets, Telegram)
  4. Activate workflow

THEN EVERY DAY, AUTOMATICALLY:

  8:00 AM  ──────────────────────────────────────────────────────────
  │
  │  JOB DISCOVERY
  │  ├─ Downloads + AI-parses your resume (skills, projects, experience)
  │  ├─ Fetches jobs from 4 APIs:
  │  │   • Remotive (remote jobs, no key needed)
  │  │   • Arbeitnow (EU/remote jobs, no key needed)
  │  │   • JSearch via RapidAPI (aggregator, free tier)
  │  │   • The Muse (company-curated jobs, no key needed)
  │  ├─ Deduplicates against jobs already in your Sheet
  │  ├─ AI scores each job 0-100 against YOUR resume
  │  ├─ Filters: only jobs scoring ≥60 are kept
  │  ├─ Saves to Google Sheets (with rotation across 4 credentials)
  │  └─ Sends you a digest via Telegram + Email
  │
  │  YOU: Review the Sheet. For jobs you like, look up the recruiter's
  │       email (LinkedIn, company page, Hunter.io) and paste it into
  │       the "Recruiter Email" column. That's your only manual step.
  │
  9:00 AM  ──────────────────────────────────────────────────────────
  │
  │  EMAIL OUTREACH
  │  ├─ Reads Sheet rows where Status=New AND Recruiter Email is filled
  │  ├─ AI generates a personalized email for each job:
  │  │   • References specific projects from YOUR resume
  │  │   • Mentions specific requirements from the job description
  │  │   • Not generic — every email is unique to that job+you
  │  ├─ Attaches your resume PDF automatically
  │  ├─ Sends via rotating Gmail accounts (4 accounts, 50/day each)
  │  ├─ CCs you on every email sent
  │  ├─ Updates Sheet: marks "Email Sent" + timestamp
  │  └─ Sends you an outreach summary digest
  │
  MIDNIGHT UTC  ─────────────────────────────────────────────────────
  │
  │  DAILY RESET
  │  └─ Resets all counters (Gmail sends, Sheets writes, Groq calls)
  │
  ANYTIME (Telegram)  ───────────────────────────────────────────────
  │
  │  TELEGRAM ASSISTANT
  │  ├─ /help    — shows all commands
  │  ├─ /stats   — job discovery numbers, email counts
  │  ├─ /status  — full multi-account dashboard (which accounts used/remaining)
  │  └─ Any question — AI answers using your job data + resume context
  │
  ──────────────────────────────────────────────────────────────────
```

---

## What You Need to Provide

### Your Information (in the User Config node)

| Field | What to put | Example |
|-------|-------------|---------|
| `name` | Your full name | `Ravi Teja Vallakatla` |
| `currentRole` | Current job title | `Senior Backend Engineer` |
| `targetRole` | What you're looking for | `Staff Engineer` |
| `experience` | Years of experience | `5 years` |
| `skills` | Your top skills (array) | `['Python', 'Node.js', 'AWS']` |
| `location` | Where you are | `Hyderabad, India` |
| `workMode` | Preference (array) | `['remote', 'hybrid']` |
| `keywords` | Search terms for APIs | `python developer OR backend engineer` |
| `resumeUrl` | Public link to your resume PDF | `https://drive.google.com/file/d/ABC123/view` |
| `sheetId` | Your Google Sheet ID | (from the Sheet URL) |
| `userEmail` | Email where you get CC'd + digests | `your@email.com` |
| `linkedinUrl` | Your LinkedIn | `https://linkedin.com/in/you` |
| `githubUrl` | Your GitHub | `https://github.com/you` |
| `portfolioUrl` | Your portfolio | `https://you.dev` |

### Accounts You Need (all free)

| # | Service | What For | Free Tier |
|---|---------|----------|-----------|
| 1-4 | **Gmail** (4 accounts) | Sending outreach emails | 50 emails/day each = **200/day total** |
| 5 | **Google Cloud Project** | OAuth for Gmail + Sheets | Free |
| 6-9 | **Google Sheets** (4 credentials) | Storing job data | 300 writes/day each = **1,200/day total** |
| 10-13 | **Groq** (4 API keys) | AI scoring + email generation | 14,400 req/day each = **57,600/day total** |
| 14 | **Telegram Bot** | Notifications + assistant | Unlimited |
| 15 | **RapidAPI** (optional) | JSearch job aggregator | 500 req/month free |

**Monthly cost: $0**

### Your Google Sheet Structure

Create a Google Sheet with these columns (the workflow reads/writes to them):

| Column | Filled by |
|--------|-----------|
| Job Title | Workflow (auto) |
| Company | Workflow (auto) |
| Location | Workflow (auto) |
| Work Mode | Workflow (auto) |
| Description | Workflow (auto) |
| Requirements | Workflow (auto) |
| Apply URL | Workflow (auto) |
| Score | Workflow (auto) |
| Source | Workflow (auto) |
| Date Found | Workflow (auto) |
| Recruiter Name | **YOU** (manual) |
| Recruiter Email | **YOU** (manual) |
| Status | Workflow (auto: "New" → "Email Sent") |
| Email Sent Date | Workflow (auto) |
| Application ID | Workflow (auto) |

---

## Why 4 Accounts? (The Rotation System)

Gmail, Google Sheets, and Groq all have daily free-tier limits. Instead of paying for premium plans, we rotate across 4 free accounts:

```
┌─────────────────────────────────────────────────────────────┐
│  GMAIL ROTATION (200 emails/day free)                       │
│                                                             │
│  Account 1 (raviintouch2@gmail.com)      ──── 50 emails    │
│  Account 2 (ravitejavallakatla7@gmail.com) ── 50 emails    │
│  Account 3 (ravitejav081@gmail.com)      ──── 50 emails    │
│  Account 4 (ravitejav0801@gmail.com)     ──── 50 emails    │
│                                                             │
│  When Account 1 hits 50 → auto-switches to Account 2       │
│  When Account 2 hits 50 → auto-switches to Account 3       │
│  ... and so on. All reset at midnight UTC.                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  GROQ AI ROTATION (57,600 requests/day free)                │
│                                                             │
│  Key 1 ──── 14,400 requests/day                            │
│  Key 2 ──── 14,400 requests/day                            │
│  Key 3 ──── 14,400 requests/day                            │
│  Key 4 ──── 14,400 requests/day                            │
│                                                             │
│  Monitors usage + alerts you on Telegram when switching.    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  GOOGLE SHEETS ROTATION (1,200 writes/day free)             │
│                                                             │
│  Credential 1 ──── 300 writes/day                          │
│  Credential 2 ──── 300 writes/day                          │
│  Credential 3 ──── 300 writes/day                          │
│  Credential 4 ──── 300 writes/day                          │
│                                                             │
│  Monitors usage + alerts you on Telegram when switching.    │
└─────────────────────────────────────────────────────────────┘
```

**Important:** Set the same display name on all 4 Gmail accounts (e.g., "Ravi Teja Vallakatla") so recruiters see a consistent sender identity regardless of which account sends.

---

## What the Emails Look Like (to recruiters)

```
From: Ravi Teja Vallakatla <raviintouch2@gmail.com>
To:   recruiter@somecompany.com
Cc:   your-personal@gmail.com
Subject: Application for Senior Backend Engineer - 3 years building distributed systems at scale

Hi Sarah,

I noticed the Senior Backend Engineer role at Acme Corp emphasizes experience 
with microservices architecture and event-driven systems. This resonates strongly 
with my work on [specific project from your resume] where I designed a distributed 
pipeline processing 2M events/day using Kafka and Python...

[... 150-200 words, specific to THIS job + YOUR resume ...]

Best regards,
Ravi Teja Vallakatla

Portfolio: https://yourportfolio.com
LinkedIn: https://linkedin.com/in/you
GitHub: https://github.com/you

Attachment: Ravi_Teja_Vallakatla_Resume.pdf
```

Every email is AI-generated using:
- The specific job description + requirements
- Your parsed resume (projects, achievements, skills)
- Your profile links

**You are CC'd on every email** so you see exactly what was sent.

---

## Setup (Step by Step)

### 1. Get n8n Running

**Option A — n8n Cloud (easiest, recommended):**
- Sign up at [n8n.io](https://n8n.io) (free tier: 5,000 executions/month)
- Go to Workflows → Import from URL → paste the import URL above

**Option B — Self-host with Docker:**
- See [`deploy/DOCKER-SETUP.md`](deploy/DOCKER-SETUP.md) for Docker instructions
- See [`deploy/render.yaml`](deploy/render.yaml) for free Render.com hosting

### 2. Create Your Accounts

Follow the detailed guide: [`guides/COMPLETE-SETUP-GUIDE.md`](guides/COMPLETE-SETUP-GUIDE.md)

Quick version:
1. Create 4 Gmail accounts (or use existing ones)
2. Create a Google Cloud project → enable Gmail API + Sheets API → create OAuth credentials
3. Create 4 Groq accounts at [console.groq.com](https://console.groq.com) (use email aliases: `you+groq1@gmail.com`, etc.)
4. Create a Telegram bot via [@BotFather](https://t.me/BotFather)
5. (Optional) Sign up for RapidAPI → subscribe to JSearch API (free tier)

### 3. Add Credentials to n8n

In n8n, go to **Credentials** and add:
- 4x Gmail OAuth2 (one per Gmail account)
- 4x Google Sheets OAuth2 (one per account)
- 4x Groq API (one per key)
- 1x Telegram Bot Token

### 4. Configure the Workflow

Open the imported workflow and edit **"User Config (Master Profile)"** node:
- Fill in all your personal details (see table above)
- Set your `resumeUrl` to a public Google Drive link
- Set your `sheetId`

### 5. Bind Credentials to Nodes

Click each node that shows a ⚠️ warning and select the appropriate credential from the dropdown:
- Gmail Account 1-4 nodes → respective Gmail credentials
- Google Sheets nodes → one of your Sheets credentials
- Groq AI nodes → one of your Groq credentials
- Telegram nodes → your bot token

### 6. Activate

Toggle the workflow to **Active**. Done.

---

## Your Daily Routine (2 minutes)

1. **Morning**: Get Telegram notification "Found 12 new jobs scoring ≥60"
2. **Glance at Sheet**: Sort by Score descending, look at top matches
3. **For the best ones**: Google the recruiter's name/email, paste into "Recruiter Email" column
4. **Next morning**: Those jobs get personalized emails sent automatically
5. **Check CC inbox**: See exactly what was sent, reply manually if recruiter responds

That's it. The system handles the rest.

---

## Repository Structure

```
Ravi-s_automation/
│
├── README.md                          ← You are here
│
├── workflow/
│   └── ENHANCED-MASTER-workflow.json  ← THE MAIN FILE (import this into n8n)
│
├── guides/
│   ├── COMPLETE-SETUP-GUIDE.md        ← Step-by-step setup (45 min)
│   └── EMAIL-SETUP-GUIDE.md           ← Gmail OAuth for 4 accounts
│
├── docs/
│   ├── MULTI-ACCOUNT-SETUP-GUIDE.md   ← 4-way rotation setup details
│   ├── ROTATION-SYSTEM-ARCHITECTURE.md← How rotation works internally
│   ├── GROQ-ROTATION-GUIDE.md         ← 4 Groq keys setup
│   ├── SHEETS-ROTATION-GUIDE.md       ← 4 Sheets credentials setup
│   ├── ACCOUNTS-CHECKLIST.json        ← Machine-readable requirements
│   └── ACCOUNTS-CREDENTIALS-TEMPLATE.txt ← Track your credential IDs
│
└── deploy/
    ├── Dockerfile                     ← Docker image for self-hosting
    ├── render.yaml                    ← One-click deploy to Render.com
    └── DOCKER-SETUP.md                ← Docker + OAuth configuration
```

---

## Workflow Stats

| Metric | Value |
|--------|-------|
| Total nodes | 90 |
| Connection edges | 106 |
| Triggers | 4 (Job Discovery, Email Outreach, Telegram, Daily Reset) |
| Job APIs | 4 (Remotive, Arbeitnow, JSearch, The Muse) |
| Gmail accounts | 4 (200 emails/day) |
| Groq AI keys | 4 (57,600 requests/day) |
| Sheets credentials | 4 (1,200 writes/day) |
| Score threshold | ≥60 (only relevant jobs) |
| Daily email limit | 50 (configurable) |
| Resume attachment | Yes (PDF, auto-downloaded from your Drive URL) |
| Monthly cost | $0 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Resume download fails | Make sure Drive link is "Anyone with the link can view" — test in incognito |
| OAuth redirect mismatch | Set `WEBHOOK_URL` env var in n8n (see [`deploy/DOCKER-SETUP.md`](deploy/DOCKER-SETUP.md)) |
| 0 emails sent | Expected! You must manually fill "Recruiter Email" in the Sheet first |
| Groq rate limit | The rotation handles this automatically — check `/status` on Telegram |
| No jobs found | Check your `keywords` in User Config — try broader terms |
| Sheet not updating | Verify `sheetId` is correct and Sheets OAuth is authorized |

---

## FAQ

**Q: Why don't emails send automatically without me doing anything?**
A: By design. Job APIs don't provide recruiter emails. You fill them in for jobs you actually want. This keeps it targeted (professional networking) instead of spamming random addresses.

**Q: Will recruiters see different "From" addresses?**
A: Yes — the 4 Gmail accounts rotate. Set the same display name on all 4 Google Accounts so the sender *name* is always consistent even if the address differs. Any single recruiter only ever gets one email from you, so they won't notice.

**Q: Can I use just 1 Gmail account?**
A: Yes — put the same credential ID on all 4 send nodes. You'll be limited to 50 emails/day instead of 200.

**Q: What if my resume changes?**
A: Just update the PDF on Google Drive (same link). The workflow re-downloads and re-parses it every morning automatically.

**Q: Is this spam?**
A: No. You manually research and add recruiter emails for specific jobs you want. Each email is AI-tailored to that specific job + your specific resume. Your resume is attached. You're CC'd. This is automated professional outreach, not bulk spam.

---

## License

MIT License — Free to use, modify, and share.

---

**Setup time: 30-45 minutes | Daily effort: 2 minutes | Monthly cost: $0**
