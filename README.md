# Job Automation System with AI

**Automated job discovery, AI-powered matching, and smart email outreach**

## What This Does

- 🔍 **Discovers jobs** from 3 sources (Remotive, Arbeitnow, Adzuna) daily at 8 AM UTC
- 🤖 **AI scoring** matches jobs to your resume (0-100 score)
- ✉️ **Personalized emails** to recruiters with automatic failover between 2 Gmail accounts
- 📊 **Tracks everything** in Google Sheets
- 💬 **Telegram bot** for job stats and queries

## Features

### Resume Intelligence
- Automatically parses your resume (PDF from Google Drive/GitHub/Dropbox)
- Extracts skills, experience, projects with AI
- Job scoring uses actual resume content
- Emails reference specific projects from your resume

### Dual Email Failover
- Primary: Your first Gmail (50 emails/day)
- Secondary: Your second Gmail (50 emails/day)
- Auto-switch when primary hits limit or errors
- Total: 100 emails/day with zero manual intervention

### 100% Free
- Groq AI: 14,400 requests/day
- Gmail: 500/day per account (we use 50 for safety)
- Google Sheets: 5M cells
- Telegram: Unlimited
- Adzuna API: 250 requests/day
- n8n Cloud: 5,000 executions/month

**Monthly cost: $0**

---

## Quick Start

### 1. Import Workflow

**n8n Cloud URL:**
```
https://raw.githubusercontent.com/vallakatlaraviteja/Ravi-s_automation/main/ENHANCED-MASTER-workflow.json
```

In n8n:
1. Go to **Workflows** → **Import from URL**
2. Paste the URL above
3. Click **Import**

### 2. Follow Setup Guide

Open: **[COMPLETE-SETUP-GUIDE.md](COMPLETE-SETUP-GUIDE.md)**

This guide walks you through:
- Creating 7 free accounts (Groq, Google Cloud, Telegram, Adzuna, etc.)
- Setting up OAuth for both Gmail accounts
- Configuring your resume URL
- Testing all features
- Activation

**Setup time: 45-60 minutes**

---

## Files in This Repo

| File | Purpose |
|------|---------|
| **ENHANCED-MASTER-workflow.json** | Main workflow (62 nodes) - import this |
| **COMPLETE-SETUP-GUIDE.md** | Step-by-step setup (beginner-friendly) |
| **EMAIL-SETUP-GUIDE.md** | Gmail OAuth for dual accounts |
| **ACCOUNTS-CHECKLIST.json** | What accounts/credentials you need |
| **ACCOUNTS-CREDENTIALS-TEMPLATE.txt** | Track IDs during setup |
| **FREE-VALIDATION-REPORT.md** | Proof all services are free |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│  TRIGGERS (3 branches)                                  │
├─────────────────────────────────────────────────────────┤
│  1. Job Discovery (8 AM UTC daily)                      │
│  2. Email Outreach (9 AM UTC daily)                     │
│  3. Telegram Bot (always listening)                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  BRANCH 1: JOB DISCOVERY                                │
├─────────────────────────────────────────────────────────┤
│  • Fetch from 3 APIs (Remotive, Arbeitnow, Adzuna)     │
│  • Parse & normalize job data                           │
│  • Download & parse resume with Groq AI                 │
│  • Score each job (0-100) against resume                │
│  • Filter duplicates                                     │
│  • Save to Google Sheets                                │
│  • Send Telegram + Email digest                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  BRANCH 2: EMAIL OUTREACH                               │
├─────────────────────────────────────────────────────────┤
│  • Read jobs from Sheet (Status=New, has recruiter)     │
│  • Limit to 10/day                                      │
│  • Generate personalized email with Groq AI             │
│  • Reference resume projects in email                   │
│  • Select Gmail account (primary or secondary)          │
│  • Send email with auto-failover                        │
│  • Update Sheet status to "Email Sent"                  │
│  • Send notification if account switches                │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  BRANCH 3: TELEGRAM ASSISTANT                           │
├─────────────────────────────────────────────────────────┤
│  • Listen for messages                                  │
│  • Handle commands: /start, /stats, /resume             │
│  • Answer questions with Groq AI                        │
│  • Query Google Sheet for stats                         │
│  • Send intelligent replies                             │
└─────────────────────────────────────────────────────────┘
```

---

## What You Need to Provide

### Accounts (7 free accounts):
1. **Groq** - AI scoring and email generation
2. **Google Cloud** - OAuth credentials
3. **Gmail Primary** - Your first email account
4. **Gmail Secondary** - Your second email account
5. **Google Sheets** - Job storage
6. **Telegram** - Bot notifications
7. **Adzuna** - Job search API

### Information:
- Your resume (PDF on Google Drive/GitHub/Dropbox)
- Your skills, experience, target roles
- Job search keywords
- Both Gmail addresses
- Telegram chat ID

**See [ACCOUNTS-CHECKLIST.json](ACCOUNTS-CHECKLIST.json) for complete list**

---

## Daily Workflow

**8:00 AM UTC:**
1. Discovers 10-50 jobs from 3 sources
2. AI scores each against your resume
3. Saves jobs scoring ≥30 to Sheet
4. Sends digest via Telegram + email

**9:00 AM UTC:**
1. Reads jobs with recruiter emails
2. Generates personalized emails citing your resume
3. Sends up to 10 emails (split between 2 accounts)
4. Updates Sheet with "Email Sent" status
5. Notifies if account failover occurs

**Anytime:**
- Message bot: `/stats` for job breakdown
- Ask: "What remote Python jobs do I have?"
- Bot responds with AI-generated answers

---

## Testing

After setup, run these 6 tests:

1. **Resume Download** - Verify resume fetched successfully
2. **Resume Parsing** - Confirm skills extracted
3. **Job Discovery** - Check Sheet populated with jobs
4. **Email Sending** - Send test email to yourself
5. **Telegram Bot** - Test `/start` and `/stats` commands
6. **Email Failover** - Simulate primary exhaustion

**See COMPLETE-SETUP-GUIDE.md Part 6 for detailed test procedures**

---

## Troubleshooting

### Common Issues

**Resume download fails:**
- Check URL is publicly accessible (test in incognito browser)
- Google Drive: Use `https://drive.google.com/uc?export=download&id=FILE_ID`
- GitHub: Use raw URL (click "Raw" button)
- Dropbox: Change `?dl=0` to `?dl=1`

**Credentials not found:**
- Click nodes with ⚠️ warnings
- Select credentials from dropdown
- Don't use placeholder text like "YOUR_GROQ_CREDENTIAL_ID"

**OAuth redirect mismatch:**
- Google Cloud redirect URI must match n8n URL exactly
- Format: `https://YOUR_N8N_URL/rest/oauth2-credential/callback`

**Emails not sending:**
- Verify both Gmail credentials are authorized
- Check User Config has both email addresses
- See EMAIL-SETUP-GUIDE.md for OAuth troubleshooting

---

## Support

- **Setup Guide:** [COMPLETE-SETUP-GUIDE.md](COMPLETE-SETUP-GUIDE.md)
- **Email Setup:** [EMAIL-SETUP-GUIDE.md](EMAIL-SETUP-GUIDE.md)
- **n8n Community:** [community.n8n.io](https://community.n8n.io)
- **Groq Docs:** [console.groq.com/docs](https://console.groq.com/docs)

---

## License

MIT License - Free to use and modify

---

**Setup time: 45-60 minutes | Cost: $0/month | Skill level: Beginner**
