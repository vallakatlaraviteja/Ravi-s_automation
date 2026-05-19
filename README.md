# Ultimate n8n Job Automation Suite 🚀

**Automate your entire job search with AI-powered workflows**

## 🎯 What This Does

Three production-ready n8n workflows that completely automate job searching, applying, and tracking:

1. **Auto Job Applications + Status Tracking** - Apply to jobs automatically and track status changes
2. **AI-Powered Job Search + Notion** - Use Google Gemini AI to find and organize jobs
3. **LinkedIn Job Scraper** - Scrape LinkedIn jobs directly into Google Sheets

## ✨ Features

- ✅ **100% Free** - Uses free tiers of Google Gemini, SerpAPI, and open-source tools
- ✅ **Production-Ready** - Clean JSON, error handling, proper data validation
- ✅ **Zero Configuration Errors** - All syntax validated and tested
- ✅ **Best AI Tools** - Optimized for Google Gemini (best free AI option)
- ✅ **Multi-Platform** - Works with LinkedIn, Indeed, and other job boards
- ✅ **Smart Tracking** - Google Sheets + Notion integration
- ✅ **Auto-Updates** - Status checks every 2 days with email notifications

## 📦 What's Included

```
├── workflow-1-auto-job-applications.json      # Auto-apply workflow
├── workflow-2-ai-job-search-notion.json       # AI job search workflow
├── workflow-3-linkedin-scraper-brightdata.json # LinkedIn scraper workflow
├── SETUP-GUIDE.md                             # Complete setup instructions
├── CONFIGURATION-REFERENCE.md                 # All configuration options
└── README.md                                  # This file
```

## 🚀 Quick Start

### Prerequisites

1. **n8n** (self-hosted or cloud) - [Get it here](https://n8n.io/)
2. **Google Account** (for Sheets & Gmail)
3. **Google Gemini API** (free) - [Get API key](https://ai.google.dev/)

### Installation

1. **Import workflows into n8n:**
   - Open n8n → Workflows → Import from File
   - Import all 3 JSON files

2. **Set up credentials:**
   - Google Sheets (OAuth2)
   - Gmail (OAuth2)
   - Google Gemini (API Key)
   - Notion (API Token) - for Workflow 2
   - Bright Data or SerpAPI - for Workflow 3

3. **Configure workflows:**
   - Update all `YOUR_*_CREDENTIAL_ID` placeholders
   - Update `YOUR_SPREADSHEET_ID` with your Google Sheet ID
   - Update `YOUR_EMAIL@example.com` with your email
   - Update `YOUR_NOTION_DATABASE_ID` (for Workflow 2)
   - Update `YOUR_BRIGHTDATA_API_KEY` (for Workflow 3)

4. **Activate workflows**

See [SETUP-GUIDE.md](./SETUP-GUIDE.md) for detailed instructions.

## 📊 Workflow Details

### Workflow 1: Auto Job Applications + Status Tracking

**What it does:**
- Reads jobs from Google Sheet
- Auto-applies to jobs with Status = "Not Applied"
- Updates sheet with application details
- Checks status every 2 days
- Sends email notifications for interviews/offers/rejections

**Schedule:** 
- Apply: Daily at 9 AM
- Status check: Every 2 days at 10 AM

**Perfect for:** Mass job applications with automated tracking

---

### Workflow 2: AI-Powered Job Search + Notion

**What it does:**
- Uses Google Gemini AI to search jobs across platforms
- Filters by role, experience, location, salary
- Ranks jobs with priority scoring
- Saves to Notion database with tags
- Sends daily summary email

**Schedule:** Daily at 8 AM

**Perfect for:** Smart job discovery with AI-powered matching

---

### Workflow 3: LinkedIn Job Finder

**What it does:**
- Scrapes LinkedIn via Bright Data API
- Accepts job search parameters via webhook
- Cleans and formats job data
- Saves to Google Sheets
- Returns JSON response

**Trigger:** Webhook (on-demand)

**Perfect for:** Fast LinkedIn scraping without manual search

---

## 💡 Best Practices

### Recommended Setup

Use all three workflows together:

1. **8:00 AM** - Workflow 2 finds new jobs → saves to Notion
2. **9:00 AM** - Workflow 1 auto-applies → updates Sheet
3. **Every 2 days** - Workflow 1 checks status → sends updates
4. **On-demand** - Workflow 3 scrapes LinkedIn → feeds Workflow 1

### Free Tier Limits

- **Google Gemini:** 60 requests/min, 1,500/day ✅
- **SerpAPI:** 100 searches/month ✅
- **Google Sheets:** Unlimited ✅
- **Gmail:** Unlimited (reasonable use) ✅
- **Notion:** Unlimited pages ✅

**Total cost:** $0/month 🎉

## 🛠️ Technology Stack

| Component | Service | Cost |
|-----------|---------|------|
| Automation | n8n | Free (self-hosted) |
| AI Search | Google Gemini | Free (1,500/day) |
| Job Scraping | Bright Data / SerpAPI | Free tier available |
| Tracking | Google Sheets | Free |
| Organization | Notion | Free |
| Notifications | Gmail | Free |

## 📖 Documentation

- **[SETUP-GUIDE.md](./SETUP-GUIDE.md)** - Step-by-step setup instructions
- **[CONFIGURATION-REFERENCE.md](./CONFIGURATION-REFERENCE.md)** - All configuration options and customization

## 🤝 Contributing

Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Share your results

## 📝 License

MIT License - Use freely for personal and commercial projects

## 🎓 Learn More

- [n8n Documentation](https://docs.n8n.io/)
- [Google Gemini AI](https://ai.google.dev/)
- [Notion API](https://developers.notion.com/)
- [n8n Community](https://community.n8n.io/)

## 💬 Support

- Open an issue on GitHub
- Join n8n community forum
- Check troubleshooting section in SETUP-GUIDE.md

---

**Made with ❤️ for job seekers everywhere**

**Stop spending hours job hunting. Let AI do it for you.** 🚀
