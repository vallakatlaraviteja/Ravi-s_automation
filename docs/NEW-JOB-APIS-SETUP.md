# New Job APIs Setup Guide (FEAT-004)

## Overview

The workflow now supports **7 job APIs** with intelligent cascading fallback and health monitoring:

### Existing APIs (3):
1. **Remotive** - Remote job listings
2. **Arbeitnow** - European job market
3. **Adzuna** - Global job search

### New APIs (4):
4. **JSearch (RapidAPI)** - 500 requests/month (requires API key)
5. **The Muse** - 500 requests/hour (no auth)
6. **USAJobs** - Unlimited federal jobs (requires API key)
7. **GitHub Jobs** - Unlimited (deprecated but working, no auth)

## Features

### 1. API Health Tracking
- Monitors success/failure for each API
- Tracks consecutive failures
- Marks API as "unhealthy" after 5+ consecutive failures
- Sends Telegram alert when API becomes unhealthy

### 2. Graceful Fallback
- All HTTP Request nodes have `continueOnFail: true`
- Failed APIs don't block the workflow
- Jobs from successful APIs are merged and processed
- Health status included in daily digest

### 3. Unified Job Schema
All 7 APIs normalize to the same structure:
```javascript
{
  source: 'API Name',
  jobTitle: 'Job Title',
  company: 'Company Name',
  location: 'City, Country',
  jobType: 'Full-time',
  workMode: 'Remote/Onsite/Hybrid',
  salary: 'Salary or "Not disclosed"',
  applyUrl: 'Application URL',
  description: 'First 500 chars',
  tags: ['tag1', 'tag2'],
  postedDate: 'YYYY-MM-DD',
  category: 'Category',
  jobId: 'source-id',
  fetchedDate: 'YYYY-MM-DD',
  recruiterEmail: '',
  recruiterName: ''
}
```

## Setup Instructions

### Step 1: Get API Keys

#### JSearch (RapidAPI)
1. Visit: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Sign up for free (no credit card required)
3. Subscribe to the free plan (500 requests/month)
4. Copy your `x-rapidapi-key` from the dashboard
5. Add to User Config: `rapidapiKey: 'YOUR_KEY_HERE'`

#### USAJobs
1. Visit: https://developer.usajobs.gov/APIRequest/Index
2. Create an account
3. Request an API key (requires email for User-Agent)
4. Copy your Authorization Key
5. Add to User Config: `usajobsApiKey: 'YOUR_KEY_HERE'`

#### The Muse (No Auth Required)
- No setup needed, API is open

#### GitHub Jobs (No Auth Required)
- No setup needed, API is deprecated but still works

### Step 2: Update User Config Node

Open the **User Config (Master Profile)** node and add:

```javascript
rapidapiKey: 'YOUR_RAPIDAPI_KEY_HERE',
usajobsApiKey: 'YOUR_USAJOBS_API_KEY_HERE'
```

### Step 3: Import Workflow

1. Open n8n
2. Import the updated `ENHANCED-MASTER-workflow.json`
3. Replace credential placeholders with your actual credentials

### Step 4: Test Individual APIs

Execute each API node individually to verify setup:

1. **Test JSearch**: Execute "Fetch JSearch API (RapidAPI)" node
   - Should return jobs data
   - Check for authentication errors (401) - means invalid key

2. **Test The Muse**: Execute "Fetch The Muse API" node
   - Should return jobs array
   - No auth required

3. **Test USAJobs**: Execute "Fetch USAJobs API" node
   - Should return SearchResult object
   - Check for missing User-Agent or Authorization-Key errors

4. **Test GitHub Jobs**: Execute "Fetch GitHub Jobs API" node
   - May return empty array (API deprecated but works intermittently)

## API Health Monitoring

### How It Works

1. **Job API State Manager** initializes health tracking:
```javascript
{
  remotive: { status: 'healthy', lastSuccess: null, consecutiveFailures: 0 },
  arbeitnow: { status: 'healthy', lastSuccess: null, consecutiveFailures: 0 },
  jsearch: { status: 'healthy', lastSuccess: null, consecutiveFailures: 0 },
  themuse: { status: 'healthy', lastSuccess: null, consecutiveFailures: 0 },
  usajobs: { status: 'healthy', lastSuccess: null, consecutiveFailures: 0 },
  githubjobs: { status: 'healthy', lastSuccess: null, consecutiveFailures: 0 }
}
```

2. **Update API Health Status** runs after merge:
   - Checks if each API returned results
   - Increments `consecutiveFailures` on error
   - Resets to 0 on success
   - Marks `status: 'unhealthy'` if failures ≥ 5

3. **Telegram Alert** sent when API marked unhealthy

### Daily Digest Includes Health

Telegram message now shows:

```
📊 Daily Job Discovery Complete

✅ Found **25** new relevant jobs!

Priority Breakdown:
🔴 High: 8
🟡 Medium: 12
🟢 Low: 5

Sources: Remotive: 10, JSearch: 8, The Muse: 5, USAJobs: 2

API Health Status:
remotive: healthy (0 failures), arbeitnow: healthy (0 failures),
jsearch: healthy (0 failures), themuse: unhealthy (5 failures),
usajobs: healthy (0 failures), githubjobs: healthy (0 failures)

⚠️ Unhealthy APIs: themuse
```

## API Rate Limits

| API | Free Tier | Limit |
|-----|-----------|-------|
| Remotive | ✅ | Unknown (high) |
| Arbeitnow | ✅ | Unknown (high) |
| Adzuna | ✅ | 5000/month |
| **JSearch** | ✅ | 500/month |
| **The Muse** | ✅ | 500/hour (12,000/day) |
| **USAJobs** | ✅ | Unlimited |
| **GitHub Jobs** | ✅ | Unlimited (deprecated) |

### Estimated Daily Usage

- Job Discovery runs once daily (8 AM)
- 7 API calls per day
- Well within all free tier limits

## Troubleshooting

### JSearch Returns 401
- Invalid API key
- Check RapidAPI dashboard for key
- Verify subscription to JSearch API

### USAJobs Returns 403
- Missing Authorization-Key header
- Missing User-Agent header (must be email)
- Check API key at developer.usajobs.gov

### The Muse Returns Empty Results
- Query might be too specific
- Try broader keywords in User Config
- Check `category` parameter matches available categories

### GitHub Jobs Returns Empty
- API deprecated, works intermittently
- Not a failure - just no active listings
- Can be disabled if not useful

### API Marked Unhealthy
- Check execution logs for error messages
- Verify API key hasn't expired
- Check if API service is down
- Reset health status by executing Job API State Manager manually

## Benefits

### Increased Job Coverage
- **3 → 7 sources** = more opportunities
- Diverse sources (tech, government, general, remote-focused)
- Better geographic coverage

### Improved Reliability
- Cascading fallback ensures at least some jobs are found
- Health tracking identifies issues early
- No single point of failure

### Cost Efficiency
- All 7 APIs free forever
- No credit card required (except JSearch optional)
- Total capacity: 18,500+ jobs/day

## Next Steps

1. **Monitor API Health**: Check daily Telegram digests for unhealthy APIs
2. **Adjust Keywords**: Tune `keywords` in User Config for better results
3. **Add More APIs**: Easy to extend pattern for future APIs
4. **Custom Alerts**: Modify unhealthy threshold (currently 5 failures)

## Architecture Diagram

```
Schedule Trigger (8 AM)
    ↓
User Config
    ↓
Job API State Manager
    ↓
┌─────────────────────────────────────────────────────┐
│ 7 Parallel API Fetches (all continueOnFail: true)  │
├─────────────────────────────────────────────────────┤
│ 1. Fetch Remotive      → Parse Remotive             │
│ 2. Fetch Arbeitnow     → Parse Arbeitnow            │
│ 3. Fetch Adzuna        → Parse Adzuna               │
│ 4. Fetch JSearch       → Parse JSearch              │
│ 5. Fetch The Muse      → Parse The Muse             │
│ 6. Fetch USAJobs       → Parse USAJobs              │
│ 7. Fetch GitHub Jobs   → Parse GitHub Jobs          │
└─────────────────────────────────────────────────────┘
    ↓
Merge All API Results (7 inputs)
    ↓
Update API Health Status
    ↓
Deduplicate Jobs
    ↓
Read Existing Jobs from Sheet
    ↓
Filter Out Already-Fetched Jobs
    ↓
Groq AI: Score Job Match (with Resume Intelligence)
    ↓
Parse AI Score
    ↓
Resume Match Analysis
    ↓
Filter by Score Threshold (≥30)
    ↓
Append to Google Sheets: Jobs Tab
    ↓
Aggregate Job Discovery Summary (includes API health)
    ↓
Send Telegram + Gmail Digest
```

## Support

For issues or questions:
1. Check execution logs in n8n
2. Verify API keys in User Config
3. Test individual API nodes
4. Review health status in daily digest
5. Check API documentation for updates
