# Email Setup Guide - Gmail OAuth for Dual Accounts

**Complete guide to setting up two Gmail accounts with OAuth for the n8n Job Automation workflow**

---

## Overview

### What is OAuth?

**OAuth** (Open Authorization) is a secure way to give n8n permission to send emails through your Gmail account **without sharing your password**. Think of it like giving someone a key to one room in your house, not the master key to everything.

**Why OAuth instead of password?**
- **More secure**: n8n never sees your Gmail password
- **Granular permissions**: You control exactly what n8n can do (only send emails, not read inbox)
- **Revocable**: You can remove access anytime from your Google account settings
- **Reliable**: No 2FA issues or "less secure app" warnings

---

### Why Two Gmail Accounts?

Gmail's free tier has email sending limits. Using two accounts provides:

**Benefits:**
- **Higher daily capacity**: 100 emails/day instead of 50
- **Automatic failover**: If one account hits its limit, workflow switches to the other
- **Error resilience**: If one account gets temporary errors, the other takes over
- **Zero downtime**: Emails keep sending even if one account is blocked

**How it works:**
1. Workflow starts with primary account
2. Sends up to 50 emails/day from primary
3. When limit hit or errors occur: automatically switches to secondary
4. Sends up to 50 more from secondary
5. At midnight UTC: resets and goes back to primary

**Daily capacity comparison:**

| Setup | Emails/Day | Annual Capacity |
|-------|------------|-----------------|
| Single account | 50 | 18,250 |
| Dual accounts | 100 | 36,500 |

**Note:** Gmail's official limit is 500/day, but we use 50/account as a conservative safety buffer to avoid spam detection.

---

## Prerequisites

Before starting, you need:

1. **Two Gmail accounts**:
   - Primary: Your main Gmail (e.g., `you@gmail.com`)
   - Secondary: A second Gmail (create free at [gmail.com](https://gmail.com))

2. **Google Cloud project**:
   - One project can handle both accounts
   - You'll create OAuth credentials once, use for both

3. **n8n instance**:
   - n8n Cloud or self-hosted
   - Admin access to add credentials

---

## Part 1: Google Cloud Console Setup

### 1.1 Create Google Cloud Project

**Steps:**

1. Go to: [console.cloud.google.com](https://console.cloud.google.com)

2. Sign in with your Google account (use your primary Gmail)

3. Click **"Select a project"** dropdown at the top

4. Click **"New Project"** button

5. Enter project details:
   - **Project name**: `n8n-job-automation`
   - **Organization**: Leave blank (not required)
   - **Location**: No organization

6. Click **"Create"**

7. Wait 10-15 seconds for project creation

**What you created:** A container for your OAuth credentials

---

### 1.2 Enable Gmail API

**Why?** Your project needs explicit permission to use Gmail's sending functionality.

**Steps:**

1. In Google Cloud Console, open the **hamburger menu** (☰ top-left)

2. Navigate to: **"APIs & Services"** → **"Library"**

3. In the search box, type: `Gmail API`

4. Click on: **"Gmail API"** (official Google API with Gmail logo)

5. Click the blue **"Enable"** button

6. Wait for activation (5-10 seconds)

7. You'll see a green checkmark and "API enabled" confirmation

**What this does:** Allows your OAuth app to send emails via Gmail

---

### 1.3 Configure OAuth Consent Screen

**What is this?** This is the authorization popup that appears when you connect n8n to Gmail. You're customizing what users see.

**Steps:**

1. In the left sidebar, go to: **"APIs & Services"** → **"OAuth consent screen"**

2. Select user type: **"External"**
   - **Why External?** "Internal" only works for Google Workspace organizations. Personal Gmail requires External.

3. Click **"Create"** button

4. Fill in the App information form:

   **App information:**
   - **App name**: `n8n Job Automation`
   - **User support email**: Select your email from dropdown
   - **App logo**: (Optional) Leave blank

   **App domain (optional):**
   - **Application home page**: Leave blank
   - **Application privacy policy link**: Leave blank
   - **Application terms of service link**: Leave blank

   **Authorized domains:**
   - Leave blank (not required)

   **Developer contact information:**
   - **Email addresses**: Enter your email

5. Click **"Save and Continue"** (bottom of page)

6. **Scopes screen**:
   - Click **"Add or Remove Scopes"** button
   - Search for: `gmail.send`
   - Check the box for: **"Gmail API .../auth/gmail.send"** (Send email on your behalf)
   - Click **"Update"**
   - Click **"Save and Continue"**

7. **Test users screen**:
   - Click **"+ Add Users"** button
   - Enter your PRIMARY Gmail address
   - Enter your SECONDARY Gmail address
   - Click **"Add"**
   - Click **"Save and Continue"**

   **Why add test users?** Your app is in "Testing" mode (not published), so only listed emails can authorize it.

8. **Summary screen**:
   - Review your settings
   - Click **"Back to Dashboard"**

**What you configured:** The authorization screen with proper scopes for email sending

---

## Part 2: Create OAuth Credentials

### 2.1 Create OAuth Client ID

**Steps:**

1. In Google Cloud Console sidebar, go to: **"APIs & Services"** → **"Credentials"**

2. Click **"+ Create Credentials"** button (top of page)

3. Select: **"OAuth client ID"**

4. **Application type**: Select **"Web application"**

5. Fill in the form:

   **Name**: `n8n Web Client`

   **Authorized JavaScript origins**: 
   - Leave empty (not needed)

   **Authorized redirect URIs**:
   - Click **"+ Add URI"**
   - Enter your n8n callback URL:
     - **For n8n Cloud**: `https://app.n8n.cloud/rest/oauth2-credential/callback`
     - **For self-hosted**: `https://YOUR_N8N_DOMAIN/rest/oauth2-credential/callback`
       (Replace `YOUR_N8N_DOMAIN` with your actual URL, e.g., `n8n.mycompany.com`)

6. Click **"Create"** button

7. A popup appears with your credentials:
   - **Client ID**: Looks like `123456789-abcdefg.apps.googleusercontent.com`
   - **Client secret**: Looks like `GOCSPX-AbC123DeF456`

8. **IMPORTANT**: Copy both values immediately:
   - Click **"Download JSON"** to save (optional backup)
   - OR copy both to a notepad/password manager

9. Click **"OK"** to close the popup

**What you created:**
- OAuth Client ID
- OAuth Client Secret

**Save these** - you'll use them twice (once for each Gmail account in n8n)

---

### 2.2 Verify Redirect URI (Important)

**Why this matters:** The most common OAuth error is redirect URI mismatch. Let's verify it's correct.

**Check your n8n URL:**

1. Open your n8n instance in a browser

2. Look at the address bar - your n8n URL should be:
   - n8n Cloud: `https://app.n8n.cloud`
   - Self-hosted example: `https://n8n.example.com`

3. The redirect URI should be: `YOUR_N8N_URL/rest/oauth2-credential/callback`

4. Go back to Google Cloud Console → Credentials → Click your OAuth client

5. Verify "Authorized redirect URIs" exactly matches: `https://YOUR_N8N_URL/rest/oauth2-credential/callback`

6. If incorrect: Edit, fix, and save

**Common mistakes:**
- ❌ `http://` instead of `https://`
- ❌ Missing `/rest/oauth2-credential/callback`
- ❌ Trailing slash: `...callback/`
- ❌ Wrong domain

---

## Part 3: Add Primary Gmail to n8n

Now you'll create the first Gmail OAuth2 credential in n8n for your primary account.

### 3.1 Open n8n Credentials

**Steps:**

1. Log in to your n8n instance

2. Click **"Credentials"** in the left sidebar (key icon 🔑)

3. Click **"Add Credential"** button (top-right)

---

### 3.2 Create Primary Gmail Credential

**Steps:**

1. In the search box, type: `gmail oauth2`

2. Click on: **"Gmail OAuth2 API"**

3. A credential form appears with these fields:

   **Display name**:
   - Enter: `Gmail Primary OAuth2`
   - (This is just for your reference in n8n)

   **Authentication**:
   - Select: **"OAuth2"**

   **Client ID**:
   - Paste the Client ID from Part 2.1
   - Should look like: `123456789-abc.apps.googleusercontent.com`

   **Client Secret**:
   - Paste the Client Secret from Part 2.1
   - Should look like: `GOCSPX-AbC123`

4. Click the **"Connect my account"** button (or "Sign in with Google")

5. A Google authorization popup will appear:
   - **IMPORTANT**: Select your **PRIMARY** Gmail account
   - If you're signed into multiple Google accounts, click the correct one
   - If not signed in, enter credentials for your PRIMARY Gmail

6. Google will show the consent screen:
   - App name: "n8n Job Automation"
   - Permissions: "Send email on your behalf"
   - Click **"Continue"** or **"Allow"**

7. If you see "This app isn't verified":
   - Click **"Advanced"**
   - Click **"Go to n8n Job Automation (unsafe)"**
   - This is safe - it's YOUR app, not verified because it's in testing mode

8. After authorization, you'll return to n8n

9. The credential form will show: ✅ **"Connected"**

10. Click **"Save"** button

---

### 3.3 Get Primary Credential ID

**Steps:**

1. After saving, you'll see the credential in your list

2. Click on the credential name: **"Gmail Primary OAuth2"**

3. Look at the browser address bar URL:
   ```
   https://app.n8n.cloud/credentials/abc-123-def-456-ghi-789
   ```

4. Copy the credential ID: `abc-123-def-456-ghi-789` (everything after `/credentials/`)

5. **Save this ID** - you'll need it in Part 5

**Alternative method:**
- Some n8n versions show the ID directly in the credentials list
- Look for "ID" column or hover tooltip

---

## Part 4: Add Secondary Gmail to n8n

Now repeat the process for your second Gmail account.

### 4.1 Create Secondary Gmail Credential

**Steps:**

1. In n8n Credentials page, click **"Add Credential"** again

2. Search for: `gmail oauth2`

3. Click: **"Gmail OAuth2 API"**

4. Fill in the form:

   **Display name**: `Gmail Secondary OAuth2`

   **Client ID**: Same as primary (from Part 2.1)

   **Client Secret**: Same as primary (from Part 2.1)

   **Note:** You use the SAME OAuth credentials for both accounts. The difference is which Google account you authorize in the next step.

5. Click **"Connect my account"**

6. In the Google popup:
   - **CRITICAL**: Select your **SECONDARY** Gmail account
   - If you see your primary account: Click **"Use another account"**
   - Sign in with your secondary Gmail

7. Grant permissions (same as primary)

8. Return to n8n, see ✅ **"Connected"**

9. Click **"Save"**

---

### 4.2 Get Secondary Credential ID

**Steps:**

1. Click on the credential: **"Gmail Secondary OAuth2"**

2. Copy the credential ID from the URL

3. **Save this ID** separately from primary

---

### 4.3 Verify Both Credentials

**Checklist:**

- [ ] Primary Gmail credential saved with name "Gmail Primary OAuth2"
- [ ] Secondary Gmail credential saved with name "Gmail Secondary OAuth2"
- [ ] Both show green ✅ "Connected" status
- [ ] You have BOTH credential IDs saved
- [ ] Credential IDs are different (each credential gets unique ID)

---

## Part 5: Configure Workflow

### 5.1 Update User Config Node

**Steps:**

1. Open your n8n workflow: **"Job Automation System"**

2. Find the node: **"User Config (Master Profile)"**

3. Double-click to open

4. Scroll to the **Dual Email Configuration** section:

```javascript
// Dual Email Configuration
primaryEmail: 'your-primary@gmail.com',                    // Your first Gmail address
secondaryEmail: 'your-secondary@gmail.com',                // Your second Gmail address
primaryGmailCredentialId: 'YOUR_PRIMARY_GMAIL_CREDENTIAL_ID',    // From Part 3.3
secondaryGmailCredentialId: 'YOUR_SECONDARY_GMAIL_CREDENTIAL_ID', // From Part 4.2
maxEmailsPerAccount: 50,                                   // Daily limit per account (keep at 50)
errorThreshold: 3                                          // Switch accounts after 3 consecutive errors
```

5. Replace the placeholders:
   - `primaryEmail`: Enter your primary Gmail address
   - `secondaryEmail`: Enter your secondary Gmail address
   - `primaryGmailCredentialId`: Paste the credential ID from Part 3.3
   - `secondaryGmailCredentialId`: Paste the credential ID from Part 4.2

6. Click **"Save"**

---

### 5.2 Update Gmail Send Nodes

Now you'll assign the credentials to the actual email-sending nodes.

**Primary Gmail Node:**

1. Find the node: **"Send Email via Gmail Primary"**

2. Double-click to open

3. In the **"Credentials"** section:
   - Click the dropdown next to **"Gmail OAuth2 API"**
   - Select: **"Gmail Primary OAuth2"**

4. Click **"Save"**

**Secondary Gmail Node:**

5. Find the node: **"Send Email via Gmail Secondary"**

6. Double-click to open

7. In the **"Credentials"** section:
   - Click the dropdown
   - Select: **"Gmail Secondary OAuth2"**

8. Click **"Save"**

---

### 5.3 Update Telegram Notification Node (Optional)

For failover notifications:

1. Find the node: **"Email Account Switch Notification"**

2. Double-click to open

3. Update `chatId` parameter:
   - Replace `YOUR_TELEGRAM_CHAT_ID` with your actual chat ID
   - (From Telegram setup in main guide)

4. Ensure Telegram credential is selected

5. Click **"Save"**

---

## Part 6: Testing

### Test 1: Primary Account Sending

**Setup:**

1. In your Google Sheet, manually add a test job (row 2):
   - **Recruiter Email**: YOUR_OWN_EMAIL@gmail.com (use your personal email)
   - **Recruiter Name**: Test Recruiter
   - **Job Title**: Test Engineer
   - **Company**: TestCorp
   - **Status**: New

**Execute:**

2. In n8n workflow editor, click: **"Schedule Trigger: Email Outreach (9 AM)"**

3. Click **"Execute Workflow"** button

4. Wait 15-20 seconds

**Verify:**

5. Check your email inbox:
   - ✅ Email received
   - ✅ Sender is your PRIMARY Gmail address
   - ✅ Subject includes "Test Engineer" and "TestCorp"

6. Check Google Sheet:
   - ✅ Status changed to "Email Sent"

**If it fails:**
- Check primary credential is connected (green checkmark)
- Verify credential ID matches in User Config
- Check execution logs for error details

---

### Test 2: Secondary Account Sending

**Setup:**

1. Manually modify workflow static data to simulate primary exhaustion:
   - In workflow editor, go to: **Workflow** → **Settings** → **Static Data**
   - Find `emailAccountState` object
   - Set: `primaryDailyCount: 50` (simulating limit hit)
   - Save

2. Add another test job in Google Sheet (row 3):
   - **Recruiter Email**: YOUR_EMAIL@example.com
   - **Status**: New

**Execute:**

3. Execute the "Schedule Trigger: Email Outreach" workflow again

**Verify:**

4. Check email:
   - ✅ Email received
   - ✅ Sender is your SECONDARY Gmail address (different from Test 1)

5. Check Telegram:
   - ✅ Notification received: "Email Account Switched"
   - ✅ Message shows reason: "Daily limit reached"

6. Check execution logs:
   - Node "Select Gmail Credential" output should be `1` (secondary)

**Reset:**

7. Reset static data:
   - Set `primaryDailyCount: 0`
   - Set `currentActive: 'primary'`
   - Save

---

### Test 3: Error Handling

**Simulate email error:**

1. In Google Sheet, add test job with invalid email:
   - **Recruiter Email**: `invalid-email-address`
   - **Status**: New

2. Execute workflow

**Verify:**

3. Workflow should:
   - ✅ Attempt to send
   - ✅ Catch error gracefully
   - ✅ Increment `primaryErrors` counter
   - ✅ Continue (not crash)

4. After 3 consecutive errors:
   - ✅ Switch to secondary account
   - ✅ Send Telegram notification

---

## Part 7: Monitoring

### View Account Status

**Option 1: Via Workflow Static Data**

1. In workflow editor: **Workflow** → **Settings** → **Static Data**

2. Find `emailAccountState` object:
```javascript
{
  primaryEmail: 'you@gmail.com',
  secondaryEmail: 'you2@gmail.com',
  currentActive: 'primary',        // Which account is active
  primaryDailyCount: 5,            // Emails sent today from primary
  secondaryDailyCount: 0,          // Emails sent today from secondary
  lastResetDate: '2024-01-20',     // Last midnight reset
  primaryErrors: 0,                // Consecutive errors for primary
  secondaryErrors: 0,              // Consecutive errors for secondary
  lastSwitchDate: '2024-01-20T09:15:00.000Z',
  lastSwitchReason: 'Daily limit reached'
}
```

**Option 2: Via Telegram**

1. Message your bot: `/stats`

2. Response includes:
```
Email Account Status:
📧 Primary (you@gmail.com): 5 sent today
📧 Secondary (you2@gmail.com): 0 sent today
✅ Active Account: primary
```

**Option 3: Via Email Digest**

Daily digest email includes account status at the bottom.

---

### Failover Notifications

When automatic switch occurs, you'll receive Telegram notification:

```
⚠️ Email Account Switched

Reason: Daily limit reached

Previous Account: Primary (you@gmail.com)
New Active Account: Secondary (you2@gmail.com)

Status:
📧 Primary: 50 sent today, 0 errors
📧 Secondary: 0 sent today, 0 errors

Time: 2024-01-20T09:15:00.000Z
```

---

## Troubleshooting

### Issue: OAuth authorization failed

**Error message:** "Error 400: redirect_uri_mismatch"

**Cause:** Redirect URI in Google Cloud doesn't match n8n URL

**Solution:**
1. Check your n8n URL in browser address bar
2. Go to Google Cloud Console → Credentials → OAuth client
3. Edit "Authorized redirect URIs"
4. Must exactly match: `https://YOUR_N8N_URL/rest/oauth2-credential/callback`
5. Save and try authorization again

---

### Issue: Emails going to spam

**Symptom:** Sent emails land in recipient spam folders

**Causes:**
- Sending too many emails too quickly (cold start)
- New Gmail account without sending history
- Email content triggers spam filters

**Solutions:**
1. **Reduce daily limit**:
   - Lower `maxEmailsPerAccount` to 30 in User Config
   - Gradually increase over 2-3 weeks

2. **Warm up accounts**:
   - Week 1: 10 emails/day per account
   - Week 2: 25 emails/day per account
   - Week 3: 40 emails/day per account
   - Week 4+: 50 emails/day per account

3. **Improve email content**:
   - Personalize more (use job-specific details)
   - Avoid spam trigger words ("make money", "guarantee", "click here")
   - Include unsubscribe option
   - Add your real contact information

4. **Authenticate your domain** (advanced):
   - Set up SPF, DKIM, and DMARC records
   - Requires custom domain (not @gmail.com)

---

### Issue: Primary account not switching

**Symptom:** Workflow keeps using primary even after hitting limit

**Cause:** Error threshold not reached, or static data not updating

**Solution:**
1. Check `errorThreshold` in User Config (default: 3)
2. Verify "Update Email State" node is executing
3. Check workflow static data for current counts
4. Manually reset if stuck:
   - Workflow Settings → Static Data
   - Set `currentActive: 'secondary'`
   - Or set `primaryDailyCount: 50` to force switch

---

### Issue: Both accounts exhausted

**Symptom:** "Both accounts exhausted, skipping email send" in logs

**Cause:** Both accounts hit 50 emails/day

**Solutions:**
1. **Wait for midnight UTC reset** (automatic)
2. **Manually reset counts**:
   - Static Data → Set `primaryDailyCount: 0` and `secondaryDailyCount: 0`
3. **Add third account** (advanced):
   - Create another Gmail credential
   - Modify workflow logic to include tertiary account
4. **Reduce emails per execution**:
   - Lower `dailyLimit` in User Config (e.g., 5 instead of 10)
   - Spread load throughout the day

---

### Issue: Daily reset not happening

**Symptom:** Counts don't reset at midnight, workflow still uses secondary

**Cause:** "Daily Reset Check" node not executing, or timezone mismatch

**Solution:**
1. Workflow runs daily reset on FIRST EXECUTION of the day
2. Ensure "Schedule Trigger: Email Outreach" runs AFTER midnight UTC
3. Check "Daily Reset Check" node execution logs
4. Manual reset:
   - Static Data → Set `lastResetDate` to yesterday's date
   - Execute workflow → should trigger reset

---

### Issue: Credentials expired

**Symptom:** "Invalid credentials" error after weeks/months

**Cause:** OAuth refresh token expired (rare, but possible)

**Solution:**
1. Go to n8n Credentials page
2. Click the expired credential
3. Click **"Reconnect"** or **"Connect my account"** again
4. Re-authorize with Google
5. Save

---

### Issue: Wrong account sending

**Symptom:** Secondary account sending when primary should be active

**Cause:** Credential IDs swapped in configuration

**Solution:**
1. Verify User Config:
   - `primaryGmailCredentialId` should match "Gmail Primary OAuth2" credential
   - `secondaryGmailCredentialId` should match "Gmail Secondary OAuth2" credential
2. Check node assignments:
   - "Send Email via Gmail Primary" uses primary credential
   - "Send Email via Gmail Secondary" uses secondary credential
3. Test by checking sender address in received emails

---

## Advanced Configuration

### Changing Daily Limits

**Increase per-account limit:**

In User Config node:
```javascript
maxEmailsPerAccount: 100,  // Increase from 50 to 100
```

**Warning:** Higher limits increase spam risk. Gmail's hard limit is 500/day, but staying under 100/account is recommended.

---

### Adjusting Error Threshold

**More tolerant (switch less often):**

```javascript
errorThreshold: 5,  // Switch after 5 errors instead of 3
```

**Less tolerant (switch immediately):**

```javascript
errorThreshold: 1,  // Switch after first error
```

---

### Adding Third Email Account

To add a third account:

1. Create another Gmail OAuth2 credential in n8n (same process as primary/secondary)

2. Add to User Config:
```javascript
tertiaryEmail: 'your-third@gmail.com',
tertiaryGmailCredentialId: 'YOUR_THIRD_CRED_ID',
```

3. Clone "Send Email via Gmail Secondary" node

4. Rename to: "Send Email via Gmail Tertiary"

5. Update "Select Gmail Credential" switch node:
   - Add output `2` for tertiary
   - Update logic to check tertiary availability

6. Update "Update Email State" node to track tertiary counts

---

## Gmail Rate Limits Reference

### Free Gmail Account Limits

| Limit Type | Value | Notes |
|------------|-------|-------|
| Daily sending limit | 500 emails/day | Hard limit enforced by Gmail |
| Recommended safe limit | 50-100/day | Avoid spam detection |
| New account warm-up | Start with 10/day | Gradually increase over 2-3 weeks |
| Per-minute rate | ~100/min | Not enforced in workflow (3s delay between sends) |
| Recipient limit | 500 total/day | Includes To, CC, BCC combined |

### Workflow Defaults

| Setting | Value | Configurable In |
|---------|-------|-----------------|
| Primary account limit | 50/day | User Config: `maxEmailsPerAccount` |
| Secondary account limit | 50/day | User Config: `maxEmailsPerAccount` |
| Total daily capacity | 100/day | Sum of both accounts |
| Error threshold | 3 consecutive errors | User Config: `errorThreshold` |
| Reset time | Midnight UTC | Automatic (uses `lastResetDate`) |

---

## Best Practices

1. **Start conservative**: Use 50/account limit initially, monitor spam rates

2. **Warm up new accounts**: Gradually increase volume over 2-3 weeks

3. **Monitor failover**: Check Telegram notifications for unexpected switches

4. **Quality over quantity**: Better to send 10 high-quality emails than 50 generic ones

5. **Rotate accounts**: Both accounts get regular use (good for sender reputation)

6. **Check spam folders**: Periodically verify your emails aren't landing in spam

7. **Refresh credentials**: Re-authorize OAuth every 6-12 months (proactive)

8. **Backup credential IDs**: Save them in password manager for easy recovery

---

## Security and Privacy

### What n8n Can Access

**With Gmail OAuth, n8n can:**
- ✅ Send emails on your behalf
- ✅ See sent email metadata (subject, recipient)

**n8n CANNOT:**
- ❌ Read your inbox
- ❌ Delete emails
- ❌ Access contacts
- ❌ Change account settings
- ❌ Access other Google services (unless separately authorized)

### Revoking Access

**To remove n8n's access:**

1. Go to: [myaccount.google.com/permissions](https://myaccount.google.com/permissions)

2. Find: "n8n Job Automation"

3. Click **"Remove Access"**

4. Confirm

**Note:** This will break the workflow's email sending until you re-authorize.

---

## Related Documentation

- **COMPLETE-SETUP-GUIDE.md**: Full workflow setup guide for beginners
- **DUAL-EMAIL-SETUP-GUIDE.md**: Technical deep-dive into failover system
- **ACCOUNTS-CHECKLIST.json**: Complete list of required accounts and credentials
- **ACCOUNTS-CREDENTIALS-TEMPLATE.txt**: Fill-in-the-blank tracking template

---

## Support

If you encounter issues:

1. Check **Execution Logs** in n8n for detailed error messages
2. Review this guide's **Troubleshooting** section
3. Verify all credentials show green ✅ "Connected" status
4. Test with your own email address first

**External resources:**
- n8n Community: [community.n8n.io](https://community.n8n.io)
- Gmail API Docs: [developers.google.com/gmail/api](https://developers.google.com/gmail/api)
- OAuth 2.0 Guide: [oauth.net/2](https://oauth.net/2/)

---

**Last Updated**: 2024-01-20  
**Feature**: FEAT-003 - Complete Documentation  
**Workflow Version**: Enhanced Master (62 nodes)  
**Related Feature**: FEAT-002 - Dual Email Failover System
