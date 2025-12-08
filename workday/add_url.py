"""
Playwright automation script for filling out NVIDIA job application form.

This script fills in website URLs on the NVIDIA career application page.
Uses stable CSS selectors that match by ID suffix to handle dynamic IDs.
"""

import asyncio
from playwright.async_api import async_playwright, Page

CDP_URL = "http://localhost:9222"


async def click_add_url(page: Page) -> None:
    """
    Click the "Add" button in the Websites section (first time).

    Use this when there are NO URL entries yet.

    Args:
        page: Playwright Page object
    """
    # First time: button is called "Add", not "Add Another"
    url_section = page.get_by_role("group", name="Websites")
    add_button = url_section.get_by_role("button", name="Add")

    await add_button.click()
    await page.wait_for_timeout(500)

    print("✓ Clicked 'Add' button in Websites")


async def click_add_another_url(page: Page) -> None:
    """
    Click the "Add Another" button in the Websites section.

    Use this when there's already at least one URL entry.

    Args:
        page: Playwright Page object
    """
    # After first entry: button is called "Add Another"
    url_section = page.get_by_role("group", name="Websites")
    add_button = url_section.get_by_role("button", name="Add Another")

    await add_button.click()
    await page.wait_for_timeout(500)

    print("✓ Clicked 'Add Another' button in Websites")


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
    # Get URL input field by index (-1 means last)
    url_input = page.locator('[id$="--url"]')
    field = url_input.last if index == -1 else url_input.nth(index)

    await field.click()
    await field.fill(url)
    await page.wait_for_timeout(300)

    print(f"✓ URL filled (index={index}): {url}")


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
            # First URL: click "Add"
            await click_add_url(page)
        else:
            # Subsequent URLs: click "Add Another"
            await click_add_another_url(page)
        await fill_url(page, index=-1, url=url)

    print(f"✓ Added {len(urls_to_add)} URL(s)")


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

                # Add URLs
                await add_urls(
                    page,
                    linkedin_url="https://linkedin.com/in/johndoe",
                    github_url="https://github.com/johndoe"
                )

                print("✓ Done!")

            except Exception as e:
                print(f"✗ Error: {e}")
                raise

    asyncio.run(main())
