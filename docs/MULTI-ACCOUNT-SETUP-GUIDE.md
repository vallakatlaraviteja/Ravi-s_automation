# Multi-Account Setup Guide - 4-Way Rotation System

**Complete guide to setting up 4 Gmail accounts, 4 Groq API keys, 4 Google Sheets credentials, and 7 FREE job APIs**

---

## Introduction

### What is the 4-Account System?

The multi-account rotation system scales your job automation workflow to **4 accounts across three key services**, dramatically increasing your daily capacity:

**Capacity Comparison:**

| Service | 2-Account System | 4-Account System | Increase |
|---------|------------------|------------------|----------|
| Gmail Sending | 100 emails/day | **200 emails/day** | 2x |
| Groq AI Processing | 14,400 requests/day | **57,600 requests/day** | 4x |
| Google Sheets Writes | 300 writes/day | **1,200 writes/day** | 4x |
| Job API Sources | 3 sources | **7 sources** | 2.3x |

### Benefits

1. **Doubled Email Capacity**: Send 200 personalized outreach emails daily (4x 50 emails each)
2. **4x Groq Processing**: Massive headroom for AI scoring and email generation
3. **4x Sheets Throughput**: Handle larger job datasets without hitting write limits
4. **Intelligent Fallback**: 7 job APIs with cascading fallback
5. **Zero Downtime**: Automatic switching if one account hits limits or errors
6. **Daily Auto-Reset**: All counters reset at midnight UTC

### How Rotation Works

**Sequential Rotation:**
1. System starts with Account 1 (primary)
2. When Account 1 hits daily limit (50) OR error threshold (3 errors): switch to Account 2
3. When Account 2 exhausted: switch to Account 3
4. When Account 3 exhausted: switch to Account 4
5. At midnight UTC: reset all counters, return to Account 1

**Example Email Rotation:**
- 8 AM: Send 50 emails from Gmail Account 1
- 10 AM: Account 1 hits limit, switch to Account 2, send 50 more
- 2 PM: Account 2 hits limit, switch to Account 3, send 50 more
- 6 PM: Account 3 hits limit, switch to Account 4, send 50 more
- Total: 200 emails sent in one day with zero manual intervention

---

## Section 1: Gmail Setup (4 Accounts)

### 1.1 Gmail Accounts Overview

You need **4 separate Gmail accounts**. You can:
- Use 4 existing Gmail accounts you already have
- Create new Gmail accounts (recommended for dedicated job search)
- Mix existing and new accounts

**Recommended Naming Convention:**
- Account 1: `yourname+jobsearch1@gmail.com`
- Account 2: `yourname+jobsearch2@gmail.com`
- Account 3: `yourname+jobsearch3@gmail.com`
- Account 4: `yourname+jobsearch4@gmail.com`

**Note:** The `+` trick creates an alias (emails go to same inbox) BUT Google treats them as separate OAuth authorizations for API purposes.

### 1.2 Create Gmail Accounts

If you need to create new accounts:

1. Go to: [accounts.google.com/signup](https://accounts.google.com/signup)
2. Fill in registration form
3. Verify phone number (required by Google)
4. Complete setup
5. Repeat for all 4 accounts

**Tip:** You can use the same phone number for all 4 accounts (Google allows multiple accounts per number).

### 1.3 Enable OAuth for All 4 Accounts

Follow the **EMAIL-SETUP-GUIDE.md** instructions for each account:

1. Create ONE Google Cloud project (handles all 4 accounts)
2. Enable Gmail API
3. Create ONE OAuth Client ID/Secret (reuse for all accounts)
4. Add all 4 Gmail addresses to OAuth consent screen "Test Users"
5. In n8n, create 4 separate Gmail OAuth2 credentials:
   - `Gmail Account 1 OAuth2` → Authorize with Account 1
   - `Gmail Account 2 OAuth2` → Authorize with Account 2
   - `Gmail Account 3 OAuth2` → Authorize with Account 3
   - `Gmail Account 4 OAuth2` → Authorize with Account 4

**Critical:** When authorizing each credential in n8n, select the CORRECT Gmail account in the Google popup.

### 1.4 Get Credential IDs

After creating each Gmail credential in n8n:

1. Click the credential name in n8n Credentials list
2. Copy the credential ID from the browser URL: `/credentials/YOUR_ID`
3. Save in tracking template:
   - Gmail Account 1 Credential ID: `_________________`
   - Gmail Account 2 Credential ID: `_________________`
   - Gmail Account 3 Credential ID: `_________________`
   - Gmail Account 4 Credential ID: `_________________`

---

## Section 2: Groq Setup (4 API Keys)

### 2.1 The Email Alias Trick

Groq allows one account per email address. To get 4 API keys, use the **email+alias** trick:

**How it works:**
- Base email: `yourname@gmail.com`
- Alias 1: `yourname+groq1@gmail.com` → Groq sees as different email, Gmail delivers to same inbox
- Alias 2: `yourname+groq2@gmail.com`
- Alias 3: `yourname+groq3@gmail.com`
- Alias 4: `yourname+groq4@gmail.com`

All verification emails go to `yourname@gmail.com`, but Groq treats each as a separate account.

### 2.2 Create 4 Groq Accounts

**For each API key:**

1. Go to: [console.groq.com](https://console.groq.com)
2. Click "Sign Up" or "Sign In"
3. Use **Email sign-up option** (not GitHub/Google)
4. Enter email alias:
   - First account: `yourname+groq1@gmail.com`
   - Second account: `yourname+groq2@gmail.com`
   - Third account: `yourname+groq3@gmail.com`
   - Fourth account: `yourname+groq4@gmail.com`
5. Check your main Gmail inbox for verification email
6. Complete verification
7. Go to API Keys section
8. Create API Key, name it: `n8n-job-automation-key-1` (or 2, 3, 4)
9. Copy the key (starts with `gsk_`)
10. **SAVE IMMEDIATELY** (you can't see it again)

**Important:** Logout after each account creation before creating the next.

### 2.3 Add Groq Keys to n8n

For each of the 4 Groq API keys:

1. n8n → Credentials → Add Credential
2. Search: `Groq API`
3. Paste API key
4. Name credential:
   - `Groq API Key 1`
   - `Groq API Key 2`
   - `Groq API Key 3`
   - `Groq API Key 4`
5. Save and copy credential ID

**Save credential IDs:**
- Groq Key 1 Credential ID: `_________________`
- Groq Key 2 Credential ID: `_________________`
- Groq Key 3 Credential ID: `_________________`
- Groq Key 4 Credential ID: `_________________`

---

## Section 3: Google Sheets OAuth (4 Credentials)

### 3.1 Why 4 Sheets Credentials?

Google Sheets has a write quota of 300 writes per day per credential. With 4 credentials, you get 1,200 writes/day, allowing the workflow to handle much larger job datasets.

### 3.2 Same Email, 4 Credentials

Unlike Groq, you DON'T need 4 different Gmail accounts for Sheets. You can authorize the SAME Google account 4 times in n8n, creating 4 separate credential instances.

**How it works:**
- All 4 credentials point to the same Google Sheet
- All 4 use the same Google account
- n8n tracks quota separately for each credential ID
- Workflow rotates through credentials to distribute write load

### 3.3 Create 4 Sheets Credentials in n8n

**For each credential:**

1. n8n → Credentials → Add Credential
2. Search: `Google Sheets OAuth2`
3. Enter Client ID and Client Secret (same OAuth client as Gmail)
4. Click "Connect my account"
5. Authorize with your Google account (can be the same account all 4 times)
6. Grant "See, edit, create, delete spreadsheets" permission
7. Name credential:
   - `Google Sheets OAuth2 - Credential 1`
   - `Google Sheets OAuth2 - Credential 2`
   - `Google Sheets OAuth2 - Credential 3`
   - `Google Sheets OAuth2 - Credential 4`
8. Save and copy credential ID

**Save credential IDs:**
- Sheets Credential 1 ID: `_________________`
- Sheets Credential 2 ID: `_________________`
- Sheets Credential 3 ID: `_________________`
- Sheets Credential 4 ID: `_________________`

---

## Section 4: New Job APIs Setup (7 Total)

### 4.1 Existing APIs (Already in Workflow)

These are already configured, just for reference:

1. **Remotive** (https://remotive.com/api/remote-jobs)
   - Free tier: Unlimited
   - Requires: No API key

2. **Arbeitnow** (https://www.arbeitnow.com/api/job-board-api)
   - Free tier: Unlimited
   - Requires: No API key

3. **Adzuna** (https://developer.adzuna.com)
   - Free tier: 250 requests/day
   - Requires: Application ID + Application Key (you already have this)

### 4.2 NEW API 1: JSearch (RapidAPI)

**What it is:** Comprehensive job search API aggregating multiple sources

**Free Tier:** 500 requests/month  
**Requires Credit Card:** No

**Setup:**

1. Go to: [rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
2. Click "Sign Up" (if new) or "Log In"
3. Click "Subscribe to Test" button
4. Select "Basic" plan (Free, 500 requests/month)
5. Complete signup (no payment required)
6. Go to "Endpoints" tab
7. Copy your API key from "X-RapidAPI-Key" header (right side code snippet)
8. Save: JSearch RapidAPI Key: `_________________`

**How to add to workflow:**
- Find node: `Fetch JSearch API`
- Headers section → `X-RapidAPI-Key` → Paste your key
- Save node

### 4.3 NEW API 2: The Muse

**What it is:** Curated job board focusing on company culture

**Free Tier:** 500 requests/hour (NO API KEY REQUIRED)  
**Requires Credit Card:** No

**Setup:**

NONE! The Muse API is completely open.

**Signup URL (for browsing):** [themuse.com/developers/api/v2](https://www.themuse.com/developers/api/v2)

**How it works:**
- Workflow already has the correct endpoint configured
- No authentication needed
- Just works out of the box

### 4.4 NEW API 3: USAJobs

**What it is:** Official U.S. government job board

**Free Tier:** Unlimited requests  
**Requires Credit Card:** No

**Setup:**

1. Go to: [developer.usajobs.gov](https://developer.usajobs.gov)
2. Click "Request API Key" link
3. Fill in request form:
   - Email: Your email
   - Name: Your name
   - Purpose: Personal job search automation
4. Submit form
5. Check email for API key
6. Save: USAJobs API Key: `_________________`

**How to add to workflow:**
- Find node: `Fetch USAJobs API`
- Headers section → `Authorization-Key` → Paste your key
- Save node

### 4.5 NEW API 4: GitHub Jobs

**What it is:** Jobs from GitHub's (deprecated but still working) job board

**Free Tier:** Unlimited  
**Requires Credit Card:** No  
**Requires API Key:** No

**Setup:**

NONE! GitHub Jobs API is completely open (no auth required).

**Note:** GitHub officially deprecated this API in 2021, but the endpoint still works and returns valid job listings. Use while available.

**How it works:**
- Workflow already configured with endpoint
- No API key needed
- May stop working in the future (GitHub hasn't shut it down yet)

### 4.6 API Cascading Fallback Logic

The workflow tries APIs in this order:

1. **Remotive** (primary, most reliable)
2. **Arbeitnow** (secondary)
3. **Adzuna** (tertiary)
4. **JSearch** (fallback 1)
5. **The Muse** (fallback 2)
6. **USAJobs** (fallback 3)
7. **GitHub Jobs** (fallback 4)

**How it works:**
- If Remotive succeeds: use those jobs
- If Remotive fails: try Arbeitnow
- If both fail: try Adzuna
- Continue down the chain until jobs found
- If ALL 7 fail: workflow logs error and sends notification

**Result:** Extremely high reliability (7 sources means near-zero chance of zero jobs found)

---

## Section 5: Workflow Configuration

### 5.1 Update User Config for 4-Account System

Open the **User Config (Master Profile)** node and update these sections:

**Gmail 4-Account Configuration:**
```javascript
// Gmail 4-Account Rotation
gmailAccounts: [
  {
    email: 'your-account1@gmail.com',
    credentialId: 'YOUR_GMAIL_1_CREDENTIAL_ID',
    dailyLimit: 50,
    currentCount: 0,
    errors: 0
  },
  {
    email: 'your-account2@gmail.com',
    credentialId: 'YOUR_GMAIL_2_CREDENTIAL_ID',
    dailyLimit: 50,
    currentCount: 0,
    errors: 0
  },
  {
    email: 'your-account3@gmail.com',
    credentialId: 'YOUR_GMAIL_3_CREDENTIAL_ID',
    dailyLimit: 50,
    currentCount: 0,
    errors: 0
  },
  {
    email: 'your-account4@gmail.com',
    credentialId: 'YOUR_GMAIL_4_CREDENTIAL_ID',
    dailyLimit: 50,
    currentCount: 0,
    errors: 0
  }
],
currentGmailIndex: 0,  // Start with first account
totalEmailCapacity: 200,
```

**Groq 4-Key Configuration:**
```javascript
// Groq 4-Key Rotation
groqKeys: [
  { credentialId: 'YOUR_GROQ_1_CREDENTIAL_ID', dailyCount: 0, errors: 0 },
  { credentialId: 'YOUR_GROQ_2_CREDENTIAL_ID', dailyCount: 0, errors: 0 },
  { credentialId: 'YOUR_GROQ_3_CREDENTIAL_ID', dailyCount: 0, errors: 0 },
  { credentialId: 'YOUR_GROQ_4_CREDENTIAL_ID', dailyCount: 0, errors: 0 }
],
currentGroqIndex: 0,
groqDailyLimit: 14400,  // Per key
totalGroqCapacity: 57600,
```

**Sheets 4-Credential Configuration:**
```javascript
// Google Sheets 4-Credential Rotation
sheetsCredentials: [
  { credentialId: 'YOUR_SHEETS_1_CREDENTIAL_ID', dailyWrites: 0 },
  { credentialId: 'YOUR_SHEETS_2_CREDENTIAL_ID', dailyWrites: 0 },
  { credentialId: 'YOUR_SHEETS_3_CREDENTIAL_ID', dailyWrites: 0 },
  { credentialId: 'YOUR_SHEETS_4_CREDENTIAL_ID', dailyWrites: 0 }
],
currentSheetsIndex: 0,
sheetsWriteLimit: 300,  // Per credential
totalSheetsCapacity: 1200,
```

### 5.2 Update Multi-Account State Manager Node

The workflow has a centralized state manager. Verify it has:

- `gmailAccountState`: Array of 4 Gmail accounts with counters
- `groqKeyState`: Array of 4 Groq keys with counters  
- `sheetsCredentialState`: Array of 4 Sheets credentials with counters
- `lastResetDate`: For daily midnight reset
- `rotationHistory`: Log of all account switches

**You don't need to manually edit this** - the workflow initializes it automatically from User Config.

### 5.3 Verify Credential Assignment in Nodes

Check these nodes have correct credential assignments:

**Gmail Sending Nodes:**
- `Send Email via Gmail Account 1` → Gmail Account 1 OAuth2 credential
- `Send Email via Gmail Account 2` → Gmail Account 2 OAuth2 credential
- `Send Email via Gmail Account 3` → Gmail Account 3 OAuth2 credential
- `Send Email via Gmail Account 4` → Gmail Account 4 OAuth2 credential

**Groq AI Nodes:**
- `Groq: Score Job (Key 1)` → Groq API Key 1 credential
- `Groq: Score Job (Key 2)` → Groq API Key 2 credential
- `Groq: Score Job (Key 3)` → Groq API Key 3 credential
- `Groq: Score Job (Key 4)` → Groq API Key 4 credential
- (Similar for email generation nodes)

**Google Sheets Nodes:**
- `Append to Sheet (Credential 1)` → Google Sheets OAuth2 - Credential 1
- `Append to Sheet (Credential 2)` → Google Sheets OAuth2 - Credential 2
- `Append to Sheet (Credential 3)` → Google Sheets OAuth2 - Credential 3
- `Append to Sheet (Credential 4)` → Google Sheets OAuth2 - Credential 4

---

## Section 6: Testing the 4-Account System

### Test 1: Gmail Rotation

**Objective:** Verify all 4 Gmail accounts can send emails and rotation works

**Steps:**

1. In Google Sheet, add 4 test jobs (rows 2-5) with:
   - Recruiter Email: YOUR_OWN_EMAIL@gmail.com
   - Recruiter Name: Test Recruiter 1, 2, 3, 4
   - Status: New

2. Execute the Email Outreach workflow branch

3. Check your inbox - should receive 4 emails

4. **Verify senders:**
   - Email 1: From Gmail Account 1
   - Email 2: From Gmail Account 2
   - Email 3: From Gmail Account 3
   - Email 4: From Gmail Account 4

5. Check workflow static data:
   - `gmailAccountState[0].currentCount`: 1
   - `gmailAccountState[1].currentCount`: 1
   - `gmailAccountState[2].currentCount`: 1
   - `gmailAccountState[3].currentCount`: 1
   - `currentGmailIndex`: 0 (reset to first after using all)

**Pass Criteria:** All 4 emails received from different sender accounts

### Test 2: Gmail Exhaustion and Switch

**Objective:** Verify automatic switching when account hits limit

**Steps:**

1. Manually set Account 1 count to limit:
   - Workflow Settings → Static Data
   - `gmailAccountState[0].currentCount = 50`
   - Save

2. Add test job to Sheet with Status: New

3. Execute Email Outreach workflow

4. **Verify:**
   - Email sent from Account 2 (not Account 1)
   - Telegram notification received: "Gmail Account Switched"
   - Static data shows `currentGmailIndex: 1`

5. Reset: `gmailAccountState[0].currentCount = 0`

**Pass Criteria:** Email sent from Account 2, notification received

### Test 3: Groq Rotation

**Objective:** Verify Groq keys rotate correctly

**Steps:**

1. Execute Job Discovery workflow

2. Check execution logs for Groq AI nodes

3. **Verify:**
   - Multiple Groq nodes executed
   - Each job scored using rotated keys
   - No "rate limit exceeded" errors

4. Check static data:
   - `groqKeyState[0].dailyCount` > 0
   - Other keys may also have counts (rotation happening)

**Pass Criteria:** Jobs scored successfully with no rate limit errors

### Test 4: Sheets Rotation

**Objective:** Verify Sheets credentials rotate

**Steps:**

1. Execute Job Discovery workflow multiple times

2. Check static data after each run:
   - `sheetsCredentialState[0].dailyWrites` increases
   - When exceeds threshold, switches to next credential
   - `currentSheetsIndex` increments

3. Check Google Sheet - all jobs saved correctly

**Pass Criteria:** Jobs saved, credentials rotate when needed

### Test 5: Job API Fallback

**Objective:** Verify 7 API cascading fallback

**Steps:**

1. Temporarily break Remotive API:
   - Edit `Fetch Remotive API` node
   - Change URL to invalid endpoint
   - Save

2. Execute Job Discovery workflow

3. **Verify:**
   - Remotive fails (expected)
   - Workflow continues to Arbeitnow
   - Jobs still found and saved
   - No workflow crash

4. Fix Remotive URL, save

5. Execute again - should use Remotive now

**Pass Criteria:** Workflow continues despite API failure, jobs still found

### Test 6: Daily Reset

**Objective:** Verify midnight UTC reset works

**Steps:**

1. Manually set yesterday's date:
   - Static Data → `lastResetDate: '2024-01-19'` (use yesterday)
   - Set some counters: `gmailAccountState[0].currentCount = 25`

2. Execute any workflow branch

3. **Verify:**
   - Daily Reset Check node triggers
   - All counters reset to 0
   - `lastResetDate` updated to today
   - `currentGmailIndex`, `currentGroqIndex`, `currentSheetsIndex` all reset to 0

**Pass Criteria:** All counters reset, indexes back to 0

---

## Section 7: Monitoring and Maintenance

### 7.1 Check System Status

**Via Telegram Bot:**

Message your bot: `/status`

Response should show:
```
Multi-Account System Status

Gmail Accounts:
- Account 1: 15/50 sent today (30%)
- Account 2: 8/50 sent today (16%)
- Account 3: 0/50 sent today (0%)
- Account 4: 0/50 sent today (0%)
- Total: 23/200 (11.5%)
- Active: Account 2

Groq API Keys:
- Key 1: 150/14400 requests today (1%)
- Key 2: 120/14400 requests today (0.8%)
- Key 3: 98/14400 requests today (0.7%)
- Key 4: 102/14400 requests today (0.7%)
- Total: 470/57600 (0.8%)
- Active: Key 3

Google Sheets:
- Credential 1: 45/300 writes today (15%)
- Credential 2: 32/300 writes today (10.7%)
- Credential 3: 0/300 writes today (0%)
- Credential 4: 0/300 writes today (0%)
- Total: 77/1200 (6.4%)
- Active: Credential 2

Last Reset: 2024-01-20 00:00:00 UTC
```

### 7.2 View Rotation History

Check workflow static data for `rotationHistory`:

```javascript
rotationHistory: [
  {
    timestamp: '2024-01-20T09:15:30Z',
    service: 'Gmail',
    from: 'Account 1',
    to: 'Account 2',
    reason: 'Daily limit reached (50/50)'
  },
  {
    timestamp: '2024-01-20T10:45:12Z',
    service: 'Groq',
    from: 'Key 2',
    to: 'Key 3',
    reason: 'Error threshold exceeded (3 errors)'
  }
]
```

### 7.3 Daily Monitoring Checklist

**Every morning:**

1. Check Telegram for overnight notifications
2. Verify Job Discovery ran at 8 AM UTC (check Google Sheet for new jobs)
3. Verify Email Outreach ran at 9 AM UTC (check Gmail sent folder)
4. Check execution logs for errors
5. Review `/status` for capacity usage

**Weekly:**

1. Review rotation patterns (are accounts balanced?)
2. Check for frequent errors (investigate root cause)
3. Verify all 7 job APIs still returning results
4. Audit Google Sheet for data quality

**Monthly:**

1. Refresh OAuth credentials if any show "expired" in n8n
2. Review and tune User Config (skills, keywords, score threshold)
3. Check for new free job APIs to add
4. Update resume URL if resume changed

---

## Troubleshooting

### Issue: Only 2 Gmail accounts working, not 4

**Symptom:** Workflow still behaving like 2-account system

**Cause:** User Config not updated to 4-account structure

**Solution:**
1. Open User Config node
2. Verify `gmailAccounts` array has 4 entries
3. Verify all 4 credential IDs are correct
4. Check workflow has 4 Gmail send nodes (not just 2)
5. Ensure Multi-Account State Manager initializes 4 accounts

### Issue: Groq "rate limit exceeded" even with 4 keys

**Symptom:** Hitting rate limits despite having 4 keys

**Cause:** Rotation not working, all requests going to one key

**Solution:**
1. Check `groqKeyState` in static data - are all 4 keys being used?
2. Verify `currentGroqIndex` increments after each request
3. Check Groq rotation logic in Multi-Account State Manager
4. Ensure all 4 Groq credentials are authorized (green checkmark)

### Issue: Sheets writes failing with quota error

**Symptom:** "Quota exceeded" error despite having 4 credentials

**Cause:** Rotation not distributing writes across credentials

**Solution:**
1. Check `sheetsCredentialState` - are writes balanced?
2. Verify threshold logic (should switch at 300 writes per credential)
3. Check `currentSheetsIndex` is incrementing
4. Ensure all 4 Sheets credentials authorized with same account

### Issue: Job APIs returning no results

**Symptom:** Zero jobs found from all 7 APIs

**Cause:** API keys expired, or endpoints changed

**Solution:**
1. Test each API individually (execute node in isolation)
2. Check JSearch and USAJobs API keys are valid
3. Verify API URLs haven't changed (check provider documentation)
4. Check workflow logs for specific API error messages
5. If one API broken, others should still work (fallback logic)

### Issue: Email rotation stuck on one account

**Symptom:** All emails sent from Account 1, never switches

**Cause:** Counter not incrementing, or limit set too high

**Solution:**
1. Check `gmailAccountState[0].currentCount` - is it incrementing?
2. Verify `dailyLimit: 50` in each account config
3. Check "Update Email State" node is executing after each send
4. Manually set `currentGmailIndex: 1` to force switch, see if Account 2 works

### Issue: Daily reset not happening

**Symptom:** Counters don't reset at midnight, accounts exhausted

**Cause:** Reset check node not executing, or timezone issue

**Solution:**
1. Workflow must execute AFTER midnight UTC to trigger reset
2. Check `lastResetDate` in static data - is it today?
3. Manually trigger reset: set `lastResetDate` to yesterday, execute workflow
4. Verify "Daily Reset Check" node runs at start of each workflow branch

---

## What if I Only Have 2 Gmail Accounts?

**Can the workflow still work?** YES!

**How to configure:**

1. In User Config, keep only 2 entries in `gmailAccounts` array:
```javascript
gmailAccounts: [
  { email: 'account1@gmail.com', credentialId: 'ID1', dailyLimit: 50, ... },
  { email: 'account2@gmail.com', credentialId: 'ID2', dailyLimit: 50, ... }
],
totalEmailCapacity: 100,  // Reduced from 200
```

2. Leave Gmail Account 3 and 4 credential IDs empty in tracking template

3. The workflow will automatically adapt:
   - Rotate between 2 accounts instead of 4
   - Total capacity: 100 emails/day
   - All other features work normally

**Capacity:**
- 2 Gmail accounts: 100 emails/day
- 4 Gmail accounts: 200 emails/day

**Note:** Groq and Sheets still benefit from 4 credentials (you don't need separate Gmail accounts for those).

---

## Summary

**You've configured:**
- ✅ 4 Gmail accounts with OAuth credentials
- ✅ 4 Groq API keys using email aliases
- ✅ 4 Google Sheets credentials (same account, 4 instances)
- ✅ 7 FREE job API sources (3 existing + 4 new)
- ✅ Intelligent rotation and fallback logic
- ✅ Daily auto-reset at midnight UTC

**Your new capacity:**
- **200 emails/day** (up from 100)
- **57,600 Groq requests/day** (up from 14,400)
- **1,200 Sheets writes/day** (up from 300)
- **7 job API sources** (up from 3)

**Zero additional cost** - all services remain 100% FREE.

---

## Next Steps

1. **Activate workflow** and let it run for 3 days
2. **Monitor via Telegram** `/status` command
3. **Review rotation patterns** in static data
4. **Tune thresholds** if needed (daily limits, error thresholds)
5. **Add more accounts** if you need even higher capacity

**Congratulations!** You now have an enterprise-grade multi-account job automation system running 100% free. 🚀

---

**Related Documentation:**
- **COMPLETE-SETUP-GUIDE.md**: Full workflow setup for beginners
- **EMAIL-SETUP-GUIDE.md**: Detailed Gmail OAuth instructions
- **FREE-APIS-LIST.md**: All 7 job APIs with examples and troubleshooting
- **ROTATION-SYSTEM-ARCHITECTURE.md**: Technical deep-dive into rotation algorithms
- **ACCOUNTS-CHECKLIST.json**: Structured requirements reference
