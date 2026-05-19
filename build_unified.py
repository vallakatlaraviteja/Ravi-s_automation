#!/usr/bin/env python3
import json

# Build complete unified MASTER workflow
workflow = {
    "name": "MASTER Job Automation System",
    "nodes": [],
    "connections": {},
    "settings": {"executionOrder": "v1"},
    "staticData": None,
    "tags": [],
    "triggerCount": 3,
    "updatedAt": "2024-01-15T00:00:00.000Z",
    "versionId": "1"
}

# Helper function to create node
def create_node(id, name, type, params, position, **kwargs):
    node = {
        "id": id,
        "name": name,
        "type": type,
        "typeVersion": kwargs.get("typeVersion", 1),
        "position": position,
        "parameters": params
    }
    if "credentials" in kwargs:
        node["credentials"] = kwargs["credentials"]
    if "continueOnFail" in kwargs:
        node["continueOnFail"] = kwargs["continueOnFail"]
    if "webhookId" in kwargs:
        node["webhookId"] = kwargs["webhookId"]
    return node

# TRIGGER 1: Schedule - Daily 8 AM (Job Discovery)
workflow["nodes"].append(create_node(
    "trigger-1-job-discovery",
    "Schedule Trigger: Job Discovery (8 AM)",
    "n8n-nodes-base.scheduleTrigger",
    {"rule": {"interval": [{"field": "cronExpression", "expression": "0 8 * * *"}]}},
    [240, 300],
    typeVersion=1.1
))

# TRIGGER 2: Schedule - Daily 9 AM (Email Outreach)
workflow["nodes"].append(create_node(
    "trigger-2-email-outreach",
    "Schedule Trigger: Email Outreach (9 AM)",
    "n8n-nodes-base.scheduleTrigger",
    {"rule": {"interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]}},
    [240, 1800],
    typeVersion=1.1
))

# TRIGGER 3: Telegram Bot
workflow["nodes"].append(create_node(
    "trigger-3-telegram",
    "Telegram Trigger: Interactive Assistant",
    "n8n-nodes-base.telegramTrigger",
    {"updates": ["message"]},
    [240, 3300],
    typeVersion=1,
    credentials={"telegramApi": {"id": "YOUR_TELEGRAM_CREDENTIAL_ID", "name": "Telegram Bot"}},
    webhookId="telegram-job-bot"
))

# USER CONFIG NODE (shared)
user_config_code = """// User profile configuration - single source of truth
return [{
  json: {
    name: 'Your Name',
    currentRole: 'Senior Backend Engineer',
    targetRole: 'Staff Engineer',
    experience: '5 years',
    skills: ['Python', 'Node.js', 'AWS', 'Docker', 'Kubernetes', 'PostgreSQL'],
    location: 'Hyderabad, India',
    workMode: ['remote', 'hybrid'],
    minSalary: 80000,
    targetRoles: ['Backend Engineer', 'Full Stack Engineer', 'DevOps Engineer'],
    keywords: 'python developer OR backend engineer OR nodejs',
    country: 'in',
    githubUrl: 'https://github.com/yourusername',
    linkedinUrl: 'https://linkedin.com/in/yourprofile',
    portfolioUrl: 'https://yourportfolio.com',
    resumeUrl: 'https://drive.google.com/file/d/YOUR_RESUME_ID/view',
    userEmail: 'YOUR_EMAIL@example.com',
    dailyLimit: 10,
    scoreThreshold: 30,
    sheetId: 'YOUR_SPREADSHEET_ID'
  }
}];"""

workflow["nodes"].append(create_node(
    "user-config",
    "User Config (Master Profile)",
    "n8n-nodes-base.code",
    {"jsCode": user_config_code},
    [460, 300],
    typeVersion=2
))


# ========== JOB DISCOVERY BRANCH (TRIGGER 1) ==========

# API Fetch nodes - Remotive
workflow["nodes"].append(create_node(
    "fetch-remotive",
    "Fetch Remotive API",
    "n8n-nodes-base.httpRequest",
    {
        "url": "https://remotive.com/api/remote-jobs",
        "method": "GET",
        "sendQuery": True,
        "queryParameters": {
            "parameters": [
                {"name": "search", "value": "={{ $('User Config (Master Profile)').item.json.keywords }}"},
                {"name": "limit", "value": "50"}
            ]
        },
        "options": {"timeout": 30000}
    },
    [680, 240],
    typeVersion=4.1,
    continueOnFail=True
))

# API Fetch nodes - Arbeitnow
workflow["nodes"].append(create_node(
    "fetch-arbeitnow",
    "Fetch Arbeitnow API",
    "n8n-nodes-base.httpRequest",
    {
        "url": "https://www.arbeitnow.com/api/job-board-api",
        "method": "GET",
        "sendQuery": True,
        "queryParameters": {
            "parameters": [
                {"name": "search", "value": "={{ $('User Config (Master Profile)').item.json.keywords }}"},
                {"name": "limit", "value": "50"}
            ]
        },
        "options": {"timeout": 30000}
    },
    [680, 360],
    typeVersion=4.1,
    continueOnFail=True
))

# API Fetch nodes - Adzuna
workflow["nodes"].append(create_node(
    "fetch-adzuna",
    "Fetch Adzuna API",
    "n8n-nodes-base.httpRequest",
    {
        "url": "=https://api.adzuna.com/v1/api/jobs/{{ $('User Config (Master Profile)').item.json.country }}/search/1",
        "method": "GET",
        "sendQuery": True,
        "queryParameters": {
            "parameters": [
                {"name": "app_id", "value": "YOUR_ADZUNA_APP_ID"},
                {"name": "app_key", "value": "YOUR_ADZUNA_APP_KEY"},
                {"name": "what", "value": "={{ $('User Config (Master Profile)').item.json.keywords }}"},
                {"name": "results_per_page", "value": "50"}
            ]
        },
        "options": {"timeout": 30000}
    },
    [680, 480],
    typeVersion=4.1,
    continueOnFail=True
))

# Parse Remotive
parse_remotive_code = """// Parse Remotive API response
const response = items[0].json;
const jobs = response.jobs || [];

return jobs.map(job => ({
  json: {
    source: 'Remotive',
    jobTitle: job.title || 'Unknown',
    company: job.company_name || 'Unknown',
    location: job.candidate_required_location || 'Remote',
    jobType: job.job_type || 'Full-time',
    workMode: 'Remote',
    salary: job.salary || 'Not disclosed',
    applyUrl: job.url || '',
    description: (job.description || '').substring(0, 500),
    tags: job.tags || [],
    postedDate: job.publication_date || new Date().toISOString().split('T')[0],
    category: job.category || '',
    jobId: `remotive-${job.id || Date.now()}`,
    fetchedDate: new Date().toISOString().split('T')[0],
    recruiterEmail: '',
    recruiterName: ''
  }
}));"""

workflow["nodes"].append(create_node(
    "parse-remotive",
    "Parse Remotive Response",
    "n8n-nodes-base.code",
    {"jsCode": parse_remotive_code},
    [900, 240],
    typeVersion=2,
    continueOnFail=True
))

# Parse Arbeitnow
parse_arbeitnow_code = """// Parse Arbeitnow API response
const response = items[0].json;
const jobs = response.data || [];

return jobs.map(job => ({
  json: {
    source: 'Arbeitnow',
    jobTitle: job.title || 'Unknown',
    company: job.company_name || 'Unknown',
    location: job.location || 'Remote',
    jobType: job.job_types?.[0] || 'Full-time',
    workMode: job.remote ? 'Remote' : 'Onsite',
    salary: 'Not disclosed',
    applyUrl: job.url || '',
    description: (job.description || '').substring(0, 500),
    tags: job.tags || [],
    postedDate: job.created_at ? new Date(job.created_at * 1000).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
    category: '',
    jobId: `arbeitnow-${job.slug || Date.now()}`,
    fetchedDate: new Date().toISOString().split('T')[0],
    recruiterEmail: '',
    recruiterName: ''
  }
}));"""

workflow["nodes"].append(create_node(
    "parse-arbeitnow",
    "Parse Arbeitnow Response",
    "n8n-nodes-base.code",
    {"jsCode": parse_arbeitnow_code},
    [900, 360],
    typeVersion=2,
    continueOnFail=True
))

# Parse Adzuna
parse_adzuna_code = """// Parse Adzuna API response
const response = items[0].json;
const jobs = response.results || [];

return jobs.map(job => ({
  json: {
    source: 'Adzuna',
    jobTitle: job.title || 'Unknown',
    company: job.company?.display_name || 'Unknown',
    location: job.location?.display_name || 'Not specified',
    jobType: job.contract_time || 'Full-time',
    workMode: 'Not specified',
    salary: job.salary_max ? `${job.salary_min || 0} - ${job.salary_max}` : 'Not disclosed',
    applyUrl: job.redirect_url || '',
    description: (job.description || '').substring(0, 500),
    tags: job.category?.tag ? [job.category.tag] : [],
    postedDate: job.created || new Date().toISOString().split('T')[0],
    category: job.category?.label || '',
    jobId: `adzuna-${job.id || Date.now()}`,
    fetchedDate: new Date().toISOString().split('T')[0],
    recruiterEmail: '',
    recruiterName: ''
  }
}));"""

workflow["nodes"].append(create_node(
    "parse-adzuna",
    "Parse Adzuna Response",
    "n8n-nodes-base.code",
    {"jsCode": parse_adzuna_code},
    [900, 480],
    typeVersion=2,
    continueOnFail=True
))


# Merge all jobs
workflow["nodes"].append(create_node(
    "merge-job-apis",
    "Merge All API Results",
    "n8n-nodes-base.merge",
    {"mode": "combine", "options": {}},
    [1120, 360],
    typeVersion=2.1
))

# Deduplicate
dedupe_code = """// Deduplicate and filter existing jobs
const jobs = items.map(item => item.json);
const seen = new Set();
const unique = [];

for (const job of jobs) {
  const key = `${job.company}-${job.jobTitle}`.toLowerCase().replace(/\\s+/g, '-');
  if (!seen.has(key) && job.applyUrl) {
    seen.add(key);
    unique.push(job);
  }
}

return unique.map(job => ({ json: job }));"""

workflow["nodes"].append(create_node(
    "deduplicate-jobs",
    "Deduplicate Jobs",
    "n8n-nodes-base.code",
    {"jsCode": dedupe_code},
    [1340, 360],
    typeVersion=2
))

# Read existing sheet to filter
workflow["nodes"].append(create_node(
    "read-existing-jobs",
    "Read Existing Jobs from Sheet",
    "n8n-nodes-base.googleSheets",
    {
        "operation": "read",
        "documentId": {"__rl": True, "value": "={{ $('User Config (Master Profile)').item.json.sheetId }}", "mode": "id"},
        "sheetName": {"__rl": True, "value": "Jobs", "mode": "name"},
        "options": {}
    },
    [1560, 360],
    typeVersion=4.2,
    credentials={"googleSheetsOAuth2Api": {"id": "YOUR_GOOGLE_SHEETS_CREDENTIAL_ID", "name": "Google Sheets OAuth2"}},
    continueOnFail=True
))

# Filter out already-seen jobs
filter_new_code = """// Filter out jobs already in sheet
const newJobs = $('Deduplicate Jobs').all().map(item => item.json);
const existingJobs = items.map(item => item.json);

const existingIds = new Set(existingJobs.map(j => j['Job ID'] || j.jobId));

const trulyNew = newJobs.filter(job => !existingIds.has(job.jobId));

if (trulyNew.length === 0) {
  throw new Error('No new jobs found - all already in sheet');
}

return trulyNew.map(job => ({ json: job }));"""

workflow["nodes"].append(create_node(
    "filter-new-jobs",
    "Filter Out Already-Fetched Jobs",
    "n8n-nodes-base.code",
    {"jsCode": filter_new_code},
    [1780, 360],
    typeVersion=2,
    continueOnFail=True
))

# Groq AI Scoring
workflow["nodes"].append(create_node(
    "groq-score-job",
    "Groq AI: Score Job Match",
    "@n8n/n8n-nodes-langchain.lmChatGroq",
    {
        "operation": "text",
        "options": {"temperature": 0.3},
        "text": """=You are a job matching expert. Score this job for relevance (0-100):

**Job:** {{ $json.jobTitle }} at {{ $json.company }}
**Location:** {{ $json.location }}
**Work Mode:** {{ $json.workMode }}
**Description:** {{ $json.description }}

**User Profile:**
- Current Role: {{ $('User Config (Master Profile)').item.json.currentRole }}
- Target Role: {{ $('User Config (Master Profile)').item.json.targetRole }}
- Skills: {{ $('User Config (Master Profile)').item.json.skills.join(', ') }}
- Work Mode: {{ $('User Config (Master Profile)').item.json.workMode.join(' or ') }}
- Location: {{ $('User Config (Master Profile)').item.json.location }}

Provide ONLY a JSON object:
{"score": <0-100>, "priority": "high|medium|low", "matchReason": "<1 sentence>"}

No other text."""
    },
    [2000, 360],
    typeVersion=1,
    credentials={"groqApi": {"id": "YOUR_GROQ_CREDENTIAL_ID", "name": "Groq API"}}
))

# Parse score
parse_score_code = """// Parse Groq scoring response
const jobData = items[0].json;
const groqResponse = $node["Groq AI: Score Job Match"].json.response || $node["Groq AI: Score Job Match"].json.text || '';

let score = 50;
let priority = 'medium';
let matchReason = 'Standard match';

try {
  const jsonMatch = groqResponse.match(/\\{[\\s\\S]*\\}/);
  if (jsonMatch) {
    const parsed = JSON.parse(jsonMatch[0]);
    score = parsed.score || 50;
    priority = parsed.priority || 'medium';
    matchReason = parsed.matchReason || 'Standard match';
  }
} catch (error) {
  console.error('Failed to parse Groq response, using defaults');
}

return [{
  json: {
    ...jobData,
    score,
    priority,
    matchReason,
    status: 'New',
    applicationId: '',
    emailSentDate: '',
    lastUpdated: new Date().toISOString().split('T')[0]
  }
}];"""

workflow["nodes"].append(create_node(
    "parse-score",
    "Parse AI Score",
    "n8n-nodes-base.code",
    {"jsCode": parse_score_code},
    [2220, 360],
    typeVersion=2
))

# Filter by score threshold
workflow["nodes"].append(create_node(
    "filter-by-score",
    "Filter by Score Threshold (≥30)",
    "n8n-nodes-base.if",
    {
        "conditions": {
            "number": [
                {"value1": "={{ $json.score }}", "operation": "largerEqual", "value2": "={{ $('User Config (Master Profile)').item.json.scoreThreshold }}"}
            ]
        }
    },
    [2440, 360],
    typeVersion=1
))

# Append to Google Sheets
workflow["nodes"].append(create_node(
    "append-to-sheet-jobs",
    "Append to Google Sheets: Jobs Tab",
    "n8n-nodes-base.googleSheets",
    {
        "operation": "append",
        "documentId": {"__rl": True, "value": "={{ $('User Config (Master Profile)').item.json.sheetId }}", "mode": "id"},
        "sheetName": {"__rl": True, "value": "Jobs", "mode": "name"},
        "columns": {
            "mappingMode": "autoMapInputData",
            "matchingColumns": [],
            "schema": [
                {"id": "jobId", "displayName": "Job ID", "type": "string"},
                {"id": "jobTitle", "displayName": "Job Title", "type": "string"},
                {"id": "company", "displayName": "Company", "type": "string"},
                {"id": "location", "displayName": "Location", "type": "string"},
                {"id": "workMode", "displayName": "Work Mode", "type": "string"},
                {"id": "salary", "displayName": "Salary", "type": "string"},
                {"id": "applyUrl", "displayName": "Apply URL", "type": "string"},
                {"id": "source", "displayName": "Source", "type": "string"},
                {"id": "score", "displayName": "Score", "type": "number"},
                {"id": "priority", "displayName": "Priority", "type": "string"},
                {"id": "matchReason", "displayName": "Match Reason", "type": "string"},
                {"id": "status", "displayName": "Status", "type": "string"},
                {"id": "postedDate", "displayName": "Posted Date", "type": "string"},
                {"id": "fetchedDate", "displayName": "Fetched Date", "type": "string"},
                {"id": "recruiterEmail", "displayName": "Recruiter Email", "type": "string"},
                {"id": "recruiterName", "displayName": "Recruiter Name", "type": "string"},
                {"id": "applicationId", "displayName": "Application ID", "type": "string"},
                {"id": "emailSentDate", "displayName": "Email Sent Date", "type": "string"},
                {"id": "lastUpdated", "displayName": "Last Updated", "type": "string"}
            ]
        },
        "options": {}
    },
    [2660, 360],
    typeVersion=4.2,
    credentials={"googleSheetsOAuth2Api": {"id": "YOUR_GOOGLE_SHEETS_CREDENTIAL_ID", "name": "Google Sheets OAuth2"}}
))


# Aggregate summary for notifications
aggregate_summary_code = """// Aggregate job discovery summary
const jobs = items.map(item => item.json);
const total = jobs.length;
const high = jobs.filter(j => j.priority === 'high').length;
const medium = jobs.filter(j => j.priority === 'medium').length;
const low = jobs.filter(j => j.priority === 'low').length;

const topJobs = jobs
  .sort((a, b) => b.score - a.score)
  .slice(0, 5)
  .map(j => `• **${j.jobTitle}** at **${j.company}** (${j.location}) - Score: ${j.score} [${j.source}]`);

const sourceBreakdown = jobs.reduce((acc, j) => {
  acc[j.source] = (acc[j.source] || 0) + 1;
  return acc;
}, {});

const sourceStats = Object.entries(sourceBreakdown)
  .map(([source, count]) => `${source}: ${count}`)
  .join(', ');

return [{
  json: {
    total,
    high,
    medium,
    low,
    topJobsList: topJobs.join('\\n'),
    sourceStats,
    date: new Date().toISOString().split('T')[0]
  }
}];"""

workflow["nodes"].append(create_node(
    "aggregate-job-summary",
    "Aggregate Job Discovery Summary",
    "n8n-nodes-base.code",
    {"jsCode": aggregate_summary_code},
    [2880, 360],
    typeVersion=2
))

# Send Telegram notification
workflow["nodes"].append(create_node(
    "send-telegram-job-digest",
    "Send Telegram: Job Discovery Digest",
    "n8n-nodes-base.telegram",
    {
        "chatId": "YOUR_TELEGRAM_CHAT_ID",
        "text": """=📊 **Daily Job Discovery Complete**

✅ Found **{{ $json.total }}** new relevant jobs!

**Priority Breakdown:**
🔴 High: {{ $json.high }}
🟡 Medium: {{ $json.medium }}
🟢 Low: {{ $json.low }}

**Sources:** {{ $json.sourceStats }}

**Top 5 Matches:**
{{ $json.topJobsList }}

All jobs saved to Google Sheet. Add recruiter emails for auto-outreach!

**Date:** {{ $json.date }}""",
        "additionalFields": {}
    },
    [3100, 300],
    typeVersion=1.2,
    credentials={"telegramApi": {"id": "YOUR_TELEGRAM_CREDENTIAL_ID", "name": "Telegram Bot"}}
))

# Send Gmail digest
workflow["nodes"].append(create_node(
    "send-gmail-job-digest",
    "Send Gmail: Job Discovery Digest",
    "n8n-nodes-base.gmail",
    {
        "sendTo": "={{ $('User Config (Master Profile)').item.json.userEmail }}",
        "subject": "📊 Daily Job Discovery - {{ $json.total }} New Jobs",
        "message": """=Hello {{ $('User Config (Master Profile)').item.json.name }},

Your job discovery engine found **{{ $json.total }}** new relevant jobs!

**Priority Breakdown:**
🔴 High: {{ $json.high }}
🟡 Medium: {{ $json.medium }}
🟢 Low: {{ $json.low }}

**Sources:**
{{ $json.sourceStats }}

**Top 5 Matches:**
{{ $json.topJobsList }}

All jobs have been added to your Google Sheet.
Review them and add recruiter emails for auto-outreach.

**Date:** {{ $json.date }}

Best regards,
Job Discovery Engine""",
        "options": {}
    },
    [3100, 420],
    typeVersion=2.1,
    credentials={"gmailOAuth2": {"id": "YOUR_GMAIL_CREDENTIAL_ID", "name": "Gmail OAuth2"}}
))

# ========== EMAIL OUTREACH BRANCH (TRIGGER 2) ==========

# Read job sheet for outreach
workflow["nodes"].append(create_node(
    "read-jobs-for-outreach",
    "Read Jobs from Sheet for Outreach",
    "n8n-nodes-base.googleSheets",
    {
        "operation": "read",
        "documentId": {"__rl": True, "value": "={{ $('User Config (Master Profile)').item.json.sheetId }}", "mode": "id"},
        "sheetName": {"__rl": True, "value": "Jobs", "mode": "name"},
        "options": {}
    },
    [680, 1800],
    typeVersion=4.2,
    credentials={"googleSheetsOAuth2Api": {"id": "YOUR_GOOGLE_SHEETS_CREDENTIAL_ID", "name": "Google Sheets OAuth2"}}
))

# Filter for sendable jobs
workflow["nodes"].append(create_node(
    "filter-sendable-jobs",
    "Filter: Status=New AND Has Recruiter Email",
    "n8n-nodes-base.if",
    {
        "conditions": {
            "string": [
                {"value1": "={{ $json.Status || $json.status }}", "operation": "equals", "value2": "New"},
                {"value1": "={{ $json['Recruiter Email'] || $json.recruiterEmail }}", "operation": "isNotEmpty"}
            ]
        },
        "combineOperation": "all"
    },
    [900, 1800],
    typeVersion=1
))

# Limit to daily max
workflow["nodes"].append(create_node(
    "limit-daily-emails",
    "Limit to Daily Max (10 emails)",
    "n8n-nodes-base.limit",
    {"numberValue": "={{ $('User Config (Master Profile)').item.json.dailyLimit }}"},
    [1120, 1800],
    typeVersion=1
))

# Generate personalized email with Groq
workflow["nodes"].append(create_node(
    "groq-generate-email",
    "Groq AI: Generate Personalized Email",
    "@n8n/n8n-nodes-langchain.lmChatGroq",
    {
        "operation": "text",
        "options": {"temperature": 0.7},
        "text": """=You are a professional email writer. Generate a personalized cold email to a recruiter.

**Job Details:**
- Title: {{ $json['Job Title'] || $json.jobTitle }}
- Company: {{ $json.Company || $json.company }}
- Recruiter: {{ $json['Recruiter Name'] || $json.recruiterName || 'Hiring Manager' }}
- Location: {{ $json.Location || $json.location }}
- Apply URL: {{ $json['Apply URL'] || $json.applyUrl }}

**Candidate Profile:**
- Name: {{ $('User Config (Master Profile)').item.json.name }}
- Current Role: {{ $('User Config (Master Profile)').item.json.currentRole }}
- Experience: {{ $('User Config (Master Profile)').item.json.experience }}
- Skills: {{ $('User Config (Master Profile)').item.json.skills.join(', ') }}
- Location: {{ $('User Config (Master Profile)').item.json.location }}

**Requirements:**
1. Professional, concise (150-200 words)
2. Show genuine interest in the company/role
3. Highlight 2-3 relevant skills from job description
4. Include a clear call-to-action
5. End with "Best regards, {{ $('User Config (Master Profile)').item.json.name }}"

**Format:**
Subject: [Generate compelling subject line]

[Email body]

Provide ONLY the subject line and email body. No additional commentary."""
    },
    [1340, 1800],
    typeVersion=1,
    credentials={"groqApi": {"id": "YOUR_GROQ_CREDENTIAL_ID", "name": "Groq API"}}
))


# Parse and format email
parse_email_code = """// Parse Groq email response
const jobData = items[0].json;
const groqResponse = $node["Groq AI: Generate Personalized Email"].json.response || $node["Groq AI: Generate Personalized Email"].json.text || '';

let subject = `Application for ${jobData['Job Title'] || jobData.jobTitle} at ${jobData.Company || jobData.company}`;
let body = groqResponse;

// Try to extract subject line
const subjectMatch = groqResponse.match(/Subject:\\s*(.+?)\\n/i);
if (subjectMatch) {
  subject = subjectMatch[1].trim();
  body = groqResponse.replace(/Subject:\\s*.+?\\n/i, '').trim();
}

const config = $('User Config (Master Profile)').item.json;

// Add signature if not present
if (!body.includes(config.name)) {
  body += `\\n\\nBest regards,\\n${config.name}`;
}

// Add profile links
body += `\\n\\nPortfolio: ${config.portfolioUrl}`;
body += `\\nLinkedIn: ${config.linkedinUrl}`;
body += `\\nGitHub: ${config.githubUrl}`;
body += `\\nResume: ${config.resumeUrl}`;

return [{
  json: {
    ...jobData,
    emailSubject: subject,
    emailBody: body,
    sentDate: new Date().toISOString().split('T')[0]
  }
}];"""

workflow["nodes"].append(create_node(
    "parse-format-email",
    "Parse & Format Email",
    "n8n-nodes-base.code",
    {"jsCode": parse_email_code},
    [1560, 1800],
    typeVersion=2
))

# Send email via Gmail
workflow["nodes"].append(create_node(
    "send-gmail-outreach",
    "Send Email via Gmail",
    "n8n-nodes-base.gmail",
    {
        "sendTo": "={{ $json['Recruiter Email'] || $json.recruiterEmail }}",
        "subject": "={{ $json.emailSubject }}",
        "message": "={{ $json.emailBody }}",
        "options": {"ccList": "={{ $('User Config (Master Profile)').item.json.userEmail }}"}
    },
    [1780, 1800],
    typeVersion=2.1,
    credentials={"gmailOAuth2": {"id": "YOUR_GMAIL_CREDENTIAL_ID", "name": "Gmail OAuth2"}}
))

# Update metadata after sending
update_metadata_code = """// Update status and add metadata
const applicationId = `EMAIL-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;

return [{
  json: {
    ...items[0].json,
    Status: 'Email Sent',
    status: 'Email Sent',
    'Application ID': applicationId,
    applicationId: applicationId,
    'Email Sent Date': new Date().toISOString().split('T')[0],
    emailSentDate: new Date().toISOString().split('T')[0],
    'Last Updated': new Date().toISOString().split('T')[0],
    lastUpdated: new Date().toISOString().split('T')[0]
  }
}];"""

workflow["nodes"].append(create_node(
    "update-email-metadata",
    "Update Metadata (Status & Application ID)",
    "n8n-nodes-base.code",
    {"jsCode": update_metadata_code},
    [2000, 1800],
    typeVersion=2
))

# Update Google Sheet
workflow["nodes"].append(create_node(
    "update-sheet-status",
    "Update Sheet: Mark Email Sent",
    "n8n-nodes-base.googleSheets",
    {
        "operation": "update",
        "documentId": {"__rl": True, "value": "={{ $('User Config (Master Profile)').item.json.sheetId }}", "mode": "id"},
        "sheetName": {"__rl": True, "value": "Jobs", "mode": "name"},
        "columns": {
            "mappingMode": "autoMapInputData",
            "matchingColumns": ["Job Title", "Company"],
            "schema": [
                {"id": "Status", "displayName": "Status", "type": "string"},
                {"id": "Application ID", "displayName": "Application ID", "type": "string"},
                {"id": "Email Sent Date", "displayName": "Email Sent Date", "type": "string"},
                {"id": "Last Updated", "displayName": "Last Updated", "type": "string"}
            ]
        },
        "options": {}
    },
    [2220, 1800],
    typeVersion=4.2,
    credentials={"googleSheetsOAuth2Api": {"id": "YOUR_GOOGLE_SHEETS_CREDENTIAL_ID", "name": "Google Sheets OAuth2"}}
))

# Rate limit delay
workflow["nodes"].append(create_node(
    "rate-limit-delay",
    "Rate Limit Delay (3 seconds)",
    "n8n-nodes-base.wait",
    {"amount": 3, "unit": "seconds"},
    [2440, 1800],
    typeVersion=1
))

# Aggregate outreach summary
aggregate_outreach_code = """// Aggregate sending summary
const jobs = items.map(item => item.json);
const total = jobs.length;

const sentList = jobs.map(j => 
  `• **${j['Job Title'] || j.jobTitle}** at **${j.Company || j.company}** → ${j['Recruiter Email'] || j.recruiterEmail}`
);

return [{
  json: {
    total,
    sentList: sentList.join('\\n'),
    date: new Date().toISOString().split('T')[0]
  }
}];"""

workflow["nodes"].append(create_node(
    "aggregate-outreach-summary",
    "Aggregate Outreach Summary",
    "n8n-nodes-base.code",
    {"jsCode": aggregate_outreach_code},
    [2660, 1800],
    typeVersion=2
))

# Send outreach digest
workflow["nodes"].append(create_node(
    "send-outreach-digest",
    "Send Gmail: Outreach Digest",
    "n8n-nodes-base.gmail",
    {
        "sendTo": "={{ $('User Config (Master Profile)').item.json.userEmail }}",
        "subject": "✅ Email Outreach Complete - {{ $json.total }} Emails Sent",
        "message": """=Hello {{ $('User Config (Master Profile)').item.json.name }},

Your daily email outreach campaign has completed!

**Total Emails Sent:** {{ $json.total }}

**Sent To:**
{{ $json.sentList }}

All applications have been logged in your Google Sheet with status "Email Sent".

Check your Gmail Sent folder for copies (you were CC'd on all emails).

**Date:** {{ $json.date }}

Best regards,
Email Outreach System""",
        "options": {}
    },
    [2880, 1800],
    typeVersion=2.1,
    credentials={"gmailOAuth2": {"id": "YOUR_GMAIL_CREDENTIAL_ID", "name": "Gmail OAuth2"}}
))


# ========== TELEGRAM ASSISTANT BRANCH (TRIGGER 3) ==========

# Extract message from Telegram
extract_message_code = """// Extract message and user info
const message = items[0].json.message || {};

const userId = message.from?.id?.toString() || 'unknown';
const username = message.from?.username || message.from?.first_name || 'User';
const chatId = message.chat?.id;
const text = message.text || '';

return [{
  json: {
    userId,
    username,
    chatId,
    text,
    timestamp: new Date().toISOString()
  }
}];"""

workflow["nodes"].append(create_node(
    "extract-telegram-message",
    "Extract Telegram Message",
    "n8n-nodes-base.code",
    {"jsCode": extract_message_code},
    [460, 3300],
    typeVersion=2
))

# Handle quick commands
quick_commands_code = """// Quick command handler
const text = items[0].json.text.toLowerCase();
const config = $('User Config (Master Profile)').item.json;

let quickResponse = '';
let isQuickCommand = false;

if (text === '/start' || text === '/help') {
  isQuickCommand = true;
  quickResponse = `**Job Hunt Assistant**

Welcome ${config.name}! 

**Commands:**
• /stats - View your application stats
• /resume - View your resume
• /help - Show this help message

Ask me anything about your job search!`;
} else if (text === '/resume') {
  isQuickCommand = true;
  quickResponse = `**Your Resume:**
${config.resumeUrl}

**Profile:**
• ${config.currentRole}
• ${config.experience}
• Skills: ${config.skills.join(', ')}
• Location: ${config.location}

**Links:**
LinkedIn: ${config.linkedinUrl}
GitHub: ${config.githubUrl}
Portfolio: ${config.portfolioUrl}`;
} else if (text === '/stats') {
  isQuickCommand = false; // Will need sheet query
  quickResponse = '';
}

return [{
  json: {
    ...items[0].json,
    quickResponse,
    isQuickCommand
  }
}];"""

workflow["nodes"].append(create_node(
    "handle-quick-commands",
    "Handle Quick Commands",
    "n8n-nodes-base.code",
    {"jsCode": quick_commands_code},
    [680, 3300],
    typeVersion=2
))

# Check if quick command
workflow["nodes"].append(create_node(
    "check-quick-command",
    "Is Quick Command?",
    "n8n-nodes-base.if",
    {
        "conditions": {
            "boolean": [{"value1": "={{ $json.isQuickCommand }}", "value2": True}]
        }
    },
    [900, 3300],
    typeVersion=1
))

# Send quick reply (TRUE branch)
workflow["nodes"].append(create_node(
    "send-quick-reply",
    "Send Quick Reply",
    "n8n-nodes-base.telegram",
    {
        "chatId": "={{ $('Extract Telegram Message').item.json.chatId }}",
        "text": "={{ $json.quickResponse }}",
        "additionalFields": {}
    },
    [1120, 3200],
    typeVersion=1.2,
    credentials={"telegramApi": {"id": "YOUR_TELEGRAM_CREDENTIAL_ID", "name": "Telegram Bot"}}
))

# Build dynamic system prompt (FALSE branch - complex queries)
build_prompt_code = """// Build dynamic system prompt for Groq
const config = $('User Config (Master Profile)').item.json;
const userMessage = $('Extract Telegram Message').item.json;

const systemPrompt = `You are ${config.name}'s personal job hunt assistant.

**User Profile:**
- Current Role: ${config.currentRole}
- Target Role: ${config.targetRole}
- Experience: ${config.experience}
- Skills: ${config.skills.join(', ')}
- Location: ${config.location}
- Work Preference: ${config.workMode.join(' or ')}
- Minimum Salary: $${config.minSalary}

**Your Capabilities:**
1. Query job tracker (see applications, stats, pending jobs)
2. Provide resume information
3. Answer job search questions
4. Give career advice

**Guidelines:**
- Be concise and action-oriented
- Suggest next steps
- Use bullet points for lists
- Keep responses under 300 words
- Be encouraging and supportive

User message: ${userMessage.text}`;

return [{
  json: {
    ...items[0].json,
    systemPrompt,
    userMessage: userMessage.text
  }
}];"""

workflow["nodes"].append(create_node(
    "build-system-prompt",
    "Build Dynamic System Prompt",
    "n8n-nodes-base.code",
    {"jsCode": build_prompt_code},
    [1120, 3400],
    typeVersion=2
))

# Groq Agent
workflow["nodes"].append(create_node(
    "groq-agent",
    "Groq Agent (Llama 3.3 70B)",
    "@n8n/n8n-nodes-langchain.lmChatGroq",
    {
        "operation": "text",
        "options": {"temperature": 0.7},
        "text": "={{ $json.systemPrompt }}"
    },
    [1340, 3400],
    typeVersion=1,
    credentials={"groqApi": {"id": "YOUR_GROQ_CREDENTIAL_ID", "name": "Groq API"}}
))

# Parse response and detect intents
parse_agent_response_code = """// Parse agent response and extract actions
const response = items[0].json.response || items[0].json.text || 'Sorry, I could not process your request.';
const userMessage = $('Extract Telegram Message').item.json.text.toLowerCase();

// Detect action intents
const needsSheetQuery = userMessage.includes('stats') || userMessage.includes('status') || userMessage.includes('how many') || userMessage.includes('count');

return [{
  json: {
    ...items[0].json,
    response,
    needsSheetQuery
  }
}];"""

workflow["nodes"].append(create_node(
    "parse-agent-response",
    "Parse Response & Detect Intents",
    "n8n-nodes-base.code",
    {"jsCode": parse_agent_response_code},
    [1560, 3400],
    typeVersion=2
))

# Check if needs sheet query
workflow["nodes"].append(create_node(
    "check-needs-sheet-query",
    "Needs Sheet Query?",
    "n8n-nodes-base.if",
    {
        "conditions": {
            "boolean": [{"value1": "={{ $json.needsSheetQuery }}", "value2": True}]
        }
    },
    [1780, 3400],
    typeVersion=1
))

# Query Google Sheet (TRUE branch)
workflow["nodes"].append(create_node(
    "query-sheet-for-stats",
    "Query Google Sheet for Stats",
    "n8n-nodes-base.googleSheets",
    {
        "operation": "read",
        "documentId": {"__rl": True, "value": "={{ $('User Config (Master Profile)').item.json.sheetId }}", "mode": "id"},
        "sheetName": {"__rl": True, "value": "Jobs", "mode": "name"},
        "options": {}
    },
    [2000, 3300],
    typeVersion=4.2,
    credentials={"googleSheetsOAuth2Api": {"id": "YOUR_GOOGLE_SHEETS_CREDENTIAL_ID", "name": "Google Sheets OAuth2"}}
))

# Aggregate stats
aggregate_stats_code = """// Aggregate sheet stats
const jobs = items.map(item => item.json);

const total = jobs.length;
const statusCounts = jobs.reduce((acc, j) => {
  const status = j.Status || j.status || 'Unknown';
  acc[status] = (acc[status] || 0) + 1;
  return acc;
}, {});

const priorityCounts = jobs.reduce((acc, j) => {
  const priority = j.Priority || j.priority || 'unknown';
  acc[priority] = (acc[priority] || 0) + 1;
  return acc;
}, {});

const stats = `**Your Job Tracker Stats:**
• Total jobs: ${total}

**Status Breakdown:**
` + Object.entries(statusCounts).map(([status, count]) => 
  `• ${status}: ${count}`
).join('\\n') + `

**Priority Breakdown:**
` + Object.entries(priorityCounts).map(([priority, count]) => 
  `• ${priority}: ${count}`
).join('\\n');

return [{
  json: {
    ...items[0].json,
    stats
  }
}];"""

workflow["nodes"].append(create_node(
    "aggregate-telegram-stats",
    "Aggregate Stats",
    "n8n-nodes-base.code",
    {"jsCode": aggregate_stats_code},
    [2220, 3300],
    typeVersion=2
))

# Send Telegram reply with stats (merge TRUE branch)
workflow["nodes"].append(create_node(
    "send-telegram-reply-with-stats",
    "Send Telegram Reply (with stats)",
    "n8n-nodes-base.telegram",
    {
        "chatId": "={{ $('Extract Telegram Message').item.json.chatId }}",
        "text": "={{ $json.response }}\\n\\n{{ $json.stats }}",
        "additionalFields": {}
    },
    [2440, 3300],
    typeVersion=1.2,
    credentials={"telegramApi": {"id": "YOUR_TELEGRAM_CREDENTIAL_ID", "name": "Telegram Bot"}}
))

# Send Telegram reply without stats (FALSE branch)
workflow["nodes"].append(create_node(
    "send-telegram-reply-simple",
    "Send Telegram Reply (simple)",
    "n8n-nodes-base.telegram",
    {
        "chatId": "={{ $('Extract Telegram Message').item.json.chatId }}",
        "text": "={{ $json.response }}",
        "additionalFields": {}
    },
    [2000, 3500],
    typeVersion=1.2,
    credentials={"telegramApi": {"id": "YOUR_TELEGRAM_CREDENTIAL_ID", "name": "Telegram Bot"}}
))


# ========== BUILD CONNECTIONS ==========

# BRANCH 1: Job Discovery (Trigger 1 → User Config → APIs → Score → Sheet → Notifications)
workflow["connections"]["Schedule Trigger: Job Discovery (8 AM)"] = {
    "main": [[{"node": "User Config (Master Profile)", "type": "main", "index": 0}]]
}

workflow["connections"]["User Config (Master Profile)"] = {
    "main": [[
        {"node": "Fetch Remotive API", "type": "main", "index": 0},
        {"node": "Fetch Arbeitnow API", "type": "main", "index": 0},
        {"node": "Fetch Adzuna API", "type": "main", "index": 0}
    ]]
}

workflow["connections"]["Fetch Remotive API"] = {
    "main": [[{"node": "Parse Remotive Response", "type": "main", "index": 0}]]
}

workflow["connections"]["Fetch Arbeitnow API"] = {
    "main": [[{"node": "Parse Arbeitnow Response", "type": "main", "index": 0}]]
}

workflow["connections"]["Fetch Adzuna API"] = {
    "main": [[{"node": "Parse Adzuna Response", "type": "main", "index": 0}]]
}

workflow["connections"]["Parse Remotive Response"] = {
    "main": [[{"node": "Merge All API Results", "type": "main", "index": 0}]]
}

workflow["connections"]["Parse Arbeitnow Response"] = {
    "main": [[{"node": "Merge All API Results", "type": "main", "index": 1}]]
}

workflow["connections"]["Parse Adzuna Response"] = {
    "main": [[{"node": "Merge All API Results", "type": "main", "index": 2}]]
}

workflow["connections"]["Merge All API Results"] = {
    "main": [[{"node": "Deduplicate Jobs", "type": "main", "index": 0}]]
}

workflow["connections"]["Deduplicate Jobs"] = {
    "main": [[{"node": "Read Existing Jobs from Sheet", "type": "main", "index": 0}]]
}

workflow["connections"]["Read Existing Jobs from Sheet"] = {
    "main": [[{"node": "Filter Out Already-Fetched Jobs", "type": "main", "index": 0}]]
}

workflow["connections"]["Filter Out Already-Fetched Jobs"] = {
    "main": [[{"node": "Groq AI: Score Job Match", "type": "main", "index": 0}]]
}

workflow["connections"]["Groq AI: Score Job Match"] = {
    "main": [[{"node": "Parse AI Score", "type": "main", "index": 0}]]
}

workflow["connections"]["Parse AI Score"] = {
    "main": [[{"node": "Filter by Score Threshold (≥30)", "type": "main", "index": 0}]]
}

workflow["connections"]["Filter by Score Threshold (≥30)"] = {
    "main": [[{"node": "Append to Google Sheets: Jobs Tab", "type": "main", "index": 0}], []]
}

workflow["connections"]["Append to Google Sheets: Jobs Tab"] = {
    "main": [[{"node": "Aggregate Job Discovery Summary", "type": "main", "index": 0}]]
}

workflow["connections"]["Aggregate Job Discovery Summary"] = {
    "main": [[
        {"node": "Send Telegram: Job Discovery Digest", "type": "main", "index": 0},
        {"node": "Send Gmail: Job Discovery Digest", "type": "main", "index": 0}
    ]]
}

# BRANCH 2: Email Outreach (Trigger 2 → Read Sheet → Filter → Generate → Send → Update)
workflow["connections"]["Schedule Trigger: Email Outreach (9 AM)"] = {
    "main": [[{"node": "Read Jobs from Sheet for Outreach", "type": "main", "index": 0}]]
}

workflow["connections"]["Read Jobs from Sheet for Outreach"] = {
    "main": [[{"node": "Filter: Status=New AND Has Recruiter Email", "type": "main", "index": 0}]]
}

workflow["connections"]["Filter: Status=New AND Has Recruiter Email"] = {
    "main": [[{"node": "Limit to Daily Max (10 emails)", "type": "main", "index": 0}], []]
}

workflow["connections"]["Limit to Daily Max (10 emails)"] = {
    "main": [[{"node": "Groq AI: Generate Personalized Email", "type": "main", "index": 0}]]
}

workflow["connections"]["Groq AI: Generate Personalized Email"] = {
    "main": [[{"node": "Parse & Format Email", "type": "main", "index": 0}]]
}

workflow["connections"]["Parse & Format Email"] = {
    "main": [[{"node": "Send Email via Gmail", "type": "main", "index": 0}]]
}

workflow["connections"]["Send Email via Gmail"] = {
    "main": [[{"node": "Update Metadata (Status & Application ID)", "type": "main", "index": 0}]]
}

workflow["connections"]["Update Metadata (Status & Application ID)"] = {
    "main": [[{"node": "Update Sheet: Mark Email Sent", "type": "main", "index": 0}]]
}

workflow["connections"]["Update Sheet: Mark Email Sent"] = {
    "main": [[{"node": "Rate Limit Delay (3 seconds)", "type": "main", "index": 0}]]
}

workflow["connections"]["Rate Limit Delay (3 seconds)"] = {
    "main": [[{"node": "Aggregate Outreach Summary", "type": "main", "index": 0}]]
}

workflow["connections"]["Aggregate Outreach Summary"] = {
    "main": [[{"node": "Send Gmail: Outreach Digest", "type": "main", "index": 0}]]
}

# BRANCH 3: Telegram Assistant (Trigger 3 → Extract → Quick Commands OR Groq → Sheet Query? → Reply)
workflow["connections"]["Telegram Trigger: Interactive Assistant"] = {
    "main": [[{"node": "Extract Telegram Message", "type": "main", "index": 0}]]
}

workflow["connections"]["Extract Telegram Message"] = {
    "main": [[{"node": "Handle Quick Commands", "type": "main", "index": 0}]]
}

workflow["connections"]["Handle Quick Commands"] = {
    "main": [[{"node": "Is Quick Command?", "type": "main", "index": 0}]]
}

# TRUE branch: Quick command
workflow["connections"]["Is Quick Command?"] = {
    "main": [
        [{"node": "Send Quick Reply", "type": "main", "index": 0}],
        [{"node": "Build Dynamic System Prompt", "type": "main", "index": 0}]
    ]
}

workflow["connections"]["Build Dynamic System Prompt"] = {
    "main": [[{"node": "Groq Agent (Llama 3.3 70B)", "type": "main", "index": 0}]]
}

workflow["connections"]["Groq Agent (Llama 3.3 70B)"] = {
    "main": [[{"node": "Parse Response & Detect Intents", "type": "main", "index": 0}]]
}

workflow["connections"]["Parse Response & Detect Intents"] = {
    "main": [[{"node": "Needs Sheet Query?", "type": "main", "index": 0}]]
}

# TRUE branch: Needs sheet query
workflow["connections"]["Needs Sheet Query?"] = {
    "main": [
        [{"node": "Query Google Sheet for Stats", "type": "main", "index": 0}],
        [{"node": "Send Telegram Reply (simple)", "type": "main", "index": 0}]
    ]
}

workflow["connections"]["Query Google Sheet for Stats"] = {
    "main": [[{"node": "Aggregate Stats", "type": "main", "index": 0}]]
}

workflow["connections"]["Aggregate Stats"] = {
    "main": [[{"node": "Send Telegram Reply (with stats)", "type": "main", "index": 0}]]
}

# Write the final JSON
with open('/projects/sandbox/Ravi-s_automation/MASTER-job-automation-workflow.json', 'w') as f:
    json.dump(workflow, f, indent=2)

print("✅ MASTER workflow generated successfully!")
print(f"Total nodes: {len(workflow['nodes'])}")
print(f"Total connections: {len(workflow['connections'])}")

