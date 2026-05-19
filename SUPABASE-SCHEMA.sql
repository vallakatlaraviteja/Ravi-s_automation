-- ================================================================
-- SUPABASE DATABASE SCHEMA FOR JOB AUTOMATION SYSTEM
-- ================================================================
-- Copy this entire file and paste into Supabase SQL Editor
-- This creates your job tracking database
-- ================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================================
-- TABLE 1: jobs (Main job listings table)
-- ================================================================
CREATE TABLE IF NOT EXISTS jobs (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- Job Identifiers
  job_id TEXT UNIQUE NOT NULL,           -- External ID from job API (e.g., 'remotive-12345')
  
  -- Job Details
  job_title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT,
  work_mode TEXT,                        -- Remote, Hybrid, Onsite
  job_type TEXT,                         -- Full-time, Part-time, Contract
  salary TEXT,
  description TEXT,
  apply_url TEXT NOT NULL,
  
  -- Source Information
  source TEXT NOT NULL,                  -- Remotive, Arbeitnow, JSearch, etc.
  category TEXT,
  tags TEXT[],                           -- Array of tags
  
  -- AI Scoring
  score INTEGER CHECK (score >= 0 AND score <= 100),
  priority TEXT CHECK (priority IN ('high', 'medium', 'low')),
  match_reason TEXT,
  
  -- Application Tracking
  status TEXT DEFAULT 'New' CHECK (status IN ('New', 'Email Sent', 'Applied', 'Interview', 'Offer', 'Rejected', 'Accepted')),
  recruiter_email TEXT,
  recruiter_name TEXT,
  application_id TEXT,
  
  -- Dates
  posted_date DATE,
  fetched_date DATE NOT NULL DEFAULT CURRENT_DATE,
  email_sent_date DATE,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Indexes for fast queries
  CONSTRAINT valid_email CHECK (recruiter_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' OR recruiter_email IS NULL)
);

-- ================================================================
-- INDEXES FOR PERFORMANCE
-- ================================================================
CREATE INDEX idx_jobs_job_id ON jobs(job_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_score ON jobs(score DESC);
CREATE INDEX idx_jobs_priority ON jobs(priority);
CREATE INDEX idx_jobs_fetched_date ON jobs(fetched_date DESC);
CREATE INDEX idx_jobs_source ON jobs(source);
CREATE INDEX idx_jobs_company ON jobs(company);

-- Full-text search index
CREATE INDEX idx_jobs_search ON jobs USING gin(to_tsvector('english', job_title || ' ' || company || ' ' || COALESCE(description, '')));

-- ================================================================
-- TABLE 2: email_logs (Track all sent emails)
-- ================================================================
CREATE TABLE IF NOT EXISTS email_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  
  -- Email Details
  recipient_email TEXT NOT NULL,
  recipient_name TEXT,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  
  -- Tracking
  sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  opened_at TIMESTAMP WITH TIME ZONE,
  clicked_at TIMESTAMP WITH TIME ZONE,
  replied_at TIMESTAMP WITH TIME ZONE,
  
  -- Status
  status TEXT DEFAULT 'sent' CHECK (status IN ('sent', 'opened', 'clicked', 'replied', 'bounced', 'failed')),
  
  -- Metadata
  email_provider TEXT,                   -- 'gmail' or 'resend'
  external_id TEXT,                      -- ID from email provider
  
  CONSTRAINT valid_recipient_email CHECK (recipient_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_email_logs_job_id ON email_logs(job_id);
CREATE INDEX idx_email_logs_sent_at ON email_logs(sent_at DESC);
CREATE INDEX idx_email_logs_status ON email_logs(status);

-- ================================================================
-- TABLE 3: job_stats (Daily statistics)
-- ================================================================
CREATE TABLE IF NOT EXISTS job_stats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stat_date DATE NOT NULL DEFAULT CURRENT_DATE,
  
  -- Discovery Stats
  jobs_discovered INTEGER DEFAULT 0,
  jobs_saved INTEGER DEFAULT 0,
  avg_score DECIMAL(5,2),
  
  -- Source Breakdown
  source_remotive INTEGER DEFAULT 0,
  source_arbeitnow INTEGER DEFAULT 0,
  source_jsearch INTEGER DEFAULT 0,
  source_themuse INTEGER DEFAULT 0,
  source_adzuna INTEGER DEFAULT 0,
  
  -- Email Stats
  emails_sent INTEGER DEFAULT 0,
  emails_opened INTEGER DEFAULT 0,
  emails_replied INTEGER DEFAULT 0,
  
  -- Application Stats
  interviews_scheduled INTEGER DEFAULT 0,
  offers_received INTEGER DEFAULT 0,
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(stat_date)
);

CREATE INDEX idx_job_stats_date ON job_stats(stat_date DESC);

-- ================================================================
-- TABLE 4: user_config (Store user profile)
-- ================================================================
CREATE TABLE IF NOT EXISTS user_config (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- Personal Info
  name TEXT NOT NULL,
  current_role TEXT,
  target_role TEXT,
  experience TEXT,
  location TEXT,
  
  -- Skills & Preferences
  skills TEXT[],
  target_roles TEXT[],
  keywords TEXT,
  work_mode TEXT[],
  min_salary INTEGER,
  country TEXT DEFAULT 'us',
  
  -- URLs
  resume_url TEXT,
  linkedin_url TEXT,
  github_url TEXT,
  portfolio_url TEXT,
  
  -- System Settings
  user_email TEXT NOT NULL,
  daily_email_limit INTEGER DEFAULT 10,
  score_threshold INTEGER DEFAULT 30 CHECK (score_threshold >= 0 AND score_threshold <= 100),
  
  -- External IDs
  google_sheet_id TEXT,
  telegram_chat_id TEXT,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Only allow one user config (single-user system)
CREATE UNIQUE INDEX idx_user_config_singleton ON user_config((TRUE));

-- ================================================================
-- VIEWS FOR EASY QUERYING
-- ================================================================

-- View: High Priority Jobs
CREATE OR REPLACE VIEW high_priority_jobs AS
SELECT 
  id, job_id, job_title, company, location, score, priority, 
  status, apply_url, fetched_date
FROM jobs
WHERE priority = 'high' AND status = 'New'
ORDER BY score DESC, fetched_date DESC;

-- View: Jobs Ready for Outreach
CREATE OR REPLACE VIEW jobs_ready_for_outreach AS
SELECT 
  id, job_id, job_title, company, location, score, 
  recruiter_email, recruiter_name, apply_url
FROM jobs
WHERE status = 'New' 
  AND recruiter_email IS NOT NULL 
  AND recruiter_email != ''
ORDER BY score DESC
LIMIT 100;

-- View: Recent Jobs (Last 7 days)
CREATE OR REPLACE VIEW recent_jobs AS
SELECT 
  id, job_id, job_title, company, location, work_mode, 
  score, priority, status, source, fetched_date
FROM jobs
WHERE fetched_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY fetched_date DESC, score DESC;

-- View: Application Pipeline
CREATE OR REPLACE VIEW application_pipeline AS
SELECT 
  status,
  COUNT(*) as count,
  AVG(score) as avg_score,
  MIN(fetched_date) as oldest,
  MAX(fetched_date) as newest
FROM jobs
GROUP BY status
ORDER BY 
  CASE status
    WHEN 'New' THEN 1
    WHEN 'Email Sent' THEN 2
    WHEN 'Applied' THEN 3
    WHEN 'Interview' THEN 4
    WHEN 'Offer' THEN 5
    WHEN 'Accepted' THEN 6
    WHEN 'Rejected' THEN 7
  END;

-- ================================================================
-- FUNCTIONS FOR AUTOMATION
-- ================================================================

-- Function: Update last_updated timestamp automatically
CREATE OR REPLACE FUNCTION update_last_updated()
RETURNS TRIGGER AS $$
BEGIN
  NEW.last_updated = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update last_updated on jobs table
CREATE TRIGGER trigger_jobs_last_updated
BEFORE UPDATE ON jobs
FOR EACH ROW
EXECUTE FUNCTION update_last_updated();

-- Trigger: Auto-update updated_at on user_config table
CREATE TRIGGER trigger_user_config_updated_at
BEFORE UPDATE ON user_config
FOR EACH ROW
EXECUTE FUNCTION update_last_updated();

-- Function: Get job statistics
CREATE OR REPLACE FUNCTION get_job_statistics()
RETURNS TABLE (
  total_jobs BIGINT,
  new_jobs BIGINT,
  email_sent BIGINT,
  interviews BIGINT,
  offers BIGINT,
  avg_score NUMERIC,
  high_priority BIGINT,
  jobs_this_week BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COUNT(*) as total_jobs,
    COUNT(*) FILTER (WHERE status = 'New') as new_jobs,
    COUNT(*) FILTER (WHERE status = 'Email Sent') as email_sent,
    COUNT(*) FILTER (WHERE status = 'Interview') as interviews,
    COUNT(*) FILTER (WHERE status = 'Offer') as offers,
    ROUND(AVG(score), 2) as avg_score,
    COUNT(*) FILTER (WHERE priority = 'high') as high_priority,
    COUNT(*) FILTER (WHERE fetched_date >= CURRENT_DATE - INTERVAL '7 days') as jobs_this_week
  FROM jobs;
END;
$$ LANGUAGE plpgsql;

-- Function: Record daily stats
CREATE OR REPLACE FUNCTION record_daily_stats()
RETURNS VOID AS $$
DECLARE
  today DATE := CURRENT_DATE;
BEGIN
  INSERT INTO job_stats (
    stat_date,
    jobs_discovered,
    jobs_saved,
    avg_score,
    source_remotive,
    source_arbeitnow,
    source_jsearch,
    source_themuse,
    source_adzuna,
    emails_sent
  )
  SELECT 
    today,
    COUNT(*) FILTER (WHERE fetched_date = today),
    COUNT(*) FILTER (WHERE fetched_date = today AND score >= 30),
    ROUND(AVG(score) FILTER (WHERE fetched_date = today), 2),
    COUNT(*) FILTER (WHERE fetched_date = today AND source = 'Remotive'),
    COUNT(*) FILTER (WHERE fetched_date = today AND source = 'Arbeitnow'),
    COUNT(*) FILTER (WHERE fetched_date = today AND source = 'JSearch'),
    COUNT(*) FILTER (WHERE fetched_date = today AND source = 'TheMuse'),
    COUNT(*) FILTER (WHERE fetched_date = today AND source = 'Adzuna'),
    COUNT(*) FILTER (WHERE email_sent_date = today)
  FROM jobs
  ON CONFLICT (stat_date) 
  DO UPDATE SET
    jobs_discovered = EXCLUDED.jobs_discovered,
    jobs_saved = EXCLUDED.jobs_saved,
    avg_score = EXCLUDED.avg_score,
    source_remotive = EXCLUDED.source_remotive,
    source_arbeitnow = EXCLUDED.source_arbeitnow,
    source_jsearch = EXCLUDED.source_jsearch,
    source_themuse = EXCLUDED.source_themuse,
    source_adzuna = EXCLUDED.source_adzuna,
    emails_sent = EXCLUDED.emails_sent;
END;
$$ LANGUAGE plpgsql;

-- ================================================================
-- ROW LEVEL SECURITY (RLS)
-- ================================================================
-- Enable RLS on all tables
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_config ENABLE ROW LEVEL SECURITY;

-- Create policies (Allow all for service role, restrict for others)
CREATE POLICY "Enable all access for service role" ON jobs
  FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON email_logs
  FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON job_stats
  FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON user_config
  FOR ALL USING (true);

-- ================================================================
-- SEED DATA: Create default user config
-- ================================================================
INSERT INTO user_config (
  name,
  current_role,
  target_role,
  experience,
  location,
  skills,
  target_roles,
  keywords,
  work_mode,
  min_salary,
  country,
  user_email
) VALUES (
  'Your Name',
  'Backend Developer',
  'Senior Backend Engineer',
  '3 years',
  'New York, USA',
  ARRAY['Python', 'JavaScript', 'AWS', 'Docker', 'PostgreSQL'],
  ARRAY['Backend Engineer', 'Full Stack Engineer', 'Software Engineer'],
  'python developer OR backend engineer OR software engineer',
  ARRAY['remote', 'hybrid'],
  80000,
  'us',
  'your.email@gmail.com'
) ON CONFLICT DO NOTHING;

-- ================================================================
-- HELPFUL QUERIES (Copy these for manual use)
-- ================================================================

-- Get all high priority new jobs:
-- SELECT * FROM high_priority_jobs LIMIT 20;

-- Get job statistics:
-- SELECT * FROM get_job_statistics();

-- Get jobs ready for email outreach:
-- SELECT * FROM jobs_ready_for_outreach LIMIT 10;

-- Get recent jobs (last 7 days):
-- SELECT * FROM recent_jobs LIMIT 50;

-- Get application pipeline overview:
-- SELECT * FROM application_pipeline;

-- Search jobs by keyword:
-- SELECT job_title, company, score, status 
-- FROM jobs 
-- WHERE to_tsvector('english', job_title || ' ' || company || ' ' || COALESCE(description, '')) @@ plainto_tsquery('english', 'python backend')
-- ORDER BY score DESC
-- LIMIT 20;

-- ================================================================
-- DONE! Your database is ready.
-- ================================================================
-- Next steps:
-- 1. Copy this entire SQL and paste into Supabase SQL Editor
-- 2. Click "Run"
-- 3. You should see: "Success. No rows returned"
-- 4. Check the "Table Editor" - you should see 4 tables
-- 5. Copy your Supabase URL and API keys for n8n
-- ================================================================
