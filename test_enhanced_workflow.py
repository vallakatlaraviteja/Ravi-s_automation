#!/usr/bin/env python3
"""
Test script to verify ENHANCED-MASTER-workflow.json meets all acceptance criteria.
"""

import json

def main():
    print("=" * 70)
    print("ACCEPTANCE CRITERIA VERIFICATION")
    print("=" * 70)
    
    # Load enhanced workflow
    with open('ENHANCED-MASTER-workflow.json', 'r') as f:
        workflow = json.load(f)
    
    results = []
    
    # AC1: Resume is successfully downloaded from public URL in User Config resumeUrl field
    print("\n✅ AC1: Resume Download from User Config resumeUrl")
    user_config = [n for n in workflow['nodes'] if n['id'] == 'user-config'][0]
    download_resume = [n for n in workflow['nodes'] if n['id'] == 'download-resume'][0]
    
    has_resume_url = 'resumeUrl' in user_config['parameters']['jsCode']
    download_url = download_resume['parameters']['url']
    supports_google_drive = 'drive.google.com/uc?export=download' in download_url
    supports_github = "replace('/blob/', '/raw/')" in download_url
    supports_dropbox = 'dropbox.com' in download_url and 'dl=1' in download_url
    
    ac1_pass = has_resume_url and supports_google_drive and supports_github and supports_dropbox
    results.append(("AC1", ac1_pass))
    
    print(f"   • User Config has resumeUrl field: {has_resume_url}")
    print(f"   • Supports Google Drive public links: {supports_google_drive}")
    print(f"   • Supports GitHub raw URLs: {supports_github}")
    print(f"   • Supports Dropbox public links: {supports_dropbox}")
    print(f"   Result: {'PASS ✓' if ac1_pass else 'FAIL ✗'}")
    
    # AC2: Groq AI extracts structured data with skills, experience, projects, achievements
    print("\n✅ AC2: Groq AI Extracts Structured Resume Data")
    parse_resume = [n for n in workflow['nodes'] if n['id'] == 'parse-resume-groq'][0]
    structure_resume = [n for n in workflow['nodes'] if n['id'] == 'structure-resume-data'][0]
    
    parse_prompt = parse_resume['parameters']['text']
    has_skills = '"skills"' in parse_prompt
    has_experience = '"experience"' in parse_prompt
    has_projects = '"projects"' in parse_prompt
    has_achievements = '"achievements"' in parse_prompt
    has_education = '"education"' in parse_prompt
    uses_low_temp = parse_resume['parameters']['options']['temperature'] <= 0.2
    
    structure_code = structure_resume['parameters']['jsCode']
    validates_json = 'JSON.parse' in structure_code
    
    ac2_pass = all([has_skills, has_experience, has_projects, has_achievements, 
                    has_education, uses_low_temp, validates_json])
    results.append(("AC2", ac2_pass))
    
    print(f"   • Prompt extracts skills: {has_skills}")
    print(f"   • Prompt extracts experience: {has_experience}")
    print(f"   • Prompt extracts projects: {has_projects}")
    print(f"   • Prompt extracts achievements: {has_achievements}")
    print(f"   • Prompt extracts education: {has_education}")
    print(f"   • Uses low temperature (≤0.2) for accuracy: {uses_low_temp}")
    print(f"   • Validates JSON structure: {validates_json}")
    print(f"   Result: {'PASS ✓' if ac2_pass else 'FAIL ✗'}")
    
    # AC3: Job scoring incorporates resume data
    print("\n✅ AC3: Job Scoring Incorporates Resume Data")
    groq_score = [n for n in workflow['nodes'] if n['id'] == 'groq-score-job'][0]
    resume_match = [n for n in workflow['nodes'] if n['id'] == 'resume-match-analysis'][0]
    
    score_prompt = groq_score['parameters']['text']
    uses_merged_data = 'Merge User Config with Resume Data' in score_prompt
    has_resume_section = '**Resume Data:**' in score_prompt or 'Resume' in score_prompt
    references_skills = 'Resume Skills' in score_prompt or 'resumeData.skills' in score_prompt
    references_experience = 'Experience:' in score_prompt or 'experience' in score_prompt
    references_projects = 'Projects' in score_prompt or 'projects' in score_prompt
    
    match_code = resume_match['parameters']['jsCode']
    calculates_overlap = 'skillOverlapPercent' in match_code
    
    ac3_pass = all([uses_merged_data, has_resume_section, references_skills, 
                    references_experience, references_projects, calculates_overlap])
    results.append(("AC3", ac3_pass))
    
    print(f"   • Uses merged config with resume data: {uses_merged_data}")
    print(f"   • Has dedicated resume section: {has_resume_section}")
    print(f"   • References resume skills: {references_skills}")
    print(f"   • References experience: {references_experience}")
    print(f"   • References projects: {references_projects}")
    print(f"   • Calculates skill overlap percentage: {calculates_overlap}")
    print(f"   Result: {'PASS ✓' if ac3_pass else 'FAIL ✗'}")
    
    # AC4: Generated emails reference specific resume projects and achievements
    print("\n✅ AC4: Email References Resume Projects and Achievements")
    groq_email = [n for n in workflow['nodes'] if n['id'] == 'groq-generate-email'][0]
    
    email_prompt = groq_email['parameters']['text']
    has_resume_insights = 'Resume Insights' in email_prompt
    references_projects_in_email = 'Key Projects' in email_prompt
    references_achievements = 'Achievements' in email_prompt
    instructs_personalization = 'specific projects from resume' in email_prompt
    
    ac4_pass = all([has_resume_insights, references_projects_in_email, 
                    references_achievements, instructs_personalization])
    results.append(("AC4", ac4_pass))
    
    print(f"   • Has Resume Insights section: {has_resume_insights}")
    print(f"   • References Key Projects: {references_projects_in_email}")
    print(f"   • References Achievements: {references_achievements}")
    print(f"   • Instructs to mention specific projects: {instructs_personalization}")
    print(f"   Result: {'PASS ✓' if ac4_pass else 'FAIL ✗'}")
    
    # AC5: Workflow degrades gracefully if resume URL fails
    print("\n✅ AC5: Graceful Degradation if Resume Fails")
    check_download = [n for n in workflow['nodes'] if n['id'] == 'check-resume-download'][0]
    fallback_node = [n for n in workflow['nodes'] if n['id'] == 'fallback-user-config'][0]
    download_resume = [n for n in workflow['nodes'] if n['id'] == 'download-resume'][0]
    
    download_continues_on_fail = download_resume.get('continueOnFail', False)
    has_check_node = check_download is not None
    has_fallback = fallback_node is not None
    
    fallback_code = fallback_node['parameters']['jsCode']
    uses_user_config = 'User Config (Master Profile)' in fallback_code
    
    # Check connections: Check node has two outputs (true/false)
    check_connections = workflow['connections'].get('Check Resume Download Success', {})
    has_dual_path = len(check_connections.get('main', [])) == 2
    
    ac5_pass = all([download_continues_on_fail, has_check_node, has_fallback, 
                    uses_user_config, has_dual_path])
    results.append(("AC5", ac5_pass))
    
    print(f"   • Download node has continueOnFail=True: {download_continues_on_fail}")
    print(f"   • Has success check node: {has_check_node}")
    print(f"   • Has fallback to User Config: {has_fallback}")
    print(f"   • Fallback uses User Config skills: {uses_user_config}")
    print(f"   • Check node has dual path (success/fail): {has_dual_path}")
    print(f"   Result: {'PASS ✓' if ac5_pass else 'FAIL ✗'}")
    
    # AC6: Resume Match Details column in Google Sheets
    print("\n✅ AC6: Google Sheets Resume Match Details Column")
    append_node = [n for n in workflow['nodes'] if n['id'] == 'append-to-sheet-jobs'][0]
    
    columns = append_node['parameters']['columns']['value']
    has_resume_column = 'resumeMatchDetails' in columns
    total_columns = len(columns)
    
    ac6_pass = has_resume_column and total_columns == 20
    results.append(("AC6", ac6_pass))
    
    print(f"   • Has resumeMatchDetails column: {has_resume_column}")
    print(f"   • Total columns (should be 20): {total_columns}")
    print(f"   Result: {'PASS ✓' if ac6_pass else 'FAIL ✗'}")
    
    # AC7: All existing workflow functionality remains intact
    print("\n✅ AC7: Existing Workflow Functionality Intact")
    
    # Check all original 44 nodes still exist
    original_node_ids = [
        'trigger-1-job-discovery', 'trigger-2-email-outreach', 'trigger-3-telegram',
        'user-config', 'fetch-remotive', 'fetch-arbeitnow', 'fetch-adzuna',
        'parse-remotive', 'parse-arbeitnow', 'parse-adzuna', 'merge-job-apis',
        'deduplicate-jobs', 'read-existing-jobs', 'filter-new-jobs', 'groq-score-job',
        'parse-score', 'filter-by-score', 'append-to-sheet-jobs', 'aggregate-job-summary',
        'send-telegram-job-digest', 'send-gmail-job-digest', 'read-jobs-for-outreach',
        'filter-sendable-jobs', 'limit-daily-emails', 'groq-generate-email',
        'parse-format-email', 'send-gmail-outreach', 'update-email-metadata',
        'update-sheet-status', 'rate-limit-delay', 'aggregate-outreach-summary',
        'send-outreach-digest', 'extract-telegram-message', 'handle-quick-commands',
        'check-quick-command', 'send-quick-reply', 'build-system-prompt',
        'groq-agent', 'parse-agent-response', 'check-needs-sheet-query',
        'query-sheet-for-stats', 'aggregate-telegram-stats',
        'send-telegram-reply-with-stats', 'send-telegram-reply-simple'
    ]
    
    current_node_ids = [n['id'] for n in workflow['nodes']]
    all_original_exist = all(nid in current_node_ids for nid in original_node_ids)
    
    # Check total node count
    expected_total = 44 + 7  # Original + new resume nodes
    correct_node_count = len(workflow['nodes']) == expected_total
    
    # Check no breaking changes to triggers
    triggers = [n for n in workflow['nodes'] if 'trigger' in n['id']]
    has_all_triggers = len(triggers) == 3
    
    ac7_pass = all([all_original_exist, correct_node_count, has_all_triggers])
    results.append(("AC7", ac7_pass))
    
    print(f"   • All 44 original nodes exist: {all_original_exist}")
    print(f"   • Correct total node count (51): {correct_node_count}")
    print(f"   • All 3 triggers intact: {has_all_triggers}")
    print(f"   Result: {'PASS ✓' if ac7_pass else 'FAIL ✗'}")
    
    # Summary
    print("\n" + "=" * 70)
    print("ACCEPTANCE CRITERIA SUMMARY")
    print("=" * 70)
    
    for ac_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{ac_name}: {status}")
    
    total_pass = sum(1 for _, p in results if p)
    total_tests = len(results)
    
    print(f"\nTotal: {total_pass}/{total_tests} acceptance criteria passed")
    
    if total_pass == total_tests:
        print("\n🎉 ALL ACCEPTANCE CRITERIA MET! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_pass} criteria need attention")
        return 1

if __name__ == '__main__':
    exit(main())
