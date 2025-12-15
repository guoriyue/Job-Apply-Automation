"""
NVIDIA Workday Job Application Workflow

This script orchestrates the full job application flow:
1. Upload resume and autofill
2. Fill personal information
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import asyncio
from playwright.async_api import async_playwright
from workday.nvidia import (
    upload_resume,
    fill_phone_number,
    save_and_continue,
    click_add_work_experience,
    click_add_another_work_experience,
    fill_work_experience,
    click_add_education,
    click_add_another_education,
    fill_education,
    add_urls,
)
from workday.nvidia.personal_info import fill_personal_info
from workday.nvidia.how_you_heard import how_you_heard_about_us

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

        # # Step 1: Upload resume
        # print("Step 1: Uploading resume...")
        # await upload_resume(
        #     page=page,
        #     resume_path=resume_path,
        # )
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
        

        # First work experience: click "Add" then fill
        await click_add_work_experience(page)
        await fill_work_experience(
            page=page,
            index=0,
            job_title="Software Engineer",
            company_name="NVIDIA",
            start_month=1,
            start_year=2024,
            end_month=1,
            end_year=2025,
        )
        print("Work experience 1 complete.\n")

        # Second work experience: click "Add Another" then fill
        await click_add_another_work_experience(page)
        await fill_work_experience(
            page=page,
            index=-1,
            job_title="Intern",
            company_name="Meta",
            start_month=1,
            start_year=2020,
            end_month=1,
            end_year=2023,
        )
        print("Work experience 2 complete.\n")
        
        # First education: click "Add" then fill
        await click_add_education(page)
        await fill_education(
            page=page,
            index=-1,  # Fill the newly added entry
            school_name="Stanford University",
            degree="PhD",
            field_of_study="Computer Science",
            gpa="3.8",
            start_year=2020,
            end_year=2024,
        )
        print("Education complete.\n")

        # Second education: click "Add Another" then fill
        await click_add_another_education(page)
        await fill_education(
            page=page,
            index=-1,  # Fill the newly added entry
            school_name="MIT",
            degree="PhD",
            field_of_study="Computer Science",
            gpa="3.8",
            start_year=2000,
            end_year=2005,
        )
        print("Education 2 complete.\n")
        
        await add_urls(
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
