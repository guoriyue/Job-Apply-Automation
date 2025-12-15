"""
Playwright automation script for filling out job application form.

This script fills in website URLs on a Workday career application page.
Uses stable CSS selectors that match by ID suffix to handle dynamic IDs.
"""

from playwright.async_api import Page


async def click_add_url(page: Page) -> None:
    """
    Click the "Add" button in the Websites section (first time).

    Use this when there are NO URL entries yet.

    Args:
        page: Playwright Page object
    """
    url_section = page.get_by_role("group", name="Websites")
    add_button = url_section.get_by_role("button", name="Add")

    await add_button.click()
    await page.wait_for_timeout(500)

    print("Clicked 'Add' button in Websites")


async def click_add_another_url(page: Page) -> None:
    """
    Click the "Add Another" button in the Websites section.

    Use this when there's already at least one URL entry.

    Args:
        page: Playwright Page object
    """
    url_section = page.get_by_role("group", name="Websites")
    add_button = url_section.get_by_role("button", name="Add Another")

    await add_button.click()
    await page.wait_for_timeout(500)

    print("Clicked 'Add Another' button in Websites")


async def fill_url(
    page: Page,
    index: int = 0,
    url: str = "https://linkedin.com/in/johndoe",
) -> None:
    """
    Fill website URL entry by index (0-based).

    Args:
        page: Playwright Page object
        index: 0-based index of the URL entry to fill
               Use 0 for first, -1 for last (newly added)
        url: The URL to enter
    """
    url_input = page.locator('[id$="--url"]')
    field = url_input.last if index == -1 else url_input.nth(index)

    await field.click()
    await field.fill(url)
    await page.wait_for_timeout(300)

    print(f"URL filled (index={index}): {url}")


async def add_urls(
    page: Page,
    linkedin_url: str = None,
    github_url: str = None,
) -> None:
    """
    Add LinkedIn and/or GitHub URLs to the application.

    This is a convenience function that adds multiple URLs.

    Args:
        page: Playwright Page object
        linkedin_url: LinkedIn profile URL (optional)
        github_url: GitHub profile URL (optional)
    """
    urls_to_add = []
    if linkedin_url:
        urls_to_add.append(linkedin_url)
    if github_url:
        urls_to_add.append(github_url)

    for i, url in enumerate(urls_to_add):
        if i == 0:
            await click_add_url(page)
        else:
            await click_add_another_url(page)
        await fill_url(page, index=-1, url=url)

    print(f"Added {len(urls_to_add)} URL(s)")
