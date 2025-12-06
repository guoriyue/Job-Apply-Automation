"""
Playwright automation script for filling out NVIDIA job application form.

This script fills in work experience details on the NVIDIA career application page.
It handles a multi-step work experience form with job titles, company names, dates, and role descriptions.
"""

import asyncio
from playwright.async_api import async_playwright, Page

CDP_URL = "http://localhost:9222"


async def fill_work_experience_form(
    job_title: str = "Software Engineer",
    company_name: str = "Tech Company Inc",
    start_month: int = 1,
    start_year: int = 2020,
    end_month: int = 12,
    end_year: int = 2023,
    role_description: str = "Developed and maintained software applications, collaborated with cross-functional teams, and implemented new features.",
) -> None:
    """
    Fill out the work experience section of the NVIDIA job application form.

    This function navigates to the NVIDIA careers page and fills in a second work experience
    entry with the provided job details. It assumes the page is already loaded at the correct URL.

    Args:
        job_title: The job title to enter (default: "Software Engineer")
        company_name: The company name to enter (default: "Tech Company Inc")
        start_month: The starting month as an integer (1-12) (default: 1)
        start_year: The starting year as an integer (default: 2020)
        end_month: The ending month as an integer (1-12) (default: 12)
        end_year: The ending year as an integer (default: 2023)
        role_description: The role description/summary (default: "Developed and maintained software applications...")
    """
    async with async_playwright() as p:
        # Attach to existing Chrome via CDP
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        page: Page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        try:
            # Navigate to the NVIDIA job application page
            url = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US,-CA,-Santa-Clara/Senior-Manager--Robotics-Quality-Assurance_JR2003248/apply/autofillWithResume"
            await page.goto(url, wait_until="load")
            await page.wait_for_timeout(1500)

            # Scroll to the "Add Another" button for Work Experience
            await page.locator('xpath=//div[@id="root"]/div/div/div[2]/div/main/div/div[3]/div[1]/div[2]/div[1]/div[3]/div/div/button').click()
            await page.wait_for_timeout(500)

            # Scroll down to see the new work experience entry
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(500)

            # Fill in Job Title for Work Experience 2
            job_title_input = page.locator('xpath=//input[@id="workExperience-71--jobTitle"]')
            await job_title_input.click()
            await job_title_input.fill(job_title)
            await page.wait_for_timeout(300)

            # Fill in Company Name
            company_input = page.locator('xpath=//input[@id="workExperience-71--companyName"]')
            await company_input.click()
            await company_input.fill(company_name)
            await page.wait_for_timeout(300)

            # Fill in Start Date - Month
            start_month_input = page.locator('xpath=//input[@id="workExperience-71--startDate-dateSectionMonth-input"]')
            await start_month_input.click()
            await start_month_input.fill(str(start_month))
            await page.wait_for_timeout(300)

            # Fill in Start Date - Year
            start_year_input = page.locator('xpath=//input[@id="workExperience-71--startDate-dateSectionYear-input"]')
            await start_year_input.click()
            await start_year_input.fill(str(start_year))
            await page.wait_for_timeout(500)

            # Fill in End Date - Month
            end_month_input = page.locator('xpath=//input[@id="workExperience-71--endDate-dateSectionMonth-input"]')
            await end_month_input.click()
            await end_month_input.fill(str(end_month))
            await page.wait_for_timeout(300)

            # Fill in End Date - Year
            end_year_input = page.locator('xpath=//input[@id="workExperience-71--endDate-dateSectionYear-input"]')
            await end_year_input.click()
            await end_year_input.fill(str(end_year))
            await page.wait_for_timeout(500)

            # Scroll down to see Role Description field
            await page.evaluate("window.scrollBy(0, 300)")
            await page.wait_for_timeout(500)

            # Fill in Role Description
            role_desc_input = page.locator('xpath=//textarea[@id="workExperience-71--roleDescription"]')
            await role_desc_input.click()
            await role_desc_input.fill(role_description)
            await page.wait_for_timeout(500)

            print("Work experience form filled successfully!")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise

        # Don't close browser - it's the user's Chrome


if __name__ == "__main__":
    # Example usage - run the automation with default values
    asyncio.run(fill_work_experience_form())

    # Example usage with custom values:
    # asyncio.run(fill_work_experience_form(
    #     job_title="Software Engineer",
    #     company_name="Tech Company Inc",
    #     start_month=1,
    #     start_year=2020,
    #     end_month=12,
    #     end_year=2023,
    #     role_description="Developed and maintained software applications"
    # ))
