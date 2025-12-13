"""
Expedia Workday Job Application Workflow

This script orchestrates the full job application flow:
1. Upload resume and autofill
2. Fill personal information (includes how you heard, phone, and saves form)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import asyncio
from playwright.async_api import async_playwright
from workday.general import open_job_application_url, apply_with_resume
from workday.expedia.personal_info import fill_job_application_info

CDP_URL = "http://localhost:9222"


EXPEDIA_JOB_URL = "https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1/apply/autofillWithResume?source=&source=Appcast_Indeed"


async def expedia_application_workflow(
    job_url: str = EXPEDIA_JOB_URL,
    resume_path: str = "resume.pdf",
    how_did_you_hear_about_us: str = "Company Career Site",
    country: str = "United States of America",
    first_name: str = "John",
    last_name: str = "Doe",
    phone_device_type: str = "Mobile",
    country_phone_code: str = "United States of America (+1)",
    phone_number: str = "6504443333",
    address_line_1: str = "",
    city: str = "",
    state: str = "",
    postal_code: str = "",
    phone_extension: str = "",
) -> None:
    """
    Run the complete Expedia job application workflow.

    Args:
        job_url: URL of the job application page
        resume_path: Path to the resume file
        how_did_you_hear_about_us: How applicant learned about the position
        country: Country of residence
        first_name: Applicant's first name
        last_name: Applicant's last name
        phone_device_type: Type of phone device (Business, Mobile, Telephone)
        country_phone_code: Country phone code (e.g., "United States of America (+1)")
        phone_number: Applicant's phone number
        address_line_1: First line of street address (optional)
        city: City of residence (optional)
        state: State/Province of residence (optional)
        postal_code: Postal code (optional)
        phone_extension: Phone extension number (optional)
    """
    print("=== Starting Expedia Application Workflow ===\n")

    # Connect to browser - all steps share the same page
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        # Step 1: Open job application URL
        print("Step 1: Opening job application URL...")
        await open_job_application_url(page, job_url)
        print("URL opened.\n")

        # # Step 2: Upload resume and click Continue
        # print("Step 2: Uploading resume...")
        # await apply_with_resume(
        #     page=page,
        #     resume_path=resume_path,
        # )
        # print("Resume upload complete.\n")

        # Step 3: Fill personal information (includes how you heard, phone, and saves)
        print("Step 2: Filling personal information...")
        await fill_job_application_info(
            page=page,
            how_did_you_hear_about_us=how_did_you_hear_about_us,
            country=country,
            first_name=first_name,
            last_name=last_name,
            phone_device_type=phone_device_type,
            country_phone_code=country_phone_code,
            phone_number=phone_number,
            address_line_1=address_line_1,
            city=city,
            state=state,
            postal_code=postal_code,
            phone_extension=phone_extension,
        )
        print("Personal info complete.\n")

    print("=== Workflow Complete ===")


if __name__ == "__main__":
    asyncio.run(expedia_application_workflow(resume_path="sample-resume.pdf"))
