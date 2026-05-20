# FREE Job APIs List - Complete Reference

**All 7 FREE job search APIs used in the n8n workflow with setup instructions, limits, and troubleshooting**

---

## Overview

This workflow uses **7 completely FREE job search APIs** with intelligent cascading fallback. If one API fails, the next takes over automatically.

**Total Monthly Cost: $0.00**

---

## API Comparison Table

| API Name | Free Limit | Signup Required | Credit Card Required | API Key Required | Response Format |
|----------|------------|-----------------|----------------------|------------------|-----------------|
| **Remotive** | Unlimited | No | No | No | JSON |
| **Arbeitnow** | Unlimited | No | No | No | JSON |
| **Adzuna** | 250/day | Yes | No | Yes (App ID + Key) | JSON |
| **JSearch** | 500/month | Yes | No | Yes (RapidAPI Key) | JSON |
| **The Muse** | 500/hour | No | No | No | JSON |
| **USAJobs** | Unlimited | Yes | No | Yes (API Key) | JSON |
| **GitHub Jobs** | Unlimited | No | No | No | JSON (deprecated but works) |

---

## API 1: Remotive

### Overview
- **Source**: Remotive.com remote job board
- **Free Tier**: Unlimited requests
- **Best For**: Remote-first jobs across all industries

### Signup
**No signup required!** Completely open API.

### API Details
- **Endpoint**: `https://remotive.com/api/remote-jobs`
- **Method**: GET
- **Authentication**: None
- **Rate Limit**: No official limit (be respectful)

### Example Request
```bash
curl https://remotive.com/api/remote-jobs
```

### Example Response
```json
{
  "jobs": [
    {
      "id": 123456,
      "title": "Senior Backend Engineer",
      "company_name": "TechCorp",
      "category": "Software Development",
      "job_type": "full-time",
      "publication_date": "2024-01-20T10:30:00",
      "candidate_required_location": "Remote",
      "salary": "$120k-150k",
      "description": "We're looking for...",
      "url": "https://remotive.com/remote-jobs/software-dev/senior-backend-engineer-123456"
    }
  ]
}
```

### Response Fields
- `id`: Unique job ID
- `title`: Job title
- `company_name`: Company name
- `category`: Job category
- `job_type`: full-time, part-time, contract
- `publication_date`: ISO 8601 timestamp
- `candidate_required_location`: Location requirements
- `salary`: Salary range (if provided)
- `description`: Full job description (HTML)
- `url`: Application URL

### Troubleshooting
| Issue | Solution |
|-------|----------|
| `jobs` array empty | API is up but no jobs match default filters. Try different category parameter. |
| Timeout | API occasionally slow. Increase n8n timeout to 30 seconds. |
| 500 error | Rare server issue. Retry in 5 minutes or skip to next API. |

---

## API 2: Arbeitnow

### Overview
- **Source**: Arbeitnow.com European job board
- **Free Tier**: Unlimited requests
- **Best For**: European remote and on-site jobs

### Signup
**No signup required!** Open API.

### API Details
- **Endpoint**: `https://www.arbeitnow.com/api/job-board-api`
- **Method**: GET
- **Authentication**: None
- **Rate Limit**: No official limit

### Example Request
```bash
curl https://www.arbeitnow.com/api/job-board-api
```

### Example Response
```json
{
  "data": [
    {
      "slug": "backend-engineer-techcorp-12345",
      "company_name": "TechCorp",
      "title": "Backend Engineer",
      "description": "Job description here...",
      "remote": true,
      "url": "https://www.arbeitnow.com/view/backend-engineer-techcorp-12345",
      "tags": ["python", "django", "postgresql"],
      "job_types": ["full-time"],
      "location": "Berlin, Germany",
      "created_at": 1705750200
    }
  ]
}
```

### Response Fields
- `slug`: Unique job identifier
- `company_name`: Company name
- `title`: Job title
- `description`: Full description (text)
- `remote`: Boolean (true if remote-friendly)
- `url`: Job posting URL
- `tags`: Array of skill tags
- `job_types`: Array of employment types
- `location`: Job location
- `created_at`: Unix timestamp

### Troubleshooting
| Issue | Solution |
|-------|----------|
| Empty `data` array | No new jobs today. Normal - Arbeitnow updates periodically. |
| Missing `tags` | Some jobs don't have tags. Handle as empty array in workflow. |
| `remote` field inconsistent | Some jobs mark remote in title but not in `remote` field. Check both. |

---

## API 3: Adzuna

### Overview
- **Source**: Adzuna job aggregator
- **Free Tier**: 250 requests/day
- **Best For**: Aggregated jobs from multiple sources, salary data

### Signup
1. Go to: [developer.adzuna.com](https://developer.adzuna.com)
2. Click "Register"
3. Fill in email, password, name
4. Verify email
5. Create application (name: `n8n Job Automation`)
6. Copy **Application ID** and **Application Key**

### API Details
- **Endpoint**: `https://api.adzuna.com/v1/api/jobs/{country}/search/1`
- **Method**: GET
- **Authentication**: Query parameters (`app_id`, `app_key`)
- **Rate Limit**: 250 requests/day

### Example Request
```bash
curl "https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY&results_per_page=50&what=python%20developer&where=remote"
```

### Query Parameters
- `app_id`: Your Application ID (required)
- `app_key`: Your Application Key (required)
- `results_per_page`: Number of results (max 50)
- `what`: Keywords (URL-encoded)
- `where`: Location (use "remote" for remote jobs)
- `salary_min`: Minimum salary
- `sort_by`: Options: `date`, `salary`, `relevance`

### Example Response
```json
{
  "results": [
    {
      "id": "1234567890",
      "title": "Senior Python Developer",
      "company": {
        "display_name": "TechCorp Inc"
      },
      "location": {
        "display_name": "Remote, USA",
        "area": ["USA"]
      },
      "description": "We are looking for...",
      "created": "2024-01-20T10:30:00Z",
      "salary_min": 100000,
      "salary_max": 150000,
      "salary_is_predicted": 0,
      "redirect_url": "https://www.adzuna.com/land/ad/1234567890",
      "category": {
        "label": "IT Jobs",
        "tag": "it-jobs"
      }
    }
  ],
  "count": 1250
}
```

### Response Fields
- `id`: Unique job ID (string)
- `title`: Job title
- `company.display_name`: Company name
- `location.display_name`: Human-readable location
- `description`: Full job description (HTML)
- `created`: ISO 8601 timestamp
- `salary_min` / `salary_max`: Salary range in local currency
- `salary_is_predicted`: 0 = actual, 1 = Adzuna's estimate
- `redirect_url`: Application URL (Adzuna redirect)
- `category.label`: Job category

### Troubleshooting
| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check `app_id` and `app_key` are correct. |
| 429 Too Many Requests | Hit 250/day limit. Wait until midnight UTC or use other APIs. |
| Empty `results` | No jobs match criteria. Broaden `what` parameter or remove `where`. |
| `salary_is_predicted: 1` | Adzuna estimated salary (not posted by employer). Filter if needed. |

---

## API 4: JSearch (RapidAPI)

### Overview
- **Source**: RapidAPI marketplace (aggregates Google for Jobs, LinkedIn, etc.)
- **Free Tier**: 500 requests/month
- **Best For**: Comprehensive job data from major platforms

### Signup
1. Go to: [rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
2. Click "Sign Up" (use Google/GitHub or email)
3. Click "Subscribe to Test"
4. Select **Basic** plan (Free, 500 requests/month)
5. No credit card required
6. Go to "Endpoints" tab → Copy **X-RapidAPI-Key** from code snippet

### API Details
- **Endpoint**: `https://jsearch.p.rapidapi.com/search`
- **Method**: GET
- **Authentication**: Header (`X-RapidAPI-Key`)
- **Rate Limit**: 500 requests/month (16/day average)

### Example Request
```bash
curl -H "X-RapidAPI-Key: YOUR_RAPID_API_KEY" \
     -H "X-RapidAPI-Host: jsearch.p.rapidapi.com" \
     "https://jsearch.p.rapidapi.com/search?query=python%20developer%20remote&num_pages=1"
```

### Query Parameters
- `query`: Search query (required, URL-encoded)
- `num_pages`: Number of pages (default: 1, max: 20)
- `date_posted`: Options: `all`, `today`, `3days`, `week`, `month`
- `remote_jobs_only`: `true` or `false`

### Example Response
```json
{
  "status": "OK",
  "request_id": "abc-123-def-456",
  "data": [
    {
      "job_id": "abcdef123456",
      "employer_name": "TechCorp Inc",
      "job_title": "Senior Python Developer",
      "job_description": "We're seeking...",
      "job_apply_link": "https://www.linkedin.com/jobs/view/123456789",
      "job_city": "San Francisco",
      "job_state": "CA",
      "job_country": "US",
      "job_is_remote": true,
      "job_posted_at_datetime_utc": "2024-01-20T10:30:00.000Z",
      "job_employment_type": "FULLTIME",
      "job_min_salary": 120000,
      "job_max_salary": 150000,
      "job_salary_currency": "USD",
      "job_salary_period": "YEAR"
    }
  ]
}
```

### Response Fields
- `job_id`: Unique ID
- `employer_name`: Company name
- `job_title`: Job title
- `job_description`: Full description
- `job_apply_link`: Application URL
- `job_city` / `job_state` / `job_country`: Location
- `job_is_remote`: Boolean
- `job_posted_at_datetime_utc`: ISO 8601 UTC timestamp
- `job_employment_type`: `FULLTIME`, `PARTTIME`, `CONTRACTOR`
- `job_min_salary` / `job_max_salary`: Salary range
- `job_salary_currency`: Currency code (USD, EUR, etc.)
- `job_salary_period`: `YEAR`, `MONTH`, `HOUR`

### Troubleshooting
| Issue | Solution |
|-------|----------|
| 403 Forbidden | Invalid RapidAPI key. Re-copy from RapidAPI dashboard. |
| 429 Rate Limit | Hit 500/month limit. Wait until next month or upgrade plan. |
| `X-RapidAPI-Host` required | Must include both `X-RapidAPI-Key` and `X-RapidAPI-Host` headers. |
| Empty `data` array | No results for query. Try broader keywords. |

---

## API 5: The Muse

### Overview
- **Source**: TheMuse.com curated job board
- **Free Tier**: 500 requests/hour
- **Best For**: Jobs with company culture info, career advice

### Signup
**No signup required!** Open API (no authentication).

### API Details
- **Endpoint**: `https://www.themuse.com/api/public/jobs`
- **Method**: GET
- **Authentication**: None
- **Rate Limit**: 500 requests/hour

### Example Request
```bash
curl "https://www.themuse.com/api/public/jobs?category=Engineering&level=Senior&page=0"
```

### Query Parameters
- `category`: Job category (e.g., `Engineering`, `Design`, `Marketing`)
- `level`: Career level (`Internship`, `Entry Level`, `Mid Level`, `Senior`, `Management`)
- `location`: City or "Flexible / Remote"
- `company`: Company name
- `page`: Page number (0-indexed)

### Example Response
```json
{
  "page": 0,
  "page_count": 50,
  "results": [
    {
      "id": 123456,
      "name": "Senior Backend Engineer",
      "company": {
        "id": 7890,
        "name": "TechCorp",
        "short_name": "techcorp"
      },
      "locations": [
        {
          "name": "Flexible / Remote"
        }
      ],
      "categories": [
        {
          "name": "Engineering"
        }
      ],
      "levels": [
        {
          "name": "Senior Level"
        }
      ],
      "tags": [
        {
          "name": "python"
        },
        {
          "name": "backend"
        }
      ],
      "publication_date": "2024-01-20T10:30:00.000000Z",
      "refs": {
        "landing_page": "https://www.themuse.com/jobs/techcorp/senior-backend-engineer"
      }
    }
  ]
}
```

### Response Fields
- `id`: Job ID
- `name`: Job title
- `company.name`: Company name
- `company.short_name`: Company slug
- `locations[].name`: Job locations (check for "Flexible / Remote")
- `categories[].name`: Job categories
- `levels[].name`: Career levels
- `tags[].name`: Skill tags
- `publication_date`: ISO 8601 timestamp
- `refs.landing_page`: Job posting URL

### Troubleshooting
| Issue | Solution |
|-------|----------|
| Empty `results` | No jobs match filters. Remove `level` or `category` parameter. |
| 429 Rate Limit | Hit 500/hour. Wait 1 hour or use other APIs. |
| Pagination issues | The Muse doesn't return total pages. Keep requesting until `results` empty. |

---

## API 6: USAJobs

### Overview
- **Source**: Official U.S. government job board
- **Free Tier**: Unlimited requests
- **Best For**: Federal government jobs, contractor positions

### Signup
1. Go to: [developer.usajobs.gov](https://developer.usajobs.gov)
2. Click "Request API Key"
3. Fill in form (email, name, purpose: "Personal job search automation")
4. Submit
5. Check email for API key

### API Details
- **Endpoint**: `https://data.usajobs.gov/api/search`
- **Method**: GET
- **Authentication**: Header (`Authorization-Key`)
- **Rate Limit**: No official limit

### Example Request
```bash
curl -H "Authorization-Key: YOUR_API_KEY" \
     -H "User-Agent: your-email@example.com" \
     "https://data.usajobs.gov/api/search?Keyword=software%20engineer&RemoteIndicator=true"
```

### Query Parameters
- `Keyword`: Search keywords (URL-encoded)
- `RemoteIndicator`: `true` for remote jobs only
- `LocationName`: City, state, or country
- `PositionTitle`: Exact job title match
- `ResultsPerPage`: Max 500 (default: 25)

**Important**: Must include `User-Agent` header with your email address.

### Example Response
```json
{
  "SearchResult": {
    "SearchResultCount": 150,
    "SearchResultItems": [
      {
        "MatchedObjectId": "123456789",
        "MatchedObjectDescriptor": {
          "PositionID": "ABC-2024-12345",
          "PositionTitle": "Software Engineer",
          "PositionURI": "https://www.usajobs.gov/job/123456789",
          "PositionLocation": [
            {
              "LocationName": "Washington, District of Columbia",
              "CountryCode": "United States",
              "CityName": "Washington",
              "Latitude": 38.8951,
              "Longitude": -77.0369
            }
          ],
          "OrganizationName": "Department of Defense",
          "DepartmentName": "Department of Defense",
          "PublicationStartDate": "2024-01-20",
          "ApplicationCloseDate": "2024-02-20",
          "PositionRemuneration": [
            {
              "MinimumRange": "100000",
              "MaximumRange": "150000",
              "RateIntervalCode": "PA"
            }
          ],
          "PositionSchedule": [
            {
              "Name": "Full-time",
              "Code": "1"
            }
          ],
          "Remot eIndicator": true
        }
      }
    ]
  }
}
```

### Response Fields
- `MatchedObjectId`: Unique job ID
- `PositionID`: Official position ID
- `PositionTitle`: Job title
- `PositionURI`: Job URL
- `PositionLocation[]`: Array of locations
- `OrganizationName`: Hiring organization
- `DepartmentName`: Government department
- `PublicationStartDate`: Posting date
- `ApplicationCloseDate`: Deadline
- `PositionRemuneration[]`: Salary info
- `RemoteIndicator`: Boolean for remote eligibility

### Troubleshooting
| Issue | Solution |
|-------|----------|
| 403 Forbidden | Missing `Authorization-Key` header or invalid key. |
| 400 Bad Request (User-Agent) | Must include `User-Agent` header with your email. |
| Empty results | Federal jobs are specific. Try broader `Keyword`. |
| Salary in cents | `MinimumRange` and `MaximumRange` are in cents (divide by 100). |

---

## API 7: GitHub Jobs

### Overview
- **Source**: GitHub's deprecated job board
- **Free Tier**: Unlimited
- **Best For**: Developer-focused jobs (while it lasts)

**Status**: Officially deprecated in 2021, but API still works.

### Signup
**No signup required!** Open API.

### API Details
- **Endpoint**: `https://jobs.github.com/positions.json`
- **Method**: GET
- **Authentication**: None
- **Rate Limit**: None

### Example Request
```bash
curl "https://jobs.github.com/positions.json?description=python&location=remote"
```

### Query Parameters
- `description`: Keywords (e.g., `python`, `react`, `devops`)
- `location`: Location or `remote`
- `full_time`: `true` or `false`
- `page`: Page number (0-indexed)

### Example Response
```json
[
  {
    "id": "abc-123-def-456",
    "type": "Full Time",
    "url": "https://jobs.github.com/positions/abc-123-def-456",
    "created_at": "Sat Jan 20 10:30:00 UTC 2024",
    "company": "TechCorp",
    "company_url": "https://techcorp.com",
    "location": "Remote",
    "title": "Senior Python Developer",
    "description": "<p>We're looking for...</p>",
    "how_to_apply": "<p>Email: jobs@techcorp.com</p>",
    "company_logo": "https://jobs.github.com/rails/active_storage/blobs/123/logo.png"
  }
]
```

### Response Fields
- `id`: Job ID
- `type`: Employment type (`Full Time`, `Part Time`, `Contract`)
- `url`: Job posting URL
- `created_at`: Timestamp (non-standard format)
- `company`: Company name
- `company_url`: Company website
- `location`: Job location
- `title`: Job title
- `description`: Full description (HTML)
- `how_to_apply`: Application instructions (HTML)
- `company_logo`: Logo URL

### Troubleshooting
| Issue | Solution |
|-------|----------|
| API stops responding | GitHub may finally shut it down. Remove from workflow. |
| Stale job listings | Postings may be outdated. Use other APIs as primary source. |
| Response is array, not object | GitHub Jobs returns array directly (no wrapper object). |

---

## Cascading Fallback Logic

### Order of Execution

The workflow tries APIs in this priority:

1. **Remotive** (most reliable, unlimited)
2. **Arbeitnow** (reliable, unlimited)
3. **Adzuna** (250/day limit)
4. **JSearch** (500/month limit)
5. **The Muse** (500/hour limit)
6. **USAJobs** (unlimited, niche)
7. **GitHub Jobs** (unlimited, deprecated)

### Fallback Rules

- If API 1 succeeds: Use those jobs, stop
- If API 1 fails: Try API 2
- If APIs 1-2 fail: Try API 3
- Continue until jobs found OR all 7 fail

**Success Criteria:**
- HTTP 200 status
- `jobs` / `data` / `results` array has length > 0

**Failure Handling:**
- Log error details
- Send Telegram notification if all APIs fail
- Continue workflow (don't crash)

### Why This Order?

1. **Remotive first**: Unlimited, reliable, good remote jobs
2. **Arbeitnow second**: Unlimited, European focus
3. **Adzuna third**: 250/day limit (conserve quota)
4. **JSearch fourth**: 500/month limit (conserve)
5. **The Muse fifth**: 500/hour (generous but niche)
6. **USAJobs sixth**: Unlimited but government-only
7. **GitHub Jobs last**: Deprecated (use as absolute fallback)

---

## Common API Errors

### Error: Rate Limit Exceeded

**Symptom:** 429 status code

**Affected APIs:**
- Adzuna (250/day)
- JSearch (500/month)
- The Muse (500/hour)

**Solution:**
1. Workflow automatically tries next API
2. Wait until quota resets (check API docs for reset time)
3. Consider reducing workflow execution frequency

### Error: Invalid API Key

**Symptom:** 401 or 403 status code

**Affected APIs:**
- Adzuna (`app_id` / `app_key`)
- JSearch (`X-RapidAPI-Key`)
- USAJobs (`Authorization-Key`)

**Solution:**
1. Verify API key is correct (copy-paste error?)
2. Check key hasn't expired
3. Ensure key is active on provider dashboard
4. For JSearch: Verify both `X-RapidAPI-Key` AND `X-RapidAPI-Host` headers

### Error: Empty Results

**Symptom:** API responds 200 OK but `results` array empty

**Cause:** No jobs match search criteria

**Solution:**
1. Broaden search keywords (remove specific tech)
2. Remove location filter (try all locations)
3. Check if API has jobs for your region (USAJobs is U.S.-only)
4. Workflow automatically tries next API

### Error: Timeout

**Symptom:** Request takes >30 seconds, times out

**Affected APIs:**
- Remotive (occasionally slow)
- Adzuna (high load times)

**Solution:**
1. Increase n8n timeout to 60 seconds:
   - Edit HTTP Request node
   - Options → Timeout → 60000 ms
2. Workflow retries or moves to next API

### Error: Malformed Response

**Symptom:** JSON parse error

**Cause:** API returned HTML error page instead of JSON

**Solution:**
1. Check API status page (provider may be down)
2. Workflow logs error and tries next API
3. Report to API provider if persistent

---

## Monthly Quota Management

### Daily Quota

| API | Daily Limit | Daily Usage (avg) | Headroom |
|-----|-------------|-------------------|----------|
| Adzuna | 250 | 1 | 99.6% available |
| JSearch | ~16 (500/month) | 0-1 | 90%+ available |
| The Muse | 12,000 (500/hour) | 1 | 99.99% available |
| Others | Unlimited | Variable | N/A |

**Workflow executes once per day (8 AM UTC)**, so even limited APIs have plenty of headroom.

### Monitoring Quota

**Check n8n execution logs:**
- Look for "Rate limit" warnings
- Check which APIs succeeded/failed

**USAJobs Dashb**: Adzuna developer dashboard shows quota usage

**RapidAPI Dashboard**: JSearch quota visible at rapidapi.com/developer/dashboard

### What If You Hit Limits?

**Scenario:** Adzuna hits 250/day, JSearch exhausts 500/month

**Impact:** Workflow still works! Remaining 5 APIs provide jobs.

**Solution (if needed):**
1. Reduce workflow executions (once per day is already minimal)
2. Upgrade API plans (optional, defeats "100% free" goal)
3. Add more free APIs (there are others available)

---

## Adding New APIs

Want to add an 8th, 9th, or 10th API? Here's how:

### 1. Find Free Job API

**Resources:**
- [RapidAPI Job Search category](https://rapidapi.com/category/Jobs)
- [Public APIs list](https://github.com/public-apis/public-apis#jobs)
- Google search: "free job search API"

**Criteria:**
- Free tier available
- No credit card required
- Returns structured JSON
- At least 50-100 requests/month

### 2. Add to n8n Workflow

1. Clone existing "Fetch [API Name]" node
2. Rename to new API name
3. Update HTTP Request URL and headers
4. Add to fallback chain (connect after last API)

### 3. Update Documentation

Add new API to:
- This `FREE-APIS-LIST.md` file
- `MULTI-ACCOUNT-SETUP-GUIDE.md` Section 4
- `ACCOUNTS-CHECKLIST.json` API section

### 4. Test

1. Execute new node in isolation
2. Verify JSON response structure
3. Test fallback logic (disable all previous APIs)

---

## API Testing Tools

### Test Endpoints Manually

**cURL (command line):**
```bash
curl "https://remotive.com/api/remote-jobs"
```

**Postman (GUI):**
1. Download Postman
2. Create new GET request
3. Add headers (for authenticated APIs)
4. Send and inspect response

**n8n (workflow testing):**
1. Create test workflow
2. Add HTTP Request node
3. Configure endpoint
4. Execute node
5. View JSON output

### Verify API Status

Most APIs have status pages:
- Adzuna: Check developer.adzuna.com
- RapidAPI: rapidapi.com shows API status
- USAJobs: Check developer.usajobs.gov for announcements

---

## Best Practices

1. **Always include fallbacks**: Never rely on a single API
2. **Handle empty results gracefully**: Don't crash workflow if API returns zero jobs
3. **Log all errors**: Helps debug which API is problematic
4. **Test regularly**: APIs change, endpoints break
5. **Respect rate limits**: Don't hammer APIs with frequent requests
6. **Monitor quotas**: Check monthly usage, especially for limited APIs
7. **Update API keys**: Keys may expire, refresh proactively
8. **Read API docs**: Providers update endpoints, parameters, limits

---

## Summary

**You have access to 7 FREE job APIs:**

✅ **Remotive**: Unlimited, remote jobs  
✅ **Arbeitnow**: Unlimited, European jobs  
✅ **Adzuna**: 250/day, aggregated jobs  
✅ **JSearch**: 500/month, comprehensive  
✅ **The Muse**: 500/hour, curated jobs  
✅ **USAJobs**: Unlimited, U.S. government  
✅ **GitHub Jobs**: Unlimited, tech jobs (deprecated but works)  

**Intelligent cascading fallback** ensures near-100% uptime.

**Total cost: $0/month**

---

## Related Documentation

- **MULTI-ACCOUNT-SETUP-GUIDE.md**: How to configure APIs in workflow
- **ROTATION-SYSTEM-ARCHITECTURE.md**: Technical deep-dive into fallback logic
- **COMPLETE-SETUP-GUIDE.md**: Full workflow setup
- **ACCOUNTS-CHECKLIST.json**: All required credentials

---

**Last Updated**: 2024-01-20  
**Feature**: FEAT-006 - Comprehensive Documentation  
**Related Feature**: FEAT-004 - 4 New Job APIs with Fallback

