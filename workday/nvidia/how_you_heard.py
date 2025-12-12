"""
NVIDIA Job Application Automation Script

This module automates filling out a NVIDIA job application form.
It handles form field interactions including dropdown selections and radio button selections.
"""

from playwright.async_api import Page
from .utils import clear_chip_field_by_input_id


async def how_you_heard_about_us(
    page: Page,
    how_heard: str = "Event/Conference",
    event_conference: str = "GTC 2025",
    previous_employee: bool = False,
) -> None:
    """
    Fill out the NVIDIA job application form fields.

    Args:
        page: Playwright Page object from the workflow
        how_heard: Response for "How did you hear about us?" field
                   Options: "Event/Conference", "Associations", "Job Board", etc.
        event_conference: The event/conference name to select
                         Options: "GTC 2025", "SIGGRAPH", "NeurIPS 2025", etc.
        previous_employee: Whether previously worked at NVIDIA (True/False)

    Returns:
        None
    """

    # Wait for page to be ready and the form to load
    print("Waiting for form to load...")
    source_input = page.locator("xpath=//input[@id='source--source']")
    await source_input.wait_for(state="visible", timeout=10000)

    # Scroll to the first dropdown ("How Did You Hear About Us?")
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.35)")
    await page.wait_for_timeout(300)

    # Handle "How Did You Hear About Us?" dropdown
    # First clear any existing selection (chip)
    print("Clearing any existing selection...")
    await clear_chip_field_by_input_id(page, "source--source")
    await page.wait_for_timeout(300)

    # This is a custom searchable dropdown - use fill + click pattern
    print(f"Selecting '{how_heard}' for 'How Did You Hear About Us?'...")
    await source_input.scroll_into_view_if_needed()
    await page.wait_for_timeout(300)
    await source_input.click()
    await page.wait_for_timeout(300)
    await source_input.fill(how_heard)
    await page.wait_for_timeout(500)

    # Click the matching option from the dropdown
    await page.locator(
        "xpath=//div[contains(@class, 'css-') and @role='option']"
    ).filter(has_text=how_heard).first.click()
    await page.wait_for_timeout(500)

    # Scroll down to the event/conference dropdown
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.5)")
    await page.wait_for_timeout(300)

    # Handle event/conference selection dropdown
    print(f"Selecting '{event_conference}' from event dropdown...")
    event_option = page.locator(
        "xpath=//div[@role='option' or @role='radio']//*[contains(text(), '"
        + event_conference + "')]"
    ).first

    # Scroll the option into view and click it
    await event_option.scroll_into_view_if_needed()
    await page.wait_for_timeout(300)
    await event_option.click()
    await page.wait_for_timeout(500)

    # Handle "Have you previously worked for NVIDIA?" radio button
    # Scroll down to this section
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.65)")
    await page.wait_for_timeout(300)

    print(f"Setting 'Have you previously worked for NVIDIA?' to '{'Yes' if previous_employee else 'No'}'...")

    # Find radio buttons by their value attribute (more stable than dynamic IDs)
    # Wait for radio buttons to be visible
    radio_group = page.locator("input[type='radio'][value='false'], input[type='radio'][value='true']")
    await radio_group.first.wait_for(state="visible", timeout=3000)

    # Select the appropriate radio button based on previous_employee parameter
    if previous_employee:
        # Select "Yes" (value='true')
        yes_radio = page.locator("input[type='radio'][value='true']")
        await yes_radio.check()
    else:
        # Select "No" (value='false')
        no_radio = page.locator("input[type='radio'][value='false']")
        await no_radio.check()

    await page.wait_for_timeout(500)

    print("✓ Form fields have been successfully filled!")
    print(f"  - How did you hear about us: {how_heard}")
    print(f"  - Event/Conference selected: {event_conference}")
    print(f"  - Previous NVIDIA employee: {previous_employee}")
