# Groq API 4-Way Rotation Setup Guide

This guide explains how to set up the 4-way Groq API key rotation system that provides **57,600 requests per day** (14,400 per key × 4 keys).

## Overview

The workflow now includes intelligent Groq API key rotation to maximize your daily capacity:

- **4 Groq API keys** (created using email alias trick)
- **14,400 requests per day per key** (Groq's free tier limit)
- **Total capacity: 57,600 requests/day**
- **Automatic key switching** when daily limit reached or rate limit errors occur
- **Daily reset at midnight UTC** (all counters reset to 0)
- **Telegram notifications** when keys switch

## Email Alias Trick

Groq (like most services) treats email aliases as separate accounts. Use your existing Gmail addresses with the `+` trick:

1. **Key 1:** `raviintouch2+groq1@gmail.com`
2. **Key 2:** `ravitejavallakatla7+groq2@gmail.com`
3. **Key 3:** `ravitejav081+groq3@gmail.com`
4. **Key 4:** `ravitejav0801+groq4@gmail.com`

All emails will arrive in your main Gmail inbox, but Groq treats each as a separate account.

## Step 1: Create 4 Groq Accounts

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with **raviintouch2+groq1@gmail.com**
3. Verify your email (check raviintouch2@gmail.com inbox)
4. Navigate to API Keys section
5. Create an API key and save it securely
6. Repeat for the other 3 email aliases

**Important:** Save all 4 API keys in a secure location.

## Step 2: Add Groq Credentials to n8n

For each of the 4 Groq API keys:

1. In n8n, go to **Settings** → **Credentials**
2. Click **Add Credential** → Search for **Groq**
3. Enter:
   - **Name:** `Groq API Key 1` (or Key 2, 3, 4)
   - **API Key:** Paste the API key from Step 1
4. Click **Save**
5. Copy the **Credential ID** (you'll see it in the URL or credential list)

Repeat for all 4 keys.

## Step 3: Configure Workflow

1. Open the workflow in n8n
2. Find the **User Config (Master Profile)** node
3. Update these fields with your actual credential IDs:

```javascript
groqKey1CredentialId: 'abc123...',  // Replace with actual ID from Step 2
groqKey2CredentialId: 'def456...',
groqKey3CredentialId: 'ghi789...',
groqKey4CredentialId: 'jkl012...',
maxGroqRequestsPerKey: 14400  // Daily limit per key (don't change)
```

4. Click **Execute Node** to test
5. Save the workflow

## Step 4: Update Groq AI Nodes (Important!)

n8n's Groq AI nodes use **static credentials** (credentials are configured at the node level, not dynamically). You have two options:

### Option A: Manual Credential Configuration (Simplest)

Use the state management to track usage, but manually configure one credential on all Groq nodes:

1. Locate these 4 Groq nodes in the workflow:
   - **Parse Resume with Groq AI** (id: `groq-parse-resume`)
   - **Groq AI: Score Job Match** (id: `groq-score-job`)
   - **Groq AI: Generate Personalized Email** (id: `groq-generate-email`)
   - **Groq Agent (Llama 3.3 70B)** (id: `groq-agent`)

2. For each node:
   - Click on the node
   - Go to **Credentials** section
   - Select **Groq API Key 1** from the dropdown
   - Save

3. When Key 1 exhausts (14,400 requests), you'll receive a Telegram notification
4. Manually update all 4 Groq nodes to use **Groq API Key 2**
5. Repeat for Key 3 and Key 4

**Note:** With typical usage (~71 requests/day), you'll only use one key and never exhaust it. The rotation system provides resilience and tracking.

### Option B: True Dynamic Switching (Advanced)

For automatic switching without manual intervention, use HTTP Request nodes with Groq's REST API:

1. Replace each Groq AI node with an HTTP Request node
2. Configure the HTTP Request to use Groq's API endpoint
3. Use the `Select Groq Credential` node to dynamically select the active key
4. Pass the credential ID to the HTTP Request headers

**Groq API Endpoint:**
```
POST https://api.groq.com/openai/v1/chat/completions
Headers:
  Authorization: Bearer YOUR_API_KEY
  Content-Type: application/json
Body:
  {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Your prompt"}],
    "temperature": 0.7
  }
```

See [Groq API Documentation](https://console.groq.com/docs/quickstart) for details.

## How It Works

### State Management

The **Groq API Key State** node tracks:

```javascript
{
  key1: {
    name: 'groq1',
    dailyRequests: 0,      // Incremented after each API call
    credentialId: '',
    lastError: null
  },
  // ... key2, key3, key4
  currentActive: 'key1',   // Which key is currently active
  lastResetDate: null,     // Last date counters were reset
  lastSwitchDate: null,    // When last switch occurred
  lastSwitchReason: ''     // Why switch happened
}
```

### Request Counter

The **Update Groq Request Counter** node:

1. Increments `dailyRequests` for the active key after each successful API call
2. Checks if `dailyRequests >= 14400`
3. If limit reached, switches to next available key
4. Sends Telegram notification on switch

### Error Handler

The **Groq Error Handler** node:

1. Detects rate limit errors (HTTP 429, quota exceeded messages)
2. Logs error to key state
3. Immediately switches to next available key
4. Prevents repeated failures on exhausted keys

### Daily Reset

At midnight UTC, the **Daily Reset Check** node:

1. Resets all 4 keys' `dailyRequests` to 0
2. Clears error states
3. Switches back to Key 1
4. Updates `lastResetDate`

## Usage Estimate

Based on your workflow's Groq API usage:

| Operation | Frequency | Requests/Day |
|-----------|-----------|--------------|
| Resume parsing | 1/day | 1 |
| Job scoring | 50/day | 50 |
| Email generation | 10/day | 10 |
| Telegram queries | 10/day | 10 |
| **TOTAL** | | **~71** |

**Capacity headroom:** 57,600 / 71 = **811x buffer**

With this usage, you'll never exhaust even a single key. The rotation system provides:

- **Resilience:** If one key fails, automatic failover to another
- **Tracking:** Monitor daily usage per key
- **Scalability:** Increase usage up to 57,600 requests/day if needed

## Telegram Notifications

When a key switch occurs, you'll receive:

```
🔑 Groq API Key Switched

Reason: Daily limit reached (14400/14400 requests)

Previous Key: Key 1 (groq1)

All Groq Key Status:
🤖 Key 1 (groq1): 14400/14400 requests
🤖 Key 2 (groq2): 0/14400 requests
🤖 Key 3 (groq3): 0/14400 requests
🤖 Key 4 (groq4): 0/14400 requests

Total Daily Capacity: 57,600 requests/day (14,400 per key × 4)

Estimated Daily Usage: ~71 requests/day
```

## Monitoring

To check Groq key status:

1. In n8n, execute the **Groq API Key State** node
2. View the output to see current request counts
3. Check Telegram notifications for switch alerts
4. Review n8n execution logs for detailed tracking

## Troubleshooting

### All Keys Exhausted

If all 4 keys reach 14,400 requests (unlikely with normal usage):

- **Wait until midnight UTC** for daily reset
- Or **manually upgrade** one Groq account to a paid plan for higher limits

### Key Not Switching

If automatic switching isn't working:

1. Verify all 4 credential IDs are correct in User Config
2. Check that `maxGroqRequestsPerKey` is set to 14400
3. Review n8n execution logs for errors
4. Manually execute the **Groq Error Handler** node to test

### Rate Limit Errors Despite Rotation

If you see rate limit errors even with rotation:

- Check that the **Update Groq Request Counter** node is connected after all Groq API calls
- Verify daily reset is working (check execution logs at midnight UTC)
- Consider adding a delay between consecutive Groq API calls

## Best Practices

1. **Monitor usage** regularly via Telegram notifications
2. **Test rotation** by manually executing the workflow multiple times
3. **Keep backup keys** ready (Key 3 and Key 4 are your safety net)
4. **Review logs** weekly to ensure counters are accurate
5. **Upgrade strategically** if you need more than 57,600 requests/day

## Support

For questions or issues:

1. Check n8n execution logs for error details
2. Review Groq console for account status
3. Test individual nodes to isolate problems
4. Verify credential IDs are correct

## Summary

- ✅ 4 Groq accounts created with email aliases
- ✅ 4 API keys configured in n8n
- ✅ User Config updated with credential IDs
- ✅ Groq AI nodes configured with credentials
- ✅ Telegram notifications enabled
- ✅ Daily reset at midnight UTC
- ✅ Total capacity: 57,600 requests/day

Your Groq rotation system is now ready! 🚀
