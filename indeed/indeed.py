"""
Indeed Job Application Workflow

This script orchestrates the full Indeed SmartApply job application flow:
1. Navigate to job application URL
2. Upload resume
3. Fill contact information
4. Fill job experience
"""

import asyncio
from playwright.async_api import async_playwright

from upload_resume import upload_resume_to_indeed
from fill_contact_info import fill_contact_information
from fill_job_experience import fill_job_experience

CDP_URL = "http://localhost:9222"

INDEED_JOB_URL = "https://us.smartapply.indeed.com/beta/indeedapply/form/contact-info-module"


async def indeed_application_workflow(
    job_url: str = INDEED_JOB_URL,
    resume_path: str = "sample-resume.pdf",
    first_name: str = "Harry",
    last_name: str = "Potter",
    phone_number: str = "650-777-9340",
    zip_code: str = "95129",
    city_state: str = "San Jose, CA",
    street_address: str = "4 Privet Drive",
    job_title: str = "security officer",
    company_name: str = "warner bros",
):
    """
    Run the complete Indeed job application workflow.

    Args:
        job_url: URL of the Indeed job application
        resume_path: Path to the resume file
        first_name: Applicant's first name
        last_name: Applicant's last name
        phone_number: Phone number in XXX-XXX-XXXX format
        zip_code: Postal/zip code
        city_state: City and state
        street_address: Street address
        job_title: Current/most recent job title
        company_name: Current/most recent company name
    """
    print("=== Starting Indeed Application Workflow ===\n")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        # Step 1: Navigate to job application URL
        print("Step 1: Opening job application URL...")
        await page.goto(job_url, wait_until="load")
        await page.wait_for_timeout(1500)
        print(f"Navigated to: {job_url}\n")

        # Step 2: Upload resume
        print("Step 2: Uploading resume...")
        await upload_resume_to_indeed(page, resume_path=resume_path, skip_navigation=True)
        print()

        # Step 3: Fill contact information
        print("Step 3: Filling contact information...")
        await fill_contact_information(
            page,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            zip_code=zip_code,
            city_state=city_state,
            street_address=street_address,
            skip_navigation=True,
        )
        print()

        # Step 4: Fill job experience
        print("Step 4: Filling job experience...")
        await fill_job_experience(
            page,
            job_title=job_title,
            company_name=company_name,
            skip_navigation=True,
        )
        print()

    print("=== Indeed Application Workflow Complete ===")


if __name__ == "__main__":
    asyncio.run(indeed_application_workflow())
