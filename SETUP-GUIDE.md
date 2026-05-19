# Complete n8n Job Automation Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Service Setup](#service-setup)
3. [Workflow Import Instructions](#workflow-import-instructions)
4. [Configuration Steps](#configuration-steps)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Services (Free Tiers Available)

1. **n8n** (Self-hosted or Cloud)
   - Self-hosted: Free forever
   - Cloud: Free tier available
   - [Sign up here](https://n8n.io/)

2. **Google Sheets**
   - Free with Google account
   - [Create account](https://sheets.google.com)

3. **Gmail**
   - Free with Google account
   - [Create account](https://gmail.com)

4. **Google Gemini AI** (Best Free AI Option)
   - Free tier: 60 requests/minute
   - [Get API key](https://ai.google.dev/)

5. **Notion** (For Workflow 2)
   - Free tier: Unlimited pages & blocks
   - [Sign up](https://notion.so)

6. **Bright Data** (For Workflow 3)
   - Free trial available
   - Alternative: Use SerpAPI free tier (100 searches/month)
   - [Bright Data](https://brightdata.com/) | [SerpAPI](https://serpapi.com/)

---

## Service Setup

### 1. Google Sheets Setup

#### Create Google Sheets Credential in n8n

1. In n8n, go to **Settings** → **Credentials** → **Add Credential**
2. Search for "Google Sheets"
3. Choose "OAuth2"
4. Click "Sign in with Google"
5. Authorize n8n to access your Google Sheets

#### Create Job Application Sheet (For Workflows 1 & 3)

Create a new Google Sheet with these columns:

| Job Title | Company | Platform | Job URL | Status | Resume URL | Cover Letter | Applied Date | Application ID | Last Updated |
|-----------|---------|----------|---------|--------|------------|--------------|--------------|----------------|--------------|

**Sample Row:**
```
Senior Developer | Google | LinkedIn | https://linkedin.com/jobs/123 | Not Applied | https://drive.google.com/your-resume | Your cover letter text | | | |
```

**Important Notes:**
- Status should be "Not Applied" for jobs you want to auto-apply to
- Resume URL should be publicly accessible (use Google Drive share link)
- Keep the sheet ID handy (it's in the URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`)

---

### 2. Gmail Setup

#### Create Gmail Credential in n8n

1. In n8n, go to **Settings** → **Credentials** → **Add Credential**
2. Search for "Gmail"
3. Choose "OAuth2"
4. Click "Sign in with Google"
5. Authorize n8n to send emails on your behalf

**Replace in workflows:**
- `YOUR_EMAIL@example.com` → your actual email address

---

### 3. Google Gemini AI Setup (FREE - Best Option)

#### Get API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new API key
4. Copy the key

#### Create Gemini Credential in n8n

1. In n8n, go to **Settings** → **Credentials** → **Add Credential**
2. Search for "Google Gemini"
3. Choose "OAuth2" or "API Key" (API Key is simpler)
4. Paste your API key

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for daily job searches

**Why Gemini?**
- ✅ Completely free
- ✅ High rate limits
- ✅ Excellent at web search and data extraction
- ✅ Structured output support

---

### 4. Notion Setup (For Workflow 2)

#### Create Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Name it "n8n Job Automation"
4. Submit and copy the "Internal Integration Token"

#### Create Job Database

1. Create a new Notion page
2. Create a database with these properties:

| Property Name | Type | Options/Values |
|--------------|------|----------------|
| Job Title | Title | - |
| Company | Text | - |
| Location | Text | - |
| Salary Range | Text | - |
| Job Type | Select | Full-time, Part-time, Contract, Internship |
| Work Mode | Select | Remote, Hybrid, Onsite |
| Experience | Text | - |
| Apply URL | URL | - |
| Status | Select | New, Applied, Interview, Rejected, Offer |
| Priority | Select | High, Medium, Low |
| Posted Date | Date | - |
| Added Date | Date | - |
| Tags | Multi-select | Add skills as needed |
| Score | Number | - |

3. Share the database with your integration:
   - Click "Share" in top right
   - Add your integration
   - Copy the database ID from URL: `https://notion.so/YOUR_DATABASE_ID?v=...`

#### Create Notion Credential in n8n

1. In n8n, go to **Settings** → **Credentials** → **Add Credential**
2. Search for "Notion"
3. Paste your Internal Integration Token

---

### 5. Bright Data Setup (For Workflow 3)

#### Option A: Bright Data (Recommended for Production)

1. Sign up at [Bright Data](https://brightdata.com/)
2. Start free trial
3. Go to **Datasets** → **LinkedIn Jobs**
4. Get your API key from settings
5. Copy the dataset ID: `gd_l7q7dkf244hwjntr0`

#### Option B: SerpAPI (100 Free Searches/Month)

1. Sign up at [SerpAPI](https://serpapi.com/)
2. Get your free API key (100 searches/month)
3. Replace Bright Data node with SerpAPI HTTP Request node

**SerpAPI Configuration:**
```
URL: https://serpapi.com/search
Method: GET
Query Parameters:
- engine: google_jobs
- q: {{ job_title }}
- location: {{ location }}
- api_key: YOUR_SERPAPI_KEY
- num: 20
```

---

## Workflow Import Instructions

### Step 1: Download Workflow Files

Download these three JSON files:
1. `workflow-1-auto-job-applications.json`
2. `workflow-2-ai-job-search-notion.json`
3. `workflow-3-linkedin-scraper-brightdata.json`

### Step 2: Import into n8n

1. Open n8n
2. Click **Workflows** → **Add Workflow** → **Import from File**
3. Select the JSON file
4. Click "Import"

Repeat for all three workflows.

---

## Configuration Steps

### Workflow 1: Auto Job Applications + Status Tracking

#### 1. Update Credentials

Replace these credential IDs in the workflow:
- `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID`
- `YOUR_GMAIL_CREDENTIAL_ID`

#### 2. Update Google Sheet ID

In nodes "Read Job List", "Update Google Sheets", "Read Applied Jobs", "Update Status in Sheet":
- Replace `YOUR_SPREADSHEET_ID` with your actual Sheet ID

#### 3. Update Email Address

In nodes "Send Email Notification" and "Send Status Email":
- Replace `YOUR_EMAIL@example.com` with your actual email

#### 4. Configure Schedule

**Schedule Trigger** node (default: 9 AM daily):
```
Cron Expression: 0 9 * * *
```

**Status Check** node (default: 10 AM every 2 days):
```
Cron Expression: 0 10 */2 * *
```

#### 5. Activate Workflow

Click the toggle in the top right to activate.

---

### Workflow 2: AI-Powered Job Search + Notion Tracking

#### 1. Update Credentials

Replace these credential IDs:
- `YOUR_GOOGLE_GEMINI_CREDENTIAL_ID`
- `YOUR_NOTION_CREDENTIAL_ID`
- `YOUR_GMAIL_CREDENTIAL_ID`

#### 2. Update Notion Database ID

In "Add to Notion" node:
- Replace `YOUR_NOTION_DATABASE_ID` with your database ID

#### 3. Update Email Address

In "Send Summary Email" node:
- Replace `YOUR_EMAIL@example.com` with your email

#### 4. Customize Job Criteria

In "Set Job Criteria" node, modify these values:
```javascript
{
  role: 'Software Engineer',              // Your target role
  experienceLevel: 'Mid-level (3-5 years)', // Your experience
  location: 'United States, Remote',      // Preferred location
  salaryRange: '$80,000 - $150,000',     // Desired salary
  workType: 'Remote or Hybrid',          // Work preference
  keywords: 'JavaScript, Node.js, React, Python, AWS' // Key skills
}
```

#### 5. Customize Ranking (Optional)

In "Rank Jobs" node, adjust the scoring logic:
```javascript
// Preferred technologies (add your preferences)
const preferredTech = ['react', 'node.js', 'python', 'aws', 'typescript', 'kubernetes'];

// Adjust score weights as needed
// Remote/Hybrid: +15 points
// Salary disclosed: +10 points
// Posted within 7 days: +20 points
```

#### 6. Configure Schedule

Default: 8 AM daily
```
Cron Expression: 0 8 * * *
```

#### 7. Activate Workflow

---

### Workflow 3: LinkedIn Job Finder (Bright Data)

#### 1. Update API Keys

In "Trigger Bright Data Scrape" node:
- Replace `YOUR_BRIGHTDATA_API_KEY` with your API key

In "Check Scrape Status" and "Download Results" nodes:
- Replace `YOUR_BRIGHTDATA_API_KEY` with your API key

#### 2. Update Google Sheets

Replace these credential IDs:
- `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID`

In "Append to Google Sheets" node:
- Replace `YOUR_SPREADSHEET_ID` with your Sheet ID
- Sheet name: "LinkedIn Jobs"

#### 3. Get Webhook URL

1. Click on "Webhook Trigger" node
2. Copy the "Production URL"
3. Save it for testing

#### 4. Activate Workflow

---

## Testing

### Test Workflow 1: Auto Job Applications

1. Add a job to your Google Sheet with Status = "Not Applied"
2. Click "Execute Workflow" in n8n
3. Check:
   - ✅ Status updated to "Applied"
   - ✅ Application ID generated
   - ✅ Email received

### Test Workflow 2: AI Job Search

1. Click "Execute Workflow"
2. Wait 30-60 seconds for AI to search
3. Check:
   - ✅ Jobs appear in Notion database
   - ✅ Jobs ranked by priority
   - ✅ Summary email received

### Test Workflow 3: LinkedIn Scraper

Using cURL:
```bash
curl -X POST https://your-n8n-instance.com/webhook/linkedin-job-search \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Software Engineer",
    "location": "San Francisco",
    "country": "United States",
    "jobType": "full-time"
  }'
```

Or use Postman/Insomnia with:
- Method: POST
- URL: Your webhook URL
- Body (JSON):
```json
{
  "jobTitle": "Software Engineer",
  "location": "San Francisco",
  "country": "United States",
  "jobType": "full-time"
}
```

Check:
- ✅ Jobs added to Google Sheet
- ✅ Response with job count

---

## Troubleshooting

### Issue: "Authentication failed"

**Solution:**
1. Recreate credentials in n8n
2. Make sure to authorize all requested permissions
3. Check if API keys are correct and active

### Issue: "Google Sheets not updating"

**Solution:**
1. Verify Sheet ID is correct
2. Check column names match exactly (case-sensitive)
3. Ensure n8n has edit permissions on the sheet

### Issue: "No jobs found by AI"

**Solution:**
1. Check Gemini API quota (60/min, 1500/day)
2. Simplify job criteria
3. Try different keywords
4. Check if Gemini credential is valid

### Issue: "Bright Data timeout"

**Solution:**
1. Increase wait time in "Wait for Scrape" node (try 60 seconds)
2. Check Bright Data API status
3. Verify dataset ID is correct
4. Consider switching to SerpAPI for free tier

### Issue: "Notion database error"

**Solution:**
1. Ensure integration is shared with the database
2. Check property names match exactly
3. Verify select/multi-select options exist
4. Update database permissions

### Issue: "Email not sending"

**Solution:**
1. Verify Gmail credential is valid
2. Check email address is correct
3. Look for emails in spam folder
4. Ensure "Less secure app access" is enabled (if using app passwords)

---

## Advanced Tips

### Combining Workflows

**Recommended Flow:**
1. **Morning (8 AM):** Workflow 2 runs → AI finds jobs → saves to Notion
2. **Morning (9 AM):** Workflow 1 runs → auto-applies to curated jobs
3. **Every 2 days (10 AM):** Workflow 1 checks application status
4. **On-demand:** Workflow 3 → scrape LinkedIn when needed

### Performance Optimization

1. **Limit results:** In AI prompts, specify "top 10" or "top 20" jobs
2. **Use filters:** Add salary, experience, location filters early
3. **Batch processing:** Group operations to reduce API calls
4. **Error handling:** Add "Continue on Fail" to non-critical nodes

### Cost Management

**Free Tier Limits:**
- Google Gemini: 60/min, 1500/day ✅
- SerpAPI: 100 searches/month ✅
- Google Sheets: Unlimited ✅
- Gmail: Unlimited (reasonable use) ✅
- Notion: Unlimited pages ✅

**Staying Free:**
- Run AI search once daily (1 job = ~1-3 API calls)
- Use SerpAPI for 3-4 searches/week
- Everything else is unlimited

---

## Support & Resources

- **n8n Documentation:** https://docs.n8n.io/
- **n8n Community:** https://community.n8n.io/
- **Google Gemini Docs:** https://ai.google.dev/docs
- **Notion API Docs:** https://developers.notion.com/
- **Bright Data Docs:** https://docs.brightdata.com/

---

## Quick Start Checklist

- [ ] n8n installed and running
- [ ] Google Sheets credential created
- [ ] Gmail credential created
- [ ] Google Gemini API key obtained
- [ ] Notion integration created (for Workflow 2)
- [ ] Bright Data or SerpAPI key obtained (for Workflow 3)
- [ ] Job Application sheet created with correct columns
- [ ] Notion database created with correct properties
- [ ] All three workflows imported
- [ ] Credential IDs updated in all workflows
- [ ] Sheet IDs and Database IDs updated
- [ ] Email addresses updated
- [ ] Job criteria customized
- [ ] Test runs completed successfully
- [ ] Workflows activated

---

**You're all set! Happy job hunting! 🚀**
