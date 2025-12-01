"""
Playwright automation for OpenAI job application form.

This script automates filling out and submitting a job application form
on the OpenAI jobs portal (Ashby ATS).
"""

import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright, Page


async def submit_openai_job_application(
    name: str = "Nico",
    email: str = "nico@gmail.com",
    github_url: str = "github.com/nico",
    linkedin_url: str = "linkedin.com/in/nico",
    resume_path: str = "sample-resume.pdf",
    phone_number: str = "1-222-333-4444",
    location: str = "San Mateo, California, United States",
    start_date: str = "12/31/2025",
    require_sponsorship: bool = False,
    can_work_from_sf_office: bool = True,
) -> None:
    """
    Automate OpenAI job application submission.

    Args:
        name: Full name of the applicant
        email: Email address of the applicant
        github_url: GitHub profile URL
        linkedin_url: LinkedIn profile URL
        resume_path: Path to resume PDF file (relative or absolute)
        phone_number: Phone number in format like "1-222-333-4444"
        location: Work location preference
        start_date: Available start date in MM/DD/YYYY format
        require_sponsorship: Whether visa sponsorship is required
        can_work_from_sf_office: Whether applicant can work from SF office 3 days/week
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to the job application URL
            url = "https://jobs.ashbyhq.com/openai/43174eb6-0ffe-4744-9323-c7969e7ea2e1/application"
            await page.goto(url, wait_until="load")
            await page.wait_for_timeout(1500)

            # Fill Name field
            name_input = page.locator("//input[@id='_systemfield_name']")
            await name_input.click()
            await name_input.fill(name)
            await page.wait_for_timeout(300)

            # Fill Email field
            email_input = page.locator("//input[@id='_systemfield_email']")
            await email_input.click()
            await email_input.fill(email)
            await page.wait_for_timeout(300)

            # Fill GitHub Link field (ID starts with digit, use attribute selector)
            github_input = page.locator('input[id="44d2e6b6-9bdf-44ab-b068-3d70459b2b61"]')
            await github_input.click()
            await github_input.fill(github_url)
            await page.wait_for_timeout(300)

            # Fill LinkedIn Profile field (ID starts with digit, use attribute selector)
            linkedin_input = page.locator('input[id="dfc4cc4e-8ea1-41af-8fad-2c436934bdd9"]')
            await linkedin_input.click()
            await linkedin_input.fill(linkedin_url)
            await page.wait_for_timeout(300)

            # Upload Resume
            abs_resume_path = os.path.abspath(resume_path)
            file_input = page.locator('input[id="_systemfield_resume"]')
            await file_input.set_input_files(abs_resume_path)
            await page.wait_for_timeout(1000)

            # Scroll down to find phone number field
            await page.wait_for_timeout(500)

            # Fill Phone Number field (ID starts with digit, use attribute selector)
            phone_input = page.locator('input[id="d5fd375a-e8e3-420a-b915-d70085f610b2"]')
            await phone_input.click()
            await phone_input.fill(phone_number)
            await page.wait_for_timeout(300)

            # Fill Location field using combobox with dropdown interaction
            location_input = page.locator("//div[@id='form']/div[3]/div/div[7]/div/input")
            await location_input.click()
            await location_input.fill("san mateo")
            await page.wait_for_timeout(500)

            # Click the location option from dropdown
            # Using aria selector to find the option with "San Mateo, California, United States"
            location_option = page.locator("text=San Mateo, California, United States").first
            await location_option.click()
            await page.wait_for_timeout(500)

            # Fill Start Date using date picker
            # Click on date input to open picker
            date_input = page.locator(
                "//div[@id='form']/div[3]/div/div[8]/div[1]/div/input"
            )
            await date_input.click()
            await page.wait_for_timeout(500)

            # Click next month button to go to December 2025
            next_month_btn = page.locator(
                "//div[@id='form']/div[3]/div/div[8]/div[2]/div/div/div[2]/div[1]/div[1]/div/button[2]"
            )
            await next_month_btn.click()
            await page.wait_for_timeout(300)

            # Click on day 31 in December
            # day_31 = page.locator("text=31").filter(has_role="option").last
            day_31 = page.get_by_role("option", name="31").last
            await day_31.click()
            await page.wait_for_timeout(500)

            # Answer visa sponsorship question based on require_sponsorship parameter
            if require_sponsorship:
                # Click "Yes" button (first button)
                sponsorship_btn = page.locator(
                    "//div[@id='form']/div[3]/div/div[9]/div[2]/button[1]"
                )
            else:
                # Click "No" button (second button)
                sponsorship_btn = page.locator(
                    "//div[@id='form']/div[3]/div/div[9]/div[2]/button[2]"
                )
            await sponsorship_btn.click()
            await page.wait_for_timeout(300)

            # Answer SF office attendance question based on can_work_from_sf_office parameter
            if can_work_from_sf_office:
                # Click "Yes" button (first button)
                sf_office_btn = page.locator(
                    "//div[@id='form']/div[3]/div/div[10]/div/button[1]"
                )
            else:
                # Click "No" button (second button)
                sf_office_btn = page.locator(
                    "//div[@id='form']/div[3]/div/div[10]/div/button[2]"
                )
            await sf_office_btn.click()
            await page.wait_for_timeout(500)

            print("Application form completed successfully!")

        except Exception as e:
            print(f"Error during application submission: {e}")
            raise
        finally:
            await context.close()
            await browser.close()


async def main():
    """Run the application automation with example parameters."""
    # await submit_openai_job_application(
    #     name="Nico",
    #     email="nico@gmail.com",
    #     github_url="github.com/nico",
    #     linkedin_url="linkedin.com/in/nico",
    #     resume_path="sample-resume.pdf",
    #     phone_number="1-222-333-4444",
    #     location="San Mateo, California, United States",
    #     start_date="12/31/2025",
    #     require_sponsorship=False,
    #     can_work_from_sf_office=True,
    # )
    
    await submit_openai_job_application(
        name="Kamisato Ayaka",
        email="ayaka@gmail.com",
        github_url="github.com/ayaka",
        linkedin_url="linkedin.com/in/ayaka",
        resume_path="sample-resume.pdf",
        phone_number="1-222-333-4444",
        location="Inazuma, Teyvat",
        start_date="12/31/2025",
        require_sponsorship=True,
        can_work_from_sf_office=False,
    )


if __name__ == "__main__":
    asyncio.run(main())
