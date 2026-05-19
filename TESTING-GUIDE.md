# Testing Guide

Complete testing procedures for all three n8n job automation workflows.

---

## Pre-Testing Checklist

Before testing, ensure:

- [ ] All workflows imported successfully
- [ ] All credentials configured and connected
- [ ] All placeholder values replaced
- [ ] Google Sheet created with correct columns
- [ ] Notion database created (for Workflow 2)
- [ ] Resume file uploaded and publicly accessible

---

## Workflow 1: Auto Job Applications

### Test 1: Single Job Application

**Setup:**
1. Add one test job to your Google Sheet:
   ```
   Job Title: Test Software Engineer
   Company: Test Company
   Platform: LinkedIn
   Job URL: https://example.com/test-job
   Status: Not Applied
   Resume URL: [your resume link]
   Cover Letter: This is a test application
   ```

**Execute:**
1. Click "Execute Workflow" in n8n
2. Watch the execution flow

**Expected Results:**
- ✅ Workflow executes without errors
- ✅ Job status changes to "Applied"
- ✅ "Applied Date" populated with today's date
- ✅ "Application ID" generated (format: APP-[timestamp]-[random])
- ✅ "Last Updated" set to today
- ✅ Email received with job details

**Troubleshooting:**
- If status doesn't update: Check Sheet ID and column names
- If no email: Verify Gmail credential and email address
- If "Application ID" missing: Check "Format Response" node

---

### Test 2: Multiple Jobs (Batch)

**Setup:**
1. Add 3-5 jobs with "Not Applied" status
2. Include different platforms (LinkedIn, Indeed, Other)

**Execute:**
1. Click "Execute Workflow"

**Expected Results:**
- ✅ All "Not Applied" jobs processed
- ✅ Each job gets unique Application ID
- ✅ Status updated for all jobs
- ✅ One email per job (or batch summary)

**Check:**
```sql
Count of applied jobs = Count of received emails
```

---

### Test 3: Status Check

**Setup:**
1. Ensure you have jobs with "Applied" status (from Test 1)
2. Manually set a test job's status to "Interview" in the sheet

**Execute:**
1. Click on "Status Check (Every 2 Days)" trigger
2. Click "Execute Workflow"

**Expected Results:**
- ✅ Workflow reads all applied jobs
- ✅ Status check attempted for each
- ✅ Email sent for "Interview" status change
- ✅ No email for unchanged statuses

**Mock API Response:**
For testing, modify "Check Application Status" node to return:
```json
{
  "status": "interview"
}
```

---

### Test 4: Schedule Validation

**Setup:**
1. Check both schedule triggers

**Validate:**
1. "Schedule Trigger" (applications):
   - Cron: `0 9 * * *` (9 AM daily)
   - Next run time should show correctly

2. "Status Check" trigger:
   - Cron: `0 10 */2 * *` (10 AM every 2 days)
   - Next run should be in 2 days

**Test Run:**
1. Temporarily change to `* * * * *` (every minute)
2. Activate workflow
3. Wait 1-2 minutes
4. Check execution history
5. Revert to original schedule

---

## Workflow 2: AI Job Search + Notion

### Test 1: Job Criteria Customization

**Setup:**
1. Edit "Set Job Criteria" node with your preferences
2. Example:
   ```javascript
   {
     role: 'Software Engineer',
     experienceLevel: 'Mid-level',
     location: 'Remote',
     salaryRange: '$100,000 - $150,000',
     workType: 'Remote',
     keywords: 'Python, AWS, Docker'
   }
   ```

**Execute:**
1. Click "Execute Workflow"

**Expected Results:**
- ✅ Criteria passed to Gemini AI
- ✅ AI returns job listings
- ✅ Jobs parsed successfully
- ✅ No syntax errors

---

### Test 2: AI Response Parsing

**Setup:**
1. Check "Google Gemini Job Search" node output

**Validate:**
Response should contain JSON array like:
```json
[
  {
    "jobTitle": "Senior Python Developer",
    "company": "TechCorp",
    "location": "Remote",
    "salaryRange": "$120,000 - $140,000",
    "jobType": "Full-time",
    "workMode": "Remote",
    "experience": "5+ years",
    "applyUrl": "https://...",
    "description": "...",
    "postedDate": "2024-01-15",
    "tags": ["python", "aws", "docker"]
  }
]
```

**Execute:**
1. Run workflow
2. Check "Parse AI Response" node output

**Expected Results:**
- ✅ Valid JSON extracted
- ✅ All required fields present
- ✅ Data formatted correctly

**Troubleshooting:**
- If parsing fails: Gemini may return non-JSON text
- Solution: Adjust prompt to emphasize JSON output
- Fallback: Use "SerpAPI Fallback" node

---

### Test 3: Job Ranking

**Setup:**
1. Execute workflow with multiple jobs

**Validate:**
Check "Rank Jobs" node output for:
- Priority assigned (High/Medium/Low)
- Score calculated (0-100+)
- Ranking logic applied

**Expected Scores:**
- Remote job with preferred tech: ~45+ points (High)
- Hybrid job with some tech: ~25-40 points (Medium)
- Onsite job, no salary: ~10-20 points (Low)

**Adjust:**
Modify scoring in "Rank Jobs" node if needed

---

### Test 4: Notion Integration

**Setup:**
1. Ensure Notion database has all required properties
2. Share database with integration

**Execute:**
1. Run workflow
2. Check Notion database

**Expected Results:**
- ✅ New pages created (one per job)
- ✅ Title = Job Title
- ✅ All properties filled correctly
- ✅ Tags added as multi-select
- ✅ Description appears in page body

**Troubleshooting:**
- "Property not found" error: Check property names match exactly
- "Database not found": Verify database ID and sharing
- Tags not saving: Ensure tag options exist in database

---

### Test 5: Summary Email

**Setup:**
1. Complete full workflow run

**Execute:**
1. Check email inbox

**Expected Results:**
- ✅ Email received
- ✅ Total job count correct
- ✅ Priority breakdown accurate
- ✅ Top 5 jobs listed
- ✅ Formatting clean and readable

**Sample Output:**
```
📊 Daily Job Search Report - 12 New Jobs Found

Priority Breakdown:
🔴 High Priority: 3
🟡 Medium Priority: 5
🟢 Low Priority: 4

Top 5 Matches:
• Senior Python Developer at TechCorp (Remote) - Priority: High
• Full Stack Engineer at StartupXYZ (Hybrid) - Priority: High
...
```

---

### Test 6: Schedule and Automation

**Setup:**
1. Set schedule to `0 8 * * *` (8 AM daily)

**Test:**
1. Change to `*/5 * * * *` (every 5 minutes) for testing
2. Activate workflow
3. Wait 5 minutes
4. Check execution history
5. Revert to original schedule

**Validate:**
- Workflow runs automatically
- Results appear in Notion
- Email sent each run

---

## Workflow 3: LinkedIn Scraper

### Test 1: Webhook Validation

**Setup:**
1. Click "Webhook Trigger" node
2. Copy "Production URL"
3. Should look like: `https://your-n8n.com/webhook/linkedin-job-search`

**Test with cURL:**
```bash
curl -X POST https://your-n8n.com/webhook/linkedin-job-search \
  -H "Content-Type: application/json" \
  -d '{
    "jobTitle": "Software Engineer",
    "location": "San Francisco",
    "country": "United States",
    "jobType": "full-time"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "totalJobs": 15,
  "searchId": "search-1234567890",
  "searchQuery": "Software Engineer",
  "searchLocation": "San Francisco",
  "uniqueCompanies": 12,
  "uniqueLocations": 8,
  "message": "Successfully scraped 15 jobs from LinkedIn",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

### Test 2: Input Validation

**Test Invalid Inputs:**

1. **Missing job title:**
   ```bash
   curl -X POST [webhook-url] \
     -H "Content-Type: application/json" \
     -d '{"location": "San Francisco"}'
   ```
   Expected: Error "Job title is required"

2. **Missing location:**
   ```bash
   curl -X POST [webhook-url] \
     -H "Content-Type: application/json" \
     -d '{"jobTitle": "Software Engineer"}'
   ```
   Expected: Error "Location is required"

3. **Valid minimal input:**
   ```bash
   curl -X POST [webhook-url] \
     -H "Content-Type: application/json" \
     -d '{
       "jobTitle": "Developer",
       "location": "NYC"
     }'
   ```
   Expected: Success (defaults applied)

---

### Test 3: Bright Data Integration

**Setup:**
1. Ensure Bright Data API key is correct
2. Verify dataset ID: `gd_l7q7dkf244hwjntr0`

**Execute:**
1. Send webhook request
2. Watch workflow execution

**Check Points:**
1. "Trigger Bright Data Scrape" → Returns snapshot_id
2. "Wait for Scrape" → Waits 30 seconds
3. "Check Scrape Status" → Returns status
4. "Check if Ready" → If "ready", proceeds; else waits again
5. "Download Results" → Fetches job data

**Expected Timeline:**
- Small search (10-20 jobs): ~30-45 seconds
- Medium search (20-50 jobs): ~45-90 seconds
- Large search (50-100 jobs): ~90-180 seconds

**Troubleshooting:**
- Timeout: Increase wait time to 60 seconds
- API error: Check API key and quota
- No results: Verify search parameters

---

### Test 4: Data Parsing

**Validate:**
Check "Parse & Clean Results" output:

**Expected Format:**
```json
{
  "jobTitle": "Senior Software Engineer",
  "company": "Google",
  "location": "Mountain View, CA",
  "jobType": "Full-time",
  "experienceLevel": "Senior level",
  "salary": "$150,000 - $200,000",
  "applyUrl": "https://www.linkedin.com/jobs/view/123456",
  "description": "We are looking for...",
  "postedDate": "2024-01-10",
  "jobId": "linkedin-123456",
  "skills": ["Python", "AWS", "Docker"],
  "benefits": ["Health insurance", "401k"],
  "applicants": "50",
  "scrapedDate": "2024-01-15",
  "searchId": "search-1234567890",
  "searchQuery": "Software Engineer",
  "searchLocation": "San Francisco"
}
```

**Validation Checks:**
- ✅ All required fields present
- ✅ URLs are valid
- ✅ Dates in correct format (YYYY-MM-DD)
- ✅ Arrays properly formatted
- ✅ No null values for required fields

---

### Test 5: Google Sheets Integration

**Setup:**
1. Create Google Sheet with name "LinkedIn Jobs"
2. Verify credential is set

**Execute:**
1. Run webhook with test data

**Expected Results:**
- ✅ New rows added to sheet
- ✅ All columns populated
- ✅ Data clean and readable
- ✅ No duplicate entries

**Check Sheet:**
| Job Title | Company | Location | Job Type | ... |
|-----------|---------|----------|----------|-----|
| Senior Software Engineer | Google | Mountain View, CA | Full-time | ... |
| Backend Developer | Meta | Menlo Park, CA | Full-time | ... |

---

### Test 6: Error Handling

**Test Scenarios:**

1. **Bright Data API Down:**
   - Expected: Error response with message
   - Workflow shouldn't hang

2. **Invalid API Key:**
   - Expected: 401 Unauthorized error
   - Clear error message returned

3. **Scrape Timeout:**
   - After 3 retry attempts
   - Expected: Error response
   - Message: "Job scraping timed out"

4. **No Results Found:**
   - Valid search with no matches
   - Expected: Success response with totalJobs: 0

**Validate Error Responses:**
```json
{
  "error": "Job scraping failed or timed out",
  "message": "Please try again or check your Bright Data API configuration",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

## Integration Testing

### Test: Workflow 3 → Workflow 1 Integration

**Scenario:** Scrape jobs, then auto-apply

**Steps:**
1. Run Workflow 3 to scrape LinkedIn jobs
2. Verify jobs added to Google Sheet
3. Set some jobs to "Not Applied" status
4. Run Workflow 1
5. Verify applications submitted

**Expected:**
- ✅ Jobs flow from scraper to applicator
- ✅ No data loss or corruption
- ✅ All fields properly mapped

---

### Test: Workflow 2 → Workflow 1 Integration

**Scenario:** AI finds jobs → saves to Notion → manual selection → auto-apply

**Steps:**
1. Run Workflow 2 (AI job search)
2. Review jobs in Notion
3. Manually copy high-priority jobs to Google Sheet
4. Set status to "Not Applied"
5. Run Workflow 1
6. Verify applications

---

## Performance Testing

### Test: High Volume Processing

**Workflow 1:**
- Add 50+ jobs to Google Sheet
- Execute workflow
- Measure execution time
- Expected: < 5 minutes for 50 jobs

**Workflow 2:**
- Request 50+ jobs from AI
- Measure execution time
- Expected: < 3 minutes

**Workflow 3:**
- Scrape 100 jobs
- Measure execution time
- Expected: < 3 minutes

---

## Load Testing

### Workflow 3 Webhook Load Test

**Tools:** Apache Bench or Artillery

**Test Command:**
```bash
# 10 concurrent requests
ab -n 10 -c 2 -H "Content-Type: application/json" \
   -p test-payload.json \
   https://your-n8n.com/webhook/linkedin-job-search
```

**test-payload.json:**
```json
{
  "jobTitle": "Software Engineer",
  "location": "San Francisco",
  "country": "United States",
  "jobType": "full-time"
}
```

**Expected:**
- All requests succeed
- Response time < 5 seconds
- No errors or timeouts

---

## Monitoring and Logging

### Setup Monitoring

**Enable n8n Execution Logging:**
1. Go to Settings → Log Streaming
2. Enable execution logging
3. Set log level to "info"

**Monitor During Tests:**
- Execution time per node
- Error rates
- Success rates
- API response times

**Create Test Log:**
```
Test Date: [DATE]
Workflow: [NAME]
Test Type: [UNIT/INTEGRATION/LOAD]
Status: [PASS/FAIL]
Execution Time: [X seconds]
Notes: [ANY ISSUES]
```

---

## Final Validation Checklist

### Workflow 1
- [ ] Single job application works
- [ ] Batch applications work
- [ ] Status checks work
- [ ] Emails sent correctly
- [ ] Schedule triggers properly
- [ ] All platforms supported (LinkedIn, Indeed, Other)
- [ ] Error handling works
- [ ] Sheet updates correctly

### Workflow 2
- [ ] AI returns valid jobs
- [ ] Jobs parsed correctly
- [ ] Ranking algorithm works
- [ ] Notion pages created
- [ ] Summary email sent
- [ ] Schedule works
- [ ] Customization working

### Workflow 3
- [ ] Webhook accepts requests
- [ ] Input validation works
- [ ] Bright Data scraping succeeds
- [ ] Data parsed correctly
- [ ] Sheet updated
- [ ] Response returned
- [ ] Error handling works
- [ ] Retry logic works

---

## Troubleshooting Common Issues

### Issue: Workflow doesn't execute

**Check:**
1. Workflow is activated (toggle in top right)
2. Trigger is properly configured
3. Credentials are valid
4. No errors in previous nodes

### Issue: Data not updating in Google Sheets

**Check:**
1. Sheet ID is correct
2. Sheet name matches exactly (case-sensitive)
3. Column names match exactly
4. n8n has edit permissions
5. Credential is still valid

### Issue: AI not returning jobs

**Check:**
1. Gemini API key valid
2. Within rate limits (60/min, 1500/day)
3. Prompt is clear and specific
4. Network connectivity
5. Try simplified criteria

### Issue: Emails not sending

**Check:**
1. Gmail credential valid
2. Email address correct
3. Not in spam folder
4. Gmail account has sending permissions
5. Check n8n execution logs for errors

### Issue: Webhook not responding

**Check:**
1. Webhook URL is correct
2. Workflow is activated
3. Request format is valid JSON
4. Content-Type header set
5. n8n instance is running

---

## Support

If tests fail after troubleshooting:
1. Check n8n execution logs
2. Review [SETUP-GUIDE.md](./SETUP-GUIDE.md)
3. Verify all configurations in [CONFIGURATION-REFERENCE.md](./CONFIGURATION-REFERENCE.md)
4. Open an issue with:
   - Workflow name
   - Test that failed
   - Error message
   - Execution logs

---

**Happy Testing! 🧪**
