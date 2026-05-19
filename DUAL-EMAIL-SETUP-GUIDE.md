# Dual Email Failover Setup Guide

This guide explains how to configure and use the dual email failover system in the Enhanced n8n Job Automation workflow (FEAT-002).

## Overview

The dual email failover system automatically switches between two Gmail accounts to avoid hitting rate limits and handle errors gracefully. This ensures your email outreach continues uninterrupted even if one account encounters issues.

## Features

- **Automatic Failover**: Switches from primary to secondary account when limits or errors are hit
- **Daily Reset**: Counters reset at midnight UTC, returning to primary account
- **Error Handling**: Tracks consecutive errors and switches accounts after threshold (default: 3 errors)
- **Rate Limit Protection**: Monitors daily email count (default: 50 per account) to stay within Gmail's free tier limits
- **Telegram Notifications**: Alerts you immediately when failover occurs
- **Status Tracking**: Shows account usage in daily digest emails

## Prerequisites

1. Two Gmail accounts with OAuth2 access
2. n8n instance with Gmail OAuth2 integration enabled
3. Telegram bot configured (for notifications)
4. Google Sheets with Jobs tracking

## Setup Instructions

### Step 1: Create Gmail OAuth2 Credentials in n8n

#### Primary Account (raviintouch2@gmail.com)

1. In n8n, go to **Settings > Credentials**
2. Click **Add Credential** and select **Gmail OAuth2**
3. Enter credential name: `Gmail Primary OAuth2`
4. Follow Google OAuth flow to authenticate `raviintouch2@gmail.com`
5. Grant permissions for sending emails
6. Save credential and note the credential ID

#### Secondary Account (ravitejavallakatla7@gmail.com)

1. Click **Add Credential** again and select **Gmail OAuth2**
2. Enter credential name: `Gmail Secondary OAuth2`
3. Follow Google OAuth flow to authenticate `ravitejavallakatla7@gmail.com`
4. Grant permissions for sending emails
5. Save credential and note the credential ID

### Step 2: Configure User Config Node

In the `User Config (Master Profile)` node, update these fields:

```javascript
{
  // ... existing fields ...
  
  // Dual Email Configuration
  primaryEmail: 'raviintouch2@gmail.com',
  secondaryEmail: 'ravitejavallakatla7@gmail.com',
  primaryGmailCredentialId: 'YOUR_PRIMARY_GMAIL_CREDENTIAL_ID',  // From Step 1
  secondaryGmailCredentialId: 'YOUR_SECONDARY_GMAIL_CREDENTIAL_ID',  // From Step 1
  maxEmailsPerAccount: 50,  // Safe limit for Gmail free tier (actual limit: 500/day)
  errorThreshold: 3  // Switch after 3 consecutive errors
}
```

### Step 3: Update Credential References

Update the credential IDs in these nodes:

1. **Send Email via Gmail Primary**
   - Go to node settings > Credentials
   - Select your `Gmail Primary OAuth2` credential
   - Or manually update credential ID in JSON

2. **Send Email via Gmail Secondary**
   - Go to node settings > Credentials
   - Select your `Gmail Secondary OAuth2` credential
   - Or manually update credential ID in JSON

3. **Email Account Switch Notification** (Telegram)
   - Update `chatId` to your Telegram chat ID
   - Ensure Telegram credential is configured

### Step 4: Verify Workflow Connections

The email outreach flow should follow this path:

```
Schedule Trigger: Email Outreach (9 AM)
  ↓
Daily Reset Check
  ↓
Email Account State
  ↓
Read Jobs from Sheet for Outreach
  ↓
Filter: Status=New AND Has Recruiter Email
  ↓
Limit to Daily Max (10 emails)
  ↓
Groq AI: Generate Personalized Email
  ↓
Parse & Format Email
  ↓
Check Email Account Status
  ↓
Select Gmail Credential (Switch)
  ↓
├── Send Email via Gmail Primary (output 0)
├── Send Email via Gmail Secondary (output 1)
└── Skip Send - Both Accounts Exhausted (output 2)
  ↓
Email Send Result Handler
  ↓
Update Email State
  ↓
├── Update Metadata (Status & Application ID) → [continues to existing flow]
└── Should Send Notification? → Email Account Switch Notification (if switched)
```

## How It Works

### Account Selection Logic

The system uses this logic to select which account to use:

1. **Daily Reset**: At midnight UTC, all counters reset and primary account becomes active
2. **Primary Account Check**:
   - If `primaryDailyCount < 50` AND `primaryErrors < 3`: Use primary
   - Else: Check secondary availability
3. **Secondary Account Check**:
   - If `secondaryDailyCount < 50` AND `secondaryErrors < 3`: Use secondary
   - Else: Skip sending (both exhausted)
4. **Automatic Switch**:
   - When primary hits limit/errors: Switch to secondary
   - When both exhausted: Skip and log warning
   - After daily reset: Return to primary

### State Tracking

The workflow uses n8n's `workflow static data` to persist state across executions:

```javascript
{
  primaryEmail: 'raviintouch2@gmail.com',
  secondaryEmail: 'ravitejavallakatla7@gmail.com',
  currentActive: 'primary',  // or 'secondary'
  primaryDailyCount: 0,  // Emails sent today from primary
  secondaryDailyCount: 0,  // Emails sent today from secondary
  lastResetDate: '2024-01-20',  // UTC date
  primaryErrors: 0,  // Consecutive errors
  secondaryErrors: 0,  // Consecutive errors
  lastSwitchDate: '2024-01-20T09:15:00.000Z',  // ISO timestamp
  lastSwitchReason: 'Daily limit reached'  // or 'Error threshold exceeded'
}
```

### Failover Triggers

**Daily Limit Reached**:
- Trigger: Account sends 50 emails in one day
- Action: Switch to secondary account
- Notification: Telegram alert with counts and reason

**Error Threshold Exceeded**:
- Trigger: Account encounters 3 consecutive errors
- Action: Switch to secondary account
- Notification: Telegram alert with error counts

**Both Accounts Exhausted**:
- Trigger: Both accounts hit limits or errors
- Action: Skip email sending, log warning
- Notification: Warning message in workflow logs

### Error Handling

**Successful Send**:
- Increment daily count for active account
- Reset error counter for active account
- Continue to next email

**Failed Send**:
- Increment error counter for active account
- Check if error threshold reached
- If threshold reached: Switch to other account
- Continue to next email (don't block workflow)

**Download/API Errors**:
- Gracefully handle with `continueOnFail: true`
- Log errors but don't trigger account switch
- Resume processing on next execution

## Monitoring Active Account

### Via Telegram Notification

When failover occurs, you'll receive this notification:

```
⚠️ Email Account Switched

Reason: Daily limit reached

Previous Account: Primary (raviintouch2@gmail.com)
New Active Account: Secondary (ravitejavallakatla7@gmail.com)

Status:
📧 Primary: 50 sent today, 0 errors
📧 Secondary: 0 sent today, 0 errors

Time: 2024-01-20T09:15:00.000Z
```

### Via Daily Digest Email

The "Send Gmail: Outreach Digest" email includes:

```
Email Account Status:
📧 Primary (raviintouch2@gmail.com): 50 sent today
📧 Secondary (ravitejavallakatla7@gmail.com): 3 sent today
✅ Active Account: secondary
```

### Via Google Sheets (Optional)

You can optionally log state changes to a "Email Logs" sheet tab for historical tracking.

## Manual State Reset

If you need to manually reset the email state:

1. Open n8n workflow editor
2. Go to **Workflow > Settings > Static Data**
3. Find `emailAccountState` object
4. Edit values:
   - Set `currentActive: 'primary'`
   - Set `primaryDailyCount: 0`
   - Set `secondaryDailyCount: 0`
   - Set `primaryErrors: 0`
   - Set `secondaryErrors: 0`
5. Save and execute workflow

Alternatively, wait until midnight UTC for automatic daily reset.

## Troubleshooting

### Issue: Both accounts exhausted message

**Cause**: Both accounts hit 50 emails/day or 3 errors  
**Solution**: Wait for midnight UTC reset, or manually reset state  
**Prevention**: Increase `dailyLimit` in workflow to spread emails across more executions

### Issue: Account not switching despite errors

**Cause**: Error threshold not reached (default: 3 consecutive errors)  
**Solution**: Check `errorThreshold` in User Config, reduce if needed  
**Check**: View workflow execution logs to see error counts

### Issue: Telegram notification not received

**Cause**: Incorrect `chatId` or Telegram credential  
**Solution**: 
1. Verify Telegram bot token in credentials
2. Send `/start` to your bot to get chat ID
3. Update `chatId` in notification node

### Issue: Emails sent from wrong account

**Cause**: Credential IDs not matching configuration  
**Solution**:
1. Check `primaryGmailCredentialId` in User Config
2. Verify credential IDs in Gmail send nodes
3. Ensure credentials are authenticated and not expired

### Issue: Daily reset not happening

**Cause**: Workflow not executing at midnight, or timezone mismatch  
**Solution**:
1. Daily reset happens on first execution of the day (9 AM trigger)
2. Uses UTC date comparison
3. Manual reset via static data if needed

## Gmail Rate Limits (Free Tier)

Understanding Gmail's actual limits:

| Limit Type | Gmail Free Tier | Workflow Default | Notes |
|------------|-----------------|------------------|-------|
| Daily emails | 500/day | 50/account | Conservative limit for safety |
| Per-minute | ~100/min | No limit set | n8n rate limiting (3s delay) provides throttling |
| Recipient limit | 500/day total | N/A | Includes To, CC, BCC combined |

**Why 50 per account?**
- Staying well below limits reduces spam detection risk
- Allows 100 total emails/day with dual accounts
- Conservative approach for cold outreach
- Can be increased in User Config if needed

## Best Practices

1. **Monitor Daily Counts**: Check digest emails to see account usage
2. **Adjust Limits**: Tune `maxEmailsPerAccount` based on your needs (max recommended: 100)
3. **Error Investigation**: If errors occur, check Gmail account health and credential validity
4. **Credential Rotation**: Refresh OAuth tokens periodically to avoid expiration
5. **Telegram Alerts**: Keep Telegram notifications enabled for real-time failover awareness
6. **Testing**: Test failover by manually setting `primaryDailyCount: 50` and executing workflow

## Advanced Configuration

### Changing Error Threshold

In User Config, adjust `errorThreshold`:

```javascript
errorThreshold: 3  // Switch after 3 consecutive errors (default)
errorThreshold: 5  // More tolerant, switch after 5 errors
errorThreshold: 1  // Immediate switch on first error
```

### Increasing Daily Limits

```javascript
maxEmailsPerAccount: 50   // Conservative (default)
maxEmailsPerAccount: 100  // Moderate (200 total/day)
maxEmailsPerAccount: 200  // Aggressive (400 total/day, watch for spam flags)
```

⚠️ **Warning**: Setting too high may trigger Gmail spam detection or rate limiting.

### Adding Third Email Account

To add a third account, modify:

1. Add tertiary email fields to User Config
2. Clone `Send Email via Gmail Secondary` node
3. Update `Select Gmail Credential` switch logic
4. Add tertiary counter tracking in state management

## Support

For issues or questions:
1. Check workflow execution logs in n8n
2. Verify credentials are valid and authenticated
3. Review Telegram notifications for failover events
4. Check Google Sheets for job processing status

## Related Documentation

- [ENHANCED-WORKFLOW-GUIDE.md](./ENHANCED-WORKFLOW-GUIDE.md) - Complete workflow documentation
- [SETUP-INSTRUCTIONS.md](./SETUP-INSTRUCTIONS.md) - Initial n8n setup
- [FEAT-001-COMPLETION-SUMMARY.md](./FEAT-001-COMPLETION-SUMMARY.md) - Resume intelligence feature

---

**Last Updated**: 2024-01-20  
**Feature**: FEAT-002 - Dual Email Failover System  
**Workflow Version**: Enhanced Master with 62 nodes
