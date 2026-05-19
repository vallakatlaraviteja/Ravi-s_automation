# Complete Setup Guide - n8n Job Automation System

**For Absolute Beginners**

---

## Introduction

### What You're Building

This guide will help you set up a **fully automated job search system** that runs 24/7 without any manual effort. Here's what it does:

- **Finds jobs automatically**: Searches 3 job boards every morning at 8 AM
- **Scores each job**: Uses AI to rate how well each job matches your skills and preferences (0-100 score)
- **Sends personalized emails**: Automatically reaches out to recruiters with customized messages
- **Tracks everything**: Stores all jobs in a Google Sheet you can view anytime
- **Telegram assistant**: Answer questions about your jobs via chat ("Show me remote Python jobs")

### Time Estimate

**Total setup time: 45-60 minutes**

- Part 1 (Account Creation): 15 minutes
- Part 2 (Credential Setup): 15 minutes
- Part 3-4 (Import & Configure): 10 minutes
- Part 5-6 (Testing): 10 minutes
- Part 7 (Activate): 5 minutes

### What Makes This Different

- **100% Free**: No paid services required, ever
- **No coding needed**: Just copy-paste configuration values
- **Privacy-first**: Your data stays in YOUR Google Sheet, not in external databases
- **Beginner-friendly**: Every step explained with screenshots descriptions

---

## Prerequisites

Before starting, you need:

1. **n8n account** (free tier):
   - Cloud: [app.n8n.cloud](https://app.n8n.cloud) (easiest, recommended)
   - OR self-hosted: Docker/npm installation (advanced users)

2. **Google account** (Gmail):
   - For Google Sheets (job storage)
   - For Gmail OAuth (sending emails)

3. **Telegram account**:
   - Download Telegram app: [telegram.org/apps](https://telegram.org/apps)
   - Available on mobile, desktop, and web

4. **Computer with internet**:
   - Modern web browser (Chrome, Firefox, Safari, Edge)
   - Stable internet connection

**No credit card required for any service.**

---

## Part 1: Account Creation

In this part, you'll create free accounts for all the services the workflow needs. Follow each step carefully.

### 1.1 Create Groq Account (AI Service)

**What is Groq?** Groq provides AI models that analyze job descriptions and write emails. Think of it as the "brain" of your automation.

**Steps:**

1. Open your browser and go to: [console.groq.com](https://console.groq.com)

2. Click **"Sign In"** or **"Get Started"** button

3. Choose sign-in method:
   - **GitHub** (recommended if you have GitHub account)
   - **Google** (use your Gmail account)

4. Complete authentication in the popup window

5. You'll land on the Groq dashboard

6. In the left sidebar, click **"API Keys"**

7. Click the **"Create API Key"** button

8. Give it a name: `n8n-job-automation`

9. Click **"Create"**

10. **IMPORTANT**: A window will show your API key (starts with `gsk_...`)
    - Copy this key immediately
    - Store it somewhere safe (notepad, password manager)
    - You **cannot** see it again after closing this window

**What you get:** Groq API Key (format: `gsk_` followed by 48 random characters)

**Free tier limits:** 14,400 requests per day (way more than you need)

---

### 1.2 Create Google Cloud Project (for Sheets & Gmail)

**What is Google Cloud Console?** This is where you create OAuth credentials that let n8n access your Google Sheets and Gmail on your behalf. OAuth is a secure way to grant limited permissions without sharing your password.

**Steps:**

1. Go to: [console.cloud.google.com](https://console.cloud.google.com)

2. Sign in with your Google account (the same one you'll use for Sheets and Gmail)

3. At the top of the page, click **"Select a project"** dropdown

4. In the dialog, click **"New Project"** button (top-right)

5. Fill in project details:
   - **Project name**: `n8n-job-automation`
   - **Organization**: Leave blank
   - **Location**: Leave as default

6. Click **"Create"** button

7. Wait 10-20 seconds for project creation

8. You'll be redirected to the project dashboard

**What you get:** A Google Cloud project (container for your API credentials)

**Cost:** $0 - Google Cloud is free for this use case

---

### 1.3 Enable Google Sheets API

**Why?** Your Google account can do many things. You need to explicitly enable "reading and writing to Google Sheets" for your project.

**Steps:**

1. In Google Cloud Console, open the **hamburger menu** (three horizontal lines, top-left)

2. Navigate to: **"APIs & Services"** > **"Library"**

3. You'll see a search box with text "Search for APIs and Services"

4. Type: `google sheets api`

5. Click on the result: **"Google Sheets API"** (official Google API)

6. Click the blue **"Enable"** button

7. Wait 5 seconds for activation

8. You'll see a dashboard with a green checkmark: "API enabled"

**What this does:** Allows n8n to read/write your Google Sheets using OAuth

---

### 1.4 Enable Gmail API

**Why?** Similar to Sheets, you need to enable "sending emails via Gmail" for your project.

**Steps:**

1. Still in Google Cloud Console, click the **"Library"** link in the left sidebar

2. Search for: `gmail api`

3. Click on: **"Gmail API"** (official Google API)

4. Click **"Enable"** button

5. Wait for activation (5 seconds)

6. Green checkmark confirms API is enabled

**What this does:** Allows n8n to send emails through your Gmail account

---

### 1.5 Configure OAuth Consent Screen

**What is this?** This is the screen that appears when you authorize n8n to access your Google account. You're setting up the app name and permissions.

**Steps:**

1. In Google Cloud Console sidebar, go to: **"APIs & Services"** > **"OAuth consent screen"**

2. Select user type: **"External"**
   - **Why External?** "Internal" is only for Google Workspace organizations. External works for personal Gmail accounts.

3. Click **"Create"** button

4. Fill in required fields on the consent screen form:
   - **App name**: `n8n Job Automation`
   - **User support email**: Your email (dropdown, pre-selected)
   - **App logo**: Leave blank (optional)
   - **App domain**: Leave blank (optional)
   - **Developer contact email**: Your email

5. Click **"Save and Continue"** button (bottom of page)

6. On "Scopes" screen: Click **"Save and Continue"** (you'll add scopes automatically later)

7. On "Test users" screen: Click **"Add Users"** and enter your own email address
   - **Why?** Your app is in "Testing" mode, so only listed users can authorize it

8. Click **"Save and Continue"**

9. Review summary, then click **"Back to Dashboard"**

**What you get:** OAuth consent configuration (needed before creating credentials)

---

### 1.6 Create OAuth Credentials for Google

**What are OAuth credentials?** Think of it as a special key that n8n can use to access your Google account with limited permissions (only Sheets and Gmail, not your entire account).

**Steps:**

1. In Google Cloud Console sidebar, go to: **"APIs & Services"** > **"Credentials"**

2. Click **"+ Create Credentials"** button (top of page)

3. Select **"OAuth client ID"** from dropdown

4. You'll see an "Application type" dropdown:
   - Select: **"Web application"**

5. Fill in the form:
   - **Name**: `n8n Web Client`
   - **Authorized JavaScript origins**: Leave blank
   - **Authorized redirect URIs**: Click **"+ Add URI"** and enter:
     - For n8n Cloud: `https://app.n8n.cloud/rest/oauth2-credential/callback`
     - For self-hosted: `https://your-n8n-domain.com/rest/oauth2-credential/callback`
       (Replace `your-n8n-domain.com` with your actual n8n URL)

6. Click **"Create"** button

7. A dialog will appear with your credentials:
   - **Client ID**: Looks like `123456789-abc123def456.apps.googleusercontent.com`
   - **Client secret**: Looks like `GOCSPX-AbCdEf123456`
   - Click **"Download JSON"** button (or copy both values to notepad)

8. Click **"OK"** to close dialog

**What you get:**
- OAuth Client ID
- OAuth Client Secret

**SAVE THESE**: You'll need them in Part 2

---

### 1.7 Create Telegram Bot

**What is a Telegram bot?** It's like a virtual assistant you can message. Your bot will answer questions about jobs, provide statistics, and send notifications.

**Steps:**

1. Open Telegram app (mobile or desktop)

2. In the search bar, type: `@BotFather`

3. Click on the official **BotFather** account (verified with blue checkmark)

4. Click **"Start"** button at the bottom

5. Send the command: `/newbot`

6. BotFather will ask: "Alright, a new bot. How are we going to call it?"
   - Type a name for your bot (can be anything): `My Job Assistant`

7. BotFather will ask: "Now, let's choose a username for your bot"
   - Type a username ending in "bot": `my_job_assistant_bot`
   - Must be unique - if taken, try adding numbers: `my_job_assistant_2024_bot`

8. BotFather will reply with:
   - "Done! Congratulations on your new bot."
   - **HTTP API Token**: Looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - Copy this token immediately

9. Send a test message to your bot:
   - Click the link BotFather provides (or search for your bot's username)
   - Send any message like "Hello"

10. Get your Chat ID:
    - Open this URL in your browser: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
    - Replace `<YOUR_TOKEN>` with the token from step 8
    - You'll see JSON data
    - Find `"chat":{"id":123456789}`
    - Copy the numeric ID (your Chat ID)

**What you get:**
- Bot Token (format: numbers, colon, random letters/numbers)
- Chat ID (format: 9-10 digit number)

**SAVE THESE**: You'll need both in Part 2

---

### 1.8 Create Adzuna Developer Account

**What is Adzuna?** A job search API that aggregates job postings from multiple sources. It's one of three job sources your workflow uses.

**Steps:**

1. Go to: [developer.adzuna.com](https://developer.adzuna.com)

2. Click **"Sign Up"** or **"Register"** button

3. Fill in the registration form:
   - **Email**: Your email address
   - **Password**: Create a strong password
   - **Name**: Your full name

4. Check your email for verification link

5. Click the verification link

6. Log in to Adzuna developer portal

7. Click **"Create New Application"** button

8. Fill in application details:
   - **Application Name**: `n8n Job Automation`
   - **Description**: `Automated job discovery system for personal use`
   - **Website URL**: Leave blank or use your portfolio URL

9. Submit the form

10. You'll see your credentials on the dashboard:
    - **Application ID**: A numeric value like `12345678`
    - **Application Key**: An alphanumeric string like `abc123def456ghi789`

11. Copy both values

**What you get:**
- Adzuna App ID (numbers)
- Adzuna App Key (letters and numbers)

**Free tier limits:** 250 API calls per day (more than enough)

**SAVE THESE**: You'll need them in Part 4

---

### 1.9 Create Resume Public URL

**Why do you need this?** The workflow downloads your resume and uses AI to extract your skills, which helps score job matches more accurately. The resume URL must be publicly accessible (no login required).

You have three options. Choose ONE that works best for you:

#### Option A: Google Drive (Easiest)

**Steps:**

1. Upload your resume PDF to Google Drive

2. Right-click the file > **"Share"** > **"Change to anyone with the link"**

3. Set permissions: **"Anyone with the link"** > **"Viewer"**

4. Click **"Copy link"**

5. You'll get a URL like:
   ```
   https://drive.google.com/file/d/1AbCdEfGhIjKlMnOpQrStUvWxYz/view?usp=sharing
   ```

6. **Convert the URL format** (important):
   - Original: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
   - Change to: `https://drive.google.com/uc?export=download&id=FILE_ID`
   - Example result: `https://drive.google.com/uc?export=download&id=1AbCdEfGhIjKlMnOpQrStUvWxYz`

7. Test the URL in an incognito browser window - it should download your resume

**Final URL format:**
```
https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
```

#### Option B: GitHub (For developers)

**Steps:**

1. Create a public GitHub repository (or use existing one)

2. Upload your resume PDF to the repo

3. Navigate to the file on GitHub

4. Click the **"Raw"** button

5. Copy the URL from the address bar

**Final URL format:**
```
https://raw.githubusercontent.com/username/repo-name/main/resume.pdf
```

#### Option C: Dropbox

**Steps:**

1. Upload your resume to Dropbox

2. Right-click the file > **"Share"** > **"Create a link"**

3. Copy the generated link

4. **Modify the URL**:
   - Original: `https://www.dropbox.com/s/abc123def456/resume.pdf?dl=0`
   - Change `?dl=0` to `?dl=1` at the end
   - Result: `https://www.dropbox.com/s/abc123def456/resume.pdf?dl=1`

**Final URL format:**
```
https://www.dropbox.com/s/FILE_ID/resume.pdf?dl=1
```

**SAVE YOUR RESUME URL**: You'll need it in Part 5

---

## Part 2: Credential Setup in n8n

Now that you've created all accounts, you'll add these credentials to n8n. This is like giving n8n the keys to access these services on your behalf.

### 2.1 Log in to n8n

**Steps:**

1. Go to your n8n instance:
   - n8n Cloud: [app.n8n.cloud](https://app.n8n.cloud)
   - Self-hosted: Your n8n URL

2. Log in with your n8n account

3. You'll see the n8n dashboard (main screen)

---

### 2.2 Add Groq API Credential

**Steps:**

1. In n8n, click **"Credentials"** in the left sidebar (icon looks like a key)

2. Click the **"Add Credential"** button (top-right)

3. In the search box, type: `groq`

4. Click on: **"Groq API"**

5. A form will appear with one field: **"API Key"**

6. Paste your Groq API key (from Part 1.1)
   - Should start with `gsk_`

7. Click **"Save"** button

8. After saving, look at the browser address bar URL:
   - It will look like: `https://app.n8n.cloud/credentials/abc-123-def-456`
   - Copy the credential ID: `abc-123-def-456` (everything after `/credentials/`)
   - OR: The credential name will appear in the list - note it for later

**What you get:** Groq credential ID

**Write this down in your tracking template (we'll create one in Part 4)**

---

### 2.3 Setup Dual Gmail Accounts

**Why two Gmail accounts?** Gmail's free tier limits email sending. With two accounts, you get:
- Account 1: 50 emails/day (conservative limit)
- Account 2: 50 emails/day (fallback)
- Total: 100 emails/day with automatic switching

**How it works:** The workflow starts with your primary account. If it hits the daily limit or gets errors, it automatically switches to your secondary account. At midnight, it resets and goes back to primary.



#### Primary Gmail Account Setup

**Steps:**

1. In n8n, click **"Credentials"** > **"Add Credential"**

2. Search for: `gmail oauth2`

3. Click on: **"Gmail OAuth2 API"**

4. Fill in the form:
   - **Client ID**: Paste from Part 1.6
   - **Client Secret**: Paste from Part 1.6

5. Click **"Connect my account"** button

6. A Google authorization popup will appear:
   - Select your PRIMARY Gmail account (the one you'll use most)
   - Click **"Continue"** or **"Allow"**
   - Grant permissions for "Send email on your behalf"

7. After authorization, you'll return to n8n

8. Give the credential a name: `Gmail Primary OAuth2`

9. Click **"Save"**

10. Copy the credential ID from the URL or credential list

**What you get:** Primary Gmail credential ID

---

#### Secondary Gmail Account Setup

**Steps:**

1. Click **"Add Credential"** again

2. Search for: `gmail oauth2`

3. Click on: **"Gmail OAuth2 API"**

4. Fill in the form:
   - **Client ID**: Same as primary (from Part 1.6)
   - **Client Secret**: Same as primary (from Part 1.6)

5. Click **"Connect my account"** button

6. In the Google popup:
   - **IMPORTANT**: Select a DIFFERENT Gmail account
   - If you only have one, create a second free Gmail account first
   - Click **"Continue"** and grant permissions

7. Name the credential: `Gmail Secondary OAuth2`

8. Click **"Save"**

9. Copy this credential ID

**What you get:** Secondary Gmail credential ID

**Note:** Both credentials can use the same OAuth Client ID/Secret from Google Cloud Console. The difference is which Google account you authorize in step 6.

---

### 2.4 Add Google Sheets OAuth2 Credential

**Steps:**

1. Click **"Add Credential"** in n8n

2. Search for: `google sheets oauth2`

3. Click on: **"Google Sheets OAuth2 API"**

4. Fill in the form:
   - **Client ID**: Same as Gmail (from Part 1.6)
   - **Client Secret**: Same as Gmail (from Part 1.6)

5. Click **"Connect my account"**

6. Authorize with your Google account (same as primary Gmail)

7. Grant permissions for "See, edit, create, and delete spreadsheets"

8. Name it: `Google Sheets OAuth2`

9. Click **"Save"**

10. Copy the credential ID

**What you get:** Google Sheets credential ID

---

### 2.5 Add Telegram Bot Credential

**Steps:**

1. Click **"Add Credential"** in n8n

2. Search for: `telegram`

3. Click on: **"Telegram API"**

4. Fill in the form:
   - **Access Token**: Paste your bot token (from Part 1.7)

5. Click **"Save"**

6. Copy the credential ID

**What you get:** Telegram credential ID

---

### Credential Setup Checklist

At this point, you should have 5 credentials saved in n8n:

- [ ] Groq API (1 credential)
- [ ] Gmail OAuth2 Primary (1 credential)
- [ ] Gmail OAuth2 Secondary (1 credential)
- [ ] Google Sheets OAuth2 (1 credential)
- [ ] Telegram API (1 credential)

**Keep all credential IDs handy** - you'll need them in Part 4.

---

## Part 3: Import Workflow into n8n

Now you'll import the pre-built workflow file into your n8n instance.

### 3.1 Download Workflow File

**Option A: From GitHub (Recommended)**

1. Go to: [github.com/vallakatlaraviteja/Ravi-s_automation](https://github.com/vallakatlaraviteja/Ravi-s_automation)

2. Find the file: `ENHANCED-MASTER-workflow.json`

3. Click the file name to open it

4. Click the **"Raw"** button (top-right of file view)

5. Right-click the page and select **"Save As..."**

6. Save to your Downloads folder

**Option B: Import Directly from URL**

In n8n, you can import from a URL:
```
https://raw.githubusercontent.com/vallakatlaraviteja/Ravi-s_automation/main/ENHANCED-MASTER-workflow.json
```

---

### 3.2 Import into n8n

**Steps:**

1. In n8n, click **"Workflows"** in the left sidebar

2. Click the **"+"** button or **"Add Workflow"** button

3. In the top menu, click the three dots (⋯) or **"Workflow"** menu

4. Select **"Import from File"** OR **"Import from URL"**

**If importing from file:**
5a. Click **"Select file"** and choose `ENHANCED-MASTER-workflow.json`
6a. Click **"Import"**

**If importing from URL:**
5b. Paste the raw GitHub URL
6b. Click **"Import"**

7. The workflow will open in the editor

8. You'll see 62 nodes arranged in 3 main branches

9. Save the workflow by clicking **"Save"** button (top-right)

10. Give it a name: `Job Automation System`

---

### 3.3 Understand the Workflow Layout

The workflow has 3 main branches (think of them as 3 separate mini-programs):

**Branch 1: Job Discovery** (top section)
- **Trigger**: Runs daily at 8:00 AM UTC
- **What it does**: Fetches jobs from 3 APIs, scores them with AI, saves to Google Sheets
- **Key nodes**: Schedule Trigger, API fetchers, Groq scoring, Sheet append

**Branch 2: Email Outreach** (middle section)
- **Trigger**: Runs daily at 9:00 AM UTC
- **What it does**: Reads jobs from Sheet, generates personalized emails, sends via Gmail
- **Key nodes**: Schedule Trigger, Read Sheet, Groq email generation, Gmail send (primary/secondary)

**Branch 3: Telegram Assistant** (bottom section)
- **Trigger**: Always listening for messages
- **What it does**: Responds to commands like /stats, answers questions about your jobs
- **Key nodes**: Telegram Trigger, Command router, Groq AI agent, Reply sender

---

## Part 4: Replace Placeholders

The workflow contains placeholder text that you must replace with your actual values. This is like filling in a form.

### 4.1 Find Placeholders

The workflow uses these placeholders:

| Placeholder | Replace with | Found in |
|-------------|--------------|----------|
| `YOUR_GROQ_CREDENTIAL_ID` | Your Groq credential ID | 3 nodes |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | Your Sheets credential ID | 5 nodes |
| `YOUR_PRIMARY_GMAIL_CREDENTIAL_ID` | Primary Gmail credential ID | 1 node |
| `YOUR_SECONDARY_GMAIL_CREDENTIAL_ID` | Secondary Gmail credential ID | 1 node |
| `YOUR_TELEGRAM_CREDENTIAL_ID` | Telegram credential ID | 5 nodes |
| `YOUR_SPREADSHEET_ID` | Google Sheet ID | User Config node |
| `YOUR_TELEGRAM_CHAT_ID` | Your chat ID number | Telegram send nodes |
| `YOUR_ADZUNA_APP_ID` | Adzuna application ID | Fetch Adzuna node |
| `YOUR_ADZUNA_APP_KEY` | Adzuna application key | Fetch Adzuna node |

---

### 4.2 Replace Credential IDs (Easy Method)

n8n makes this easy:

1. Look for nodes with **yellow warning triangles** (⚠️) - these have missing credentials

2. Click on a node with a warning

3. In the right panel, you'll see **"Credentials"** section

4. Click the **dropdown** next to the credential type

5. Select the credential you created in Part 2 (by name)

6. Click **"Save"** on the node

7. Repeat for all nodes with warnings

**Nodes to update:**

- `Parse Resume with Groq AI` → Groq API credential
- `Groq AI: Score Job Match` → Groq API credential
- `Groq AI: Generate Personalized Email` → Groq API credential
- `Groq Agent (Llama 3.3 70B)` → Groq API credential
- `Read Existing Jobs from Sheet` → Google Sheets OAuth2 credential
- `Append to Google Sheets: Jobs Tab` → Google Sheets OAuth2 credential
- `Read Jobs from Sheet for Outreach` → Google Sheets OAuth2 credential
- `Update Sheet: Mark Email Sent` → Google Sheets OAuth2 credential
- `Query Google Sheet for Stats` → Google Sheets OAuth2 credential
- `Send Email via Gmail Primary` → Gmail Primary OAuth2 credential
- `Send Email via Gmail Secondary` → Gmail Secondary OAuth2 credential
- `Telegram Trigger: Interactive Assistant` → Telegram API credential
- `Send Telegram: Job Discovery Digest` → Telegram API credential
- `Send Quick Reply` → Telegram API credential
- `Send Telegram Reply (with stats)` → Telegram API credential
- `Send Telegram Reply (simple)` → Telegram API credential
- `Email Account Switch Notification` → Telegram API credential

---

### 4.3 Replace Adzuna Credentials (Manual)

Adzuna credentials are NOT stored as n8n credentials. You add them directly in the HTTP node:

1. Find the node named: `Fetch Adzuna API`

2. Double-click to open it

3. Scroll to **"Query Parameters"** section

4. Find parameter `app_id`:
   - Replace value with your Adzuna Application ID (from Part 1.8)

5. Find parameter `app_key`:
   - Replace value with your Adzuna Application Key (from Part 1.8)

6. Click **"Save"**

---

## Part 5: Configure Your Profile

The workflow has a central configuration node where you set your personal information and job search criteria.

### 5.1 Open User Config Node

1. In the workflow editor, find the node named: **"User Config (Master Profile)"**
   - It's near the top-left, connected to all 3 trigger branches

2. Double-click to open it

3. You'll see JavaScript code with a JSON object

---

### 5.2 Update Personal Information

Replace the example values in the code:

**Personal Details Section:**
```javascript
name: 'John Doe',              // Your full name
currentRole: 'Backend Developer',  // Your current job title  
targetRole: 'Senior Engineer',     // Your desired next role
experience: '3 years',             // Years of experience
location: 'San Francisco, USA',    // Your city and country
```

**Skills Section:**
```javascript
skills: ['Python', 'Django', 'PostgreSQL', 'Docker', 'AWS'],  // Your top 5-10 skills
```

**Job Search Criteria:**
```javascript
targetRoles: ['Backend Engineer', 'Full Stack Developer'],  // Roles you want
keywords: 'python backend OR django developer OR fastapi',  // API search terms
workMode: ['remote', 'hybrid'],  // Options: 'remote', 'hybrid', 'onsite'
minSalary: 80000,               // Minimum annual salary
country: 'us',                  // Two-letter country code (us, gb, in, au, ca, de)
```

**URLs Section:**
```javascript
resumeUrl: 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID',  // From Part 1.9
githubUrl: 'https://github.com/yourusername',
linkedinUrl: 'https://linkedin.com/in/yourprofile',
portfolioUrl: 'https://yourportfolio.com',
```

**System Settings:**
```javascript
userEmail: 'yourema il@example.com',  // Your email
dailyLimit: 10,                      // Max emails per day
scoreThreshold: 30,                  // Minimum AI score (0-100)
sheetId: 'YOUR_SPREADSHEET_ID',      // From Part 1 (Google Sheet ID)
resumeParsingEnabled: true,          // Keep as true
```

**Dual Email Configuration:**
```javascript
primaryEmail: 'your-primary@gmail.com',              // Your first Gmail
secondaryEmail: 'your-secondary@gmail.com',          // Your second Gmail
primaryGmailCredentialId: 'YOUR_PRIMARY_CRED_ID',    // From Part 2.3
secondaryGmailCredentialId: 'YOUR_SECONDARY_CRED_ID', // From Part 2.3
maxEmailsPerAccount: 50,                             // Daily limit per account
errorThreshold: 3                                     // Switch after 3 errors
```

3. Click **"Execute Node"** to test - you should see your config in the output

4. Click **"Save"**

---

### 5.3 Configuration Tips

**Country Codes:** Use ISO 3166-1 alpha-2:
- United States: `us`
- United Kingdom: `gb`
- India: `in`
- Australia: `au`
- Canada: `ca`
- Germany: `de`

**Score Threshold:**
- Start with `30` (balanced)
- Too many irrelevant jobs? Increase to `40` or `50`
- Too few jobs? Decrease to `20`

**Daily Limit:**
- Start with `10` (safe)
- Don't exceed `20` to avoid spam flags
- The workflow already splits load between 2 accounts

---

## Part 6: Test Everything

Before activating, test each part to ensure it works.

### Test 1: Resume Download

1. Click on node: **"Download Resume"**

2. Click **"Execute Node"** button

3. Check the output panel:
   - ✅ Should show binary data (PDF content)
   - ✅ No error messages

**If it fails:** Check your resume URL is publicly accessible (open in incognito browser)

---

### Test 2: Resume Parsing

1. After Test 1 succeeds, click node: **"Parse Resume with Groq AI"**

2. Click **"Execute Node"**

3. Check output:
   - ✅ Should show JSON with extracted skills, experience, education
   - ✅ Skills array should match your resume

**If it fails:** Check Groq credential is correct and API key is valid

---

### Test 3: Job Discovery

1. Click on: **"Schedule Trigger: Job Discovery (8 AM)"**

2. Click **"Execute Workflow"** (play button)

3. Wait 30-60 seconds for completion

4. Open your Google Sheet

5. Check:
   - ✅ New jobs appear in rows 2+
   - ✅ All 19 columns filled
   - ✅ Score column has values 0-100
   - ✅ Status is "New"

**If it fails:**
- Check Google Sheets credential is authorized
- Verify Sheet ID in User Config
- Ensure sheet tab is named "Jobs" exactly

---

### Test 4: Email Sending

**Setup:**

1. In your Google Sheet, row 2, add:
   - **Job Title**: Test Job
   - **Company**: Test Corp
   - **Recruiter Email**: YOUR_OWN_EMAIL@example.com
   - **Recruiter Name**: Test Recruiter
   - **Status**: New

**Execute:**

2. Click on: **"Schedule Trigger: Email Outreach (9 AM)"**

3. Click **"Execute Workflow"**

4. Wait 20 seconds

**Verify:**

5. Check your email inbox:
   - ✅ Email received from your primary Gmail
   - ✅ Subject mentions "Test Job" and "Test Corp"
   - ✅ Email body is personalized

6. Check Google Sheet row 2:
   - ✅ Status changed to "Email Sent"
   - ✅ Application ID filled
   - ✅ Email Sent Date is today

---

### Test 5: Telegram Bot

1. Open Telegram and message your bot

2. Send: `/start`
   - ✅ Should get welcome message

3. Send: `/stats`
   - ✅ Should show job statistics

4. Send: "What jobs do I have?"
   - ✅ Should get AI-generated answer

---

### Test 6: Email Failover

**Simulate primary account exhaustion:**

1. Open **"Email Account State"** node

2. Click **"Execute Node"** to see current state

3. Manually set `primaryDailyCount` to `50` in the static data (workflow settings)

4. Execute email outreach trigger again

5. Check:
   - ✅ Email sent from SECONDARY account
   - ✅ Telegram notification received about account switch

6. Reset state by setting `primaryDailyCount` back to `0`

---

## Part 7: Activate and Monitor

### 7.1 Activate the Workflow

1. In the workflow editor, top-right corner

2. Toggle the **"Active"** switch to **ON**

3. The workflow indicator turns green

4. All 3 triggers are now live:
   - Job Discovery: Runs at 8:00 AM UTC daily
   - Email Outreach: Runs at 9:00 AM UTC daily
   - Telegram: Always listening

---

### 7.2 Adjust Schedule (Optional)

**To change trigger times:**

1. Click on a Schedule Trigger node

2. Click **"Add Rule"** or edit existing

3. Cron expression format: `minute hour day month weekday`

Examples:
- `0 8 * * *` → 8:00 AM every day
- `0 9 * * 1-5` → 9:00 AM Monday-Friday
- `0 */6 * * *` → Every 6 hours
- `30 7 * * *` → 7:30 AM every day

**Convert UTC to your timezone:**
- If you're in EST (UTC-5): 8 AM UTC = 3 AM EST
- If you're in IST (UTC+5:30): 8 AM UTC = 1:30 PM IST
- Use a timezone converter tool

---

### 7.3 Monitor Executions

**View execution history:**

1. Click **"Executions"** in n8n sidebar

2. See list of all runs with timestamps

3. Click any execution to see:
   - Which nodes ran
   - Data passed between nodes
   - Any errors

**Set up error alerts:**

1. Go to n8n **Settings** > **Workflows**

2. Enable **"Error Workflow"** (optional)

3. Get email notifications on failures

---

### 7.4 Daily Workflow

**What happens automatically:**

**8:00 AM UTC:**
1. Job Discovery runs
2. Fetches 150 jobs from 3 sources
3. AI scores each job (0-100)
4. Saves top jobs to Google Sheet
5. Sends you Telegram + email digest

**9:00 AM UTC:**
1. Email Outreach runs
2. Reads "New" jobs from Sheet with recruiter emails
3. Generates personalized email for each
4. Sends up to 10 emails (5 per account)
5. Updates Sheet with "Email Sent" status

**Anytime:**
- Message your Telegram bot for job stats
- Ask questions like "Show me Python jobs"
- Bot responds with AI-generated answers

---

## Understanding the Workflow

### What Triggers Do

**Schedule Trigger** = Alarm clock for your workflow
- Runs workflow automatically at set times
- Uses cron expressions (like `0 8 * * *` for 8 AM daily)
- No manual clicking needed

**Telegram Trigger** = Always listening
- Waits for messages to your bot
- Activates workflow when you send a command
- Event-driven (not time-based)

---

### How Data Flows

**Job Discovery Branch:**
```
API calls → Fetch jobs → AI scores each → Filter by score → Check duplicates → Save to Sheet
```

**Email Outreach Branch:**
```
Read Sheet → Filter (Status=New, has email) → AI generates email → Select account → Send email → Update Sheet
```

**Telegram Branch:**
```
Receive message → Check if command or question → Route to handler → Generate response → Send reply
```

---

### Where Your Data Lives

- **Google Sheets**: All jobs, scores, statuses, application tracking
- **Workflow Static Data**: Email account state (counts, errors)
- **n8n Execution Logs**: History of runs, errors, data passed

**NO external databases** = Your data stays in your control

---

## Common Mistakes and Solutions

### 1. Wrong Resume URL Format

**Mistake:** Using Google Drive `/view` URL instead of `/uc?export=download`

**Symptom:** Resume download fails with "Access Denied" error

**Solution:**
- Google Drive: `https://drive.google.com/uc?export=download&id=FILE_ID`
- GitHub: Use "Raw" button URL
- Dropbox: Change `?dl=0` to `?dl=1`

**Test:** Open URL in incognito browser - should download PDF, not show preview

---

### 2. OAuth Redirect URI Mismatch

**Mistake:** n8n redirect URI doesn't match Google Cloud Console

**Symptom:** "Error 400: redirect_uri_mismatch" when authorizing

**Solution:**
1. Check your n8n URL (e.g., `https://app.n8n.cloud` or `https://your-domain.com`)
2. In Google Cloud Console, go to Credentials > OAuth Client
3. Add redirect URI: `https://YOUR_N8N_URL/rest/oauth2-credential/callback`
4. Save and retry authorization

---

### 3. Credential ID Not Found

**Mistake:** Copied credential name instead of ID, or didn't update placeholders

**Symptom:** "Credentials with ID 'YOUR_GROQ_CREDENTIAL_ID' not found"

**Solution:**
1. Go to n8n Credentials page
2. Click on the credential
3. Copy ID from URL: `.../credentials/ABC-123-DEF-456`
4. Replace placeholder in node settings (don't copy/paste the text "YOUR_GROQ_CREDENTIAL_ID")

---

### 4. Placeholder Not Replaced

**Mistake:** Left `YOUR_SPREADSHEET_ID` in User Config without replacing

**Symptom:** Google Sheets errors like "Spreadsheet not found"

**Solution:**
- Open User Config node
- Replace ALL placeholders starting with `YOUR_`
- Must be actual values, not the placeholder text

---

### 5. Adzuna Country Code Wrong

**Mistake:** Using full country name ("United States") or 3-letter code ("USA")

**Symptom:** Adzuna API returns no results or error

**Solution:**
- Use 2-letter ISO codes: `us`, `gb`, `in`, `au`, `ca`, `de`
- Update in User Config node: `country: 'us'`
- See full list: [Adzuna API docs](https://developer.adzuna.com/docs/search)

---

### 6. Telegram Chat ID Not Numeric

**Mistake:** Using Telegram username like `@myusername` instead of numeric ID

**Symptom:** "Bad Request: chat not found" error

**Solution:**
1. Open URL: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
2. Look for `"chat":{"id":123456789}`
3. Copy the NUMBER only (no quotes, no @)
4. Update in Telegram send nodes

---

### 7. Gmail Daily Limit Confusion

**Mistake:** Setting `maxEmailsPerAccount: 500` thinking that's safe

**Symptom:** Gmail marks emails as spam or blocks sending

**Solution:**
- Gmail free tier: 500/day MAXIMUM (hard limit)
- **Safe limit**: 50/day per account (conservative to avoid spam flags)
- With 2 accounts: 100/day total (safe)
- Workflow default: 50 per account (keep this)
- New accounts: Start with 20/day, gradually increase (warm-up period)

---

### 8. Schedule Timezone Confusion

**Mistake:** Thinking schedule times are in local timezone

**Symptom:** Workflow runs at unexpected times (e.g., 3 AM instead of 8 AM)

**Solution:**
- n8n cron expressions use **UTC timezone**
- Convert local time to UTC
- Example: 8 AM EST = 1 PM UTC (EST is UTC-5)
- Use a timezone converter
- OR: Change cron expression to match your timezone in UTC

---

## Troubleshooting Checklist

Before asking for help, check:

- [ ] All credentials saved in n8n with green checkmarks
- [ ] All credential IDs copied (not placeholder text)
- [ ] Google Sheet tab named "Jobs" exactly (case-sensitive)
- [ ] Google Sheet has 19 columns in correct order
- [ ] Resume URL is publicly accessible (test in incognito)
- [ ] Telegram bot token is correct (test with getMe endpoint)
- [ ] Adzuna credentials added to HTTP node query parameters
- [ ] User Config has all YOUR_ placeholders replaced
- [ ] Workflow is activated (toggle ON in top-right)
- [ ] Test executions complete successfully

---

## Testing Checklist

Use this checklist to verify everything works before going live:

### Pre-Activation Tests

- [ ] **Test 1: Resume Download** - Execute "Download Resume" node, verify binary data output
- [ ] **Test 2: Resume Parsing** - Execute "Parse Resume with Groq AI" node, verify JSON structure with skills
- [ ] **Test 3: Job Discovery** - Execute job discovery trigger, verify Google Sheet populated with jobs (10+ rows)
- [ ] **Test 4: Email Sending** - Add test job with your email, execute outreach, verify email received
- [ ] **Test 5: Telegram Bot** - Send `/start`, `/stats`, and a question, verify all responses
- [ ] **Test 6: Email Failover** - Simulate primary exhausted, verify switch to secondary with notification

### Post-Activation Monitoring

- [ ] Check executions log after 8 AM UTC - Job Discovery ran successfully
- [ ] Check Google Sheet has new jobs from today
- [ ] Check executions log after 9 AM UTC - Email Outreach ran
- [ ] Check your Gmail sent folder for outreach emails
- [ ] Verify Telegram digest notifications received
- [ ] Monitor execution logs for 3 days for any errors

---

## What to Expect

### First Day

- **8 AM UTC**: 10-50 jobs added to your Sheet (depends on keywords)
- **9 AM UTC**: 0-10 emails sent (only if jobs have recruiter emails)
- **Throughout day**: You can message Telegram bot anytime

### First Week

- **Total jobs discovered**: 50-300 (depending on how broad your keywords are)
- **Emails sent**: 10-70 (most jobs won't have recruiter emails initially)
- **Manual work needed**: Add recruiter emails to high-priority jobs in Sheet

### Ongoing Maintenance

**Weekly tasks:**
- Review new jobs in Sheet
- Research recruiters for top companies, add emails manually
- Adjust score threshold if needed (raise if too many low-quality jobs)

**Monthly tasks:**
- Update skills in User Config as you learn new technologies
- Refresh OAuth tokens if they expire
- Review and respond to any recruiter replies

---

## Next Steps After Setup

1. **Let it run for 3 days** and monitor execution logs

2. **Review job quality**:
   - Too many irrelevant jobs? Increase `scoreThreshold` to 40-50
   - Too few jobs? Decrease to 20, or broaden `keywords`

3. **Add recruiter research**:
   - Manually find recruiter emails for companies you love
   - Add to Sheet in "Recruiter Email" and "Recruiter Name" columns
   - Workflow will automatically email them next day

4. **Optimize email content**:
   - Read sent emails to check quality
   - Edit Groq prompt in "Generate Personalized Email" node if needed

5. **Expand job sources** (advanced):
   - Add more API nodes (LinkedIn, Indeed, etc.)
   - Follow same pattern as existing API nodes

---

## Support and Resources

### Documentation Files

- **EMAIL-SETUP-GUIDE.md**: Detailed Gmail OAuth setup for dual accounts
- **ACCOUNTS-CHECKLIST.json**: Structured list of all required accounts and credentials
- **ACCOUNTS-CREDENTIALS-TEMPLATE.txt**: Fill-in-the-blank tracking template
- **DUAL-EMAIL-SETUP-GUIDE.md**: Deep dive into email failover system

### External Resources

- **n8n Community**: [community.n8n.io](https://community.n8n.io) - Technical questions
- **Groq Docs**: [console.groq.com/docs](https://console.groq.com/docs) - AI model documentation
- **Adzuna API**: [developer.adzuna.com/docs](https://developer.adzuna.com/docs) - Job API reference
- **Telegram Bots**: [core.telegram.org/bots](https://core.telegram.org/bots) - Bot API documentation

---

## Frequently Asked Questions

**Q: Do I need coding experience?**  
A: No. Just copy-paste configuration values as shown in this guide.

**Q: Is this really free forever?**  
A: Yes. All services have generous free tiers that exceed our usage.

**Q: What if I only have one Gmail account?**  
A: You can still use the workflow, but create a second free Gmail for better daily limits (100 vs 50 emails).

**Q: Can I use this for job markets outside the US?**  
A: Yes. Change the `country` code in User Config (e.g., `gb` for UK, `in` for India, `au` for Australia).

**Q: How do I stop the workflow temporarily?**  
A: Toggle the "Active" switch to OFF in the workflow editor.

**Q: Will this work on n8n self-hosted?**  
A: Yes. Follow the same steps, just use your self-hosted URL for OAuth redirects.

**Q: What if my OAuth tokens expire?**  
A: Re-authorize in n8n Credentials page (click credential > Connect my account again).

**Q: Can I run this more frequently than once a day?**  
A: Yes. Edit cron expressions in Schedule Triggers (e.g., `0 */6 * * *` for every 6 hours). Be mindful of API rate limits.

---

## Success! 🎉

You've completed the setup! Your automated job search system is now running 24/7.

**What happens next:**
- Every day, new jobs are discovered and scored
- Emails are sent to recruiters automatically
- You get daily digests via Telegram and email
- You can chat with your Telegram bot anytime

**Remember:**
- Check execution logs weekly
- Tune score threshold based on job quality
- Add recruiter emails for companies you love
- Update your profile as your skills grow

**Good luck with your job search!** 🚀

---

**Last Updated**: 2024-01-20  
**Version**: 1.0.0 (FEAT-003)  
**Workflow**: ENHANCED MASTER with Resume Intelligence and Dual Email Failover  
**Total Nodes**: 62
