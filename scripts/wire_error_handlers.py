#!/usr/bin/env python3
"""Modernise the two error handlers to use centralised multiAccountState
   and wire them as side branches off the counter nodes."""
import json

WF = 'workflow/ENHANCED-MASTER-workflow.json'
with open(WF) as f:
    wf = json.load(f)

nodes = {n['name']: n for n in wf['nodes']}
conn = wf['connections']


def add_edge(src, target, src_output_index=0):
    if src not in conn:
        conn[src] = {}
    if 'main' not in conn[src]:
        conn[src]['main'] = []
    while len(conn[src]['main']) <= src_output_index:
        conn[src]['main'].append([])
    branch = conn[src]['main'][src_output_index]
    for c in branch:
        if c.get('node') == target:
            return
    branch.append({'node': target, 'type': 'main', 'index': 0})


# --- Modernise Sheets Error Handler ---
sheets_eh = nodes['Sheets Error Handler']
sheets_eh['parameters']['jsCode'] = """// Handle Google Sheets API errors and trigger account switch
// (Centralised state version - reads multiAccountState.sheets)
const staticData = this.getWorkflowStaticData('global');
const item = items[0].json;

// Pass through if state not initialised yet
if (!staticData.multiAccountState || !staticData.multiAccountState.sheets) {
  return [{ json: { ...item, errorHandled: false, reason: 'state not initialised' } }];
}

const state = staticData.multiAccountState.sheets;
let switched = false;
let switchReason = '';

if (item.error) {
  const errorCode = item.error.httpCode || item.error.code;
  const errorMessage = item.error.message || '';

  // Detect quota / rate-limit errors
  if (errorCode === 429 || errorCode === 403 ||
      errorMessage.includes('quota') || errorMessage.includes('rate limit')) {
    const currentAccount = state.currentActive;
    state[currentAccount].lastError = { code: errorCode, message: errorMessage, time: new Date().toISOString() };

    // Find next viable account
    const accounts = ['account1', 'account2', 'account3', 'account4'];
    const currentIndex = accounts.indexOf(currentAccount);
    const config = $('User Config (Master Profile)').item.json;
    const maxWrites = config.maxSheetsWritesPerAccount || 300;

    for (let i = 1; i <= 4; i++) {
      const next = accounts[(currentIndex + i) % 4];
      if (state[next].dailyWrites < maxWrites && !state[next].lastError) {
        state.currentActive = next;
        switched = true;
        switchReason = `Error ${errorCode}: ${errorMessage}`;
        console.log(`Sheets account switched from ${currentAccount} to ${next} due to error`);
        break;
      }
    }
  }
}

return [{
  json: {
    ...item,
    errorHandled: true,
    sheetsAccountSwitched: switched,
    sheetsSwitchReason: switchReason,
    sheetsAccount: state.currentActive,
    sheetsNeedsSwitch: switched
  }
}];
"""

# --- Modernise Groq Error Handler ---
groq_eh = nodes['Groq Error Handler']
groq_eh['parameters']['jsCode'] = """// Handle Groq API errors and trigger key switch
// (Centralised state version - reads multiAccountState.groq)
const staticData = this.getWorkflowStaticData('global');
const item = items[0].json;

if (!staticData.multiAccountState || !staticData.multiAccountState.groq) {
  return [{ json: { ...item, errorHandled: false, reason: 'state not initialised' } }];
}

const state = staticData.multiAccountState.groq;
let switched = false;
let switchReason = '';

if (item.error) {
  const errorCode = item.error.httpCode || item.error.code;
  const errorMessage = item.error.message || '';

  if (errorCode === 429 ||
      errorMessage.includes('rate limit') ||
      errorMessage.includes('quota') ||
      errorMessage.includes('exceeded')) {
    const currentKey = state.currentActive;
    state[currentKey].lastError = { code: errorCode, message: errorMessage, time: new Date().toISOString() };

    const keys = ['key1', 'key2', 'key3', 'key4'];
    const currentIndex = keys.indexOf(currentKey);
    const config = $('User Config (Master Profile)').item.json;
    const maxRequests = config.maxGroqRequestsPerKey || 14400;

    for (let i = 1; i <= 4; i++) {
      const next = keys[(currentIndex + i) % 4];
      if (state[next].dailyRequests < maxRequests && !state[next].lastError) {
        state.currentActive = next;
        switched = true;
        switchReason = `Error ${errorCode}: ${errorMessage}`;
        console.log(`Groq key switched from ${currentKey} to ${next} due to error`);
        break;
      }
    }
  }
}

return [{
  json: {
    ...item,
    errorHandled: true,
    groqKeySwitched: switched,
    groqSwitchReason: switchReason,
    groqKey: state.currentActive,
    groqNeedsSwitch: switched
  }
}];
"""

# Wire them in: each runs after its respective counter, then chains into the
# Check-if-switch-needed node so detected errors flow through the same
# switch-notification chain.
# Pattern:  Counter -> Error Handler -> Check-if-X-switch-needed
# Currently:  Counter -> Check-if-X-switch-needed
# We change to:  Counter -> Error Handler -> Check-if-X-switch-needed
# (and keep Counter -> Check direct too, in case Error Handler is a no-op)
add_edge('Update Sheets Write Counter', 'Sheets Error Handler')
add_edge('Sheets Error Handler', 'Check if Sheets Switch Notification Needed')
add_edge('Update Groq Request Counter', 'Groq Error Handler')
add_edge('Groq Error Handler', 'Check if Groq Switch Notification Needed')


# Save
with open(WF, 'w') as f:
    json.dump(wf, f, indent=2)

print('Error handlers modernised and wired.')

# Validate reachability again
all_names = {n['name'] for n in wf['nodes']}

def reachable_from(start):
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
    r = reachable_from(t)
    print(f"  reachable from {t!r}: {len(r)}")
    all_reachable |= r

unreachable = all_names - all_reachable
print(f"\nUnreachable ({len(unreachable)}):")
for n in sorted(unreachable):
    print(f"  - {n}")
