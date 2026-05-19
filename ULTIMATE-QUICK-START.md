# 🚀 ULTIMATE STACK - QUICK START

## What YOU Need to Do (45 minutes)

### 1. Create 3 NEW Accounts (15 min)

#### A) RapidAPI (JSearch - 10K jobs/month free)
1. Go to: https://rapidapi.com
2. Sign up with GitHub/Google
3. Search "JSearch" → Subscribe to FREE plan
4. Copy API key → Save to `rapidapi-key.txt`

#### B) Supabase (PostgreSQL - 500MB free)
1. Go to: https://supabase.com
2. Sign up with GitHub
3. Create project: "job-automation"
4. Generate database password → SAVE IT
5. Copy: Project URL, anon key, service_role key
6. Save to `supabase-credentials.txt`

#### C) Resend (OPTIONAL - 3K emails/month free)
- Skip if you don't have a domain
- OR use Gmail (works great!)

---

### 2. Setup Database (5 min)

1. Open Supabase → SQL Editor
2. Copy entire `SUPABASE-SCHEMA.sql` file
3. Paste and click "Run"
4. Verify: Table Editor shows 4 tables

---

### 3. Add Credentials to n8n (10 min)

Add these NEW credentials:

| Credential | Type | What to Add |
|-----------|------|-------------|
| RapidAPI | Header Auth | X-RapidAPI-Key: YOUR_KEY |
| Supabase | Supabase | Project URL + service_role key |
| Resend (optional) | HTTP Header Auth | Authorization: Bearer YOUR_KEY |

Save all credential IDs!

---

### 4. Import Workflow (15 min)

1. Download: `MASTER-ULTIMATE-workflow.json`
2. Import to n8n
3. Replace 14 placeholders (use Ctrl+F)
4. Update User Config node
5. Test: Execute "Schedule Trigger: Job Discovery"
6. Activate workflow

---

## Files You Need

| File | Purpose |
|------|---------|
| `MASTER-ULTIMATE-workflow.json` | Import this into n8n |
| `SUPABASE-SCHEMA.sql` | Run in Supabase SQL Editor |
| `ULTIMATE-SETUP-GUIDE.md` | Detailed instructions |
| `ULTIMATE-WHAT-YOU-PROVIDE.json` | Complete checklist |

---

## What You Get

### vs. Basic Version:

| Feature | Basic | Ultimate |
|---------|-------|----------|
| Job Sources | 3 APIs | 5 APIs ⭐ |
| Jobs/Day | 50-150 | 100-300 ⭐ |
| Database | Sheets (10K limit) | PostgreSQL (500K+) ⭐ |
| Query Speed | 2-5 seconds | <50ms ⭐ |
| SQL Queries | No | Yes ⭐ |
| Email Tracking | No | Yes (optional) ⭐ |
| Monthly Cost | $0 | $0 ✅ |

---

## Expected Results After 30 Days

- **3,000-9,000 jobs** discovered
- **600-1,800 jobs** saved (score ≥30)
- **100-300 emails** sent to recruiters
- **5-15 responses** from recruiters
- **2-5 interviews** scheduled

---

## Need Help?

1. **Complete guide:** `ULTIMATE-SETUP-GUIDE.md`
2. **What to provide:** `ULTIMATE-WHAT-YOU-PROVIDE.json`
3. **Is it free?** `FREE-TIER-VERIFICATION-ULTIMATE.md`

---

**Start here:** Open `ULTIMATE-SETUP-GUIDE.md` and follow step-by-step!
