# Rotation System Architecture - Technical Deep Dive

**Technical documentation for the multi-account rotation system in the n8n job automation workflow**

---

## Overview

The workflow implements a sophisticated multi-account rotation system across three key services:
- **Gmail**: 4 accounts, 200 emails/day total
- **Groq AI**: 4 API keys, 57,600 requests/day total
- **Google Sheets**: 4 credentials, 1,200 writes/day total

This document explains the technical implementation, algorithms, and design decisions.

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│  Multi-Account State Manager (Centralized)                   │
├──────────────────────────────────────────────────────────────┤
│  • Gmail Account State (4 accounts)                          │
│  • Groq Key State (4 keys)                                   │
│  • Sheets Credential State (4 credentials)                   │
│  • Daily Reset Logic                                          │
│  • Rotation History                                           │
└──────────────────────────────────────────────────────────────┘
             │                    │                    │
             ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Gmail Rotation  │  │ Groq Rotation   │  │ Sheets Rotation │
│ Engine          │  │ Engine          │  │ Engine          │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ • Account 1     │  │ • Key 1         │  │ • Credential 1  │
│ • Account 2     │  │ • Key 2         │  │ • Credential 2  │
│ • Account 3     │  │ • Key 3         │  │ • Credential 3  │
│ • Account 4     │  │ • Key 4         │  │ • Credential 4  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## State Management

### Centralized vs Distributed

**Design Decision: Centralized State Manager**

The workflow uses a single "Multi-Account State Manager" node that maintains all rotation state in workflow static data.

**Why Centralized?**
- ✅ Single source of truth
- ✅ Easier to debug (one place to check state)
- ✅ Atomic updates (no race conditions)
- ✅ Simplified daily reset logic

**Why Not Distributed?**
- ❌ Multiple state nodes would require synchronization
- ❌ Higher chance of state drift
- ❌ Complex error recovery

### State Schema

```javascript
// Workflow Static Data Schema
{
  // Gmail Account State
  gmailAccountState: [
    {
      email: 'account1@gmail.com',
      credentialId: 'credential-id-1',
      dailyLimit: 50,
      currentCount: 15,    // Emails sent today
      errors: 0,            // Consecutive errors
      lastUsed: '2024-01-20T09:15:00Z',
      status: 'active'      // active, exhausted, error
    },
    // ... accounts 2-4
  ],
  currentGmailIndex: 0,   // Active account index
  totalEmailCapacity: 200,
  
  // Groq Key State
  groqKeyState: [
    {
      credentialId: 'groq-key-1',
      dailyCount: 150,      // Requests today
      errors: 0,
      lastUsed: '2024-01-20T10:30:00Z'
    },
    // ... keys 2-4
  ],
  currentGroqIndex: 0,    // Active key index
  groqDailyLimit: 14400,  // Per key
  totalGroqCapacity: 57600,
  
  // Google Sheets Credential State
  sheetsCredentialState: [
    {
      credentialId: 'sheets-cred-1',
      dailyWrites: 45,      // Writes today
      lastUsed: '2024-01-20T08:00:00Z'
    },
    // ... credentials 2-4
  ],
  currentSheetsIndex: 0,  // Active credential index
  sheetsWriteLimit: 300,  // Per credential
  totalSheetsCapacity: 1200,
  
  // Daily Reset
  lastResetDate: '2024-01-20',
  
  // Rotation History
  rotationHistory: [
    {
      timestamp: '2024-01-20T09:15:30Z',
      service: 'Gmail',
      from: 'Account 1',
      to: 'Account 2',
      reason: 'Daily limit reached (50/50)'
    }
  ]
}
```

---

## Rotation Algorithms

### 1. Sequential Rotation (Gmail)

**Algorithm:**
```
Function SelectGmailAccount():
  current = gmailAccountState[currentGmailIndex]
  
  IF current.currentCount >= current.dailyLimit:
    CALL SwitchToNextAccount('limit_reached')
    current = gmailAccountState[currentGmailIndex]
  
  IF current.errors >= errorThreshold:
    CALL SwitchToNextAccount('error_threshold')
    current = gmailAccountState[currentGmailIndex]
  
  IF current.status == 'active':
    RETURN current.credentialId
  ELSE:
    CALL SwitchToNextAccount('account_inactive')
    RETURN SelectGmailAccount()  // Recursive retry

Function SwitchToNextAccount(reason):
  LogRotation(currentGmailIndex, currentGmailIndex + 1, reason)
  currentGmailIndex = (currentGmailIndex + 1) % 4
  
  IF AllAccountsExhausted():
    NOTIFY('All Gmail accounts exhausted for today')
    RETURN null
```

**Time Complexity:** O(1) average, O(n) worst case (all accounts exhausted)
**Space Complexity:** O(n) for state storage

**Characteristics:**
- Round-robin selection with health checks
- Automatic skip of exhausted/errored accounts
- Graceful degradation when accounts fail

### 2. Round-Robin with Error Tracking (Groq)

**Algorithm:**
```
Function SelectGroqKey():
  key = groqKeyState[currentGroqIndex]
  
  IF key.dailyCount >= groqDailyLimit:
    currentGroqIndex = (currentGroqIndex + 1) % 4
    RETURN SelectGroqKey()  // Try next key
  
  IF key.errors > 0:
    // Exponential backoff on errors
    IF TimeSinceLastError(key) < (2 ^ key.errors) minutes:
      currentGroqIndex = (currentGroqIndex + 1) % 4
      RETURN SelectGroqKey()
  
  RETURN key.credentialId

Function UpdateGroqState(keyIndex, success):
  IF success:
    groqKeyState[keyIndex].dailyCount += 1
    groqKeyState[keyIndex].errors = 0  // Reset error count
  ELSE:
    groqKeyState[keyIndex].errors += 1
  
  groqKeyState[keyIndex].lastUsed = NOW()
```

**Characteristics:**
- Pure round-robin for load distribution
- Exponential backoff for errored keys
- Automatic error recovery on success

### 3. Quota-Based Rotation (Google Sheets)

**Algorithm:**
```
Function SelectSheetsCredential():
  cred = sheetsCredentialState[currentSheetsIndex]
  
  IF cred.dailyWrites >= sheetsWriteLimit:
    currentSheetsIndex = (currentSheetsIndex + 1) % 4
    RETURN SelectSheetsCredential()
  
  RETURN cred.credentialId

Function UpdateSheetsState(credIndex, writesCount):
  sheetsCredentialState[credIndex].dailyWrites += writesCount
  sheetsCredentialState[credIndex].lastUsed = NOW()
  
  // Proactive switch near limit
  IF sheetsCredentialState[credIndex].dailyWrites >= sheetsWriteLimit - 10:
    currentSheetsIndex = (currentSheetsIndex + 1) % 4
```

**Characteristics:**
- Proactive switching (before hitting limit)
- Batch write counting
- No error tracking (Sheets errors are fatal)

---

## Daily Reset Mechanism

### Reset Logic

**Trigger:** First workflow execution after midnight UTC

**Algorithm:**
```
Function CheckAndResetDaily():
  today = GetCurrentDateUTC()
  
  IF today != lastResetDate:
    // Reset Gmail
    FOR account IN gmailAccountState:
      account.currentCount = 0
      account.errors = 0
      account.status = 'active'
    currentGmailIndex = 0
    
    // Reset Groq
    FOR key IN groqKeyState:
      key.dailyCount = 0
      key.errors = 0
    currentGroqIndex = 0
    
    // Reset Sheets
    FOR cred IN sheetsCredentialState:
      cred.dailyWrites = 0
    currentSheetsIndex = 0
    
    // Archive rotation history (keep last 7 days)
    ArchiveHistory(rotationHistory, 7)
    
    lastResetDate = today
    
    SendTelegramNotification('Daily reset completed')
```

**Reset Time:** Midnight UTC (00:00:00 UTC)

**Why UTC?**
- Consistent across all timezones
- n8n workflow schedules use UTC
- Avoids DST complications

---

## Error Handling Patterns

### 1. Transient Errors (Retry)

**Strategy:** Exponential backoff with account switch

```
Function HandleTransientError(accountIndex, error):
  account = gmailAccountState[accountIndex]
  account.errors += 1
  
  IF account.errors >= errorThreshold:
    SwitchToNextAccount('error_threshold')
    RETURN RETRY_WITH_NEXT_ACCOUNT
  ELSE:
    WAIT(2 ^ account.errors)  // Exponential backoff
    RETURN RETRY_SAME_ACCOUNT
```

**Examples:**
- Gmail: 429 Rate Limit (temporary)
- Groq: 503 Service Unavailable
- Sheets: 500 Internal Server Error

### 2. Permanent Errors (Skip)

**Strategy:** Mark account as failed, skip permanently

```
Function HandlePermanentError(accountIndex, error):
  account = gmailAccountState[accountIndex]
  account.status = 'failed'
  account.errors = 999  // Mark as permanently failed
  
  SwitchToNextAccount('permanent_failure')
  LogError('Account permanently failed', error)
  SendTelegramAlert('Account failed, check logs')
```

**Examples:**
- Gmail: 401 Unauthorized (credential revoked)
- Groq: 403 Forbidden (API key invalid)
- Sheets: 404 Not Found (sheet deleted)

### 3. Quota Errors (Switch)

**Strategy:** Immediately switch to next account

```
Function HandleQuotaError(accountIndex):
  account = gmailAccountState[accountIndex]
  account.currentCount = account.dailyLimit  // Mark as exhausted
  account.status = 'exhausted'
  
  SwitchToNextAccount('quota_exhausted')
  RETURN USE_NEXT_ACCOUNT
```

**Examples:**
- Gmail: "User rate limit exceeded"
- Groq: "Rate limit exceeded"
- Sheets: "Quota exceeded"

---

## Capacity Calculations

### Gmail Email Capacity

**Formula:**
```
Total Daily Capacity = Σ(account.dailyLimit for each active account)
Current Available = Total - Σ(account.currentCount)
```

**Example:**
- Account 1: 50 limit, 25 sent → 25 remaining
- Account 2: 50 limit, 10 sent → 40 remaining
- Account 3: 50 limit, 0 sent → 50 remaining
- Account 4: 50 limit, 0 sent → 50 remaining
- **Total Available: 165 emails**

### Groq Request Capacity

**Formula:**
```
Total Daily Capacity = Σ(groqDailyLimit for each key)
Current Available = Total - Σ(key.dailyCount)
```

**With 4 keys:**
```
Total = 4 × 14,400 = 57,600 requests/day
Per hour = 57,600 / 24 = 2,400 requests/hour
Per minute = 2,400 / 60 = 40 requests/minute
```

**Rate Limiting:**
- Groq enforces 30 requests/minute per key
- With 4 keys: 120 requests/minute theoretical max
- Workflow uses ~10 requests/minute (well under limit)

### Google Sheets Write Capacity

**Formula:**
```
Total Daily Capacity = Σ(sheetsWriteLimit for each credential)
Current Available = Total - Σ(cred.dailyWrites)
```

**Write Counting:**
- 1 append operation = 1 write
- 1 batch update of 10 rows = 10 writes
- 1 read operation = 0 writes (different quota)

---

## Monitoring and Observability

### Telegram Status Command

**Command:** `/status`

**Response:**
```
Multi-Account System Status

Gmail Accounts:
- Account 1: 25/50 sent today (50%)
- Account 2: 10/50 sent today (20%)
- Account 3: 0/50 sent today (0%)
- Account 4: 0/50 sent today (0%)
- Total: 35/200 (17.5%)
- Active: Account 1

Groq API Keys:
- Key 1: 150/14400 requests (1.0%)
- Key 2: 120/14400 requests (0.8%)
- Key 3: 98/14400 requests (0.7%)
- Key 4: 102/14400 requests (0.7%)
- Total: 470/57600 (0.8%)
- Active: Key 3

Google Sheets:
- Credential 1: 45/300 writes (15%)
- Credential 2: 32/300 writes (10.7%)
- Credential 3: 0/300 writes (0%)
- Credential 4: 0/300 writes (0%)
- Total: 77/1200 (6.4%)
- Active: Credential 2

Last Reset: 2024-01-20 00:00:00 UTC
Next Reset: 2024-01-21 00:00:00 UTC (in 14h 45m)
```

### Rotation History

**Query Static Data:**
```javascript
rotationHistory.slice(-10)  // Last 10 rotations
```

**Example Output:**
```json
[
  {
    "timestamp": "2024-01-20T09:15:30Z",
    "service": "Gmail",
    "from": "Account 1",
    "to": "Account 2",
    "reason": "Daily limit reached (50/50)"
  },
  {
    "timestamp": "2024-01-20T10:45:12Z",
    "service": "Groq",
    "from": "Key 2",
    "to": "Key 3",
    "reason": "Round-robin rotation"
  }
]
```

---

## Performance Optimizations

### 1. Lazy Account Switching

**Problem:** Checking account status on every request is expensive

**Solution:** Only check when operation fails

```
// Before (expensive)
FOR EACH request:
  CheckAccountStatus()
  SendRequest()

// After (lazy)
TRY:
  SendRequest()
CATCH QuotaError:
  SwitchAccount()
  SendRequest()
```

**Result:** 50% fewer status checks

### 2. Batch State Updates

**Problem:** Updating static data on every operation is slow

**Solution:** Batch updates every N operations

```
Local state buffer = []

Function SendEmail():
  buffer.append({accountIndex, timestamp})
  
  IF buffer.length >= 10:
    FlushToStaticData(buffer)
    buffer = []
```

**Result:** 90% fewer static data writes

### 3. Proactive Switching

**Problem:** Hitting quota mid-operation causes failures

**Solution:** Switch before reaching limit

```
IF account.currentCount >= account.dailyLimit - 5:
  SwitchToNextAccount('proactive')
```

**Result:** Fewer quota-related errors

---

## Design Trade-offs

### 1. Round-Robin vs Load Balancing

**Chosen:** Round-robin

**Why?**
- Simple implementation
- Predictable behavior
- All accounts get equal use (good for sender reputation)

**Not Chosen:** Load balancing (least-used-first)

**Why Not?**
- More complex
- Could concentrate load on fastest account
- No significant benefit for this use case

### 2. Immediate Switch vs Backoff

**Chosen:** Immediate switch on quota, backoff on errors

**Why?**
- Quota errors are deterministic (know account is exhausted)
- Transient errors may resolve (retry same account)

### 3. Centralized vs Distributed State

**Chosen:** Centralized

**Why?**
- Simpler mental model
- Easier debugging
- No synchronization issues

**Not Chosen:** Distributed (per-service state nodes)

**Why Not?**
- More complex
- State drift risk
- No performance benefit (n8n is single-threaded)

---

## Future Enhancements

### 1. Adaptive Rotation

**Current:** Fixed limits (50 emails/account)

**Future:** Learn optimal limits based on success rates

```
Function AdaptiveLimit(account):
  successRate = account.successfulSends / account.totalAttempts
  
  IF successRate > 0.95:
    account.dailyLimit = MIN(account.dailyLimit + 5, 100)
  ELSE IF successRate < 0.85:
    account.dailyLimit = MAX(account.dailyLimit - 5, 25)
```

### 2. Predictive Switching

**Current:** Reactive (switch when limit hit)

**Future:** Predictive (switch based on time of day)

```
Function PredictiveSwitch():
  hoursRemaining = 24 - CurrentHour()
  emailsRemaining = TotalCapacity - TotalSent
  
  IF emailsRemaining / hoursRemaining > CurrentAccount.remaining:
    SwitchToNextAccount('predictive_balancing')
```

### 3. Health Scoring

**Current:** Binary (active/exhausted)

**Future:** Health score (0-100) based on:
- Success rate
- Response time
- Error rate
- Quota remaining

```
Function HealthScore(account):
  score = 100
  score -= (account.errors * 10)
  score -= ((account.dailyLimit - account.currentCount) / account.dailyLimit) * 30
  score -= (account.avgResponseTime / 1000) * 5
  RETURN MAX(score, 0)

Function SelectBestAccount():
  accounts = SortBy(gmailAccountState, HealthScore, DESC)
  RETURN accounts[0]
```

---

## Troubleshooting

### Issue: Accounts not rotating

**Symptoms:**
- All emails from Account 1
- `currentGmailIndex` stuck at 0

**Debug:**
1. Check static data: `gmailAccountState[0].currentCount`
2. Verify limit: `gmailAccountState[0].dailyLimit` should be 50
3. Check "Update Email State" node execution logs

**Common Causes:**
- `dailyLimit` set too high (e.g., 500 instead of 50)
- "Update Email State" node not executing
- State not persisting (workflow not saved)

### Issue: Daily reset not happening

**Symptoms:**
- Counters don't reset after midnight
- All accounts exhausted

**Debug:**
1. Check `lastResetDate` in static data
2. Verify workflow executes after midnight UTC
3. Check "Daily Reset Check" node logs

**Common Causes:**
- Workflow only runs at 8 AM UTC (after reset should trigger)
- Timezone confusion (using local time instead of UTC)
- `lastResetDate` format incorrect

### Issue: All accounts exhausted mid-day

**Symptoms:**
- `currentGmailIndex` cycles through all accounts
- No emails sending

**Debug:**
1. Check each account's `currentCount` and `dailyLimit`
2. Review rotation history for excessive switches
3. Check for errors: `account.errors > 0`

**Common Causes:**
- Accounts hitting Gmail's actual limit (500/day)
- Email content triggering spam filters
- OAuth credentials expired

---

## Related Documentation

- **MULTI-ACCOUNT-SETUP-GUIDE.md**: User setup instructions
- **FREE-APIS-LIST.md**: Job API details and fallback logic
- **ACCOUNTS-CHECKLIST.json**: Configuration reference
- **EMAIL-SETUP-GUIDE.md**: Gmail OAuth setup
- **GROQ-ROTATION-GUIDE.md**: Groq key rotation details
- **SHEETS-ROTATION-GUIDE.md**: Sheets credential rotation details

---

**Last Updated**: 2024-01-20  
**Feature**: FEAT-006 - Comprehensive Documentation  
**Related Features**: FEAT-001 (4-way Gmail), FEAT-003 (4-way Groq), FEAT-002 (4-way Sheets), FEAT-005 (Centralized State Manager)
