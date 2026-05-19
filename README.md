# MASTER Job Automation System

## 🎯 What This Is

**ONE complete, production-grade n8n workflow** that automates your entire job search process using **ONLY genuinely free tools** - no trials, no hidden costs, no paid dependencies.

This system:
- ✅ Discovers 50-150 relevant jobs per day from 3 free APIs
- ✅ AI-scores each job against your profile (Groq AI)
- ✅ Automatically sends personalized outreach emails to recruiters
- ✅ Tracks all applications in Google Sheets
- ✅ Provides an interactive Telegram bot for stats and queries
- ✅ Costs **$0/month** forever (all services genuinely free)

---

## 📦 What's Included

### Core Files

1. **MASTER-job-automation-workflow.json** (48KB)
   - The complete unified n8n workflow (44 nodes, 3 triggers)
   - Import this into n8n to get started
   - Merges all functionality from 4 original workflows

2. **SETUP-INSTRUCTIONS.md** (22KB, 602 lines)
   - Complete 7-step deployment guide
   - Credential setup for all 5 services
   - Test procedures for each workflow branch
   - Troubleshooting guide with 8 common issues

3. **USER-CONFIG-TEMPLATE.json** (4.1KB)
   - Template for your personal profile
   - Job search preferences and criteria
   - Includes field-by-field mapping guide

4. **WHAT-YOU-MUST-PROVIDE.json** (18KB)
   - Complete checklist of what YOU need to provide
   - Accounts, credentials, IDs, personal data
   - Step-by-step guidance on WHERE and HOW

5. **FREE-VALIDATION-REPORT.md** (9.5KB)
   - Verification that ALL tools are genuinely free
   - Service-by-service analysis with proof
   - Cost breakdown and sustainability report

6. **README.md** (this file)
   - Quick start overview and navigation

### Original Workflows (Reference)

- `workflow-1-job-discovery-engine.json` - Original job discovery logic
- `workflow-2-email-outreach-sender.json` - Original email automation
- `workflow-3-job-scraper-fallback.json` - Original scraper (removed ScraperAPI)
- `workflow-4-telegram-job-assistant.json` - Original Telegram bot

**Note:** You only need the MASTER workflow. Original files kept for reference.

---

## 🚀 Quick Start

### Prerequisites

- **n8n instance** (self-hosted or n8n Cloud free tier)
- **Google account** (for Sheets and Gmail OAuth)
- **Telegram account** (to create your bot)
- **30 minutes** to complete setup

### Setup Steps (Summary)

1. **Import** `MASTER-job-automation-workflow.json` into n8n
2. **Create accounts** (Groq, Telegram bot, Adzuna - all free)
3. **Configure OAuth** (Google Sheets + Gmail in Google Cloud Console)
4. **Replace placeholders** (8 credential IDs and API keys)
5. **Update profile** (use `USER-CONFIG-TEMPLATE.json` as guide)
6. **Create Google Sheet** (19-column schema in "Jobs" tab)
7. **Test workflow** (run each branch manually to verify)
8. **Activate** (toggle ON in n8n)

**Detailed instructions:** See `SETUP-INSTRUCTIONS.md`

---

## 🏗️ Architecture

### 3 Independent Triggers

```
┌─────────────────────────────────────────────────────────────┐
│  TRIGGER 1: Schedule (Daily 8 AM)                           │
│  ├─ Fetch jobs from 3 FREE APIs (Remotive, Arbeitnow, Adzuna)│
│  ├─ Parse & normalize to common schema                       │
│  ├─ Deduplicate & check against existing jobs                │
│  ├─ AI scoring with Groq (0-100 match score)                 │
│  ├─ Filter by threshold (≥30)                                 │
│  ├─ Append to Google Sheets                                   │
│  └─ Send Telegram + Gmail digest                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TRIGGER 2: Schedule (Daily 9 AM)                           │
│  ├─ Read jobs from Sheet (Status="New", has recruiter email) │
│  ├─ Limit to 10 per day                                       │
│  ├─ Generate personalized emails with Groq AI                 │
│  ├─ Send via Gmail (user CC'd)                                │
│  ├─ Update Sheet (Status="Email Sent")                        │
│  ├─ Rate limit (3s delay between emails)                      │
│  └─ Send outreach digest email                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  TRIGGER 3: Telegram Bot (Always On)                        │
│  ├─ Quick commands (/start, /help, /resume, /stats)          │
│  ├─ Complex queries → Groq AI agent                           │
│  ├─ Stats queries → Google Sheets read                        │
│  └─ Reply to user in Telegram                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 💰 Cost Analysis

### Monthly Costs

| Service | Free Tier | Your Usage | Cost |
|---------|-----------|------------|------|
| Groq AI | 14,400 req/day | 80 req/day | $0 |
| Remotive API | Unlimited | 1 req/day | $0 |
| Arbeitnow API | Unlimited | 1 req/day | $0 |
| Adzuna API | 250 req/day | 1 req/day | $0 |
| Google Sheets | 5M cells | 18K rows/year | $0 |
| Gmail | 500/day | 13/day | $0 |
| Telegram | Unlimited | 30/day | $0 |
| n8n (self-hosted) | Unlimited | 300 exec/month | $0 |

**Total:** $0/month, $0/year

**Sustainable:** ✅ YES - All free tiers are permanent, not promotional

**See detailed analysis:** `FREE-VALIDATION-REPORT.md`

---

## 📊 Expected Results

### Daily Job Discovery (8 AM)
- **50-150 jobs** discovered from 3 sources
- **10-30 jobs** pass AI scoring threshold (≥30)
- **Telegram notification** with summary
- **Email digest** with top 5 matches

### Daily Email Outreach (9 AM)
- **0-10 emails** sent (only if recruiter emails added manually)
- **Gmail copies** (you're CC'd on all emails)
- **Sheet updates** (Status changed to "Email Sent")
- **Outreach digest** email with sending stats

### Telegram Assistant (Anytime)
- **/start, /help** → Instant reply with commands
- **/stats** → Real-time application statistics
- **/resume** → Your profile and links
- **Natural language** → AI-powered responses

---

## 🔧 Configuration

### Essential Config (Required)

Edit the **"User Config (Master Profile)"** node in n8n:

```javascript
{
  name: 'Your Name',
  currentRole: 'Senior Backend Engineer',
  targetRole: 'Staff Engineer',
  experience: '5 years',
  skills: ['Python', 'Node.js', 'AWS', 'Docker', 'Kubernetes'],
  location: 'Hyderabad, India',
  workMode: ['remote', 'hybrid'],
  minSalary: 80000,
  keywords: 'python developer OR backend engineer OR nodejs',
  country: 'in',  // Adzuna country code (us, gb, in, au, ca, etc.)
  
  // URLs
  resumeUrl: 'https://drive.google.com/file/d/YOUR_ID/view',
  linkedinUrl: 'https://linkedin.com/in/yourprofile',
  githubUrl: 'https://github.com/yourusername',
  portfolioUrl: 'https://yourportfolio.com',
  
  // Settings
  userEmail: 'YOUR_EMAIL@example.com',
  dailyLimit: 10,         // Max emails per day
  scoreThreshold: 30,     // Min AI score to save job
  sheetId: 'YOUR_SPREADSHEET_ID'
}
```

### Optional Tuning

**Adjust AI scoring sensitivity:**
- `scoreThreshold: 20` → More jobs, lower quality
- `scoreThreshold: 40` → Fewer jobs, higher quality

**Change schedule times:**
- Edit cron expressions in Schedule Trigger nodes
- Default: 8 AM (discovery), 9 AM (outreach) in UTC

**Modify email limit:**
- `dailyLimit: 10` → Standard (recommended)
- `dailyLimit: 5` → Conservative (new Gmail accounts)
- `dailyLimit: 20` → Aggressive (established accounts only)

---

## 📋 Google Sheets Schema

The workflow expects a Google Sheet named **"Jobs"** with these **19 columns**:

| Column | Header | Type | Filled By |
|--------|--------|------|-----------|
| A | Job ID | String | Workflow |
| B | Job Title | String | Workflow |
| C | Company | String | Workflow |
| D | Location | String | Workflow |
| E | Work Mode | String | Workflow |
| F | Salary | String | Workflow |
| G | Apply URL | String | Workflow |
| H | Source | String | Workflow |
| I | Score | Number | Workflow (AI) |
| J | Priority | String | Workflow (AI) |
| K | Match Reason | String | Workflow (AI) |
| L | Status | String | Workflow + You |
| M | Posted Date | Date | Workflow |
| N | Fetched Date | Date | Workflow |
| O | Recruiter Email | String | **YOU** (manual) |
| P | Recruiter Name | String | **YOU** (manual) |
| Q | Application ID | String | Workflow |
| R | Email Sent Date | Date | Workflow |
| S | Last Updated | Date | Workflow |

**Critical:**
- Column order must match exactly (A-S, left to right)
- Tab must be named "Jobs" (case-sensitive)
- You manually add **Recruiter Email** and **Recruiter Name** for jobs you want to apply to

---

## 🛠️ Troubleshooting

### Common Issues

**1. No jobs appearing in Sheet**
- Check API responses in n8n execution logs
- Try broader `keywords` in User Config
- Lower `scoreThreshold` to 20

**2. Emails not sending**
- Verify Gmail OAuth is authorized
- Check that `recruiterEmail` column is filled in Sheet
- Ensure Status="New" for jobs you want to send to

**3. Telegram bot not responding**
- Verify bot token is correct (test with getMe API)
- Check workflow is activated (toggle ON)
- Ensure n8n instance is publicly accessible (for webhook)

**4. Credential errors**
- Re-authorize OAuth credentials in n8n
- Verify credential IDs match in workflow nodes
- Check API keys haven't expired

**5. Groq rate limit errors**
- Free tier: 30 req/min, 14,400/day
- Workflow uses ~80/day - shouldn't hit limits
- If hit, reduce job volume or add delays

**See full troubleshooting guide:** `SETUP-INSTRUCTIONS.md` (Section 7)

---

## 📚 Documentation

### Complete Guides

1. **SETUP-INSTRUCTIONS.md** - Start here for deployment
2. **WHAT-YOU-MUST-PROVIDE.json** - Checklist of requirements
3. **USER-CONFIG-TEMPLATE.json** - Profile configuration template
4. **FREE-VALIDATION-REPORT.md** - Proof all services are free

### Quick Reference

**Credential Placeholders to Replace:**
- `YOUR_GROQ_CREDENTIAL_ID` (3 nodes)
- `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` (5 nodes)
- `YOUR_GMAIL_CREDENTIAL_ID` (3 nodes)
- `YOUR_TELEGRAM_CREDENTIAL_ID` (5 nodes)
- `YOUR_SPREADSHEET_ID` (1 node)
- `YOUR_TELEGRAM_CHAT_ID` (1 node)
- `YOUR_ADZUNA_APP_ID` (1 node)
- `YOUR_ADZUNA_APP_KEY` (1 node)

**Total:** 8 placeholders across 20 locations

---

## 🎯 Workflow Stats

- **Total Nodes:** 44
- **Total Connections:** 38
- **Triggers:** 3 (2 scheduled, 1 event-driven)
- **HTTP Requests:** 3 job APIs
- **AI Operations:** 3 Groq nodes
- **Google Sheets Operations:** 5 (read/append/update)
- **Notifications:** 5 (Telegram + Gmail)
- **Error Handling:** All HTTP nodes have `continueOnFail: true`
- **Rate Limiting:** 3-second delay between outreach emails

---

## 🔒 Privacy & Security

### Data Storage
- **Job data:** Stored in YOUR Google Sheet (you own it)
- **Email copies:** In YOUR Gmail Sent folder (you control it)
- **Telegram messages:** Not logged (only stored by Telegram, not by workflow)

### API Keys
- All credentials stored in n8n (encrypted at rest)
- No credentials hardcoded in workflow JSON
- OAuth tokens auto-refresh

### Email Sending
- You're CC'd on every outreach email (full transparency)
- Sent from YOUR Gmail account (your sender reputation)
- No third-party SMTP or email proxies

### Personal Data
- Resume URL, LinkedIn, GitHub - you provide links (stored in User Config node)
- No PII sent to AI models except what's in job descriptions
- Groq AI doesn't train on your data (per their privacy policy)

---

## 🚀 Next Steps

After successful setup:

### Week 1
- ✅ Monitor daily executions in n8n
- ✅ Check job quality (adjust `scoreThreshold` if needed)
- ✅ Manually research top companies
- ✅ Add recruiter emails to high-priority jobs in Sheet

### Week 2-4
- ✅ Review sent emails (check Gmail Sent folder)
- ✅ Track responses (update Status column in Sheet)
- ✅ Refine skills and keywords in User Config
- ✅ Test Telegram bot for quick stats queries

### Monthly
- ✅ Re-authorize OAuth if credentials expire
- ✅ Update target roles and salary expectations
- ✅ Review and clean old jobs from Sheet
- ✅ Adjust AI temperature if email quality degrades

---

## 🤝 Contributing

This is a single-workflow project, but improvements welcome:

- **Found a bug?** Check execution logs and troubleshooting guide first
- **Want to add a free job API?** Fork and add a new HTTP Request node
- **Better AI prompts?** Edit Groq node parameters
- **UI improvements?** Adjust node positioning

---

## 📄 License

This workflow configuration is provided as-is for personal use.

**Underlying Services:**
- n8n: Fair-code license (Apache 2.0 with Commons Clause)
- Job APIs: Check respective ToS (all allow personal use)
- Groq, Google, Telegram: See their service agreements

---

## 🎉 Success Metrics

**After 30 days, you should see:**
- 1,000+ jobs discovered
- 300+ jobs saved (≥30 score)
- 50-100 emails sent to recruiters
- 5-10 recruiter responses
- 1-3 interviews scheduled

**Adjust configuration if:**
- Too many irrelevant jobs → Increase `scoreThreshold`
- Too few jobs → Decrease `scoreThreshold`, broaden `keywords`
- Low response rate → Review email templates in Groq node
- System errors → Check `SETUP-INSTRUCTIONS.md` troubleshooting

---

## 🙏 Acknowledgments

Built by ruthlessly merging and refactoring 4 original workflows:
- Job Discovery Engine
- Email Outreach Sender
- Job Scraper Fallback (ScraperAPI removed, free APIs added)
- Telegram Job Assistant

**Philosophy:** Only genuinely free tools. No trials. No hidden costs. Production-grade quality.

---

## 📞 Support

**Need help?**

1. Read `SETUP-INSTRUCTIONS.md` (covers 95% of issues)
2. Check n8n execution logs for specific errors
3. Consult `FREE-VALIDATION-REPORT.md` for API limits
4. Visit n8n community: https://community.n8n.io
5. Check service-specific docs (Groq, Adzuna, Telegram)

**Don't email support** - this is a community workflow template, not a commercial product.

---

## ✅ Quick Validation Checklist

Before activating workflow, verify:

- ☐ All 5 credentials added to n8n and authorized
- ☐ All 8 placeholders replaced with actual IDs
- ☐ User Config node updated with your profile
- ☐ Google Sheet created with exact 19-column schema
- ☐ Test execution of each trigger successful
- ☐ Telegram bot responding to /start command
- ☐ Test email received in your inbox
- ☐ Jobs appearing in Google Sheet

**If all checked, you're ready to activate!** 🚀

---

**Good luck with your job search!**

This system will save you 10-15 hours per week by automating discovery, scoring, outreach, and tracking.

Deploy it. Activate it. Let it work for you. 💪
