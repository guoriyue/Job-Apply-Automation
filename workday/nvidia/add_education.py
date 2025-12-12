"""
Playwright automation script for filling NVIDIA job application with education details.

This script automates the process of adding education information to a job application form.
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
    edu_section = page.get_by_role("group", name="Education")
    add_button = edu_section.get_by_role("button", name="Add")

    await add_button.click()
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    print("Clicked 'Add' button in Education")


async def click_add_another_education(page: Page) -> None:
    """
    Click the "Add Another" button in the Education section.

    Use this when there's already at least one education entry.

    Args:
        page: Playwright Page object
    """
    edu_section = page.get_by_role("group", name="Education")
    add_button = edu_section.get_by_role("button", name="Add Another")

    await add_button.click()
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    print("Clicked 'Add Another' button in Education")


async def fill_education(
    page: Page,
    index: int = -1,
    school_name: str = "Stanford University",
    degree: str = "Masters",
    field_of_study: str = "Electrical & Computer Engineering",
    gpa: str = "3.0",
    start_year: int = 2012,
    end_year: int = 2014,
) -> None:
    """
    Fill out the education section of a job application form.

    This function automates the process of:
    - Filling in school/university name
    - Selecting degree type
    - Selecting field of study
    - Entering GPA
    - Setting start and end years

    Args:
        page: The Playwright page object for interaction
        index: 0-based index of the education entry to fill.
               Use -1 for last (newly added), 0 for first, etc.
        school_name: Name of the school or university
        degree: Degree type to select (e.g., "Masters", "Bachelors", "PhD")
        field_of_study: Field of study selection
        gpa: Grade point average
        start_year: Year started
        end_year: Year ended/graduated

    Returns:
        None
    """

    # Helper to get element by index (-1 means last)
    def get_field(locator):
        return locator.last if index == -1 else locator.nth(index)

    # Fill in School or University name
    school_input = get_field(page.get_by_role("textbox", name="School or University"))
    await school_input.click()
    await school_input.fill(school_name)
    await page.wait_for_timeout(500)

    # Click on Degree dropdown button and select
    degree_button = get_field(page.get_by_role("button", name="Degree Select One Required"))
    await degree_button.click()
    await page.wait_for_timeout(500)
    # await page.get_by_text(degree, exact=True).click()
    await page.get_by_role("option", name=degree).click()
    await page.wait_for_timeout(500)

    # Click on Field of Study input and search
    field_input = get_field(page.get_by_role("textbox", name="Field of Study"))
    await field_input.click()
    await page.wait_for_timeout(500)

    # Type first few chars to search for field of study
    search_term = field_of_study[:4] if len(field_of_study) > 4 else field_of_study
    await field_input.fill(search_term)
    await page.wait_for_timeout(300)

    # Press Enter to confirm search
    await field_input.press("Enter")
    await page.wait_for_timeout(500)

    # Select the matching field of study option
    await page.get_by_text(field_of_study, exact=True).click()
    await page.wait_for_timeout(500)

    # Fill in GPA field
    gpa_field = get_field(page.get_by_role("textbox", name="Overall Result (GPA)"))
    await gpa_field.click()
    await gpa_field.fill(gpa)
    await page.wait_for_timeout(500)

    # Fill in start year
    start_year_input = get_field(page.get_by_role("spinbutton", name="Year"))
    await start_year_input.fill(str(start_year))
    await page.wait_for_timeout(500)

    # Fill in end year
    end_year_input = get_field(page.locator('input[id*="lastYearAttended"][id$="-input"]'))
    await end_year_input.fill(str(end_year))
    await page.wait_for_timeout(500)

    print(f"Education filled successfully (index={index})")


if __name__ == "__main__":
    async def main():
        async with async_playwright() as p:
            if CDP_URL:
                # Connect to existing browser via CDP
                browser = await p.chromium.connect_over_cdp(CDP_URL)
                ctx = browser.contexts[0]
                page = ctx.pages[0] if ctx.pages else await ctx.new_page()
            else:
                # Launch new headless browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

            try:
                # Navigate to the job application page
                await page.goto(
                    "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US,-CA,-Santa-Clara/Senior-ASIC-Test-Timing-Engineer_JR2005476/apply?source=Eightfold",
                    wait_until="load",
                )
                await page.wait_for_timeout(1500)

                # Call the education form filling function
                await fill_education(
                    page,
                    school_name="Stanford University",
                    degree="Masters",
                    field_of_study="Electrical & Computer Engineering",
                    gpa="3.0",
                    start_year=2012,
                    end_year=2014,
                )

                print("Done!")

            except Exception as e:
                print(f"Error: {e}")
                raise

    asyncio.run(main())
