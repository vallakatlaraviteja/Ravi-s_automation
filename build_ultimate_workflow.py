#!/usr/bin/env python3
"""
Build MASTER-ULTIMATE-workflow.json
Complete production workflow with 5 APIs + Supabase
"""
import json
from datetime import datetime

def build_ultimate_workflow():
    workflow = {
        "name": "MASTER Job Automation - ULTIMATE Stack",
        "nodes": [],
        "connections": {},
        "settings": {"executionOrder": "v1"},
        "staticData": None,
        "tags": ["ultimate", "production", "supabase"],
        "triggerCount": 3,
        "updatedAt": datetime.now().isoformat() + "Z",
        "versionId": "2.0.0"
    }
    
    nodes = []
    
    # ============================================================
    # SECTION 1: TRIGGER NODES
    # ============================================================
    
    nodes.append({
        "id": "trigger-job-discovery",
        "name": "Schedule: Job Discovery (8 AM)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.1,
        "position": [240, 300],
        "parameters": {
            "rule": {"interval": [{"field": "cronExpression", "expression": "0 8 * * *"}]}
        }
    })
    
    nodes.append({
        "id": "trigger-email-outreach",
        "name": "Schedule: Email Outreach (9 AM)",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.1,
        "position": [240, 2200],
        "parameters": {
            "rule": {"interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]}
        }
    })
    
    nodes.append({
        "id": "trigger-telegram",
        "name": "Telegram: Interactive Assistant",
        "type": "n8n-nodes-base.telegramTrigger",
        "typeVersion": 1,
        "position": [240, 3800],
        "parameters": {"updates": ["message"]},
        "credentials": {"telegramApi": {"id": "YOUR_TELEGRAM_CREDENTIAL_ID", "name": "Telegram Bot"}},
        "webhookId": "telegram-ultimate"
    })
    
    # ============================================================
    # SECTION 2: USER CONFIG
    # ============================================================
    
    nodes.append({
        "id": "user-config",
        "name": "User Config (Master Profile)",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [460, 300],
        "parameters": {
            "jsCode": """return [{
  json: {
    name: 'Your Name',
    currentRole: 'Backend Developer',
    targetRole: 'Senior Backend Engineer',
    experience: '3 years',
    skills: ['Python', 'JavaScript', 'AWS'],
    keywords: 'python developer OR backend engineer',
    workMode: ['remote', 'hybrid'],
    minSalary: 80000,
    country: 'us',
    resumeUrl: 'https://drive.google.com/file/d/ID/view',
    linkedinUrl: 'https://linkedin.com/in/profile',
    githubUrl: 'https://github.com/username',
    portfolioUrl: 'https://yoursite.com',
    userEmail: 'your.email@gmail.com',
    dailyLimit: 10,
    scoreThreshold: 30,
    sheetId: 'YOUR_SPREADSHEET_ID'
  }
}];"""
        }
    })
    
    print(f"Built {len(nodes)} foundation nodes")
    return {"workflow": workflow, "nodes": nodes}

if __name__ == "__main__":
    result = build_ultimate_workflow()
    print(f"✅ Foundation ready: {len(result['nodes'])} nodes")
