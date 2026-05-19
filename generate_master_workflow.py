#!/usr/bin/env python3
"""
Complete MASTER Job Automation Workflow Generator
Merges all 4 workflows into one unified production-grade system
"""

import json

def generate_complete_workflow():
    """Generate the complete unified workflow with all nodes and connections"""
    
    workflow = {
        "name": "MASTER Job Automation - Unified AI System",
        "nodes": [],
        "connections": {},
        "settings": {"executionOrder": "v1"},
        "staticData": None,
        "tags": ["production", "job-automation", "ai-powered"],
        "triggerCount": 0,
        "updatedAt": "2024-01-01T00:00:00.000Z",
        "versionId": "1"
    }
    
    nodes = workflow["nodes"]
    connections = workflow["connections"]
    
    # ========================================================
    # SECTION 1: TRIGGER SYSTEM (Multi-Trigger Architecture)
    # ========================================================
    
    # Trigger 1: Schedule (Daily 8 AM for job discovery)
    nodes.append({
        "parameters": {
            "rule": {
                "interval": [{
                    "field": "cronExpression",
                    "expression": "0 8 * * *"
                }]
            }
        },
        "id": "schedule-trigger-discovery",
        "name": "Schedule: Daily Job Discovery (8 AM)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.1,
        "position": [240, 300]
    })
    
    # Trigger 2: Schedule (Daily 9 AM for email outreach)
    nodes.append({
        "parameters": {
            "rule": {
                "interval": [{
                    "field": "cronExpression",
                    "expression": "0 9 * * *"
                }]
            }
        },
        "id": "schedule-trigger-outreach",
        "name": "Schedule: Daily Email Outreach (9 AM)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.1,
        "position": [240, 600]
    })
    
    # Trigger 3: Telegram Bot
    nodes.append({
        "parameters": {
            "updates": ["message"]
        },
        "id": "telegram-trigger",
        "name": "Telegram Bot Trigger",
        "type": "n8n-nodes-base.telegramTrigger",
        "typeVersion": 1,
        "position": [240, 900],
        "webhookId": "telegram-job-bot",
        "credentials": {
            "telegramApi": {
                "id": "YOUR_TELEGRAM_CREDENTIAL_ID",
                "name": "telegram-bot"
            }
        }
    })
    
    # Trigger 4: Manual Webhook
    nodes.append({
        "parameters": {
            "httpMethod": "POST",
            "path": "job-search-manual",
            "responseMode": "responseNode",
            "options": {}
        },
        "id": "webhook-trigger",
        "name": "Webhook: Manual Job Search",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 1.1,
        "position": [240, 1200],
        "webhookId": "job-search-manual"
    })
    
    # ========================================================
    # SECTION 2: USER CONFIGURATION (Embedded Config)
    # ========================================================
    
    nodes.append({
        "parameters": {
            "jsCode": """// ===== USER CONFIGURATION =====
// Customize this for your profile
return [{
  json: {
    // Personal Info
    userId: 'user-001',
    name: 'Your Name',
    email: 'YOUR_EMAIL@example.com',
    
    // Career Profile
    currentRole: 'Senior Backend Engineer',
    targetRole: 'Staff Engineer / Lead Backend / Principal Engineer',
    experience: '5 years',
    skills: [
      'Python', 'Node.js', 'TypeScript', 'Go',
      'AWS', 'Docker', 'Kubernetes', 'Terraform',
      'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
      'GraphQL', 'REST APIs', 'Microservices', 'System Design'
    ],
    
    // Job Preferences
    location: 'Hyderabad, India',
    workMode: ['remote', 'hybrid'],  // 'remote', 'hybrid', 'onsite'
    minSalary: 80000,
    country: 'in',  // for Adzuna API: 'us', 'gb', 'in', 'au', 'ca', 'de'
    
    // External Links
    sheetId: 'YOUR_SPREADSHEET_ID',
    resumeUrl: 'https://drive.google.com/file/d/YOUR_RESUME_ID/view',
    githubUrl: 'https://github.com/yourusername',
    linkedinUrl: 'https://linkedin.com/in/yourprofile',
    portfolioUrl: 'https://yourportfolio.com',
    
    // System Limits
    dailyEmailLimit: 10,
    groqRateLimit: 25,  // per minute (30/min limit, stay safe)
    minJobScore: 30  // filter jobs below this score
  }
}];"""
        },
        "id": "user-config",
        "name": "User Config",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [460, 300]
    })
    
    # ========================================================
    # SECTION 3: JOB DISCOVERY FLOW
    # ========================================================
    
    # Build Search Query
    nodes.append({
        "parameters": {
            "jsCode": """// Build dynamic search query from user config
const config = $('User Config').item.json;

// Create keyword string from top skills
const keywords = config.skills.slice(0, 3).join(' OR ') + ' developer';

return [{
  json: {
    config,
    searchConfig: {
      keywords,
      location: config.location,
      country: config.country,
      skills: config.skills,
      minSalary: config.minSalary,
      workMode: config.workMode
    },
    timestamp: new Date().toISOString()
  }
}];"""
        },
        "id": "build-search-query",
        "name": "Build Search Query",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [680, 300]
    })
    
    # Parallel API Calls - Remotive
    nodes.append({
        "parameters": {
            "url": "https://remotive.com/api/remote-jobs",
            "method": "GET",
            "sendQuery": True,
            "queryParameters": {
                "parameters": [
                    {"name": "search", "value": "={{ $json.searchConfig.keywords }}"},
                    {"name": "limit", "value": "50"}
                ]
            },
            "options": {"timeout": 30000}
        },
        "id": "fetch-remotive",
        "name": "API: Remotive (Free, Unlimited)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.1,
        "position": [900, 200],
        "continueOnFail": True
    })
    
    # Parallel API Calls - Arbeitnow
    nodes.append({
        "parameters": {
            "url": "https://www.arbeitnow.com/api/job-board-api",
            "method": "GET",
            "sendQuery": True,
            "queryParameters": {
                "parameters": [
                    {"name": "search", "value": "={{ $json.searchConfig.keywords }}"},
                    {"name": "limit", "value": "50"}
                ]
            },
            "options": {"timeout": 30000}
        },
        "id": "fetch-arbeitnow",
        "name": "API: Arbeitnow (Free, Unlimited)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.1,
        "position": [900, 300],
        "continueOnFail": True
    })
    
    # Parallel API Calls - Adzuna
    nodes.append({
        "parameters": {
            "url": "=https://api.adzuna.com/v1/api/jobs/{{ $json.searchConfig.country }}/search/1",
            "method": "GET",
            "sendQuery": True,
            "queryParameters": {
                "parameters": [
                    {"name": "app_id", "value": "YOUR_ADZUNA_APP_ID"},
                    {"name": "app_key", "value": "YOUR_ADZUNA_APP_KEY"},
                    {"name": "what", "value": "={{ $json.searchConfig.keywords }}"},
                    {"name": "results_per_page", "value": "50"}
                ]
            },
            "options": {"timeout": 30000}
        },
        "id": "fetch-adzuna",
        "name": "API: Adzuna (Free, 250/day)",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.1,
        "position": [900, 400],
        "continueOnFail": True
    })
    
    # Parse Remotive
    nodes.append({
        "parameters": {
            "jsCode": """// Parse Remotive API response
const response = items[0].json;
const jobs = response.jobs || [];

if (jobs.length === 0) {
  return [];
}

return jobs.map(job => ({
  json: {
    source: 'Remotive',
    jobId: `remotive-${job.id || Date.now()}`,
    jobTitle: job.title || 'Unknown',
    company: job.company_name || 'Unknown',
    location: job.candidate_required_location || 'Remote',
    jobType: job.job_type || 'Full-time',
    workMode: 'Remote',
    salary: job.salary || 'Not disclosed',
    applyUrl: job.url || '',
    description: (job.description || '').substring(0, 500),
    tags: job.tags || [],
    category: job.category || '',
    postedDate: job.publication_date || new Date().toISOString().split('T')[0],
    fetchedDate: new Date().toISOString().split('T')[0]
  }
}));"""
        },
        "id": "parse-remotive",
        "name": "Parse Remotive",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1120, 200],
        "continueOnFail": True
    })
    
    # Parse Arbeitnow
    nodes.append({
        "parameters": {
            "jsCode": """// Parse Arbeitnow API response
const response = items[0].json;
const jobs = response.data || [];

if (jobs.length === 0) {
  return [];
}

return jobs.map(job => ({
  json: {
    source: 'Arbeitnow',
    jobId: `arbeitnow-${job.slug || Date.now()}`,
    jobTitle: job.title || 'Unknown',
    company: job.company_name || 'Unknown',
    location: job.location || 'Remote',
    jobType: job.job_types?.[0] || 'Full-time',
    workMode: job.remote ? 'Remote' : 'Onsite',
    salary: 'Not disclosed',
    applyUrl: job.url || '',
    description: (job.description || '').substring(0, 500),
    tags: job.tags || [],
    category: '',
    postedDate: job.created_at ? new Date(job.created_at * 1000).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
    fetchedDate: new Date().toISOString().split('T')[0]
  }
}));"""
        },
        "id": "parse-arbeitnow",
        "name": "Parse Arbeitnow",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1120, 300],
        "continueOnFail": True
    })
    
    # Parse Adzuna
    nodes.append({
        "parameters": {
            "jsCode": """// Parse Adzuna API response
const response = items[0].json;
const jobs = response.results || [];

if (jobs.length === 0) {
  return [];
}

return jobs.map(job => ({
  json: {
    source: 'Adzuna',
    jobId: `adzuna-${job.id || Date.now()}`,
    jobTitle: job.title || 'Unknown',
    company: job.company?.display_name || 'Unknown',
    location: job.location?.display_name || 'Not specified',
    jobType: job.contract_time || 'Full-time',
    workMode: 'Not specified',
    salary: job.salary_max ? `${job.salary_min || 0} - ${job.salary_max}` : 'Not disclosed',
    applyUrl: job.redirect_url || '',
    description: (job.description || '').substring(0, 500),
    tags: job.category?.tag ? [job.category.tag] : [],
    category: job.category?.label || '',
    postedDate: job.created || new Date().toISOString().split('T')[0],
    fetchedDate: new Date().toISOString().split('T')[0]
  }
}));"""
        },
        "id": "parse-adzuna",
        "name": "Parse Adzuna",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1120, 400],
        "continueOnFail": True
    })
    
    # Merge all jobs
    nodes.append({
        "parameters": {
            "mode": "combine",
            "mergeByFields": {
                "fields": [{"fieldName": "jobId"}]
            },
            "options": {}
        },
        "id": "merge-all-jobs",
        "name": "Merge All Jobs",
        "type": "n8n-nodes-base.merge",
        "typeVersion": 2.1,
        "position": [1340, 300]
    })
    
    # Load existing jobs from Sheet (for deduplication)
    nodes.append({
        "parameters": {
            "operation": "read",
            "documentId": {
                "__rl": True,
                "value": "={{ $('User Config').item.json.sheetId }}",
                "mode": "id"
            },
            "sheetName": {
                "__rl": True,
                "value": "Jobs",
                "mode": "name"
            },
            "options": {}
        },
        "id": "load-existing-jobs",
        "name": "Load Existing Jobs from Sheet",
        "type": "n8n-nodes-base.googleSheets",
        "typeVersion": 4.2,
        "position": [1340, 500],
        "credentials": {
            "googleSheetsOAuth2Api": {
                "id": "YOUR_GOOGLE_SHEETS_CREDENTIAL_ID",
                "name": "google-sheets-oauth"
            }
        },
        "continueOnFail": True
    })
    
    # Deduplicate jobs
    nodes.append({
        "parameters": {
            "jsCode": """// Deduplicate: check against existing jobs in Sheet
const newJobs = $('Merge All Jobs').all().map(item => item.json);
const existingJobs = $('Load Existing Jobs from Sheet').all().map(item => item.json);

// Build set of existing job keys
const existingKeys = new Set(
  existingJobs.map(j => `${(j.Company || j.company || '').toLowerCase()}-${(j['Job Title'] || j.jobTitle || '').toLowerCase()}`.replace(/\\s+/g, '-'))
);

// Filter out duplicates and invalid jobs
const unique = [];
const seen = new Set();

for (const job of newJobs) {
  const key = `${job.company.toLowerCase()}-${job.jobTitle.toLowerCase()}`.replace(/\\s+/g, '-');
  
  // Skip if: no URL, already in Sheet, or already seen in this batch
  if (!job.applyUrl || existingKeys.has(key) || seen.has(key)) {
    continue;
  }
  
  seen.add(key);
  unique.push(job);
}

if (unique.length === 0) {
  console.log('No new unique jobs found');
  return [];
}

console.log(`Found ${unique.length} new unique jobs (${newJobs.length} total, ${existingJobs.length} existing)`);
return unique.map(job => ({ json: job }));"""
        },
        "id": "deduplicate-jobs",
        "name": "Deduplicate & Filter",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1560, 300]
    })
    
    return workflow

# Write Part 1 (first 20 nodes)
workflow = generate_complete_workflow()
print(f"Generated {len(workflow['nodes'])} nodes so far...")
print("This is a multi-part generation. Continuing...")
