"""
NVIDIA Job Application Automation

Automates filling out a job application form on NVIDIA's Workday careers site.
Specifically fills in the Education section with school information, degree,
field of study, GPA, and years attended.
"""

import asyncio
from playwright.async_api import async_playwright, Page

CDP_URL = "http://localhost:9222"


async def complete_nvidia_education_application(
    school_name: str = "Stanford University",
    degree_selection: str = "0c40f6bd1d8f10ae2a312e6b440c8d82",
    field_of_study: str = "Computer Science",
    gpa: str = "3.8",
    start_year: str = "2015",
    end_year: str = "2019",
) -> None:
    """
    Complete the Education section of NVIDIA job application form.

    This function automates the process of filling out the second education entry
    in a NVIDIA Workday job application. It navigates through the form, fills in
    school information, selects degree type, enters field of study, GPA, and
    the years the applicant attended the institution.

    Args:
        school_name: Name of the school or university (default: "Stanford University")
        degree_selection: Internal ID for degree selection -
                         "0c40f6bd1d8f10ae2a312e6b440c8d82" for PhD
        field_of_study: Field of study (default: "Computer Science")
        gpa: Overall Result/GPA (default: "3.8")
        start_year: Start year (default: "2015")
        end_year: End year (default: "2019")

    Returns:
        None
    """

    async with async_playwright() as p:
        # Attach to existing Chrome via CDP
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        page: Page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        try:
            # Navigate to the application page
            url = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US,-CA,-Santa-Clara/Senior-Manager--Robotics-Quality-Assurance_JR2003248/apply"
            await page.goto(url, wait_until="load")
            await page.wait_for_timeout(1500)

            # Scroll to Education section
            await page.evaluate("window.scrollBy(0, 2073)")
            await page.wait_for_timeout(500)

            # Click "Add Another" button to add second education entry
            add_another_button = page.locator(
                '//div[@id="root"]/div/div/div[2]/div/main/div/div[3]/div[1]/div[2]/div[3]/div[3]/div/div/button'
            )
            await add_another_button.click()
            await page.wait_for_timeout(500)

            # Scroll to Education 2 section
            await page.evaluate("window.scrollBy(0, -120)")
            await page.wait_for_timeout(500)

            # Fill in School/University name for Education 2
            school_input = page.locator('//input[@id="education-41--schoolName"]')
            await school_input.click()
            await school_input.fill(school_name)
            await page.wait_for_timeout(300)

            # Click on Degree dropdown
            degree_button = page.locator('//button[@id="education-41--degree"]')
            await degree_button.click()
            await page.wait_for_timeout(500)

            # Set the degree selection (PhD)
            degree_input = page.locator(
                '//div[@id="root"]/div/div/div[2]/div/main/div/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/input'
            )
            await degree_input.fill(degree_selection)
            await page.wait_for_timeout(500)

            # Fill in Field of Study
            field_of_study_input = page.locator('//input[@id="education-41--fieldOfStudy"]')
            await field_of_study_input.click()
            await field_of_study_input.fill(field_of_study)
            await page.wait_for_timeout(800)

            # Fill in GPA
            gpa_input = page.locator('//input[@id="education-41--gradeAverage"]')
            await gpa_input.click()
            await gpa_input.fill(gpa)
            await page.wait_for_timeout(300)

            # Fill in Start Year
            start_year_input = page.locator(
                '//input[@id="education-41--firstYearAttended-dateSectionYear-input"]'
            )
            await start_year_input.click()
            await start_year_input.fill(start_year)
            await page.wait_for_timeout(300)

            # Fill in End Year
            end_year_input = page.locator(
                '//input[@id="education-41--lastYearAttended-dateSectionYear-input"]'
            )
            await end_year_input.click()
            await end_year_input.fill(end_year)
            await page.wait_for_timeout(500)

            print("Education section filled successfully!")

        except Exception as e:
            print(f"Error occurred during automation: {str(e)}")
            raise

        # Don't close browser - it's the user's Chrome


if __name__ == "__main__":
    # Example usage - fill education section with custom values
    asyncio.run(
        complete_nvidia_education_application(
            school_name="Stanford University",
            degree_selection="0c40f6bd1d8f10ae2a312e6b440c8d82",  # PhD
            field_of_study="Computer Science",
            gpa="3.8",
            start_year="2015",
            end_year="2019"
        )
    )
