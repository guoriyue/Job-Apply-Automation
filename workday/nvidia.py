"""
NVIDIA Workday Job Application Workflow

This script orchestrates the full job application flow:
1. Upload resume and autofill
2. Fill personal information
"""

import asyncio
from playwright.async_api import async_playwright
from upload_resume import upload_resume
from personal_info import fill_personal_info
from how_you_heard import how_you_heard_about_us
from phone_number import fill_phone_number
from save_and_continue import save_and_continue

CDP_URL = "http://localhost:9222"


async def nvidia_application_workflow(
    resume_path: str = "resume.pdf",
    job_url: str = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US,-CA,-Santa-Clara/Senior-ASIC-Test-Timing-Engineer_JR2005476?source=Eightfold",
    first_name: str = "John",
    last_name: str = "Doe"
) -> None:
    """
    Run the complete NVIDIA job application workflow.

    Args:
        resume_path: Path to the resume file
        job_url: The job posting URL
        first_name: Applicant's first name
        last_name: Applicant's last name
        has_preferred_name: Whether to check the preferred name checkbox
    """
    print("=== Starting NVIDIA Application Workflow ===\n")

    # Connect to browser - all steps share the same page
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        # Navigate to job posting URL first
        print(f"Navigating to job posting: {job_url}")
        await page.goto(job_url, wait_until="load")
        await page.wait_for_timeout(1500)
        await page.set_viewport_size({"width": 1508, "height": 859})

        # Click the Apply button
        print("Clicking Apply button...")
        apply_button = page.locator('xpath=//div[@id="mainContent"]/div/div[1]/div[1]/div[1]/div/div/div/div/div/a')
        await apply_button.click()
        await page.wait_for_timeout(1000)

        # Step 1: Upload resume
        print("Step 1: Uploading resume...")
        await upload_resume(
            page=page,
            resume_path=resume_path,
        )
        print("Resume upload complete.\n")

        # Step 2: Fill "How you heard about us"
        print("Step 2: Filling 'How you heard about us'...")
        await how_you_heard_about_us(
            page=page,
            how_heard="Event/Conference",
            event_conference="GTC 2025",
            previous_employee=False,
        )
        print("How you heard about us complete.\n")

        # Step 3: Fill personal information
        print("Step 3: Filling personal information...")
        await fill_personal_info(
            page=page,
            first_name=first_name,
            last_name=last_name
        )
        
        await fill_phone_number(
            page=page,
            phone_device_type="Home",
            country_phone_code="+1",
            phone_number="6504443333",
        )
        
        await save_and_continue(
            page=page,
        )
        print("Personal info complete.\n")
        
        await add_education(
            page=page,
            education_type="Bachelor's Degree",
            school_name="Stanford University",
            degree="Bachelor of Science in Computer Science",
            start_month="2020",
            end_month="2024",
        )
        print("Education complete.\n")
        
        await add_work_experience(
            page=page,
            job_title="Software Engineer",
            company_name="NVIDIA",
            start_month="2024",
            end_month="2025",
        )
        print("Work experience complete.\n")
        
        await add_url(
            page=page,
            linkedin_url="https://www.linkedin.com/in/johndoe",
            github_url="https://github.com/johndoe",
        )
        print("URLs complete.\n")
        
        await save_and_continue(
            page=page,
        )
        

    print("=== Workflow Complete ===")


if __name__ == "__main__":
    asyncio.run(nvidia_application_workflow(resume_path="sample-resume.pdf"))
