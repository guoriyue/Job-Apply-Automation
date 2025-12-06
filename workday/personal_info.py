"""
Playwright Python automation script for Workday job application form filling.

This script automates filling out a Workday job application form with personal information.
"""

from playwright.async_api import Page


async def fill_personal_info(
    page: Page,
    first_name: str = "John",
    last_name: str = "Doe",
) -> None:
    """
    Fill out a Workday job application form with personal information.

    Args:
        page: Playwright Page object from the workflow
        first_name: The applicant's first name. Defaults to "John".
        last_name: The applicant's last name. Defaults to "Doe".
    """
    # Fill in First Name field
    first_name_input = page.locator('input[id="name--legalName--firstName"]')
    await first_name_input.click()
    await first_name_input.fill(first_name)
    await page.wait_for_timeout(500)

    # Fill in Last Name field
    last_name_input = page.locator('input[id="name--legalName--lastName"]')
    await last_name_input.click()
    await last_name_input.fill(last_name)
    await page.wait_for_timeout(500)

    # Scroll to the preferred name checkbox
    await page.wait_for_timeout(300)
    await page.evaluate("window.scrollBy(0, 500)")
    await page.wait_for_timeout(500)

    print("✓ Successfully filled out the job application form")
    print(f"  - First Name: {first_name}")
    print(f"  - Last Name: {last_name}")
