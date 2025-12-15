"""
Playwright Python automation script for filling Indeed job application contact information form.
Fills out contact details including name, phone, and location information.
"""

import asyncio
from playwright.async_api import async_playwright


async def fill_contact_information(
    page,
    first_name: str = "Harry",
    last_name: str = "Potter",
    phone_number: str = "650-777-9340",
    zip_code: str = "95129",
    city_state: str = "San Jose, CA",
    street_address: str = "4 Privet Drive",
    skip_navigation: bool = False,
):
    """
    Fill out the Indeed job application contact information form.

    Args:
        page: Playwright page object
        first_name: Applicant's first name. Default: "Harry"
        last_name: Applicant's last name. Default: "Potter"
        phone_number: Phone number in format XXX-XXX-XXXX. Default: "650-777-9340"
        zip_code: Postal/zip code. Default: "95129"
        city_state: City and state information. Default: "San Jose, CA"
        street_address: Street address. Default: "4 Privet Drive"
        skip_navigation: If True, skip page navigation (for workflow use)
    """

    if not skip_navigation:
        # Navigate to the contact information form
        await page.goto(
            "https://us.smartapply.indeed.com/beta/indeedapply/form/contact-info-module",
            wait_until="load"
        )
    await page.wait_for_timeout(1500)

    # Fill first name
    first_name_input = page.get_by_test_id("name-fields-first-name-input")
    await first_name_input.click()
    await first_name_input.fill(first_name)
    await page.wait_for_timeout(300)

    # Fill last name
    last_name_input = page.get_by_test_id("name-fields-last-name-input")
    await last_name_input.click()
    await last_name_input.fill(last_name)
    await page.wait_for_timeout(300)

    # Fill phone number
    phone_input = page.get_by_role("textbox", name="Type phone number")
    await phone_input.click()
    await phone_input.fill(phone_number)
    await page.wait_for_timeout(500)

    # Click Continue button to proceed to next section
    continue_button = page.get_by_test_id("81fa2ee401fae0bc3addc8c4c29e6ffa9610a7d7ca0eee6949a40d1689b131fb")
    await continue_button.click()
    await page.wait_for_timeout(1500)

    # Wait for location information section to load
    await page.wait_for_selector("[data-test-id='location-fields-postal-code-input']", timeout=5000)

    # Fill postal/zip code
    postal_code_input = page.get_by_test_id("location-fields-postal-code-input")
    await postal_code_input.click()
    await postal_code_input.fill(zip_code)
    await page.wait_for_timeout(500)

    # Fill city and state (this is an autocomplete/combobox field)
    city_state_input = page.get_by_test_id("location-fields-locality-input")
    await city_state_input.click()
    await city_state_input.fill(city_state)
    await page.wait_for_timeout(800)

    # Fill street address
    address_input = page.get_by_test_id("location-fields-address-input")
    await address_input.click()
    await address_input.fill(street_address)
    await page.wait_for_timeout(500)

    # Click Continue button to submit location information
    continue_button = page.get_by_test_id("81fa2ee401fae0bc3addc8c4c29e6ffa9610a7d7ca0eee6949a40d1689b131fb")
    await continue_button.click()
    await page.wait_for_timeout(1500)


if __name__ == "__main__":
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

            try:
                # Call the automation function with default parameters
                await fill_contact_information(page)
                print("Contact information form filled successfully!")
            except Exception as e:
                print(f"Error during automation: {e}")
                raise
            finally:
                await browser.close()

    asyncio.run(main())
