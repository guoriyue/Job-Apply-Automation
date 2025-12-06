"""
Save and Continue button click automation for NVIDIA job application.
"""

from playwright.async_api import Page


async def save_and_continue(page: Page) -> None:
    """
    Click the 'Save and Continue' button to proceed to the next step.

    Args:
        page: Playwright Page object from the workflow
    """
    # Scroll down to see the Save and Continue button
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(500)

    # Find the "Save and Continue" button
    save_button = page.locator("xpath=//div[@id='root']/div/div/div[2]/div/main/div/div[3]/div[2]/div[3]/div/button")

    # Wait for the button to be visible
    await save_button.wait_for(state="visible", timeout=3000)
    await save_button.click()

    # Wait for the form submission and navigation
    await page.wait_for_timeout(1000)

    # Scroll back to the top of the page
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(500)

    print("Successfully clicked 'Save and Continue' button.")
