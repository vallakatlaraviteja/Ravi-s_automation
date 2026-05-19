# Configuration Reference

Complete guide to all configuration options in the n8n job automation workflows.

---

## Table of Contents

1. [Workflow 1 Configuration](#workflow-1-configuration)
2. [Workflow 2 Configuration](#workflow-2-configuration)
3. [Workflow 3 Configuration](#workflow-3-configuration)
4. [Credential Setup](#credential-setup)
5. [Advanced Customization](#advanced-customization)

---

## Workflow 1 Configuration

### Required Replacements

| Placeholder | Replace With | Where to Find | Used In Nodes |
|-------------|-------------|---------------|---------------|
| `YOUR_SPREADSHEET_ID` | Google Sheet ID | Sheet URL | Read Job List, Update Google Sheets, Read Applied Jobs, Update Status in Sheet |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | Credential ID | n8n Credentials | All Google Sheets nodes |
| `YOUR_GMAIL_CREDENTIAL_ID` | Credential ID | n8n Credentials | Send Email Notification, Send Status Email |
| `YOUR_EMAIL@example.com` | Your email | - | Send Email Notification, Send Status Email |

### Google Sheet Structure

**Required Columns:**

```
Job Title | Company | Platform | Job URL | Status | Resume URL | Cover Letter | Applied Date | Application ID | Last Updated
```

**Column Details:**

- **Job Title:** Position name (e.g., "Senior Software Engineer")
- **Company:** Company name (e.g., "Google")
- **Platform:** "LinkedIn", "Indeed", or "Other"
- **Job URL:** Full application URL
- **Status:** "Not Applied", "Applied", "Under Review", "Interview", "Rejected", "Offer"
- **Resume URL:** Publicly accessible link to your resume (Google Drive, Dropbox, etc.)
- **Cover Letter:** Text of your cover letter or URL to it
- **Applied Date:** Auto-filled by workflow
- **Application ID:** Auto-generated unique ID
- **Last Updated:** Auto-updated on status changes

### Schedule Configuration

**Application Schedule (Default: 9 AM Daily)**

```json
{
  "cronExpression": "0 9 * * *"
}
```

**Common Alternatives:**
- Every 2 hours: `0 */2 * * *`
- Twice daily (9 AM & 5 PM): `0 9,17 * * *`
- Weekdays only at 9 AM: `0 9 * * 1-5`
- Every 6 hours: `0 */6 * * *`

**Status Check Schedule (Default: Every 2 Days at 10 AM)**

```json
{
  "cronExpression": "0 10 */2 * *"
}
```

**Common Alternatives:**
- Daily: `0 10 * * *`
- Every 3 days: `0 10 */3 * *`
- Weekly (Monday): `0 10 * * 1`

### Application Status Mapping

The workflow maps API responses to readable statuses:

```javascript
{
  'under_review': 'Under Review',
  'interview': 'Interview',
  'rejected': 'Rejected',
  'offer': 'Offer',
  'pending': 'Applied'
}
```

### Email Notification Customization

**Subject Line:**
```
Job Application Submitted: {{ $json['Job Title'] }} at {{ $json.Company }}
```

**Message Template:**
```
Hello,

Your application has been successfully submitted:

**Job Title:** {{ $json['Job Title'] }}
**Company:** {{ $json.Company }}
**Platform:** {{ $json.Platform }}
**Application ID:** {{ $json['Application ID'] }}
**Applied Date:** {{ $json['Applied Date'] }}
**Job URL:** {{ $json['Job URL'] }}

Good luck with your application!

Best regards,
Your Job Automation System
```

---

## Workflow 2 Configuration

### Required Replacements

| Placeholder | Replace With | Where to Find | Used In Nodes |
|-------------|-------------|---------------|---------------|
| `YOUR_GOOGLE_GEMINI_CREDENTIAL_ID` | Credential ID | n8n Credentials | Google Gemini Job Search |
| `YOUR_NOTION_DATABASE_ID` | Database ID | Notion database URL | Add to Notion |
| `YOUR_NOTION_CREDENTIAL_ID` | Credential ID | n8n Credentials | Add to Notion |
| `YOUR_GMAIL_CREDENTIAL_ID` | Credential ID | n8n Credentials | Send Summary Email |
| `YOUR_EMAIL@example.com` | Your email | - | Send Summary Email |

### Job Criteria Configuration

Edit in "Set Job Criteria" node:

```javascript
{
  role: 'Software Engineer',               // Target role
  experienceLevel: 'Mid-level (3-5 years)', // Experience requirement
  location: 'United States, Remote',       // Location preference
  salaryRange: '$80,000 - $150,000',      // Desired salary
  workType: 'Remote or Hybrid',           // Work arrangement
  keywords: 'JavaScript, Node.js, React, Python, AWS' // Required skills
}
```

**Role Examples:**
- Software Engineer
- Frontend Developer
- Backend Engineer
- Full Stack Developer
- DevOps Engineer
- Data Scientist
- Product Manager

**Experience Levels:**
- Entry-level (0-2 years)
- Mid-level (3-5 years)
- Senior (5-8 years)
- Lead (8+ years)
- Principal/Staff

**Location Formats:**
- "United States, Remote"
- "San Francisco, CA"
- "New York, NY, Hybrid"
- "Europe, Remote"
- "Worldwide, Remote"

### Notion Database Structure

**Required Properties:**

| Property | Type | Options |
|----------|------|---------|
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
| Tags | Multi-select | (Add skills as you go) |
| Score | Number | - |

### Priority Scoring Algorithm

Edit in "Rank Jobs" node:

```javascript
// Base scoring
let score = 0;

// Preferred technologies (+10 each)
const preferredTech = [
  'react', 
  'node.js', 
  'python', 
  'aws', 
  'typescript', 
  'kubernetes'
];

// Remote/Hybrid preference (+15)
if (workMode.includes('remote') || workMode.includes('hybrid')) {
  score += 15;
}

// Salary disclosed (+10)
if (salaryRange && !salaryRange.includes('not disclosed')) {
  score += 10;
}

// Recent posting
// Within 7 days: +20
// Within 14 days: +10
if (daysAgo <= 7) score += 20;
else if (daysAgo <= 14) score += 10;

// Final priority assignment
// >= 40: High
// >= 20: Medium
// < 20: Low
```

**Customize Scoring:**
- Adjust technology list to match your skills
- Modify score weights (e.g., make remote worth +20)
- Add new criteria (company size, benefits, etc.)

### Gemini AI Prompt Customization

Current prompt in "Google Gemini Job Search" node:

```
You are a job search assistant. Search and compile a list of software engineering jobs that match the following criteria:

**Role:** {{ role }}
**Experience Level:** {{ experienceLevel }}
**Location:** {{ location }}
**Salary Range:** {{ salaryRange }}
**Remote/Hybrid/Onsite:** {{ workType }}
**Keywords:** {{ keywords }}

For each job, provide the following information in JSON format:
- jobTitle: string
- company: string
- location: string
- salaryRange: string (if available)
- jobType: string (Full-time, Part-time, Contract, etc.)
- workMode: string (Remote, Hybrid, Onsite)
- experience: string
- applyUrl: string
- description: string (brief summary)
- postedDate: string
- tags: array of strings (relevant skills/technologies)

Return the results as a valid JSON array of job objects. Search across LinkedIn, Indeed, Glassdoor, and other major job boards.
```

**Customization Tips:**
- Add specific platforms: "Focus on LinkedIn and Indeed"
- Request more details: "Include benefits and team size"
- Filter results: "Only include jobs posted within last 7 days"
- Specify industries: "Focus on fintech and healthtech companies"

### Schedule Configuration

**Default: 8 AM Daily**

```json
{
  "cronExpression": "0 8 * * *"
}
```

**Alternatives:**
- Twice daily (8 AM & 6 PM): `0 8,18 * * *`
- Every 12 hours: `0 */12 * * *`
- Weekdays only: `0 8 * * 1-5`
- Every 2 days: `0 8 */2 * *`

---

## Workflow 3 Configuration

### Required Replacements

| Placeholder | Replace With | Where to Find | Used In Nodes |
|-------------|-------------|---------------|---------------|
| `YOUR_BRIGHTDATA_API_KEY` | API Key | Bright Data dashboard | Trigger Bright Data Scrape, Check Scrape Status, Download Results |
| `YOUR_SPREADSHEET_ID` | Google Sheet ID | Sheet URL | Append to Google Sheets |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | Credential ID | n8n Credentials | Append to Google Sheets |

### Webhook Configuration

**Webhook URL Format:**
```
https://your-n8n-instance.com/webhook/linkedin-job-search
```

**Request Format:**

```bash
curl -X POST https://your-n8n-instance.com/webhook/linkedin-job-search \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Software Engineer",
    "location": "San Francisco",
    "country": "United States",
    "jobType": "full-time",
    "experienceLevel": "mid-senior",
    "remote": true
  }'
```

**Request Parameters:**

| Parameter | Type | Required | Options |
|-----------|------|----------|---------|
| jobTitle | string | Yes | Any job title |
| location | string | Yes | City name |
| country | string | No | Default: "United States" |
| jobType | string | No | full-time, part-time, contract, internship |
| experienceLevel | string | No | entry-level, mid-senior, director, executive |
| remote | boolean | No | true/false |

### Google Sheet Structure

**Auto-created Columns:**

```
Job Title | Company | Location | Job Type | Experience Level | Salary | Apply URL | Description | Posted Date | Job ID | Applicants | Scraped Date | Search Query | Search Location
```

### Bright Data Configuration

**Dataset ID:** `gd_l7q7dkf244hwjntr0` (LinkedIn Jobs)

**API Endpoint:** `https://api.brightdata.com/datasets/v3/trigger`

**Parameters:**
```json
{
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "endpoint": "linkedin_jobs",
  "discover_by": "keyword",
  "keyword": "{{ jobTitle }}",
  "location": "{{ location }}, {{ country }}",
  "job_type": "{{ jobType }}",
  "limit": 50,
  "include_errors": false,
  "format": "json"
}
```

**Adjust Limits:**
- Change `"limit": 50` to scrape more/fewer jobs
- Max recommended: 100 (higher limits take longer)

### Wait Times

**Initial Wait (Default: 30 seconds)**
```json
{
  "amount": 30,
  "unit": "seconds"
}
```

**Retry Wait (Default: 30 seconds)**
```json
{
  "amount": 30,
  "unit": "seconds"
}
```

**Adjustment Guidelines:**
- Small searches (< 20 jobs): 20 seconds
- Medium searches (20-50 jobs): 30 seconds
- Large searches (50-100 jobs): 60 seconds

### Alternative: SerpAPI Configuration

Replace Bright Data nodes with:

**HTTP Request Node:**
```json
{
  "url": "https://serpapi.com/search",
  "method": "GET",
  "queryParameters": {
    "engine": "google_jobs",
    "q": "{{ jobTitle }}",
    "location": "{{ location }}",
    "api_key": "YOUR_SERPAPI_KEY",
    "num": 20
  }
}
```

**Benefits:**
- ✅ 100 free searches/month
- ✅ Faster response time
- ✅ No waiting for scrape completion

**Limitations:**
- ❌ Lower quality data
- ❌ Fewer details per job
- ❌ Limited to 20 results per search

---

## Credential Setup

### Google Sheets OAuth2

1. In n8n: **Credentials** → **Add Credential** → **Google Sheets OAuth2**
2. Click **Sign in with Google**
3. Authorize n8n
4. Copy the credential ID

### Gmail OAuth2

1. In n8n: **Credentials** → **Add Credential** → **Gmail OAuth2**
2. Click **Sign in with Google**
3. Authorize n8n
4. Copy the credential ID

### Google Gemini API

**Method 1: API Key (Recommended)**

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click **Get API Key**
3. Create new API key
4. In n8n: **Credentials** → **Add Credential** → **Google Gemini API**
5. Select "API Key" authentication
6. Paste your key

**Method 2: OAuth2**

1. Create Google Cloud project
2. Enable Gemini API
3. Create OAuth2 credentials
4. Configure in n8n

**Free Tier Limits:**
- 60 requests/minute
- 1,500 requests/day
- 32,000 tokens per request

### Notion API

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click **+ New integration**
3. Name: "n8n Job Automation"
4. Submit and copy **Internal Integration Token**
5. Share your database with this integration
6. In n8n: **Credentials** → **Add Credential** → **Notion API**
7. Paste token

### Bright Data API

1. Sign up at [Bright Data](https://brightdata.com/)
2. Go to **Datasets** → **LinkedIn Jobs**
3. Get API key from **Settings** → **API Access**
4. Use as Bearer token in HTTP Request nodes

### SerpAPI (Alternative)

1. Sign up at [SerpAPI](https://serpapi.com/)
2. Get API key from dashboard
3. Free tier: 100 searches/month
4. Use in query parameters

---

## Advanced Customization

### Adding Custom Job Boards

In Workflow 1, add a new switch case:

```javascript
// In "Check Platform" node
{
  "conditions": {
    "string": [
      {
        "value1": "={{ $json.Platform }}",
        "operation": "equals",
        "value2": "YourPlatform"
      }
    ]
  }
}
```

Then create a new "Apply to Job" node for that platform.

### Custom Email Templates

**HTML Email Template:**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .header { background: #4CAF50; color: white; padding: 20px; }
    .content { padding: 20px; }
    .job-title { font-size: 20px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Application Submitted!</h1>
  </div>
  <div class="content">
    <p class="job-title">{{ $json['Job Title'] }}</p>
    <p><strong>Company:</strong> {{ $json.Company }}</p>
    <p><strong>Application ID:</strong> {{ $json['Application ID'] }}</p>
    <p><strong>Applied:</strong> {{ $json['Applied Date'] }}</p>
    <p><a href="{{ $json['Job URL'] }}">View Job</a></p>
  </div>
</body>
</html>
```

### Webhook Security

Add authentication to Workflow 3:

```javascript
// In "Validate Input" node
const authHeader = $input.item.json.headers.authorization;
const expectedToken = 'your-secret-token';

if (authHeader !== `Bearer ${expectedToken}`) {
  throw new Error('Unauthorized');
}
```

Then call with:
```bash
curl -X POST https://your-webhook-url \
  -H "Authorization: Bearer your-secret-token" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### Rate Limiting

Add rate limiting to prevent API quota exhaustion:

```javascript
// In any node before API call
const lastRun = $('Storage').item.json.lastRun || 0;
const now = Date.now();
const minInterval = 60000; // 1 minute

if (now - lastRun < minInterval) {
  throw new Error('Rate limit: please wait before running again');
}

// Save current time
$('Storage').item.json.lastRun = now;
```

### Data Validation

Add strict validation to webhook inputs:

```javascript
// In "Validate Input" node
const body = items[0].json.body || {};

// Required fields
if (!body.jobTitle || body.jobTitle.length < 3) {
  throw new Error('Job title must be at least 3 characters');
}

if (!body.location || body.location.length < 2) {
  throw new Error('Location must be at least 2 characters');
}

// Allowed job types
const allowedTypes = ['full-time', 'part-time', 'contract', 'internship'];
if (body.jobType && !allowedTypes.includes(body.jobType)) {
  throw new Error(`Job type must be one of: ${allowedTypes.join(', ')}`);
}

// Sanitize inputs
return [{
  json: {
    jobTitle: body.jobTitle.trim(),
    location: body.location.trim(),
    country: body.country?.trim() || 'United States',
    jobType: body.jobType || 'full-time'
  }
}];
```

### Duplicate Detection

Prevent duplicate job entries:

```javascript
// Before adding to Google Sheets
const existingJobs = $('Read Job List').all();
const newJobUrl = $json.applyUrl;

const isDuplicate = existingJobs.some(
  job => job.json['Apply URL'] === newJobUrl
);

if (isDuplicate) {
  throw new Error('Job already exists in sheet');
}
```

---

## Environment Variables

For security, use n8n environment variables:

```bash
# In .env file or n8n settings
GOOGLE_SHEETS_CREDENTIAL_ID=abc123
GMAIL_CREDENTIAL_ID=def456
GEMINI_API_KEY=your-key
BRIGHTDATA_API_KEY=your-key
NOTION_API_KEY=your-key
YOUR_EMAIL=your@email.com
```

Then reference in workflows:
```javascript
const email = $env.YOUR_EMAIL;
```

---

## Monitoring & Logging

### Add Logging Node

After critical operations:

```javascript
// In a Code node
console.log('Job application submitted:', {
  jobTitle: $json['Job Title'],
  company: $json.Company,
  applicationId: $json['Application ID'],
  timestamp: new Date().toISOString()
});

return items;
```

### Error Notifications

Add error handling with email alerts:

```javascript
// In "On Error" workflow
{
  "sendTo": "YOUR_EMAIL@example.com",
  "subject": "⚠️ Workflow Error: {{ $workflow.name }}",
  "message": "Error occurred: {{ $json.error }}"
}
```

---

## Performance Tips

1. **Batch Operations:** Process multiple items at once
2. **Parallel Execution:** Use n8n's parallel processing
3. **Caching:** Store frequently accessed data
4. **Lazy Loading:** Only fetch data when needed
5. **Optimize Queries:** Use filters early in the pipeline

---

**Need help? Check the [SETUP-GUIDE.md](./SETUP-GUIDE.md) or open an issue!**
