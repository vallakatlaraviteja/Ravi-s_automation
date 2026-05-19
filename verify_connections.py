#!/usr/bin/env python3
import json

with open('/projects/sandbox/Ravi-s_automation/MASTER-job-automation-workflow.json', 'r') as f:
    workflow = json.load(f)

all_nodes = {node['name'] for node in workflow['nodes']}
referenced_nodes = set()

# Triggers don't need incoming connections
triggers = {node['name'] for node in workflow['nodes'] if 'Trigger' in node['type']}

# Get all referenced nodes from connections
for source, targets in workflow['connections'].items():
    if source not in all_nodes:
        print(f"❌ Connection references non-existent source node: {source}")
    for branch in targets['main']:
        for target in branch:
            target_name = target['node']
            referenced_nodes.add(target_name)
            if target_name not in all_nodes:
                print(f"❌ Connection references non-existent target node: {target_name}")

# Check for orphans (nodes with no incoming connections except triggers)
nodes_with_incoming = referenced_nodes | triggers
orphans = all_nodes - nodes_with_incoming

if orphans:
    print(f"❌ Found {len(orphans)} orphan nodes (no incoming connections):")
    for orphan in orphans:
        print(f"  - {orphan}")
else:
    print("✅ No orphan nodes found - all nodes are connected")

# Check for nodes that should have outgoing connections but don't
nodes_with_outgoing = set(workflow['connections'].keys())
terminal_nodes = {
    'Send Telegram: Job Discovery Digest',
    'Send Gmail: Job Discovery Digest',
    'Send Gmail: Outreach Digest',
    'Send Quick Reply',
    'Send Telegram Reply (with stats)',
    'Send Telegram Reply (simple)'
}

non_terminal_without_outgoing = all_nodes - nodes_with_outgoing - terminal_nodes - triggers
if non_terminal_without_outgoing:
    print(f"⚠️  Found {len(non_terminal_without_outgoing)} non-terminal nodes without outgoing connections:")
    for node in non_terminal_without_outgoing:
        print(f"  - {node}")

print(f"\n📊 Summary:")
print(f"Total nodes: {len(all_nodes)}")
print(f"Trigger nodes: {len(triggers)}")
print(f"Nodes with connections: {len(workflow['connections'])}")
print(f"Terminal nodes (end of workflow): {len(terminal_nodes & all_nodes)}")
