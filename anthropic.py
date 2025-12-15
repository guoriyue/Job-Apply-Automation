import os
import re
import asyncio
from playwright.async_api import async_playwright


async def fill_anthropic_job_application(
    page,
    first_name: str = "Asuka",
    last_name: str = "Langley",
    email: str = "asuka.langley@nerv.org",
    country_phone: str = "United States +1",
    phone: str = "(650) 842-2015",
    resume_path: str = "sample-resume.pdf",
    personal_preferences: str = "Asuka",
    website: str = "https://asuka-langley.dev",
    publications_url: str = "https://scholar.google.com/citations?user=asuka_langley",
    github_url: str = "https://github.com/asuka-langley",
    in_person_work: str = "Yes",
    start_date: str = "January 15 2025",
    timeline_considerations: str = "No specific timeline constraints. Ready to start immediately.",
    ai_policy: str = "Yes",
    why_anthropic: str = "I am deeply passionate about building AI systems that are safe, beneficial, and aligned with human values. Anthropic's commitment to AI safety research and responsible development resonates strongly with my own philosophy. Having worked on complex autonomous systems at NERV, I understand the critical importance of building technology that humans can trust and control. I want to contribute to Claude's development and help ensure AI serves humanity's best interests. Plus, I never settle for second best - and Anthropic is clearly leading the frontier of safe AI development.",
    impressive_achievement: str = "At NERV, I optimized the neural synchronization algorithms for EVA Unit-02, achieving a 400% improvement in response latency by rewriting critical path code in hand-tuned assembly and implementing a novel lock-free data structure for real-time sensor fusion. I also developed a custom memory allocator that reduced GC pauses from 50ms to under 1ms, which was essential for maintaining pilot safety during combat operations. The system now processes over 10 million sensor readings per second with sub-millisecond latency.",
    additional_info: str = "Fluent in German, Japanese, and English. Graduated from university at age 13 with a degree in Computer Science. Former EVA pilot with extensive experience in high-pressure, mission-critical environments. Strong background in real-time systems, neural interfaces, and distributed computing. I bring both technical excellence and the determination to be the best at everything I do.",
    relocation_open: str = "Yes",
    previous_interview: str = "No",
    visa_sponsorship: str = "No",
    gender: str = "Female",
    hispanic_latino: str = "No",
    race: str = "Two or More Races",
    veteran_status: str = "I am not a protected veteran",
    disability_status: str = "No, I do not have a disability and have not had one in the past",
) -> None:
    """
    Fill out the Anthropic job application form.

    Args:
        page: Playwright page object
        first_name: Applicant's first name
        last_name: Applicant's last name
        email: Applicant's email address
        country_phone: Country and phone code. Options: United States +1, and other country codes
        phone: Phone number in format (XXX) XXX-XXXX
        resume_path: Path to resume file (PDF, DOC, DOCX, TXT, or RTF)
        personal_preferences: Personal preferences (optional field)
        website: Website URL (optional field)
        publications_url: Publications or Google Scholar URL (optional field)
        github_url: GitHub profile URL (optional field)
        in_person_work: Open to working in-person 25% of the time. Options: Yes, No
        start_date: Earliest start date (e.g., "March 1 2026")
        timeline_considerations: Timeline or deadline considerations (e.g., "No")
        ai_policy: Acknowledgment of AI policy. Options: Yes, No
        why_anthropic: Essay response on why interested in Anthropic
        impressive_achievement: Description of impressive low-level or performance achievement
        additional_info: Additional information textarea (optional)
        relocation_open: Open to relocation. Options: Yes, No
        previous_interview: Have interviewed at Anthropic before. Options: Yes, No
        visa_sponsorship: Requires visa sponsorship. Options: Yes, No
        gender: Gender identity. Options: Male, Female, Decline To Self Identify
        hispanic_latino: Hispanic or Latino ethnicity. Options: Yes, No, Decline To Self Identify
        race: Race/ethnicity. Options: American Indian or Alaskan Native, Asian, Black or African American,
            White, Native Hawaiian or Other Pacific Islander, Two or More Races, Decline To Self Identify
        veteran_status: Veteran status. Options: I am not a protected veteran,
            I identify as one or more of the classifications of a protected veteran, I don't wish to answer
        disability_status: Disability status. Options: Yes, I have a disability, or have had one in the past,
            No, I do not have a disability and have not had one in the past, I do not want to answer
    """

    # Navigate to the job application page
    await page.goto("https://job-boards.greenhouse.io/anthropic/jobs/4020350008", wait_until="load")
    await page.wait_for_timeout(1500)

    # ==================== SECTION 1: BASIC INFORMATION ====================

    # Fill First Name
    first_name_field = page.get_by_role("textbox", name=re.compile(r"^First Name\*?$"))
    await first_name_field.click()
    await first_name_field.fill(first_name)
    await page.wait_for_timeout(300)

    # Fill Last Name
    last_name_field = page.get_by_role("textbox", name=re.compile(r"^Last Name\*?$"))
    await last_name_field.click()
    await last_name_field.fill(last_name)
    await page.wait_for_timeout(300)

    # Fill Email
    email_field = page.get_by_role("textbox", name=re.compile(r"^Email\*?$"))
    await email_field.click()
    await email_field.fill(email)
    await page.wait_for_timeout(300)

    # Select Country Code for Phone
    country_dropdown = page.get_by_role("combobox", name=re.compile(r"^Country\*?$"))
    await country_dropdown.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=re.compile(f"^{re.escape(country_phone)}$")).click()
    await page.wait_for_timeout(300)

    # Fill Phone Number
    phone_field = page.get_by_role("textbox", name=re.compile(r"^Phone\*?$"))
    await phone_field.click()
    await phone_field.fill(phone)
    await page.wait_for_timeout(300)

    # Upload Resume/CV
    await page.wait_for_selector('input#resume', state="attached", timeout=3000)
    resume_abs_path = os.path.abspath(resume_path)
    await page.locator('input#resume').set_input_files(resume_abs_path)
    await page.wait_for_timeout(1000)

    # ==================== SECTION 2: APPLICATION QUESTIONS ====================

    # Scroll to next section
    await page.evaluate("window.scrollBy(0, 2330)")
    await page.wait_for_timeout(500)

    # Fill Personal Preferences (optional)
    personal_pref_field = page.get_by_role("textbox", name="Personal Preferences")
    await personal_pref_field.click()
    await personal_pref_field.fill(personal_preferences)
    await page.wait_for_timeout(300)

    # Fill Website (optional)
    website_field = page.get_by_role("textbox", name=re.compile(r"^Website\*?$"))
    await website_field.click()
    await website_field.fill(website)
    await page.wait_for_timeout(300)

    # Fill Publications URL (optional)
    publications_field = page.get_by_role("textbox", name=re.compile(r"^Publications.*Google Scholar.*\*?$", flags=re.DOTALL))
    await publications_field.click()
    await publications_field.fill(publications_url)
    await page.wait_for_timeout(300)

    # Fill GitHub URL (optional)
    github_field = page.get_by_role("textbox", name=re.compile(r"^GitHub.*\*?$"))
    await github_field.click()
    await github_field.fill(github_url)
    await page.wait_for_timeout(300)

    # Select In-Person Work Preference
    in_person_dropdown = page.get_by_role("combobox", name=re.compile(r".*in-person.*25%.*", flags=re.IGNORECASE | re.DOTALL))
    await in_person_dropdown.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=in_person_work).click()
    await page.wait_for_timeout(300)

    # Fill Start Date
    start_date_field = page.get_by_role("textbox", name=re.compile(r".*earliest.*start.*", flags=re.IGNORECASE | re.DOTALL))
    await start_date_field.click()
    await start_date_field.fill(start_date)
    await page.wait_for_timeout(300)

    # Fill Timeline Considerations
    timeline_field = page.get_by_role("textbox", name=re.compile(r".*deadlines.*timeline.*", flags=re.IGNORECASE | re.DOTALL))
    await timeline_field.click()
    await timeline_field.fill(timeline_considerations)
    await page.wait_for_timeout(300)

    # Scroll to continue
    await page.evaluate("window.scrollBy(0, 350)")
    await page.wait_for_timeout(500)

    # Select AI Policy
    ai_policy_dropdown = page.get_by_role("combobox", name=re.compile(r".*AI Policy.*", flags=re.IGNORECASE))
    await ai_policy_dropdown.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=ai_policy).click()
    await page.wait_for_timeout(300)

    # Fill Why Anthropic textarea
    why_anthropic_field = page.get_by_role("textbox", name=re.compile(r".*Why Anthropic.*", flags=re.IGNORECASE | re.DOTALL))
    await why_anthropic_field.click()
    await why_anthropic_field.fill(why_anthropic)
    await page.wait_for_timeout(300)

    # Fill Impressive Achievement textarea
    achievement_field = page.get_by_role("textbox", name=re.compile(r".*impressive.*low-level.*performance.*", flags=re.IGNORECASE | re.DOTALL))
    await achievement_field.click()
    await achievement_field.fill(impressive_achievement)
    await page.wait_for_timeout(300)

    # ==================== SECTION 3: ADDITIONAL QUESTIONS & EEOC ====================

    # Fill additional information field
    additional_info_field = page.get_by_role("textbox", name="Additional Information")
    await additional_info_field.click()
    await additional_info_field.fill(additional_info)
    await page.wait_for_timeout(300)

    # Fill relocation dropdown
    relocation_combo = page.get_by_role("combobox", name="Are you open to relocation for this role?")
    await relocation_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=relocation_open).click()
    await page.wait_for_timeout(500)

    # Scroll down to see more fields
    await page.evaluate("window.scrollBy(0, 500)")
    await page.wait_for_timeout(500)

    # Fill previous interview dropdown
    interview_combo = page.get_by_role("combobox", name="Have you ever interviewed at Anthropic before?")
    await interview_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=previous_interview).click()
    await page.wait_for_timeout(500)

    # Fill visa sponsorship dropdown
    visa_combo = page.get_by_role("combobox", name="Do you require visa sponsorship?")
    await visa_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=visa_sponsorship).click()
    await page.wait_for_timeout(500)

    # Scroll down
    await page.evaluate("window.scrollBy(0, 500)")
    await page.wait_for_timeout(500)

    # Fill gender dropdown
    gender_combo = page.get_by_role("combobox", name="Gender")
    await gender_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=gender).click()
    await page.wait_for_timeout(500)

    # Fill Hispanic/Latino dropdown
    hispanic_combo = page.get_by_role("combobox", name="Are you Hispanic/Latino?")
    await hispanic_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=hispanic_latino).click()
    await page.wait_for_timeout(500)

    # Fill race dropdown
    race_combo = page.get_by_role("combobox", name="Please identify your race")
    await race_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=race).click()
    await page.wait_for_timeout(500)

    # Fill veteran status dropdown
    veteran_combo = page.get_by_role("combobox", name="Veteran Status")
    await veteran_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=veteran_status).click()
    await page.wait_for_timeout(500)

    # Scroll down
    await page.evaluate("window.scrollBy(0, 500)")
    await page.wait_for_timeout(500)

    # Fill disability status dropdown
    disability_combo = page.get_by_role("combobox", name="Disability Status")
    await disability_combo.click()
    await page.wait_for_timeout(500)
    await page.get_by_role("option", name=disability_status).click()
    await page.wait_for_timeout(500)

    # Form submission is handled separately or after this function completes
    print("Job application form filled successfully!")


if __name__ == "__main__":
    CDP_URL = "http://localhost:9222"  # Set to None for new browser

    async def main():
        async with async_playwright() as p:
            if CDP_URL:
                # Connect to existing browser via CDP
                browser = await p.chromium.connect_over_cdp(CDP_URL)
                ctx = browser.contexts[0]
                page = await ctx.new_page()
            else:
                # Launch new headless browser
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()

            try:
                # Call the function with custom parameters or defaults
                await fill_anthropic_job_application(page)

                # Optional: Wait before closing to see results
                await page.wait_for_timeout(2000)

            finally:
                await browser.close()

    asyncio.run(main())
