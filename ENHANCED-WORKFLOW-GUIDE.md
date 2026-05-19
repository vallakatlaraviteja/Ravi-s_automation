# Enhanced Master Workflow - Resume Intelligence Guide

## Overview

The **ENHANCED-MASTER-workflow.json** extends the original 44-node job automation system with intelligent resume parsing capabilities. This enhancement adds 7 new nodes to automatically download, parse, and incorporate your actual resume content into job scoring and email personalization.

## What's New

### Key Features Added

1. **Automatic Resume Download** - Fetches your resume from public URLs (Google Drive, GitHub, Dropbox)
2. **AI-Powered Resume Parsing** - Extracts skills, experience, projects, and achievements using Groq AI
3. **Enhanced Job Scoring** - Matches jobs against your actual resume content, not just static config
4. **Personalized Emails** - References specific projects and achievements from your resume
5. **Graceful Degradation** - Falls back to User Config if resume parsing fails
6. **Match Analytics** - Tracks skill overlap percentage and relevance scores in Google Sheets

## New Nodes Added (7 Total)

### 1. Download Resume
- **Type:** HTTP Request
- **Position:** [680, 150]
- **Function:** Downloads resume from User Config `resumeUrl` field
- **Supports:** Google Drive, GitHub raw URLs, Dropbox public links
- **Error Handling:** `continueOnFail: true` - workflow continues even if download fails

### 2. Check Resume Download Success
- **Type:** IF Node
- **Position:** [900, 150]
- **Function:** Checks if resume was downloaded successfully
- **Branches:**
  - **TRUE:** Proceeds to parse resume with AI
  - **FALSE:** Falls back to User Config only

### 3. Parse Resume with Groq AI
- **Type:** LangChain Groq Chat
- **Position:** [1120, 100]
- **Model:** llama-3.3-70b-versatile
- **Temperature:** 0.1 (for accurate extraction)
- **Function:** Extracts structured JSON with skills, experience, projects, achievements, education
- **Output Format:**
  ```json
  {
    "skills": ["Python", "AWS", "Docker", ...],
    "experience": [
      {
        "role": "Senior Engineer",
        "company": "Tech Corp",
        "duration": "2020-2023",
        "responsibilities": "Led backend development..."
      }
    ],
    "projects": [
      {
        "name": "Microservices Platform",
        "description": "Built scalable API",
        "technologies": ["Node.js", "Kubernetes"]
      }
    ],
    "achievements": ["Reduced latency by 40%", ...],
    "education": [{"degree": "BS CS", "institution": "MIT", "year": "2019"}]
  }
  ```

### 4. Structure Resume Data
- **Type:** Code Node (JavaScript)
- **Position:** [1340, 100]
- **Function:** Validates Groq JSON response, handles parsing errors
- **Fallback:** Uses User Config skills if parsing fails

### 5. Fallback: User Config Only
- **Type:** Code Node (JavaScript)
- **Position:** [1120, 200]
- **Function:** Creates resume data structure from User Config when download/parsing fails
- **Use Case:** Resume URL invalid, network error, or parsing failure

### 6. Merge User Config with Resume Data
- **Type:** Code Node (JavaScript)
- **Position:** [1560, 150]
- **Function:** Combines User Config with parsed resume data
- **Priority:** Resume data > User Config for skills and experience
- **Output:** Enriched profile object with `resumeData`, `projects`, `achievements` fields

### 7. Resume Match Analysis
- **Type:** Code Node (JavaScript)
- **Position:** [2220, 480]
- **Function:** Analyzes job match against resume
- **Calculations:**
  - Skill overlap percentage
  - Matched skills list
  - Experience relevance score
  - Project alignment check
- **Output:** `resumeMatchDetails` JSON string for Google Sheets column T

## Modified Nodes

### User Config (Master Profile)
**New Fields Added:**
```javascript
{
  resumeUrl: 'https://drive.google.com/file/d/YOUR_RESUME_ID/view',
  resumeParsingEnabled: true  // Set to false to disable resume features
}
```

### Groq AI: Score Job Match
**Enhanced Prompt:**
- Now includes **Resume Data** section with parsed skills, experience, and projects
- Scoring instructions updated to give bonus points for resume skill overlap (+20 points)
- References actual resume content in match reasoning

**Before:** Only used User Config skills array  
**After:** Uses parsed resume skills, experience, and projects for more accurate scoring

### Groq AI: Generate Personalized Email
**Enhanced Prompt:**
- New **Resume Insights** section with key projects, achievements, and recent experience
- Instructs AI to mention 2-3 specific projects from resume that align with job
- References actual achievements and technical details from resume

**Before:** Generic email with config skills  
**After:** Personalized email citing specific resume projects and achievements

### Parse & Format Email
**Updated to:**
- Use merged config instead of direct User Config reference
- Ensures profile links include resume URL

### Google Sheets: Append Node
**New Column Added:**
- **Column T:** `Resume Match Details` (JSON string with skill overlap, matched skills, relevance score)
- Existing 19 columns preserved

## Workflow Flow

### Job Discovery Branch (Enhanced)
```
Trigger → User Config → Download Resume
                         ↓
                      Check Success?
                      ↙         ↘
              (Success)         (Fail)
              Parse Resume      Fallback to
                  ↓             User Config
              Structure Data        ↓
                  ↓                 ↓
              Merge Config ← ───────┘
                  ↓
            [Existing nodes]
                  ↓
            Score Job Match (uses resume data)
                  ↓
            Resume Match Analysis
                  ↓
            Filter by Score
                  ↓
            Append to Sheets (with Resume Match Details)
```

### Email Outreach Branch (Enhanced)
```
[Existing trigger and filter nodes]
    ↓
Generate Email (references resume projects)
    ↓
Parse & Format Email
    ↓
Send Email
```

## User Configuration

### Setting Up Resume URL

1. **Google Drive (Recommended):**
   - Upload resume to Google Drive
   - Right-click → Share → "Anyone with the link can view"
   - Copy the share link (format: `https://drive.google.com/file/d/FILE_ID/view`)
   - Paste into User Config `resumeUrl` field
   - Node automatically converts to download URL

2. **GitHub:**
   - Upload resume to public GitHub repo
   - Navigate to file, click "Raw"
   - Copy raw URL (format: `https://raw.githubusercontent.com/user/repo/main/resume.pdf`)
   - Paste into User Config `resumeUrl` field

3. **Dropbox:**
   - Upload resume to Dropbox
   - Right-click → Share → Create public link
   - Copy link and ensure it ends with `?dl=1`
   - Paste into User Config `resumeUrl` field

### Supported Resume Formats
- **PDF** (Recommended - best parsing accuracy)
- **DOCX** (Microsoft Word)
- **TXT** (Plain text)

### Disabling Resume Features

If you prefer to use only User Config (no resume parsing):

```javascript
{
  resumeParsingEnabled: false
}
```

The workflow will skip resume download and use User Config data only.

## Google Sheets Schema Update

### New Column T: Resume Match Details

**Format:** JSON string  
**Example:**
```json
{
  "skillOverlapPercent": 75,
  "matchedSkills": ["Python", "AWS", "Docker", "Kubernetes"],
  "totalResumeSkills": 12,
  "experienceYears": 5,
  "hasRelevantProjects": true,
  "relevanceScore": 85,
  "resumeParsed": true
}
```

**Use Case:** Filter jobs by skill overlap percentage, identify high-relevance matches

## Benefits

### Before Enhancement
- Job scoring based on static User Config skills array
- Emails generic, mentioning only config fields
- No insight into actual resume content
- Manual effort to align applications with resume

### After Enhancement
- **20+ point scoring boost** for jobs matching resume skills
- **Emails reference 2-3 specific resume projects** relevant to each job
- **Automatic skill overlap analysis** - see which jobs match your resume
- **Credible, personalized outreach** citing actual achievements
- **Resume analytics** - track which skills appear in matched jobs

## Error Handling

### Scenario 1: Invalid Resume URL
- Download node fails (continueOnFail: true)
- Check node routes to "Fallback: User Config Only"
- Workflow continues with User Config skills
- `resumeParsed: false` in output

### Scenario 2: Groq Parsing Fails
- Structure Resume Data catches JSON parse error
- Falls back to User Config skills
- Logs error but continues workflow
- `resumeParsed: false` in output

### Scenario 3: Resume Not Accessible
- HTTP 403/404 on download
- Workflow continues with fallback
- No workflow execution blocked

**Key Principle:** Resume features enhance but never break the workflow.

## Verification Checklist

After importing into n8n:

- [ ] User Config node has `resumeUrl` and `resumeParsingEnabled` fields
- [ ] Download Resume node shows correct URL transformation logic
- [ ] Check Resume Download Success node has two output branches
- [ ] Parse Resume with Groq AI credential points to YOUR_GROQ_CREDENTIAL_ID
- [ ] Merge User Config with Resume Data node exists at [1560, 150]
- [ ] Groq Score Job prompt includes "**Resume Data:**" section
- [ ] Groq Generate Email prompt includes "**Resume Insights:**" section
- [ ] Resume Match Analysis calculates `skillOverlapPercent`
- [ ] Google Sheets append has 20 columns including `resumeMatchDetails`
- [ ] All existing nodes (44) are intact
- [ ] Total nodes = 51

## Testing

### Manual Test: Resume Download
1. Add valid Google Drive resume URL to User Config
2. Execute "Download Resume" node manually
3. Verify output contains resume text (PDF content or DOCX text)

### Manual Test: Resume Parsing
1. Execute "Parse Resume with Groq AI" node
2. Verify JSON output with skills, experience, projects arrays
3. Check "Structure Resume Data" output has `parsed: true`

### Manual Test: Job Scoring
1. Run Job Discovery branch with sample job
2. Check "Groq AI: Score Job Match" prompt includes resume data
3. Verify score is higher for jobs matching resume skills

### Manual Test: Email Generation
1. Run Email Outreach branch
2. Check "Parse & Format Email" output
3. Verify email mentions specific resume projects

### Manual Test: Graceful Degradation
1. Set `resumeUrl` to invalid URL (e.g., "http://invalid")
2. Execute workflow
3. Verify it continues with User Config fallback
4. Check `resumeParsed: false` in output

## Migration from Original Workflow

If you're already using MASTER-job-automation-workflow.json:

1. **Backup existing workflow** - Export from n8n
2. **Copy credentials** - Note your credential IDs
3. **Import ENHANCED-MASTER-workflow.json**
4. **Update User Config** - Add `resumeUrl` and `resumeParsingEnabled` fields
5. **Replace credential placeholders** - Update all YOUR_*_CREDENTIAL_ID
6. **Test resume download** - Execute Download Resume node
7. **Verify connections** - Check all nodes have proper connections
8. **Test existing features** - Run Job Discovery and Email Outreach branches
9. **Activate workflow** - Enable all three triggers

**No data loss:** All existing Google Sheets data remains intact. New column T is optional.

## Troubleshooting

### Issue: Resume download fails with 403 Forbidden
**Solution:** Ensure Google Drive file is set to "Anyone with the link can view"

### Issue: Groq parsing returns empty skills array
**Solution:** 
- Check resume format (PDF works best)
- Verify resume content is readable (not scanned image)
- Check Groq API key is valid

### Issue: Emails don't mention resume projects
**Solution:**
- Check "Merge User Config with Resume Data" output has `projects` array
- Verify "Parse Resume with Groq AI" extracted projects successfully
- Check `resumeParsed: true` in merged config

### Issue: Workflow breaks on resume error
**Solution:** Verify:
- Download Resume has `continueOnFail: true`
- Check Resume Download Success node exists
- Fallback node is connected

### Issue: Google Sheets error about column count
**Solution:** 
- Add "Resume Match Details" as column T header in your sheet
- Or remove `resumeMatchDetails` from append node columns

## Performance Impact

- **Resume download:** +2-5 seconds per workflow execution
- **Groq parsing:** +3-8 seconds per workflow execution
- **Total overhead:** ~10 seconds per job discovery run
- **Daily API calls:** +1 Groq call for resume parsing (cached in workflow context)
- **Cost:** $0 (Groq free tier: 30 requests/minute, 14,400/day)

**Optimization:** Resume is parsed once per workflow run, then reused for all jobs.

## Credits

- **Original Workflow:** 44-node job automation system
- **Enhancement:** Resume intelligence with Groq AI parsing
- **Added Nodes:** 7 (51 total)
- **Free Services:** Groq AI (llama-3.3-70b-versatile)
- **Compatibility:** n8n 1.0+

---

For support or questions, refer to the original README.md and SETUP-INSTRUCTIONS.md.
