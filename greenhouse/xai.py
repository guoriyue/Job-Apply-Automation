"""
Playwright automation script for XAI job application form submission.
Fills out the Greenhouse job application form with provided information.
"""

import os
import asyncio
from playwright.async_api import async_playwright


async def fill_xai_job_application(
    page,
    first_name: str = "Hermione",
    last_name: str = "Granger",
    email: str = "hermione.granger@hogwarts.edu",
    country: str = "United Kingdom +44",
    phone: str = "7700900123",
    resume_path: str = "sample-resume.pdf",
    website: str = "https://hermione-granger.dev",
    linkedin_profile: str = "https://linkedin.com/in/hermione-granger",
    ideal_candidate_response: str = "I bring a unique combination of analytical rigor and creative problem-solving honed through years of tackling complex challenges. My background includes developing novel algorithms for pattern recognition, optimizing distributed systems under extreme constraints, and leading cross-functional teams to deliver mission-critical projects. I thrive in fast-paced environments where precision and innovation are paramount, and I'm deeply motivated by xAI's mission to advance our understanding of the universe through AI.",
    exceptional_work_response: str = "I architected and implemented a real-time spell-checking system that processes millions of queries per second with sub-millisecond latency, using a novel trie-based data structure I designed. I also led the development of an automated research assistant that synthesized information from over 10,000 ancient texts, reducing research time by 95%. Most notably, I developed a time-series prediction model that achieved state-of-the-art accuracy in forecasting rare events, which was later adopted as the standard approach in the field.",
    visa_sponsorship: str = "No",
    full_legal_name: str = "Hermione Jean Granger",
    how_heard_about_job: str = "LinkedIn",
    please_specify: str = "Recommended by a colleague in the AI research community",
    x_profile: str = "https://x.com/hermionegranger",
):
    """
    Fill out the XAI job application form on Greenhouse.

    Args:
        page: Playwright page object
        first_name: Applicant's first name
        last_name: Applicant's last name
        email: Applicant's email address
        country: Phone country code. Options: United States +1, United Arab Emirates +971,
            United Kingdom +44, and many others
        phone: Applicant's phone number
        resume_path: Path to resume file (PDF, DOC, DOCX, TXT, or RTF)
        website: Website/portfolio URL
        linkedin_profile: LinkedIn profile URL
        ideal_candidate_response: Response to "What makes you the ideal candidate for this position?"
        exceptional_work_response: Response to "What exceptional work have you done?"
        visa_sponsorship: Visa sponsorship requirement (Yes or No)
        full_legal_name: Full legal name
        how_heard_about_job: How applicant heard about the job
        please_specify: Specification if other source was selected
        x_profile: X (formerly Twitter) profile URL
    """

    # Navigate to the job posting page
    await page.goto(
        "https://job-boards.greenhouse.io/xai/jobs/4977264007",
        wait_until="load"
    )
    await page.wait_for_timeout(1500)

    # Fill First Name
    await page.get_by_role("textbox", name="First Name").click()
    await page.get_by_role("textbox", name="First Name").fill(first_name)
    await page.wait_for_timeout(300)

    # Fill Last Name
    await page.get_by_role("textbox", name="Last Name").click()
    await page.get_by_role("textbox", name="Last Name").fill(last_name)
    await page.wait_for_timeout(300)

    # Fill Email
    await page.get_by_role("textbox", name="Email").click()
    await page.get_by_role("textbox", name="Email").fill(email)
    await page.wait_for_timeout(300)

    # Handle Country dropdown (custom dropdown with combobox)
    await page.wait_for_timeout(500)
    country_input = page.get_by_role("combobox", name="Country")
    await country_input.click()
    await country_input.fill("united")
    await page.wait_for_timeout(500)

    # Click the appropriate country option
    # Using dynamic ID matching since the option ID contains numbers
    await page.locator("#react-select-country-option-232").click()
    await page.wait_for_timeout(300)

    # Fill Phone number
    await page.get_by_role("textbox", name="Phone").fill(phone)
    await page.wait_for_timeout(300)

    # Upload Resume
    await page.get_by_label("Resume/CV*").get_by_role("button", name="Attach").click()
    await page.wait_for_timeout(300)
    resume_full_path = os.path.abspath(resume_path)
    await page.locator("#resume").set_input_files(resume_full_path)
    await page.wait_for_timeout(1000)

    # Scroll to next section
    await page.wait_for_timeout(500)

    # Fill Website
    await page.get_by_role("textbox", name="Website").click()
    await page.get_by_role("textbox", name="Website").fill(website)
    await page.wait_for_timeout(300)

    # Fill LinkedIn Profile
    await page.locator("#question_10758823007-label").click()
    await page.wait_for_timeout(300)
    await page.get_by_role("textbox", name="LinkedIn Profile").fill(linkedin_profile)
    await page.wait_for_timeout(300)

    # Fill "What makes you the ideal candidate for this position?"
    await page.locator("#question_10758824007-label").click()
    await page.wait_for_timeout(300)
    await page.get_by_role(
        "textbox",
        name="What makes you the ideal candidate for this position?"
    ).fill(ideal_candidate_response)
    await page.wait_for_timeout(300)

    # Fill "What exceptional work have you done?"
    await page.get_by_role(
        "textbox",
        name="What exceptional work have you done?"
    ).click()
    await page.wait_for_timeout(300)
    await page.get_by_role(
        "textbox",
        name="What exceptional work have you done?"
    ).fill(exceptional_work_response)
    await page.wait_for_timeout(300)

    # Handle visa sponsorship dropdown
    await page.wait_for_timeout(500)
    # Click on the dropdown using its label
    visa_dropdown = page.locator("label:has-text('Will you now, or in the future, require sponsorship')").locator("..").locator("[class*='select__control']")
    await visa_dropdown.click()
    await page.wait_for_timeout(500)

    # Select Yes or No based on visa_sponsorship parameter
    if visa_sponsorship == "Yes":
        await page.get_by_text("Yes", exact=True).click()
    else:
        await page.get_by_text("No", exact=True).click()
    await page.wait_for_timeout(300)

    # Fill Full Legal Name
    await page.get_by_role("textbox", name="Full Legal Name").click()
    await page.get_by_role("textbox", name="Full Legal Name").fill(full_legal_name)
    await page.wait_for_timeout(300)

    # Fill "How did you hear about this job?"
    await page.get_by_role("textbox", name="How did you hear about this job?").click()
    await page.get_by_role("textbox", name="How did you hear about this job?").fill(how_heard_about_job)
    await page.wait_for_timeout(300)

    # Fill "Please specify."
    await page.get_by_role("textbox", name="Please specify.").click()
    await page.get_by_role("textbox", name="Please specify.").fill(please_specify)
    await page.wait_for_timeout(300)

    # Fill X Profile
    await page.get_by_role("textbox", name="X Profile").click()
    await page.get_by_role("textbox", name="X Profile").fill(x_profile)
    await page.wait_for_timeout(300)

    print("Application form filled successfully!")


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
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

            try:
                # Call the automation function with default or custom parameters
                await fill_xai_job_application(page)
            finally:
                await browser.close()

    asyncio.run(main())
