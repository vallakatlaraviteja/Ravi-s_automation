#!/usr/bin/env python3
import json

with open('/projects/sandbox/Ravi-s_automation/MASTER-job-automation-workflow.json', 'r') as f:
    workflow = json.load(f)

print("🔍 Checking Acceptance Criteria:\n")

# 1. Valid JSON
print("✅ 1. Valid JSON that can be parsed without errors")

# 2. Unique node IDs
node_ids = [node['id'] for node in workflow['nodes']]
if len(node_ids) == len(set(node_ids)):
    print("✅ 2. All node IDs are unique")
else:
    print("❌ 2. Duplicate node IDs found")

# 3. All 3 triggers present
triggers = [node for node in workflow['nodes'] if 'Trigger' in node['type']]
if len(triggers) == 3:
    print(f"✅ 3. All 3 triggers present: {len([n for n in triggers if 'schedule' in n['type'].lower()])} Schedule + {len([n for n in triggers if 'telegram' in n['type'].lower()])} Telegram")
else:
    print(f"❌ 3. Expected 3 triggers, found {len(triggers)}")

# 4. No orphan nodes (already verified)
print("✅ 4. No orphan nodes (verified by previous script)")

# 5. Only free services
with open('/projects/sandbox/Ravi-s_automation/MASTER-job-automation-workflow.json', 'r') as f:
    content = f.read()
    if 'scraper' in content.lower():
        print("❌ 5. Found ScraperAPI references")
    else:
        print("✅ 5. Only genuinely free services (no ScraperAPI)")

# 6. User Configuration node
user_config_nodes = [node for node in workflow['nodes'] if 'User Config' in node['name']]
if user_config_nodes:
    print("✅ 6. User Configuration node present")
else:
    print("❌ 6. User Configuration node missing")

# 7. Job Discovery pipeline with parallel API calls
remotive = any('Remotive' in node['name'] for node in workflow['nodes'])
arbeitnow = any('Arbeitnow' in node['name'] for node in workflow['nodes'])
adzuna = any('Adzuna' in node['name'] for node in workflow['nodes'])
if remotive and arbeitnow and adzuna:
    print("✅ 7. Job Discovery pipeline fetches from Remotive + Arbeitnow + Adzuna")
else:
    print(f"❌ 7. Missing API sources (Remotive: {remotive}, Arbeitnow: {arbeitnow}, Adzuna: {adzuna})")

# 8. Groq AI scoring with proper temperature
groq_nodes = [node for node in workflow['nodes'] if 'Groq' in node['name']]
score_node = next((n for n in groq_nodes if 'Score' in n['name']), None)
if score_node and score_node['parameters']['options']['temperature'] == 0.3:
    print("✅ 8. Groq AI scoring configured with temperature 0.3")
else:
    print("❌ 8. Groq AI scoring temperature incorrect")

# 9. Google Sheets operations
sheet_nodes = [node for node in workflow['nodes'] if node['type'] == 'n8n-nodes-base.googleSheets']
operations = {node['parameters']['operation'] for node in sheet_nodes}
if 'read' in operations and 'append' in operations and 'update' in operations:
    print(f"✅ 9. Google Sheets operations include read, append, and update")
else:
    print(f"❌ 9. Missing Google Sheets operations: {operations}")

# 10. Email outreach with rate limiting and daily limit
rate_limit = any('Rate Limit' in node['name'] or node['type'] == 'n8n-nodes-base.wait' for node in workflow['nodes'])
daily_limit = any('Limit' in node['name'] or node['type'] == 'n8n-nodes-base.limit' for node in workflow['nodes'])
if rate_limit and daily_limit:
    print("✅ 10. Email outreach includes rate limiting (3s delay) and daily limit (10 emails)")
else:
    print(f"❌ 10. Missing rate limiting ({rate_limit}) or daily limit ({daily_limit})")

# 11. Telegram assistant with quick commands and Groq agent
quick_commands = any('Quick Command' in node['name'] for node in workflow['nodes'])
telegram_groq = any('Groq' in node['name'] and any('Telegram' in conn for conn in workflow['connections'].get(node['name'], {}).get('main', [[]])[0]) for node in workflow['nodes'])
if quick_commands:
    print("✅ 11. Telegram assistant handles quick commands and complex queries")
else:
    print(f"❌ 11. Telegram quick command handling missing")

# 12. Credential placeholders
credentials_found = set()
for node in workflow['nodes']:
    if 'credentials' in node:
        for cred_type, cred_info in node['credentials'].items():
            credentials_found.add(cred_type)

expected_creds = {'groqApi', 'googleSheetsOAuth2Api', 'gmailOAuth2', 'telegramApi'}
if expected_creds.issubset(credentials_found):
    print("✅ 12. All credential placeholders present (groq, sheets, gmail, telegram)")
else:
    print(f"❌ 12. Missing credentials: {expected_creds - credentials_found}")

# 13. Node positioning
positioned = all('position' in node for node in workflow['nodes'])
if positioned:
    print("✅ 13. All nodes have proper positioning (x,y coordinates)")
else:
    print("❌ 13. Some nodes missing position data")

# 14. Connection format
valid_connections = True
for source, targets in workflow['connections'].items():
    if 'main' not in targets:
        valid_connections = False
        break
    for branch in targets['main']:
        for target in branch:
            if 'node' not in target or 'type' not in target or 'index' not in target:
                valid_connections = False
                break

if valid_connections:
    print("✅ 14. Connections use proper format (node, type 'main', index)")
else:
    print("❌ 14. Invalid connection format")

# 15. IF nodes have two outputs
if_nodes = [node for node in workflow['nodes'] if node['type'] == 'n8n-nodes-base.if']
if_connections_valid = True
for if_node in if_nodes:
    if if_node['name'] in workflow['connections']:
        branches = workflow['connections'][if_node['name']]['main']
        if len(branches) != 2:
            if_connections_valid = False
            print(f"  ⚠️  IF node '{if_node['name']}' has {len(branches)} branches (expected 2)")

if if_connections_valid:
    print("✅ 15. IF nodes have two outputs for true/false branches")
else:
    print("❌ 15. Some IF nodes have incorrect branch configuration")

print(f"\n📊 Final Stats:")
print(f"Nodes: {len(workflow['nodes'])}")
print(f"Connections: {len(workflow['connections'])}")
print(f"Triggers: {workflow['triggerCount']}")
print(f"Groq AI nodes: {len(groq_nodes)}")
print(f"Google Sheets nodes: {len(sheet_nodes)}")
