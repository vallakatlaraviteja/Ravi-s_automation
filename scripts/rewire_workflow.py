#!/usr/bin/env python3
"""
Comprehensive rewiring script for ENHANCED-MASTER-workflow.json

Goals:
  1. Convert id-keyed connection sources to name-keyed (n8n requires names)
  2. Remove the dead single-account 'Send Email via Gmail' node
  3. Wire 7 job APIs + Job API State Manager into the discovery branch
  4. Wire Sheets credential rotation (state init, counter, switch notification, log)
  5. Wire Groq key rotation (state init, counter, switch notification, log)
  6. Wire Daily Reset trigger -> (init) -> Daily Reset Handler
  7. Wire Telegram /status path through Needs State Report?
  8. Wire Account Switch Logger / Route to Appropriate Notification chain
  9. Patch Daily Reset Handler so it self-initialises state when triggered standalone
"""
import json
from copy import deepcopy

WORKFLOW_PATH = 'workflow/ENHANCED-MASTER-workflow.json'

with open(WORKFLOW_PATH) as f:
    wf = json.load(f)

nodes = {n['name']: n for n in wf['nodes']}
id_to_name = {n.get('id'): n['name'] for n in wf['nodes']}
conn = wf['connections']


def add_edge(src, target, src_output_index=0, target_input_index=0):
    """Append a connection from src to target. Idempotent."""
    if src not in conn:
        conn[src] = {}
    if 'main' not in conn[src]:
        conn[src]['main'] = []
    while len(conn[src]['main']) <= src_output_index:
        conn[src]['main'].append([])
    branch = conn[src]['main'][src_output_index]
    for c in branch:
        if c.get('node') == target and c.get('index', 0) == target_input_index:
            return  # already present
    branch.append({'node': target, 'type': 'main', 'index': target_input_index})


def remove_edge(src, target):
    if src not in conn:
        return
    branches = conn[src].get('main', [])
    for branch in branches:
        for c in list(branch):
            if c.get('node') == target:
                branch.remove(c)


# -----------------------------------------------------------------
# STEP 1: Convert id-keyed connection sources to node names
# -----------------------------------------------------------------
print('=== Step 1: Fix id-keyed connection sources ===')
new_conn = {}
for src, payload in conn.items():
    if src in nodes:
        # already a name
        if src in new_conn:
            # merge payloads
            for branch_type, branches in payload.items():
                if branch_type not in new_conn[src]:
                    new_conn[src][branch_type] = branches
                else:
                    # merge per-output-index
                    while len(new_conn[src][branch_type]) < len(branches):
                        new_conn[src][branch_type].append([])
                    for i, branch in enumerate(branches):
                        for c in branch:
                            if c not in new_conn[src][branch_type][i]:
                                new_conn[src][branch_type][i].append(c)
        else:
            new_conn[src] = payload
    elif src in id_to_name:
        name = id_to_name[src]
        print(f'  remap: {src} -> {name}')
        if name in new_conn:
            # merge
            for branch_type, branches in payload.items():
                if branch_type not in new_conn[name]:
                    new_conn[name][branch_type] = branches
                else:
                    while len(new_conn[name][branch_type]) < len(branches):
                        new_conn[name][branch_type].append([])
                    for i, branch in enumerate(branches):
                        for c in branch:
                            if c not in new_conn[name][branch_type][i]:
                                new_conn[name][branch_type][i].append(c)
        else:
            new_conn[name] = payload
    else:
        print(f'  WARNING unknown source key: {src}')
        new_conn[src] = payload
conn = new_conn
wf['connections'] = conn

# Also rewrite any connection TARGETS that still use IDs
for src, payload in conn.items():
    for branches in payload.values():
        for branch in branches:
            for c in branch:
                if c['node'] not in nodes and c['node'] in id_to_name:
                    print(f'  remap target: {c["node"]} -> {id_to_name[c["node"]]}')
                    c['node'] = id_to_name[c['node']]


# -----------------------------------------------------------------
# STEP 2: Remove dead 'Send Email via Gmail' node (single-account leftover)
# -----------------------------------------------------------------
print('\n=== Step 2: Remove dead Send Email via Gmail node ===')
dead_name = 'Send Email via Gmail'
if dead_name in nodes:
    wf['nodes'] = [n for n in wf['nodes'] if n['name'] != dead_name]
    nodes.pop(dead_name)
    if dead_name in conn:
        conn.pop(dead_name)
    # remove any incoming references too (none expected)
    for src, payload in conn.items():
        for branches in payload.values():
            for branch in branches:
                for c in list(branch):
                    if c['node'] == dead_name:
                        branch.remove(c)
    print(f'  removed {dead_name}')


# -----------------------------------------------------------------
# STEP 3: Wire Job Discovery init chain (state managers)
#   User Config (Master Profile) -> Multi-Account State Manager -> {Sheets State, Groq State}
# -----------------------------------------------------------------
print('\n=== Step 3: Wire init chain on Job Discovery branch ===')
add_edge('User Config (Master Profile)', 'Multi-Account State Manager')
add_edge('Multi-Account State Manager', 'Google Sheets Account State')
add_edge('Multi-Account State Manager', 'Groq API Key State')
# Side branches into selectors so they execute and log usage
add_edge('Google Sheets Account State', 'Select Sheets Credential')
add_edge('Groq API Key State', 'Select Groq Credential')


# -----------------------------------------------------------------
# STEP 4: Sheets rotation - counter + switch detection chain (Job Discovery)
#   Append to Google Sheets: Jobs Tab -> Update Sheets Write Counter
#   Update Sheets Write Counter -> Check if Sheets Switch Notification Needed
#   Check ... [true] -> Log Sheets Switch
# -----------------------------------------------------------------
print('\n=== Step 4: Wire Sheets rotation counter + switch detection ===')
add_edge('Append to Google Sheets: Jobs Tab', 'Update Sheets Write Counter')
add_edge('Update Sheet: Mark Email Sent', 'Update Sheets Write Counter')
add_edge('Update Sheets Write Counter', 'Check if Sheets Switch Notification Needed')
# IF node: output 0 = true (switch needed) -> Log Sheets Switch
add_edge('Check if Sheets Switch Notification Needed', 'Log Sheets Switch', src_output_index=0)


# -----------------------------------------------------------------
# STEP 5: Groq rotation - counter + switch detection chain
#   Groq AI: Score Job Match -> Update Groq Request Counter
#   Groq AI: Generate Personalized Email -> Update Groq Request Counter
#   Parse Resume with Groq AI -> Update Groq Request Counter
#   Groq Agent (Llama 3.3 70B) -> Update Groq Request Counter
#   Update Groq Request Counter -> Check if Groq Switch Notification Needed
#   Check ... [true] -> Log Groq Switch
# -----------------------------------------------------------------
print('\n=== Step 5: Wire Groq rotation counter + switch detection ===')
add_edge('Groq AI: Score Job Match', 'Update Groq Request Counter')
add_edge('Groq AI: Generate Personalized Email', 'Update Groq Request Counter')
add_edge('Parse Resume with Groq AI', 'Update Groq Request Counter')
add_edge('Groq Agent (Llama 3.3 70B)', 'Update Groq Request Counter')
add_edge('Update Groq Request Counter', 'Check if Groq Switch Notification Needed')
add_edge('Check if Groq Switch Notification Needed', 'Log Groq Switch', src_output_index=0)


# -----------------------------------------------------------------
# STEP 6: Wire Email Outreach branch state init + Sheets/Groq init
# -----------------------------------------------------------------
print('\n=== Step 6: Wire Email Outreach init chain ===')
add_edge('Daily Reset Check', 'Multi-Account State Manager')
add_edge('Email Account State', 'Google Sheets Account State')
add_edge('Email Account State', 'Groq API Key State')


# -----------------------------------------------------------------
# STEP 7: Wire Switch Notification chain
#   Should Send Notification? [true] -> Log Email Switch  (replace direct -> Email Account Switch Notification)
#   Log Email Switch -> Account Switch Logger
#   Log Sheets Switch -> Account Switch Logger
#   Log Groq Switch -> Account Switch Logger
#   Account Switch Logger -> Route to Appropriate Notification
#   Route [0]=gmail -> Email Account Switch Notification
#   Route [1]=sheets -> Sheets Account Switch Notification
#   Route [2]=groq -> Groq Key Switch Notification
# (Many of these came from the id-keyed entries already remapped in Step 1.
#  Here we ensure they exist and add the email branch.)
# -----------------------------------------------------------------
print('\n=== Step 7: Wire switch notification chain ===')
# Replace Should Send Notification? [true] -> direct notification with -> Log Email Switch
remove_edge('Should Send Notification?', 'Email Account Switch Notification')
add_edge('Should Send Notification?', 'Log Email Switch', src_output_index=0)
# Ensure log -> logger -> router -> notifications chain
add_edge('Log Email Switch', 'Account Switch Logger')
add_edge('Log Sheets Switch', 'Account Switch Logger')
add_edge('Log Groq Switch', 'Account Switch Logger')
add_edge('Account Switch Logger', 'Route to Appropriate Notification')
add_edge('Route to Appropriate Notification', 'Email Account Switch Notification', src_output_index=0)
add_edge('Route to Appropriate Notification', 'Sheets Account Switch Notification', src_output_index=1)
add_edge('Route to Appropriate Notification', 'Groq Key Switch Notification', src_output_index=2)


# -----------------------------------------------------------------
# STEP 8: Telegram /status path
#   Insert Needs State Report? between Handle Quick Commands and Is Quick Command?
# -----------------------------------------------------------------
print('\n=== Step 8: Wire Telegram /status path ===')
remove_edge('Handle Quick Commands', 'Is Quick Command?')
add_edge('Handle Quick Commands', 'Needs State Report?')
# Needs State Report? [true=0] -> Get Full State Report (already there from id remap)
# Needs State Report? [false=1] -> Is Quick Command? (already there from id remap)
# Get Full State Report -> Send Telegram Reply (status) (already there)
add_edge('Needs State Report?', 'Get Full State Report', src_output_index=0)
add_edge('Needs State Report?', 'Is Quick Command?', src_output_index=1)
add_edge('Get Full State Report', 'Send Telegram Reply (status)')


# -----------------------------------------------------------------
# STEP 9: Daily Reset trigger chain
#   Schedule Trigger: Daily Reset (Midnight UTC) -> Daily Reset Handler
#   Daily Reset Handler -> Account Switch Logger (so it can log + notify if needed)
# -----------------------------------------------------------------
print('\n=== Step 9: Wire Daily Reset trigger ===')
add_edge('Schedule Trigger: Daily Reset (Midnight UTC)', 'Daily Reset Handler')


# -----------------------------------------------------------------
# STEP 10: Patch Daily Reset Handler to self-initialise state
# (so the orphaned trigger works without needing User Config / MASM upstream)
# -----------------------------------------------------------------
print('\n=== Step 10: Patch Daily Reset Handler to self-init state ===')
drh = nodes.get('Daily Reset Handler')
if drh:
    code = drh['parameters'].get('jsCode', '')
    if "if (!staticData.multiAccountState) {\n  return [{ json: { error: 'multiAccountState not initialized', date: today } }];\n}" in code:
        new_init = """if (!staticData.multiAccountState) {
  // Self-initialise state on first run (e.g. when triggered standalone by midnight reset)
  staticData.multiAccountState = {
    gmail: {
      account1: { email: 'raviintouch2@gmail.com', dailyCount: 0, errors: 0, credentialId: '', lastError: null },
      account2: { email: 'ravitejavallakatla7@gmail.com', dailyCount: 0, errors: 0, credentialId: '', lastError: null },
      account3: { email: 'ravitejav081@gmail.com', dailyCount: 0, errors: 0, credentialId: '', lastError: null },
      account4: { email: 'ravitejav0801@gmail.com', dailyCount: 0, errors: 0, credentialId: '', lastError: null },
      currentActive: 'account1'
    },
    sheets: {
      account1: { email: 'raviintouch2@gmail.com', dailyWrites: 0, errors: 0, credentialId: '', lastError: null },
      account2: { email: 'ravitejavallakatla7@gmail.com', dailyWrites: 0, errors: 0, credentialId: '', lastError: null },
      account3: { email: 'ravitejav081@gmail.com', dailyWrites: 0, errors: 0, credentialId: '', lastError: null },
      account4: { email: 'ravitejav0801@gmail.com', dailyWrites: 0, errors: 0, credentialId: '', lastError: null },
      currentActive: 'account1'
    },
    groq: {
      key1: { name: 'groq1', dailyRequests: 0, credentialId: '', lastError: null },
      key2: { name: 'groq2', dailyRequests: 0, credentialId: '', lastError: null },
      key3: { name: 'groq3', dailyRequests: 0, credentialId: '', lastError: null },
      key4: { name: 'groq4', dailyRequests: 0, credentialId: '', lastError: null },
      currentActive: 'key1'
    },
    lastResetDate: null,
    rotationHistory: []
  };
}"""
        old_init = """if (!staticData.multiAccountState) {
  return [{ json: { error: 'multiAccountState not initialized', date: today } }];
}"""
        drh['parameters']['jsCode'] = code.replace(old_init, new_init)
        print('  patched Daily Reset Handler')
    else:
        print('  Daily Reset Handler already patched or unexpected format')


# -----------------------------------------------------------------
# STEP 11: Save and validate
# -----------------------------------------------------------------
print('\n=== Step 11: Save ===')
with open(WORKFLOW_PATH, 'w') as f:
    json.dump(wf, f, indent=2)
print(f'  wrote {WORKFLOW_PATH}')


# -----------------------------------------------------------------
# Validation
# -----------------------------------------------------------------
print('\n=== Validation: reachability ===')
all_names = {n['name'] for n in wf['nodes']}
print(f'  total nodes: {len(all_names)}')

# Verify all connection keys + targets resolve to node names
unknown_keys = [k for k in conn.keys() if k not in all_names]
unknown_targets = []
for src, payload in conn.items():
    for branches in payload.values():
        for branch in branches:
            for c in branch:
                if c['node'] not in all_names:
                    unknown_targets.append(c['node'])
print(f'  unknown source keys: {len(unknown_keys)}  {unknown_keys}')
print(f'  unknown target refs: {len(unknown_targets)}  {set(unknown_targets)}')

# Reachability
def reachable_from(start, conn):
    seen = {start}
    stack = [start]
    while stack:
        cur = stack.pop()
        for branches in conn.get(cur, {}).values():
            for branch in branches:
                for c in branch:
                    if c['node'] not in seen:
                        seen.add(c['node'])
                        stack.append(c['node'])
    return seen

triggers = [n['name'] for n in wf['nodes'] if 'trigger' in n.get('type', '').lower()]
all_reachable = set()
for t in triggers:
    r = reachable_from(t, conn)
    print(f'  reachable from {t!r}: {len(r)}')
    all_reachable |= r

unreachable = all_names - all_reachable
print(f'\n  unreachable nodes ({len(unreachable)}):')
for n in sorted(unreachable):
    print(f'    - {n}')
