"""
Automation script for Expedia job application on Workday.
Fills out job application with work experience and education information.
"""

import os
import re
from datetime import datetime


async def fill_job_application(
    page,
    work_experiences: list = None,
    educations: list = None,
):
    """
    Fill out the Expedia job application form with work experience and education.

    Args:
        page: Playwright page object
        work_experiences: List of work experience dictionaries with keys:
            - job_title (str): Job title
            - company (str): Company name
            - location (str, optional): Job location
            - start_month (int): Start month (1-12)
            - start_year (int): Start year
            - end_month (int): End month (1-12)
            - end_year (int): End year
            - role_description (str, optional): Description of role
        educations: List of education dictionaries with keys:
            - school_name (str): School or university name
            - degree (str): Degree type (e.g., "Masters", "Doctorate")
            - field_of_study (str): Field of study
            - gpa (str): GPA/Grade average
    """

    # Default values for testing
    if work_experiences is None:
        work_experiences = [
            {
                "job_title": "Senior Software Engineer",
                "company": "Google",
                "location": "Mountain View, CA",
                "start_month": 6,
                "start_year": 2020,
                "end_month": 12,
                "end_year": 2024,
                "role_description": "Led development of scalable microservices architecture serving 10M+ users.",
            },
            {
                "job_title": "Software Engineer",
                "company": "Amazon",
                "location": "Seattle, WA",
                "start_month": 7,
                "start_year": 2017,
                "end_month": 5,
                "end_year": 2020,
                "role_description": "Developed backend services for AWS Lambda.",
            },
        ]

    if educations is None:
        educations = [
            {
                "school_name": "Stanford University",
                "degree": "Masters",
                "field_of_study": "Computer Science",
                "gpa": "3.85",
            },
            {
                "school_name": "University of California, Berkeley",
                "degree": "Bachelors",
                "field_of_study": "Electrical Engineering",
                "gpa": "3.72",
            },
        ]

    # Fill work experience sections
    for idx, work_exp in enumerate(work_experiences):
        if idx == 0:
            # Click "Add" button for first work experience entry
            work_exp_section = page.get_by_role("group", name="Work Experience")
            add_button = work_exp_section.get_by_role("button", name="Add")
            await add_button.click()
            await page.wait_for_timeout(500)
            await page.evaluate("window.scrollBy(0, 300)")
            await page.wait_for_timeout(300)
            print("Clicked 'Add' button in Work Experience")
        else:
            # Click "Add Another" button to add new work experience
            work_exp_section = page.get_by_role("group", name="Work Experience")
            add_another_button = work_exp_section.get_by_role("button", name="Add Another")
            await add_another_button.click()
            await page.wait_for_timeout(500)
            await page.evaluate("window.scrollBy(0, 300)")
            await page.wait_for_timeout(300)
            print("Clicked 'Add Another' button in Work Experience")

        # Scroll to work experience section
        await page.wait_for_timeout(300)

        # Fill Job Title
        job_title_field = page.get_by_role("textbox", name=re.compile(r"^Job Title\*?$"))
        await job_title_field.click()
        await job_title_field.fill(work_exp["job_title"])
        await page.wait_for_timeout(300)

        # Fill Company
        company_field = page.get_by_role("textbox", name=re.compile(r"^Company\*?$"))
        await company_field.click()
        await company_field.fill(work_exp["company"])
        await page.wait_for_timeout(300)

        # Fill Location (if provided)
        if work_exp.get("location"):
            location_field = page.get_by_role("textbox", name="Location")
            await location_field.click()
            await location_field.fill(work_exp["location"])
            await page.wait_for_timeout(300)

        # Fill in work experience start date - month field
        start_month_input = page.locator("input[id$='--startDate-dateSectionMonth-input']").last
        await start_month_input.click()
        await start_month_input.fill(str(work_exp["start_month"]))
        await page.wait_for_timeout(300)

        # Fill in work experience start date - year field
        start_year_input = page.locator("input[id$='--startDate-dateSectionYear-input']").last
        await start_year_input.click()
        await start_year_input.fill(str(work_exp["start_year"]))
        await page.wait_for_timeout(300)

        # Fill in work experience end date - month field
        end_month_input = page.locator("input[id$='--endDate-dateSectionMonth-input']").last
        await end_month_input.click()
        await end_month_input.fill(str(work_exp["end_month"]))
        await page.wait_for_timeout(300)

        # Fill in work experience end date - year field
        end_year_input = page.locator("input[id$='--endDate-dateSectionYear-input']").last
        await end_year_input.click()
        await end_year_input.fill(str(work_exp["end_year"]))
        await page.wait_for_timeout(500)

        print(f"✓ Work experience dates filled: {work_exp['start_month']}/{work_exp['start_year']} to {work_exp['end_month']}/{work_exp['end_year']}")

        # Fill Role Description (if provided)
        if work_exp.get("role_description"):
            role_field = page.get_by_role("textbox", name="Role Description")
            await role_field.click()
            await role_field.fill(work_exp["role_description"])
            await page.wait_for_timeout(300)

    # Scroll to education section
    await page.wait_for_timeout(500)
    education_heading = page.get_by_text("Education")
    await education_heading.scroll_into_view_if_needed()

    # Fill education sections
    for idx, education in enumerate(educations):
        if idx == 0:
            # Click "Add" button for first education entry
            edu_section = page.get_by_role("group", name="Education")
            add_button = edu_section.get_by_role("button", name="Add")
            await add_button.click()
            await page.wait_for_timeout(500)
            await page.evaluate("window.scrollBy(0, 300)")
            await page.wait_for_timeout(300)
            print("Clicked 'Add' button in Education")
        else:
            # Click "Add Another" button to add new education
            edu_section = page.get_by_role("group", name="Education")
            add_another_button = edu_section.get_by_role("button", name="Add Another")
            await add_another_button.click()
            await page.wait_for_timeout(500)
            await page.evaluate("window.scrollBy(0, 300)")
            await page.wait_for_timeout(300)
            print("Clicked 'Add Another' button in Education")

        # Scroll to education section
        await page.wait_for_timeout(300)

        # Fill School or University
        school_field = page.get_by_role("textbox", name=re.compile(r"^School or University\*?$"))
        await school_field.click()
        await school_field.fill(education["school_name"])
        await page.wait_for_timeout(300)

        # Select Degree
        degree_button = page.get_by_role("button", name=re.compile(r"Degree.*Required"))
        await degree_button.click()
        await page.wait_for_timeout(500)

        # Click the degree option from dropdown
        await page.get_by_text(education["degree"]).click()
        await page.wait_for_timeout(500)

        # Fill Field of Study
        field_input = page.get_by_role("textbox", name="Field of Study")
        await field_input.click()
        await field_input.fill(education["field_of_study"])
        await page.wait_for_timeout(500)

        # Press Enter to select from dropdown
        await field_input.press("Enter")
        await page.wait_for_timeout(500)

        # Fill GPA
        gpa_field = page.get_by_role("textbox", name="Overall Result (GPA)")
        await gpa_field.click()
        await gpa_field.fill(education["gpa"])
        await page.wait_for_timeout(300)

    # Wait for form to be ready
    await page.wait_for_timeout(1000)


if __name__ == "__main__":
    import asyncio
    from playwright.async_api import async_playwright

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

            # Navigate to the application page
            await page.goto(
                "https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1/apply",
                wait_until="load",
            )
            await page.wait_for_timeout(1500)

            # Call the function
            await fill_job_application(page)

            await browser.close()

    asyncio.run(main())
