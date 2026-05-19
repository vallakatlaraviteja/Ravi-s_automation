# MASTER Job Automation System - Setup Instructions

Complete step-by-step guide to deploy and configure your automated job search workflow.

---

## Prerequisites

Before you begin, ensure you have the following:

- **n8n Instance**: Either self-hosted (Docker, npm) or n8n Cloud account ([n8n.io](https://n8n.io))
- **Google Account**: For Google Sheets OAuth2 and Gmail OAuth2 integration
- **Telegram Account**: To create a bot for interactive job assistant
- **Groq Account**: For AI-powered job scoring and email generation (free tier)
- **Adzuna Developer Account**: For job search API access (free 250 requests/day)

---

## Step 1: Import Workflow

### 1.1 Download the Workflow File

Ensure you have the `MASTER-job-automation-workflow.json` file saved locally.

### 1.2 Import into n8n

1. Open your n8n instance in your web browser
2. Click on **"Workflows"** in the left sidebar
3. Click the **"Import from File"** button (or use the menu: **Workflows → Import from File**)
4. Select the `MASTER-job-automation-workflow.json` file
5. The workflow will open in the editor with all 44 nodes visible

> **Note:** The workflow will show credential warnings initially - this is expected. You'll configure these in the next step.

---

## Step 2: Configure Credentials

You need to set up 5 different credentials for the workflow to function. Follow each section carefully.

### 2.1 Groq API (AI Scoring & Email Generation)

**Sign up and get API key:**

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account (GitHub or Google sign-in available)
3. Navigate to **API Keys** section in the dashboard
4. Click **"Create API Key"**
5. Copy the generated API key (starts with `gsk_...`)

**Add to n8n:**

1. In n8n, click **"Credentials"** in the left sidebar
2. Click **"Add Credential"**
3. Search for **"Groq API"** and select it
4. Paste your API key in the **"API Key"** field
5. Click **"Save"**
6. Copy the credential ID from the URL (e.g., `groq-api-123`)

### 2.2 Google Sheets OAuth2

**Create OAuth app in Google Cloud Console:**

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable **Google Sheets API**:
   - Go to **"APIs & Services" → "Library"**
   - Search for "Google Sheets API"
   - Click **"Enable"**
4. Create OAuth credentials:
   - Go to **"APIs & Services" → "Credentials"**
   - Click **"Create Credentials" → "OAuth client ID"**
   - If prompted, configure the OAuth consent screen first (choose "External", add your email)
   - Select **"Web application"** as application type
   - Add authorized redirect URI: `https://your-n8n-instance.com/rest/oauth2-credential/callback`
     - For self-hosted: use your actual n8n URL
     - For n8n Cloud: use `https://app.n8n.cloud/rest/oauth2-credential/callback`
   - Click **"Create"**
   - Copy the **Client ID** and **Client Secret**

**Add to n8n:**

1. In n8n, go to **"Credentials"** → **"Add Credential"**
2. Search for **"Google Sheets OAuth2 API"** and select it
3. Paste your **Client ID** and **Client Secret**
4. Click **"Connect my account"** and authorize access in the popup
5. Click **"Save"**
6. Copy the credential ID for later use

### 2.3 Gmail OAuth2

**Reuse the same Google OAuth app:**

1. In Google Cloud Console (same project as above), enable **Gmail API**:
   - Go to **"APIs & Services" → "Library"**
   - Search for "Gmail API"
   - Click **"Enable"**
2. Use the same OAuth credentials (Client ID and Secret) from Step 2.2

**Add to n8n:**

1. In n8n, go to **"Credentials"** → **"Add Credential"**
2. Search for **"Gmail OAuth2 API"** and select it
3. Paste the same **Client ID** and **Client Secret** from Step 2.2
4. Click **"Connect my account"** and authorize Gmail access
5. Click **"Save"**
6. Copy the credential ID for later use

### 2.4 Telegram Bot

**Create bot with BotFather:**

1. Open Telegram app on your phone or desktop
2. Search for **@BotFather** (official Telegram bot creation tool)
3. Start a chat and send the command: `/newbot`
4. Follow the prompts:
   - Enter a **name** for your bot (e.g., "My Job Assistant")
   - Enter a **username** ending in "bot" (e.g., "my_job_assistant_bot")
5. BotFather will reply with your **HTTP API token** (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
6. Copy this token

**Get your Chat ID:**

1. Send a message to your new bot (any text, like "Hello")
2. Open this URL in your browser: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Replace `<YOUR_BOT_TOKEN>` with the token from BotFather
3. Look for `"chat":{"id":123456789}` in the JSON response
4. Copy the numeric chat ID

**Add to n8n:**

1. In n8n, go to **"Credentials"** → **"Add Credential"**
2. Search for **"Telegram API"** and select it
3. Paste your **Bot Token**
4. Click **"Save"**
5. Copy the credential ID for later use

### 2.5 Adzuna API

**Register and get API credentials:**

1. Go to [developer.adzuna.com](https://developer.adzuna.com)
2. Click **"Sign Up"** and create a free account
3. After email verification, log in to the developer dashboard
4. Click **"Create New Application"**
5. Fill in application details:
   - **Name**: "Job Search Automation"
   - **Description**: "Automated job discovery system"
6. Submit the form
7. You'll receive two credentials:
   - **Application ID** (numeric, e.g., `12345678`)
   - **Application Key** (alphanumeric string)
8. Copy both values

> **Note:** Adzuna API credentials are NOT stored as n8n credentials. You'll add these directly as HTTP query parameters in Step 4.

---

## Step 3: Create Google Sheet

### 3.1 Create New Spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Click **"Blank"** to create a new spreadsheet
3. Name it **"Job Automation Database"** (or any name you prefer)
4. Rename the first tab from "Sheet1" to **"Jobs"** (exact name required)

### 3.2 Set Up Column Headers

In the first row of the "Jobs" tab, add these **19 column headers** in this exact order:

| Column | Header Name |
|--------|-------------|
| A | Job ID |
| B | Job Title |
| C | Company |
| D | Location |
| E | Work Mode |
| F | Salary |
| G | Apply URL |
| H | Source |
| I | Score |
| J | Priority |
| K | Match Reason |
| L | Status |
| M | Posted Date |
| N | Fetched Date |
| O | Recruiter Email |
| P | Recruiter Name |
| Q | Application ID |
| R | Email Sent Date |
| S | Last Updated |

**Important:** 
- Column order matters - the workflow maps data by column position
- Use exact header names (case-sensitive)
- Leave row 2 onwards empty - the workflow will populate them automatically

### 3.3 Get Spreadsheet ID

1. Look at your browser's address bar - the URL looks like:
   ```
   https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit#gid=0
   ```
2. Copy the long string between `/d/` and `/edit` - this is your **Spreadsheet ID**
3. Example: `1A2B3C4D5E6F7G8H9I0J`
4. Save this ID - you'll need it in Step 4

---

## Step 4: Replace Placeholders

The workflow contains placeholder values that you must replace with your actual credentials and IDs.

### 4.1 Placeholder Table

| Placeholder | What to Replace It With | Where to Find It |
|-------------|-------------------------|------------------|
| `YOUR_GROQ_CREDENTIAL_ID` | Groq credential ID from n8n | Step 2.1 - copy from n8n Credentials page |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | Google Sheets credential ID | Step 2.2 - copy from n8n Credentials page |
| `YOUR_GMAIL_CREDENTIAL_ID` | Gmail credential ID | Step 2.3 - copy from n8n Credentials page |
| `YOUR_TELEGRAM_CREDENTIAL_ID` | Telegram credential ID | Step 2.4 - copy from n8n Credentials page |
| `YOUR_SPREADSHEET_ID` | Google Sheet ID | Step 3.3 - from your Google Sheets URL |
| `YOUR_TELEGRAM_CHAT_ID` | Your numeric Telegram chat ID | Step 2.4 - from Telegram API getUpdates |
| `YOUR_ADZUNA_APP_ID` | Adzuna Application ID | Step 2.5 - from Adzuna developer dashboard |
| `YOUR_ADZUNA_APP_KEY` | Adzuna Application Key | Step 2.5 - from Adzuna developer dashboard |

### 4.2 How to Replace in n8n

**Option A: Using n8n's Find & Replace**

1. In the workflow editor, press **Ctrl+F** (or **Cmd+F** on Mac)
2. Enter the placeholder text (e.g., `YOUR_GROQ_CREDENTIAL_ID`)
3. Click through each occurrence and update manually in the node settings

**Option B: Edit JSON Directly**

1. Click the **"Download"** button in n8n to export the workflow
2. Open the JSON file in a text editor
3. Use Find & Replace (Ctrl+H) to replace all placeholders
4. Save the file
5. Re-import into n8n

**Nodes that Need Credential ID Updates:**

- **Groq AI nodes** (3 nodes): Update `credentials.groqApi.id`
- **Google Sheets nodes** (3 nodes): Update `credentials.googleSheetsOAuth2.id`
- **Gmail nodes** (2 nodes): Update `credentials.gmailOAuth2.id`
- **Telegram nodes** (2 nodes): Update `credentials.telegramApi.id`

**Nodes that Need Other Placeholder Updates:**

- **"User Config (Master Profile)"** node: Update `sheetId`, `userEmail` (see Step 5)
- **"Fetch Adzuna API"** node: Update query parameters `app_id` and `app_key`
- **"Send Telegram Notification"** nodes: Update `chatId` parameter

---

## Step 5: Configure User Profile

The workflow uses a centralized configuration node that stores all your personal information and preferences.

### 5.1 Locate the User Config Node

1. In the workflow editor, find the node named **"User Config (Master Profile)"**
2. It's positioned near the top-left, connected to all three trigger branches
3. Double-click to open the node settings

### 5.2 Update Personal Information

Replace the example values in the JavaScript code with your actual information:

```javascript
{
  // Personal Details
  name: 'John Smith',                    // Your full name
  currentRole: 'Senior Backend Engineer', // Your current job title
  targetRole: 'Staff Engineer',           // Your desired next role
  experience: '5 years',                  // Years of experience
  location: 'Hyderabad, India',           // Your city and country
  
  // Skills & Expertise
  skills: [
    'Python', 'Node.js', 'AWS', 
    'Docker', 'Kubernetes', 'PostgreSQL'
  ],  // Your top 5-10 technical skills
  
  // Job Search Criteria
  targetRoles: [
    'Backend Engineer', 
    'Full Stack Engineer', 
    'DevOps Engineer'
  ],  // Job titles you're interested in
  keywords: 'python developer OR backend engineer OR nodejs',  // Search keywords for job APIs
  workMode: ['remote', 'hybrid'],         // Preferred work mode: 'remote', 'hybrid', 'onsite'
  minSalary: 80000,                       // Minimum annual salary (USD or local currency)
  country: 'in',                          // Two-letter country code for Adzuna (us, gb, in, au, ca, etc.)
  
  // URLs
  githubUrl: 'https://github.com/yourusername',
  linkedinUrl: 'https://linkedin.com/in/yourprofile',
  portfolioUrl: 'https://yourportfolio.com',
  resumeUrl: 'https://drive.google.com/file/d/YOUR_RESUME_ID/view',  // Make sure it's publicly accessible
  
  // System Settings
  userEmail: 'YOUR_EMAIL@example.com',    // Your email address (for CC on outreach emails)
  dailyLimit: 10,                         // Max number of outreach emails per day
  scoreThreshold: 30,                     // Minimum AI match score (0-100) to save jobs
  sheetId: 'YOUR_SPREADSHEET_ID'          // Your Google Sheet ID from Step 3.3
}
```

### 5.3 Configuration Tips

- **skills**: List your most relevant technical/domain skills that you want to highlight
- **keywords**: Use `OR` to combine multiple search terms (improves job discovery coverage)
- **workMode**: Include all modes you're open to - filters will be applied during AI scoring
- **country**: Use ISO 3166-1 alpha-2 codes (see [Adzuna API docs](https://developer.adzuna.com/docs/search))
- **minSalary**: Set realistic expectations - jobs below this won't be filtered out but will score lower
- **scoreThreshold**: Start with 30, adjust up if you get too many irrelevant jobs, down if too few
- **dailyLimit**: Keep at 10 or lower to avoid being flagged as spam by email providers

---

## Step 6: Test Workflow

Before activating the workflow, test each branch to ensure everything works correctly.

### 6.1 Test Job Discovery Branch

**Purpose:** Verify that jobs are fetched, scored, and saved to Google Sheets.

1. In the workflow editor, click on the **"Schedule Trigger: Job Discovery (8 AM)"** node
2. Click the **"Execute Node"** button (play icon)
3. Watch the execution flow through the nodes (they'll turn green as they complete)
4. Open your Google Sheet and verify:
   - ✅ New jobs are added (rows 2+)
   - ✅ All 19 columns are populated
   - ✅ Score values are between 0-100
   - ✅ Priority is set to "High", "Medium", or "Low"
   - ✅ Status is "New"
5. Check your Telegram for a summary notification
6. Check your email for a job discovery digest

**Expected Results:**
- 10-50 new jobs added to the sheet (depending on API results)
- Execution time: 30-90 seconds
- No error messages in n8n execution log

**Troubleshooting:**
- If no jobs appear: Check that your Google Sheet has the correct name ("Jobs") and column headers
- If API errors: Verify your Adzuna credentials in the "Fetch Adzuna API" node
- If Groq errors: Check your Groq API key and rate limits

### 6.2 Test Email Outreach Branch

**Purpose:** Verify that personalized emails are generated and sent to recruiters.

**Setup:**

1. In your Google Sheet, manually add a test row (row 2):
   - **Job Title**: "Senior Backend Engineer"
   - **Company**: "TestCorp"
   - **Recruiter Email**: `your-own-email@example.com` (use your own email for testing)
   - **Recruiter Name**: "Jane Doe"
   - **Status**: "New"
   - Fill in other required columns with dummy data

**Execute:**

1. In the workflow editor, click on the **"Schedule Trigger: Email Outreach (9 AM)"** node
2. Click **"Execute Node"**
3. Wait for the execution to complete (15-30 seconds)

**Verify:**

1. Check your email inbox for:
   - ✅ An email from your Gmail account
   - ✅ Subject line mentions the job title and company
   - ✅ Email body is personalized with your name and skills
   - ✅ Email includes your portfolio links at the bottom
2. Check your Google Sheet:
   - ✅ Row 2 Status changed to "Email Sent"
   - ✅ Application ID is populated (format: `EMAIL-<timestamp>-<random>`)
   - ✅ Email Sent Date is today's date
   - ✅ Last Updated is today's date

**Expected Results:**
- 1 email received in your inbox
- Sheet updated with email metadata
- No errors in n8n execution log

**Troubleshooting:**
- If no email received: Check Gmail OAuth credentials and ensure sender reputation is good
- If email content is poor: Adjust the Groq prompt in "Groq AI: Generate Personalized Email" node
- If rate limit errors: Check you haven't exceeded daily limits (10 emails/day default)

### 6.3 Test Telegram Assistant

**Purpose:** Verify interactive commands work correctly.

**Execute:**

1. Open Telegram and find your bot (search for the username you created)
2. Send the command: `/start`
   - Expected response: Welcome message with instructions
3. Send the command: `/help`
   - Expected response: List of available commands
4. Send the command: `/stats`
   - Expected response: Statistics from your Google Sheet (total jobs, by status, by priority)
5. Send a complex query: `"What remote backend jobs do I have?"`
   - Expected response: AI-generated summary based on your sheet data

**Verify:**

1. All commands return responses within 5-10 seconds
2. `/stats` shows accurate counts from your Google Sheet
3. Complex queries are answered intelligently by Groq AI

**Expected Results:**
- All 4 quick commands respond instantly
- Stats match your Google Sheet data
- Complex queries get intelligent responses

**Troubleshooting:**
- If bot doesn't respond: Check Telegram credential and webhook configuration
- If stats are wrong: Verify Google Sheets credential has read access
- If AI responses are poor: Adjust temperature or system prompt in Groq nodes

---

## Step 7: Activate Workflow

Once all tests pass, activate the workflow to run automatically.

### 7.1 Activate the Workflow

1. In the workflow editor (top-right corner), toggle the **"Active"** switch to ON
2. The workflow status will change to "Active"
3. All 3 triggers are now enabled:
   - **Job Discovery**: Runs daily at 8:00 AM (UTC)
   - **Email Outreach**: Runs daily at 9:00 AM (UTC)
   - **Telegram Assistant**: Always listening for messages

### 7.2 Adjust Trigger Schedules (Optional)

**To change execution times:**

1. Double-click on a Schedule Trigger node
2. Modify the **"Cron Expression"**:
   - `0 8 * * *` = 8:00 AM every day (UTC)
   - `0 9 * * *` = 9:00 AM every day (UTC)
   - `0 */6 * * *` = Every 6 hours
   - `0 8 * * 1-5` = 8:00 AM Monday-Friday only
3. Click **"Save"** and re-activate the workflow

> **Note:** All times are in UTC timezone. Adjust for your local timezone accordingly.

### 7.3 Monitor Executions

**View execution history:**

1. In n8n, go to **"Executions"** in the left sidebar
2. You'll see a list of all workflow runs with timestamps and status
3. Click on any execution to see detailed logs and data flow

**Set up alerts (optional):**

1. Go to **"Settings"** → **"Workflow Settings"**
2. Enable **"Error Workflow"** to get notified on failures
3. Configure email or webhook notifications

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Credential Errors

**Symptom:** "Credentials not found" or "Invalid credentials" errors

**Solutions:**
- Verify credential IDs are correct (check in n8n Credentials page)
- Ensure OAuth tokens haven't expired (re-authorize if needed)
- For Google OAuth: Make sure both Sheets API and Gmail API are enabled in Google Cloud Console
- For Telegram: Verify bot token is correct (test with `getMe` API endpoint)

#### 2. API Rate Limit Errors

**Symptom:** "Too many requests" or 429 status codes

**Solutions:**
- **Adzuna**: Free tier is limited to 250 requests/day. Reduce workflow frequency or upgrade plan.
- **Groq**: Free tier has rate limits. Add delays between API calls or reduce daily job processing volume.
- **Gmail**: Sending limit is ~500 emails/day for free accounts. Keep `dailyLimit` at 10 or lower.

#### 3. Google Sheet Permission Errors

**Symptom:** "Permission denied" or "Sheet not found" errors

**Solutions:**
- Ensure the Google account used for OAuth has edit access to the spreadsheet
- Verify the Sheet ID is correct (check URL)
- Confirm the tab name is exactly "Jobs" (case-sensitive)
- Try re-authorizing Google Sheets OAuth credential in n8n

#### 4. Telegram Webhook Not Responding

**Symptom:** Bot doesn't reply to messages

**Solutions:**
- Check if workflow is activated (toggle in top-right)
- Verify Telegram credential is correct
- Test bot token: `https://api.telegram.org/bot<TOKEN>/getMe` should return bot details
- Check n8n executions log for errors when you send a message
- For self-hosted n8n: Ensure your server is publicly accessible (Telegram needs to reach your webhook)

#### 5. Groq API Errors

**Symptom:** "Unauthorized" or "Model not found" errors

**Solutions:**
- Verify API key is correct (starts with `gsk_`)
- Check free tier limits haven't been exceeded
- Ensure model name is valid (default: `mixtral-8x7b-32768`)
- Try regenerating API key in Groq console

#### 6. No Jobs Found

**Symptom:** Job Discovery runs successfully but no jobs are saved

**Solutions:**
- Check if APIs are returning data (click "Execute Node" on individual API nodes)
- Verify `keywords` in User Config match real job postings (try broader terms)
- Lower `scoreThreshold` (try 20 instead of 30) to be less restrictive
- Check API responses in execution logs - some APIs may be temporarily down
- Verify duplicate filtering isn't too aggressive (check Sheet for existing jobs)

#### 7. Emails Not Sending

**Symptom:** Email outreach execution completes but no emails received

**Solutions:**
- Check Gmail sent folder to confirm emails were sent
- Verify Gmail OAuth credential has "Send email" permission
- Check spam folder (both yours and recipient's)
- Ensure `recruiterEmail` column in Sheet has valid email addresses
- Review Gmail's sending limits (500/day) - you may have hit the cap
- Check that `Status` filter is working (only "New" jobs with emails should be processed)

#### 8. Duplicate Jobs in Sheet

**Symptom:** Same job appears multiple times in Google Sheet

**Solutions:**
- Verify "Check for Duplicates" node is properly connected in the workflow
- Check if `jobId` generation is unique (should include source and job ID)
- Ensure Google Sheet read operation is working before append
- Review deduplication logic in the workflow (may need to adjust matching criteria)

---

## Next Steps

✅ **You're all set!** Your automated job search system is now running.

**What happens next:**

- Every day at 8 AM: New jobs are discovered, scored, and added to your Sheet
- Every day at 9 AM: Personalized emails are sent to recruiters for top jobs
- Anytime: Ask your Telegram bot for job stats, resume, or custom queries

**Recommended Actions:**

1. **Monitor first week**: Check executions daily to ensure everything runs smoothly
2. **Tune scoring**: Adjust `scoreThreshold` based on job quality (raise if too many low-quality jobs)
3. **Update profile**: Keep skills and preferences current in User Config node
4. **Add recruiters**: Manually research and add recruiter emails to high-priority jobs in Sheet
5. **Review emails**: Check sent emails periodically to ensure quality (adjust Groq prompts if needed)

**Maintenance:**

- **Weekly**: Review new jobs in Sheet, manually research top companies
- **Monthly**: Re-authorize OAuth credentials if they expire
- **Quarterly**: Update skills, target roles, and salary expectations

---

## Need Help?

If you encounter issues not covered in this guide:

1. Check n8n **Executions** log for detailed error messages
2. Review n8n community forum: [community.n8n.io](https://community.n8n.io)
3. Consult API documentation:
   - [n8n Docs](https://docs.n8n.io)
   - [Groq API Docs](https://console.groq.com/docs)
   - [Adzuna API Docs](https://developer.adzuna.com/docs)
   - [Telegram Bot API](https://core.telegram.org/bots/api)

Good luck with your job search! 🚀
