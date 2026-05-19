#!/usr/bin/env python3
"""
Build ENHANCED-MASTER-workflow.json with resume intelligence features.
Adds 11 new nodes for resume download, parsing, validation, and enhanced scoring/email generation.
"""

import json
import copy

def main():
    # Load existing workflow
    with open('MASTER-job-automation-workflow.json', 'r') as f:
        workflow = json.load(f)
    
    print(f"Loaded existing workflow with {len(workflow['nodes'])} nodes")
    
    # Step 1: Update User Config node to include resumeUrl and resumeParsingEnabled
    user_config_node = [n for n in workflow['nodes'] if n['id'] == 'user-config'][0]
    
    # Update the jsCode to include new fields
    user_config_node['parameters']['jsCode'] = """// User profile configuration - single source of truth
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
    resumeParsingEnabled: true,
    userEmail: 'YOUR_EMAIL@example.com',
    dailyLimit: 10,
    scoreThreshold: 30,
    sheetId: 'YOUR_SPREADSHEET_ID'
  }
}];"""
    
    print("✓ Step 1: Updated User Config node with resumeUrl and resumeParsingEnabled")
    
    # Step 2: Add new nodes for resume intelligence
    new_nodes = []
    
    # Node 1: Download Resume (HTTP Request)
    download_resume = {
        "id": "download-resume",
        "name": "Download Resume",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.1,
        "position": [680, 150],
        "parameters": {
            "url": "={{ \n  const config = $('User Config (Master Profile)').item.json;\n  const url = config.resumeUrl || '';\n  \n  // Convert Google Drive view URL to download URL\n  if (url.includes('drive.google.com/file/d/')) {\n    const match = url.match(/\\/d\\/([^\\/]+)/);\n    if (match) return `https://drive.google.com/uc?export=download&id=${match[1]}`;\n  }\n  \n  // Convert GitHub blob URL to raw URL\n  if (url.includes('github.com') && url.includes('/blob/')) {\n    return url.replace('/blob/', '/raw/');\n  }\n  \n  // Add Dropbox download parameter\n  if (url.includes('dropbox.com')) {\n    return url.includes('?') ? url + '&dl=1' : url + '?dl=1';\n  }\n  \n  return url;\n}}",
            "method": "GET",
            "options": {
                "timeout": 30000,
                "response": {
                    "response": {
                        "fullResponse": False,
                        "responseFormat": "text"
                    }
                }
            }
        },
        "continueOnFail": True
    }
    new_nodes.append(download_resume)
    
    # Node 2: Check Resume Download Success (IF)
    check_download = {
        "id": "check-resume-download",
        "name": "Check Resume Download Success",
        "type": "n8n-nodes-base.if",
        "typeVersion": 1,
        "position": [900, 150],
        "parameters": {
            "conditions": {
                "boolean": [
                    {
                        "value1": "={{ $('User Config (Master Profile)').item.json.resumeParsingEnabled && $json.data && $json.data.length > 100 }}",
                        "operation": "equal",
                        "value2": True
                    }
                ]
            }
        }
    }
    new_nodes.append(check_download)
    
    # Node 3: Parse Resume with Groq AI (LangChain)
    parse_resume = {
        "id": "parse-resume-groq",
        "name": "Parse Resume with Groq AI",
        "type": "@n8n/n8n-nodes-langchain.lmChatGroq",
        "typeVersion": 1,
        "position": [1120, 100],
        "parameters": {
            "model": "llama-3.3-70b-versatile",
            "options": {
                "temperature": 0.1
            },
            "text": "=You are a resume parser. Extract structured information from this resume text.\n\n**Resume Content:**\n{{ $('Download Resume').item.json.data }}\n\n**Extract the following in JSON format ONLY:**\n{\n  \"skills\": [\"skill1\", \"skill2\", ...],\n  \"experience\": [\n    {\n      \"role\": \"Job Title\",\n      \"company\": \"Company Name\",\n      \"duration\": \"2020-2023\",\n      \"responsibilities\": \"Key achievements and responsibilities\"\n    }\n  ],\n  \"projects\": [\n    {\n      \"name\": \"Project Name\",\n      \"description\": \"Brief description\",\n      \"technologies\": [\"tech1\", \"tech2\"]\n    }\n  ],\n  \"achievements\": [\"achievement1\", \"achievement2\", ...],\n  \"education\": [\n    {\n      \"degree\": \"Degree Name\",\n      \"institution\": \"University Name\",\n      \"year\": \"2019\"\n    }\n  ]\n}\n\nProvide ONLY valid JSON. No additional text or explanation."
        },
        "credentials": {
            "groqApi": {
                "id": "YOUR_GROQ_CREDENTIAL_ID",
                "name": "Groq API"
            }
        }
    }
    new_nodes.append(parse_resume)
    
    # Node 4: Structure Resume Data (Code)
    structure_resume = {
        "id": "structure-resume-data",
        "name": "Structure Resume Data",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1340, 100],
        "parameters": {
            "jsCode": """// Parse and validate Groq resume response
const config = $('User Config (Master Profile)').item.json;
const groqResponse = $node["Parse Resume with Groq AI"].json.response || $node["Parse Resume with Groq AI"].json.text || '';

let resumeData = {
  skills: config.skills || [],
  experience: [],
  projects: [],
  achievements: [],
  education: [],
  parsed: false
};

try {
  // Extract JSON from response
  const jsonMatch = groqResponse.match(/\\{[\\s\\S]*\\}/);
  if (jsonMatch) {
    const parsed = JSON.parse(jsonMatch[0]);
    
    // Validate and use parsed data
    if (parsed.skills && Array.isArray(parsed.skills) && parsed.skills.length > 0) {
      resumeData.skills = parsed.skills;
      resumeData.parsed = true;
    }
    
    if (parsed.experience && Array.isArray(parsed.experience)) {
      resumeData.experience = parsed.experience;
    }
    
    if (parsed.projects && Array.isArray(parsed.projects)) {
      resumeData.projects = parsed.projects;
    }
    
    if (parsed.achievements && Array.isArray(parsed.achievements)) {
      resumeData.achievements = parsed.achievements;
    }
    
    if (parsed.education && Array.isArray(parsed.education)) {
      resumeData.education = parsed.education;
    }
  }
} catch (error) {
  console.error('Resume parsing failed, using User Config fallback:', error.message);
}

return [{
  json: {
    resumeData,
    config
  }
}];"""
        }
    }
    new_nodes.append(structure_resume)
    
    # Node 5: Fallback to User Config Only (Code)
    fallback_config = {
        "id": "fallback-user-config",
        "name": "Fallback: User Config Only",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1120, 200],
        "parameters": {
            "jsCode": """// Use User Config when resume download/parsing fails
const config = $('User Config (Master Profile)').item.json;

return [{
  json: {
    resumeData: {
      skills: config.skills || [],
      experience: [],
      projects: [],
      achievements: [],
      education: [],
      parsed: false
    },
    config
  }
}];"""
        }
    }
    new_nodes.append(fallback_config)
    
    # Node 6: Merge User Config with Resume Data (Code)
    merge_data = {
        "id": "merge-config-resume",
        "name": "Merge User Config with Resume Data",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [1560, 150],
        "parameters": {
            "jsCode": """// Merge resume data with user config, prioritize resume data
const input = items[0].json;
const resumeData = input.resumeData;
const config = input.config;

// Create enriched profile
const enrichedProfile = {
  ...config,
  resumeData: resumeData,
  
  // Skills: resume data takes priority if available
  skills: resumeData.parsed ? resumeData.skills : config.skills,
  
  // Enhanced fields from resume
  experience: resumeData.experience || [],
  projects: resumeData.projects || [],
  achievements: resumeData.achievements || [],
  education: resumeData.education || [],
  
  // Resume parsing metadata
  resumeParsed: resumeData.parsed,
  resumeSkillCount: (resumeData.skills || []).length,
  resumeProjectCount: (resumeData.projects || []).length
};

return [{
  json: enrichedProfile
}];"""
        }
    }
    new_nodes.append(merge_data)
    
    # Node 7: Resume Match Analysis (Code) - positioned in scoring branch
    resume_match_analysis = {
        "id": "resume-match-analysis",
        "name": "Resume Match Analysis",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [2220, 480],
        "parameters": {
            "jsCode": """// Analyze resume match with job requirements
const jobData = items[0].json;
const enrichedProfile = $('Merge User Config with Resume Data').item.json;
const resumeData = enrichedProfile.resumeData;

// Extract job requirements (basic keyword extraction from description)
const jobDesc = (jobData.description || '').toLowerCase();
const jobTitle = (jobData.jobTitle || '').toLowerCase();

// Calculate skill overlap
const resumeSkills = (resumeData.skills || []).map(s => s.toLowerCase());
const matchedSkills = resumeSkills.filter(skill => 
  jobDesc.includes(skill) || jobTitle.includes(skill)
);

const skillOverlapPercent = resumeSkills.length > 0 
  ? Math.round((matchedSkills.length / resumeSkills.length) * 100)
  : 0;

// Calculate experience relevance
const experienceYears = parseInt(enrichedProfile.experience.match(/\\d+/)?.[0] || '0');
const hasRelevantProjects = (resumeData.projects || []).some(project => {
  const projectTech = (project.technologies || []).join(' ').toLowerCase();
  return matchedSkills.some(skill => projectTech.includes(skill));
});

const experienceScore = Math.min(experienceYears * 10, 50);
const projectScore = hasRelevantProjects ? 20 : 0;

// Overall relevance score
const relevanceScore = Math.min(skillOverlapPercent + experienceScore + projectScore, 100);

// Generate match details
const matchDetails = {
  skillOverlapPercent,
  matchedSkills: matchedSkills.slice(0, 5), // Top 5
  totalResumeSkills: resumeSkills.length,
  experienceYears,
  hasRelevantProjects,
  relevanceScore,
  resumeParsed: resumeData.parsed
};

return [{
  json: {
    ...jobData,
    resumeMatchDetails: JSON.stringify(matchDetails)
  }
}];"""
        }
    }
    new_nodes.append(resume_match_analysis)
    
    # Add all new nodes to workflow
    workflow['nodes'].extend(new_nodes)
    print(f"✓ Step 2: Added {len(new_nodes)} new resume intelligence nodes")
    
    # Step 3: Update Groq Score Job prompt to include resume data
    groq_score_node = [n for n in workflow['nodes'] if n['id'] == 'groq-score-job'][0]
    groq_score_node['parameters']['text'] = """=You are a job matching expert. Score this job for relevance (0-100):

**Job:** {{ $json.jobTitle }} at {{ $json.company }}
**Location:** {{ $json.location }}
**Work Mode:** {{ $json.workMode }}
**Description:** {{ $json.description }}

**User Profile:**
- Current Role: {{ $('Merge User Config with Resume Data').item.json.currentRole }}
- Target Role: {{ $('Merge User Config with Resume Data').item.json.targetRole }}
- Skills: {{ $('Merge User Config with Resume Data').item.json.skills.join(', ') }}
- Work Mode: {{ $('Merge User Config with Resume Data').item.json.workMode.join(' or ') }}
- Location: {{ $('Merge User Config with Resume Data').item.json.location }}

**Resume Data:**
- Resume Parsed: {{ $('Merge User Config with Resume Data').item.json.resumeParsed ? 'Yes' : 'No (using config)' }}
- Resume Skills: {{ ($('Merge User Config with Resume Data').item.json.resumeData.skills || []).join(', ') }}
- Experience: {{ ($('Merge User Config with Resume Data').item.json.resumeData.experience || []).map(e => e.role + ' at ' + e.company).join('; ') }}
- Key Projects: {{ ($('Merge User Config with Resume Data').item.json.resumeData.projects || []).slice(0, 3).map(p => p.name).join(', ') }}

**Scoring Instructions:**
- Give +20 points for strong skill overlap with resume
- Give +15 points for relevant project experience
- Give +10 points for matching work mode and location
- Give +10 points for career progression alignment

Provide ONLY a JSON object:
{"score": <0-100>, "priority": "high|medium|low", "matchReason": "<1 sentence mentioning resume skills if parsed>"}

No other text."""
    print("✓ Step 3: Enhanced Groq Score Job prompt with resume data")
    
    # Step 4: Update Groq Generate Email prompt to reference resume projects
    groq_email_node = [n for n in workflow['nodes'] if n['id'] == 'groq-generate-email'][0]
    groq_email_node['parameters']['text'] = """=You are a professional email writer. Generate a personalized cold email to a recruiter.

**Job Details:**
- Title: {{ $json['Job Title'] || $json.jobTitle }}
- Company: {{ $json.Company || $json.company }}
- Recruiter: {{ $json['Recruiter Name'] || $json.recruiterName || 'Hiring Manager' }}
- Location: {{ $json.Location || $json.location }}
- Apply URL: {{ $json['Apply URL'] || $json.applyUrl }}

**Candidate Profile:**
- Name: {{ $('Merge User Config with Resume Data').item.json.name }}
- Current Role: {{ $('Merge User Config with Resume Data').item.json.currentRole }}
- Experience: {{ $('Merge User Config with Resume Data').item.json.experience }}
- Skills: {{ $('Merge User Config with Resume Data').item.json.skills.join(', ') }}
- Location: {{ $('Merge User Config with Resume Data').item.json.location }}

**Resume Insights (Use to personalize email):**
- Resume Parsed: {{ $('Merge User Config with Resume Data').item.json.resumeParsed }}
- Key Projects: {{ ($('Merge User Config with Resume Data').item.json.resumeData.projects || []).slice(0, 3).map(p => p.name + ' (' + (p.technologies || []).join(', ') + ')').join('; ') }}
- Recent Experience: {{ ($('Merge User Config with Resume Data').item.json.resumeData.experience || []).slice(0, 2).map(e => e.role + ' at ' + e.company).join('; ') }}
- Achievements: {{ ($('Merge User Config with Resume Data').item.json.resumeData.achievements || []).slice(0, 2).join('; ') }}

**Requirements:**
1. Professional, concise (150-200 words)
2. Show genuine interest in the company/role
3. Mention 2-3 specific projects from resume that align with job requirements
4. Reference relevant achievements from resume
5. Highlight matching technical skills
6. Include a clear call-to-action
7. End with "Best regards, {{ $('Merge User Config with Resume Data').item.json.name }}"

**Format:**
Subject: [Generate compelling subject line]

[Email body with specific resume project references]

Provide ONLY the subject line and email body. No additional commentary."""
    print("✓ Step 4: Enhanced Groq Generate Email prompt with resume projects")
    
    # Step 5: Update Parse & Format Email node to use merged config
    parse_email_node = [n for n in workflow['nodes'] if n['id'] == 'parse-format-email'][0]
    parse_email_node['parameters']['jsCode'] = """// Parse Groq email response
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

const config = $('Merge User Config with Resume Data').item.json;

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
    print("✓ Step 5: Updated Parse & Format Email node to use merged config")
    
    # Step 6: Update Google Sheets append node to include Resume Match Details column
    append_sheet_node = [n for n in workflow['nodes'] if n['id'] == 'append-to-sheet-jobs'][0]
    
    # Add Resume Match Details to columns
    append_sheet_node['parameters']['columns']['mappingMode'] = 'defineBelow'
    append_sheet_node['parameters']['columns']['value'] = {
        'jobId': '={{ $json.jobId }}',
        'jobTitle': '={{ $json.jobTitle }}',
        'company': '={{ $json.company }}',
        'location': '={{ $json.location }}',
        'workMode': '={{ $json.workMode }}',
        'salary': '={{ $json.salary }}',
        'applyUrl': '={{ $json.applyUrl }}',
        'source': '={{ $json.source }}',
        'score': '={{ $json.score }}',
        'priority': '={{ $json.priority }}',
        'matchReason': '={{ $json.matchReason }}',
        'status': '={{ $json.status }}',
        'postedDate': '={{ $json.postedDate }}',
        'fetchedDate': '={{ $json.fetchedDate }}',
        'recruiterEmail': '={{ $json.recruiterEmail }}',
        'recruiterName': '={{ $json.recruiterName }}',
        'applicationId': '={{ $json.applicationId }}',
        'emailSentDate': '={{ $json.emailSentDate }}',
        'lastUpdated': '={{ $json.lastUpdated }}',
        'resumeMatchDetails': '={{ $json.resumeMatchDetails || "" }}'
    }
    print("✓ Step 6: Updated Google Sheets node to include Resume Match Details column")
    
    # Step 7: Update connections
    # Connection 1: User Config -> Download Resume
    if 'User Config (Master Profile)' not in workflow['connections']:
        workflow['connections']['User Config (Master Profile)'] = {'main': [[]]}
    
    # Add Download Resume to User Config connections
    workflow['connections']['User Config (Master Profile)']['main'][0].append({
        'node': 'Download Resume',
        'type': 'main',
        'index': 0
    })
    
    # Connection 2: Download Resume -> Check Resume Download Success
    workflow['connections']['Download Resume'] = {
        'main': [[{
            'node': 'Check Resume Download Success',
            'type': 'main',
            'index': 0
        }]]
    }
    
    # Connection 3: Check Resume Download Success -> Parse Resume (TRUE) or Fallback (FALSE)
    workflow['connections']['Check Resume Download Success'] = {
        'main': [
            [{
                'node': 'Parse Resume with Groq AI',
                'type': 'main',
                'index': 0
            }],
            [{
                'node': 'Fallback: User Config Only',
                'type': 'main',
                'index': 0
            }]
        ]
    }
    
    # Connection 4: Parse Resume -> Structure Resume Data
    workflow['connections']['Parse Resume with Groq AI'] = {
        'main': [[{
            'node': 'Structure Resume Data',
            'type': 'main',
            'index': 0
        }]]
    }
    
    # Connection 5: Structure Resume Data -> Merge
    workflow['connections']['Structure Resume Data'] = {
        'main': [[{
            'node': 'Merge User Config with Resume Data',
            'type': 'main',
            'index': 0
        }]]
    }
    
    # Connection 6: Fallback -> Merge
    workflow['connections']['Fallback: User Config Only'] = {
        'main': [[{
            'node': 'Merge User Config with Resume Data',
            'type': 'main',
            'index': 0
        }]]
    }
    
    # Connection 7: Parse AI Score -> Resume Match Analysis
    workflow['connections']['Parse AI Score']['main'][0].append({
        'node': 'Resume Match Analysis',
        'type': 'main',
        'index': 0
    })
    
    # Connection 8: Resume Match Analysis -> Filter by Score
    workflow['connections']['Resume Match Analysis'] = {
        'main': [[{
            'node': 'Filter by Score Threshold (≥30)',
            'type': 'main',
            'index': 0
        }]]
    }
    
    # Update Parse AI Score to NOT directly connect to Filter (now goes through Resume Match Analysis)
    # Remove direct connection to filter
    parse_score_connections = workflow['connections']['Parse AI Score']['main'][0]
    workflow['connections']['Parse AI Score']['main'][0] = [
        conn for conn in parse_score_connections 
        if conn['node'] != 'Filter by Score Threshold (≥30)'
    ]
    
    print("✓ Step 7: Updated workflow connections for resume intelligence flow")
    
    # Update workflow metadata
    workflow['name'] = 'ENHANCED MASTER Job Automation System (with Resume Intelligence)'
    workflow['updatedAt'] = '2024-01-20T00:00:00.000Z'
    
    # Save enhanced workflow
    with open('ENHANCED-MASTER-workflow.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"\n✅ Enhanced workflow created successfully!")
    print(f"   Total nodes: {len(workflow['nodes'])} (was 44, added {len(new_nodes)})")
    print(f"   Total connections: {len(workflow['connections'])}")
    print(f"   Output: ENHANCED-MASTER-workflow.json")
    
    # Validation
    print("\n🔍 Validating workflow structure...")
    
    # Check all node IDs are unique
    node_ids = [n['id'] for n in workflow['nodes']]
    if len(node_ids) != len(set(node_ids)):
        print("   ⚠️  WARNING: Duplicate node IDs found!")
    else:
        print("   ✓ All node IDs are unique")
    
    # Check all connections reference valid nodes
    all_valid = True
    for source, targets in workflow['connections'].items():
        for branch in targets.get('main', []):
            for conn in branch:
                target_node = conn['node']
                if target_node not in [n['name'] for n in workflow['nodes']]:
                    print(f"   ⚠️  WARNING: Connection references non-existent node: {target_node}")
                    all_valid = False
    
    if all_valid:
        print("   ✓ All connections reference valid nodes")
    
    print("\n✅ Build complete! Import ENHANCED-MASTER-workflow.json into n8n.")

if __name__ == '__main__':
    main()
