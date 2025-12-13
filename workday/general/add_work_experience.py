"""
Playwright automation script for filling out job application form.

This script fills in work experience details on a Workday career application page.
Uses stable CSS selectors that match by ID suffix to handle dynamic IDs.
"""

from playwright.async_api import Page


async def click_add_work_experience(page: Page) -> None:
    """
    Click the "Add" button in the Work Experience section (first time).

    Use this when there are NO work experience entries yet.

    Args:
        page: Playwright Page object
    """
    work_exp_section = page.get_by_role("group", name="Work Experience")
    add_button = work_exp_section.get_by_role("button", name="Add")

    await add_button.click()
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    print("Clicked 'Add' button in Work Experience")


async def click_add_another_work_experience(page: Page) -> None:
    """
    Click the "Add Another" button in the Work Experience section.

    Use this when there's already at least one work experience entry.

    Args:
        page: Playwright Page object
    """
    work_exp_section = page.get_by_role("group", name="Work Experience")
    add_button = work_exp_section.get_by_role("button", name="Add Another")

    await add_button.click()
    await page.wait_for_timeout(500)
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    print("Clicked 'Add Another' button in Work Experience")


async def fill_work_experience(
    page: Page,
    index: int = 0,
    job_title: str = "Software Engineer",
    company_name: str = "Tech Company Inc",
    start_month: int = 1,
    start_year: int = 2020,
    end_month: int = 12,
    end_year: int = 2023,
    role_description: str = "Developed and maintained software applications.",
) -> None:
    """
    Fill work experience entry by index (0-based).

    Args:
        page: Playwright Page object
        index: 0-based index of the work experience entry to fill
               Use 0 for first, -1 for last (newly added)
        job_title: The job title to enter
        company_name: The company name to enter
        start_month: The starting month (1-12)
        start_year: The starting year
        end_month: The ending month (1-12)
        end_year: The ending year
        role_description: The role description/summary
    """
    # Helper to get element by index (-1 means last)
    def get_field(selector: str):
        loc = page.locator(selector)
        return loc.last if index == -1 else loc.nth(index)

    # Fill in Job Title
    job_title_input = get_field('[id$="--jobTitle"]')
    await job_title_input.click()
    await job_title_input.fill(job_title)
    await page.wait_for_timeout(300)

    # Fill in Company Name
    company_input = get_field('[id$="--companyName"]')
    await company_input.click()
    await company_input.fill(company_name)
    await page.wait_for_timeout(300)

    # Fill in Start Date - click the display element first to reveal input
    start_month_display = get_field("div[id^='workExperience-'][id$='--startDate-dateSectionMonth-display']")
    await start_month_display.click()
    await page.keyboard.type(str(start_month))  # Type month, focus auto-moves to year
    await page.keyboard.type(str(start_year))   # Type year
    await page.wait_for_timeout(300)

    # Fill in End Date - click the display element first to reveal input
    end_month_display = get_field("div[id^='workExperience-'][id$='--endDate-dateSectionMonth-display']")
    await end_month_display.click()
    await page.keyboard.type(str(end_month))  # Type month, focus auto-moves to year
    await page.keyboard.type(str(end_year))   # Type year
    await page.wait_for_timeout(300)

    # Scroll down to see Role Description field
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(300)

    # Fill in Role Description
    role_desc_input = get_field('[id$="--roleDescription"]')
    await role_desc_input.click()
    await role_desc_input.fill(role_description)
    await page.wait_for_timeout(300)

    print(f"Work experience filled (index={index})")
