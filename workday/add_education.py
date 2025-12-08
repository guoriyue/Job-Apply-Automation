"""
Playwright automation script for filling out NVIDIA job application form.

This script fills in education details on the NVIDIA career application page.
Uses stable CSS selectors that match by ID suffix to handle dynamic IDs.
"""

import asyncio
from playwright.async_api import async_playwright, Page

CDP_URL = "http://localhost:9222"


async def click_add_education(page: Page) -> None:
    """
    Click the "Add" button in the Education section (first time).

    Use this when there are NO education entries yet.

    Args:
        page: Playwright Page object
    """
    # First time: button is called "Add", not "Add Another"
    edu_section = page.get_by_role("group", name="Education")
    add_button = edu_section.get_by_role("button", name="Add")

    await add_button.click()
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    print("✓ Clicked 'Add' button in Education")


async def click_add_another_education(page: Page) -> None:
    """
    Click the "Add Another" button in the Education section.

    Use this when there's already at least one education entry.

    Args:
        page: Playwright Page object
    """
    # After first entry: button is called "Add Another"
    edu_section = page.get_by_role("group", name="Education")
    add_button = edu_section.get_by_role("button", name="Add Another")

    await add_button.click()
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    print("✓ Clicked 'Add Another' button in Education")


async def fill_education(
    page: Page,
    index: int = 0,
    school_name: str = "Stanford University",
    degree: str = "Bachelor's Degree",
    field_of_study: str = "Computer Science",
    gpa: str = "3.8",
    start_year: str = "2015",
    end_year: str = "2019",
) -> None:
    """
    Fill education entry by index (0-based).

    Args:
        page: Playwright Page object
        index: 0-based index of the education entry to fill
               Use 0 for first, -1 for last (newly added)
        school_name: Name of the school or university
        degree: Degree type (e.g., "Bachelor's Degree", "Master's Degree", "PhD")
        field_of_study: Field of study
        gpa: Overall GPA
        start_year: Start year
        end_year: End year
    """
    # Helper to get element by index (-1 means last)
    def get_field(selector: str):
        loc = page.locator(selector)
        return loc.last if index == -1 else loc.nth(index)

    # Fill in School/University name
    school_input = get_field('[id$="--schoolName"]')
    await school_input.click()
    await school_input.fill(school_name)
    await page.wait_for_timeout(300)

    # Click on Degree dropdown and select
    degree_button = get_field('[id$="--degree"]')
    await degree_button.click()
    await page.wait_for_timeout(300)

    # Select degree from dropdown
    degree_option = page.get_by_role("option", name=degree)
    await degree_option.click()
    await page.wait_for_timeout(300)

    # Fill in Field of Study
    field_input = get_field('[id$="--fieldOfStudy"]')
    await field_input.click()
    await field_input.fill(field_of_study)
    await page.wait_for_timeout(300)

    # Fill in GPA
    gpa_input = get_field('[id$="--gradeAverage"]')
    await gpa_input.click()
    await gpa_input.fill(gpa)
    await page.wait_for_timeout(300)

    # Fill in Start Year
    start_year_input = get_field('[id$="--firstYearAttended-dateSectionYear-input"]')
    await start_year_input.click()
    await start_year_input.fill(start_year)
    await page.wait_for_timeout(300)

    # Fill in End Year
    end_year_input = get_field('[id$="--lastYearAttended-dateSectionYear-input"]')
    await end_year_input.click()
    await end_year_input.fill(end_year)
    await page.wait_for_timeout(300)

    print(f"✓ Education filled (index={index})")


if __name__ == "__main__":
    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
            page: Page = ctx.pages[0] if ctx.pages else await ctx.new_page()

            try:
                url = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US,-CA,-Santa-Clara/Senior-Manager--Robotics-Quality-Assurance_JR2003248/apply"
                await page.goto(url, wait_until="load")
                await page.wait_for_timeout(1500)

                # Fill first education
                await fill_education(page, index=0, school_name="MIT", degree="Bachelor's Degree")

                # Add another and fill
                await click_add_education(page, use_last=True)
                await fill_education(page, index=-1, school_name="Stanford", degree="Master's Degree")

                print("✓ Done!")

            except Exception as e:
                print(f"✗ Error: {e}")
                raise

    asyncio.run(main())
