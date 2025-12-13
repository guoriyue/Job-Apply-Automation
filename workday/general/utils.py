"""
Utility functions for Workday job application automation.
These are general-purpose functions that work across different Workday implementations.
"""

from playwright.async_api import Page


async def clear_chip_in_container(page: Page, container) -> bool:
    """
    Clear chip(s) in a given container by clicking X buttons.

    Args:
        page: Playwright Page object
        container: Playwright Locator for the container element

    Returns:
        True if chips were found and cleared, False if field was already empty
    """
    # Try to find Workday-style X icons (SVG with wd-icon-x class)
    wd_icons = container.locator("svg[class*='wd-icon-x']")
    count = await wd_icons.count()
    if count > 0:
        print(f"Found {count} Workday chip(s) to clear")
        while await wd_icons.count() > 0:
            await wd_icons.nth(0).click()
            await page.wait_for_timeout(200)
        return True

    # Try to find delete buttons with aria-label
    delete_icons = container.locator(
        "xpath=.//button[contains(@aria-label, 'Remove') or contains(@aria-label, 'Clear')]"
    )
    count = await delete_icons.count()
    if count > 0:
        print(f"Found {count} chip(s) to clear")
        while await delete_icons.count() > 0:
            await delete_icons.nth(0).click()
            await page.wait_for_timeout(100)
        return True

    # Fallback: look for any SVG that might be a close button
    close_svgs = container.locator("svg")
    svg_count = await close_svgs.count()
    if svg_count > 0:
        print(f"Found {svg_count} SVG(s), trying to click them...")
        for i in range(svg_count):
            svg = close_svgs.nth(0)
            try:
                await svg.click(timeout=1000)
                await page.wait_for_timeout(100)
            except:
                break
        return True

    # No chips found - field is already empty
    print("No existing chips found in container")
    return False


async def clear_chip_field_by_input_id(page: Page, input_id: str) -> bool:
    """
    Clear a chip-style field by finding it via input element ID.

    This is more reliable than label-based finding for Workday fields.

    Args:
        page: Playwright Page object
        input_id: The ID attribute of the input element (e.g., 'source--source')

    Returns:
        True if chips were found and cleared, False if field was already empty
    """
    # Find the input element and go up to find the field wrapper container
    # Workday typically wraps inputs in multiple div layers
    container = page.locator(f"#{input_id}").locator("xpath=ancestor::div[contains(@class, 'css-')][1]/parent::div")

    # Debug: print what we found
    count = await container.count()
    print(f"Found {count} container(s) for input #{input_id}")

    return await clear_chip_in_container(page, container.first)


async def clear_and_fill_input(page: Page, locator_str: str, value: str) -> None:
    """
    Clear existing content in an input field and fill with new value.

    Args:
        page: Playwright Page object
        locator_str: The locator string for the input field
        value: The value to fill
    """
    element = page.locator(locator_str)
    await element.click(click_count=3)  # Triple click to select all
    await page.keyboard.press("Backspace")
    await page.wait_for_timeout(100)
    await element.fill(value)
