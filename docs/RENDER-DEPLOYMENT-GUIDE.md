# Render.com Deployment Guide - n8n Job Automation

## Overview

Deploy your n8n job automation workflow to Render.com for **free 24/7 operation** with automatic dual-email failover.

**What you get:**
- 🆓 Free hosting (750 hours/month = 24/7)
- 🔒 Built-in HTTPS (free SSL)
- 🔄 Auto-deploy from GitHub
- 💾 Persistent storage (1 GB)
- 📧 Dual-email failover (100 emails/day total)
- ⚡ Auto-restart on crash

---

## Prerequisites

Before deploying:
1. ✅ GitHub account with this repository
2. ✅ Render.com account (sign up at [render.com](https://render.com))
3. ✅ Groq API key ([console.groq.com](https://console.groq.com))
4. ✅ Google Cloud project with OAuth credentials
5. ✅ Telegram bot token ([@BotFather](https://t.me/BotFather))
6. ✅ Two Gmail accounts:
   - Primary: raviintouch2@gmail.com
   - Secondary: ravitejavallakatla7@gmail.com

---

## Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **Sign Up**
3. Sign up with GitHub (recommended) or email
4. Verify your email

---

## Step 2: Deploy n8n to Render

### Option A: One-Click Deploy (Easiest)

1. Click this button (after we push the files):
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/vallakatlaraviteja/Ravi-s_automation)

2. Render will ask you to connect your GitHub account
3. Click **Connect**
4. Render will read `render.yaml` and create the service
5. Wait 3-5 minutes for the build to complete

### Option B: Manual Setup

1. In Render dashboard, click **New +** > **Web Service**
2. Connect your GitHub account
3. Select repository: `vallakatlaraviteja/Ravi-s_automation`
4. Configure:
   - **Name:** `n8n-job-automation` (or your choice)
   - **Environment:** Docker
   - **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
   - **Branch:** main
   - **Dockerfile Path:** `./Dockerfile`
5. Click **Create Web Service**

---

## Step 3: Configure Environment Variables

After deployment, add environment variables:

1. In Render dashboard, go to your service
2. Click **Environment** tab
3. Add these variables:

| Key | Value | Description |
|-----|-------|-------------|
| `WEBHOOK_URL` | `https://YOUR-APP-NAME.onrender.com/` | Replace YOUR-APP-NAME with your actual service name |
| `N8N_PORT` | `5678` | Port n8n runs on |
| `N8N_PROTOCOL` | `https` | Use HTTPS |
| `NODE_ENV` | `production` | Production mode |
| `EXECUTIONS_TIMEOUT` | `300` | Execution timeout (5 min) |
| `EXECUTIONS_TIMEOUT_MAX` | `600` | Max execution timeout (10 min) |

**Important:** Replace `YOUR-APP-NAME` with your actual Render service name (found in the URL).

4. Click **Save Changes**
5. Service will automatically redeploy (takes 2-3 minutes)

---

## Step 4: Access n8n

1. Once deployment is complete, your n8n is available at:
   ```
   https://YOUR-APP-NAME.onrender.com/
   ```

2. First-time setup:
   - Create an admin account (email + password)
   - Save these credentials securely

---

## Step 5: Configure OAuth Credentials

### Google Cloud Console Setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Select your project (or create a new one)
3. Go to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Name: `n8n-render`
7. **Authorized redirect URIs:** Add this exact URL:
   ```
   https://YOUR-APP-NAME.onrender.com/rest/oauth2-credential/callback
   ```
8. Click **Create**
9. Copy **Client ID** and **Client Secret**

### Enable Required APIs

In Google Cloud Console, enable these APIs:
- ✅ Google Sheets API
- ✅ Gmail API

Go to **APIs & Services** > **Library**, search for each, and click **Enable**.

### Add Test Users (OAuth Consent Screen)

1. Go to **APIs & Services** > **OAuth consent screen**
2. Under **Test users**, click **Add Users**
3. Add both email addresses:
   - raviintouch2@gmail.com
   - ravitejavallakatla7@gmail.com
4. Click **Save**

---

## Step 6: Import Workflow

1. In n8n, click **Workflows** > **Add workflow** > **Import from URL**
2. Paste this URL:
   ```
   https://raw.githubusercontent.com/vallakatlaraviteja/Ravi-s_automation/main/workflow/ENHANCED-MASTER-workflow.json
   ```
3. Click **Import**
4. Workflow name: `Job Automation - Production`

---

## Step 7: Configure Credentials in n8n

### 1. Groq API

1. In n8n, go to **Credentials** > **Add Credential**
2. Search: **Groq**
3. API Key: Get from [console.groq.com/keys](https://console.groq.com/keys)
4. Save

### 2. Google Sheets OAuth2

1. **Credentials** > **Add Credential** > **Google Sheets OAuth2 API**
2. Paste **Client ID** and **Client Secret** from Google Cloud
3. Click **Connect**
4. Sign in with your Google account
5. Allow access

### 3. Gmail Primary (raviintouch2@gmail.com)

1. **Credentials** > **Add Credential** > **Gmail OAuth2 API**
2. Paste **Client ID** and **Client Secret**
3. Click **Connect**
4. Sign in with **raviintouch2@gmail.com**
5. Allow access
6. Save as: `Gmail Primary`

### 4. Gmail Secondary (ravitejavallakatla7@gmail.com)

**Option A: OAuth2 (Recommended)**
1. **Credentials** > **Add Credential** > **Gmail OAuth2 API**
2. Use same Client ID/Secret OR create a new one
3. Click **Connect**
4. Sign in with **ravitejavallakatla7@gmail.com**
5. Allow access
6. Save as: `Gmail Secondary`

**Option B: App Password (Simpler)**
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security) (logged in as ravitejavallakatla7)
2. Enable **2-Step Verification**
3. Search **App passwords**
4. Generate a new app password for "n8n"
5. Copy the 16-character password
6. In n8n: **Credentials** > **SMTP** (not Gmail OAuth2)
   - Host: `smtp.gmail.com`
   - Port: `465`
   - SSL: Yes
   - User: `ravitejavallakatla7@gmail.com`
   - Password: (16-char app password)
7. Save as: `Gmail Secondary SMTP`

### 5. Telegram Bot

1. Open Telegram, search for [@BotFather](https://t.me/BotFather)
2. Send: `/newbot`
3. Follow prompts:
   - Bot name: `Job Hunt Assistant`
   - Username: `your_job_bot` (must end in `bot`)
4. Copy the **API token** (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. In n8n: **Credentials** > **Telegram API**
6. Paste token
7. Save

### 6. Get Your Telegram Chat ID

1. Start a chat with your bot (search for `@your_job_bot` in Telegram)
2. Send any message (e.g., `/start`)
3. Go to this URL in browser (replace TOKEN):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":123456789,...}`
5. Copy the chat ID number
6. You'll need this for the User Config node

---

## Step 8: Create Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new sheet named: `Job Applications Tracker`
3. Create a tab named: `Jobs`
4. Add these column headers in row 1:

| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Job ID | Job Title | Company | Location | Work Mode | Salary | Apply URL | Source | Score | Priority | Match Reason | Status | Posted Date | Fetched Date | Recruiter Email | Recruiter Name | Application ID | Email Sent Date | Last Updated |

5. Copy the **Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```

---

## Step 9: Update User Config Node

1. In the workflow, click the **User Config (Master Profile)** node
2. Update the code with your information:

```javascript
return [{
  json: {
    // YOUR PERSONAL INFO
    name: 'Ravi Teja Vallakatla',  // Your full name
    currentRole: 'Full Stack Developer',  // Your current role
    targetRole: 'Senior Full Stack Engineer',  // Target role
    experience: '3 years',  // Years of experience
    
    // YOUR SKILLS (AI will also extract from resume)
    skills: ['JavaScript', 'Python', 'React', 'Node.js', 'Docker'],
    
    // JOB PREFERENCES
    location: 'Hyderabad, India',
    workMode: ['remote', 'hybrid'],  // remote, hybrid, onsite
    minSalary: 50000,  // Annual salary in USD
    targetRoles: ['Full Stack Engineer', 'Backend Engineer', 'DevOps Engineer'],
    keywords: 'javascript OR python OR react OR nodejs',  // Job search keywords
    country: 'in',  // Country code
    
    // YOUR RESUME (IMPORTANT - AI will parse this!)
    resumeUrl: 'https://drive.google.com/file/d/YOUR_RESUME_ID/view',
    resumeParsingEnabled: true,  // Set to true to use AI resume parsing
    
    // YOUR LINKS
    githubUrl: 'https://github.com/vallakatlaraviteja',
    linkedinUrl: 'https://linkedin.com/in/yourprofile',
    portfolioUrl: 'https://yourportfolio.com',
    
    // YOUR GOOGLE SHEET
    sheetId: 'YOUR_GOOGLE_SHEET_ID',
    
    // YOUR EMAIL
    userEmail: 'raviintouch2@gmail.com',
    
    // DUAL EMAIL CONFIGURATION
    primaryEmail: 'raviintouch2@gmail.com',
    secondaryEmail: 'ravitejavallakatla7@gmail.com',
    primaryGmailCredentialId: 'YOUR_PRIMARY_GMAIL_CREDENTIAL_ID',  // Get from n8n
    secondaryGmailCredentialId: 'YOUR_SECONDARY_GMAIL_CREDENTIAL_ID',  // Get from n8n
    
    // EMAIL LIMITS
    maxEmailsPerAccount: 50,  // Gmail daily limit
    errorThreshold: 3,  // Switch accounts after 3 errors
    
    // WORKFLOW SETTINGS
    dailyLimit: 10,  // Max emails to send per day
    scoreThreshold: 30  // Minimum job match score (0-100)
  }
}];
```

**How to get credential IDs:**
1. In n8n, go to **Credentials**
2. Click on a credential (e.g., Gmail Primary)
3. Look at the URL: `https://your-app.onrender.com/credentials/CREDENTIAL_ID_HERE`
4. Copy the ID and paste it in the User Config

---

## Step 10: Connect Credentials to Nodes

The workflow has placeholder credential IDs. Update them:

1. Open each node that uses credentials (look for red warning icons)
2. Click the credential dropdown
3. Select the credential you created
4. Save

**Nodes that need credentials:**
- `Parse Resume with Groq AI` → Groq API
- `Groq AI: Score Job Match` → Groq API
- `Groq AI: Generate Personalized Email` → Groq API
- `Read Existing Jobs from Sheet` → Google Sheets OAuth2
- `Append to Google Sheets: Jobs Tab` → Google Sheets OAuth2
- `Update Sheet: Mark Email Sent` → Google Sheets OAuth2
- `Send Email via Gmail Primary` → Gmail Primary OAuth2
- `Send Email via Gmail Secondary` → Gmail Secondary OAuth2/SMTP
- `Send Telegram: Job Discovery Digest` → Telegram API
- All other Telegram nodes → Telegram API

---

## Step 11: Test the Workflow

### Test 1: Job Discovery (Manual Test)

1. Click the **Schedule Trigger: Job Discovery (8 AM)** node
2. Click **Execute Node** (play button)
3. Check if jobs are fetched from Remotive and Arbeitnow
4. Verify jobs are saved to Google Sheet
5. Check Telegram for digest message

### Test 2: Email Outreach (Manual Test)

1. In your Google Sheet, manually add a recruiter email to one job:
   - Set Status to `New`
   - Add email in `Recruiter Email` column
2. Click **Schedule Trigger: Email Outreach (9 AM)** node
3. Click **Execute Node**
4. Verify email was sent (check Gmail Sent folder)
5. Verify Sheet status updated to `Email Sent`

### Test 3: Telegram Assistant

1. Open Telegram, find your bot
2. Send: `/start`
3. You should get a welcome message
4. Try: `/stats` (shows application stats)
5. Try: `/resume` (shows your resume)

---

## Step 12: Activate Workflow

1. In n8n workflow, click the **Inactive** toggle (top right)
2. It should turn green: **Active**
3. Your workflow is now running 24/7

**Automated Schedule:**
- **8:00 AM daily:** Job discovery (fetches jobs, scores them, saves to Sheet)
- **9:00 AM daily:** Email outreach (sends emails to new jobs with recruiter emails)

---

## Dual-Email Failover - How It Works

Your workflow automatically manages two Gmail accounts:

### Normal Operation
- **Primary (raviintouch2@gmail.com)** sends emails by default
- Daily counter tracks emails sent
- At midnight, counter resets

### Automatic Failover Triggers
1. **Daily limit reached:** Primary hits 50 emails/day
2. **Error threshold exceeded:** 3 consecutive errors from primary
3. **Manual switch:** Secondary takes over

### Switch Behavior
- Switches to **Secondary (ravitejavallakatla7@gmail.com)**
- You get a **Telegram notification** about the switch
- Secondary continues sending until its limit (50/day)
- Next day at midnight: resets to primary

### Total Capacity
- 50 emails/day (primary) + 50 emails/day (secondary) = **100 emails/day**

**You set:** `dailyLimit: 10` in User Config, so workflow sends max 10/day total.

---

## Monitoring & Maintenance

### Check Workflow Status

1. In Render dashboard: **Logs** tab shows n8n output
2. In n8n: **Executions** tab shows workflow runs
3. In Telegram: Daily digest messages
4. In Gmail: CC'd on all sent emails

### Common Issues

#### Issue: Workflow not triggering at scheduled time

**Cause:** Render free tier sleeps after 15 min inactivity

**Solution:** Already handled! The workflow uses cron triggers which automatically wake the service.

#### Issue: OAuth credentials expired

**Cause:** Google OAuth tokens expire after 7 days (if app is in "Testing" mode)

**Solution:**
1. In Google Cloud Console, go to **OAuth consent screen**
2. Change app status to **In production** (requires verification)
3. OR: Re-authenticate in n8n every 7 days

#### Issue: Gmail sending errors

**Cause:** Daily limit exceeded or suspicious activity detected

**Solution:**
- Check Gmail account for security alerts
- Verify you're under 50 emails/day per account
- Dual-email failover should handle this automatically

#### Issue: Resume parsing failed

**Cause:** Resume URL inaccessible or wrong format

**Solution:**
1. Make sure resume URL is publicly accessible
2. Use direct download links:
   - Google Drive: `https://drive.google.com/uc?export=download&id=FILE_ID`
   - GitHub: Use raw URL (not blob)
   - Dropbox: Add `?dl=1` to URL
3. Check n8n execution logs for specific error

---

## Scaling & Upgrading

### When to Upgrade to Paid Plan

**Free tier is enough if:**
- ✅ You send <100 emails/day
- ✅ You don't mind 15-second cold starts after inactivity
- ✅ 512 MB RAM is sufficient

**Upgrade to Starter ($7/month) if:**
- ❌ You need instant response (no cold starts)
- ❌ You process >100 jobs/day
- ❌ You need more RAM

### Alternative Platforms

If Render free tier doesn't work for you:

| Platform | Free Tier | Sleep | Best For |
|----------|-----------|-------|----------|
| **Render** | 750h/month | Yes (15 min) | Easy setup, auto-deploy |
| **Fly.io** | 3 VMs free | No | True 24/7, no sleep |
| **Railway** | $5 credit/month | No | Hobby projects |
| **Oracle Cloud** | Forever free | No | Production, unlimited |

---

## Backup & Disaster Recovery

### Backup Your Data

n8n stores everything in `/home/node/.n8n/`. Render persistent disk keeps this safe.

**Manual backup (recommended monthly):**
1. In n8n, go to each workflow
2. Click **⋮** (three dots) > **Export**
3. Save JSON file to your computer
4. Commit to GitHub

### Restore After Crash

If Render service crashes or is deleted:
1. Redeploy from GitHub (Steps 1-2)
2. Import workflow from GitHub URL
3. Reconfigure credentials (Step 7)
4. Update User Config (Step 9)
5. Activate workflow

---

## Cost Breakdown

| Service | Cost | Usage |
|---------|------|-------|
| **Render.com** | $0 | 750 hours/month (enough for 24/7) |
| **Groq API** | $0 | Free tier: 14,400 requests/day |
| **Gmail API** | $0 | 50 emails/day per account |
| **Google Sheets API** | $0 | 60 requests/minute |
| **Telegram Bot** | $0 | Unlimited messages |
| **Domain (optional)** | $12/year | Custom domain |
| **SSL Certificate** | $0 | Included with Render |

**Total: $0/month** (or $1/month if you buy a domain)

---

## Next Steps

1. ✅ Deploy to Render (Steps 1-3)
2. ✅ Configure OAuth credentials (Steps 4-5)
3. ✅ Import workflow (Step 6)
4. ✅ Set up credentials (Step 7)
5. ✅ Create Google Sheet (Step 8)
6. ✅ Update User Config (Step 9)
7. ✅ Connect credentials to nodes (Step 10)
8. ✅ Test workflow (Step 11)
9. ✅ Activate workflow (Step 12)
10. 🎉 Enjoy automated job hunting!

---

## Support

**Documentation:**
- n8n Docs: [docs.n8n.io](https://docs.n8n.io)
- Render Docs: [render.com/docs](https://render.com/docs)

**Your Repository:**
- GitHub: [github.com/vallakatlaraviteja/Ravi-s_automation](https://github.com/vallakatlaraviteja/Ravi-s_automation)

**Community:**
- n8n Community: [community.n8n.io](https://community.n8n.io)
- Render Community: [community.render.com](https://community.render.com)

---

**You're all set!** Your job automation workflow will run 24/7 on Render for free with automatic dual-email failover. 🚀
