"""
Playwright automation script for Expedia job application form.

This script fills out the "My Information" step of the job application at:
https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1/apply/autofillWithResume
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import asyncio
import os
from playwright.async_api import async_playwright
from workday.general import clear_chip_field_by_input_id


async def fill_job_application_info(
    page,
    how_did_you_hear_about_us: str = "Company Career Site",
    country: str = "United States of America",
    first_name: str = "nico",
    last_name: str = "guo",
    phone_device_type: str = "Mobile",
    country_phone_code: str = "United States of America (+1)",
    phone_number: str = "844-555-2698",
    address_line_1: str = "",
    city: str = "",
    state: str = "",
    postal_code: str = "",
    phone_extension: str = "",
) -> None:
    """
    Fill out the "My Information" step of the Expedia job application form.

    This function automates filling in personal information including name, contact details,
    and address information. It handles dropdown selections, text inputs, and form submission.

    Args:
        page: Playwright page object
        how_did_you_hear_about_us: How applicant learned about the position.
            Options: Company Career Site, Current Contingent Worker, Former Employee,
            I am an employee, I know someone in the company, Job Advert/Job Board
        country: Country of residence. Options: 396 countries available
            (e.g., "United States of America", "Canada", "United Kingdom", etc.)
        first_name: Applicant's first name
        last_name: Applicant's last name
        phone_device_type: Type of phone device. Options: Business, Mobile, Telephone
        country_phone_code: Country phone code for phone number.
            Options: All country phone codes (e.g., "United States of America (+1)",
            "Canada (+1)", "United Kingdom (+44)", etc.)
        phone_number: Applicant's phone number (e.g., "844-555-2698")
        address_line_1: First line of street address (optional)
        city: City of residence (optional)
        state: State/Province of residence (optional)
        postal_code: Postal code (optional)
        phone_extension: Phone extension number (optional)
    """

    # Wait for page to load
    await page.wait_for_timeout(1000)

    # Step 1: Fill "How Did You Hear About Us?" dropdown
    # Open the dropdown
    await page.click("#source--source")
    await page.wait_for_timeout(500)

    # Click the option matching the selected value (use role="option" to avoid matching the button)
    await page.get_by_role("option", name=how_did_you_hear_about_us, exact=True).click()
    await page.wait_for_timeout(500)

    # Step 2: Fill "Country" dropdown
    # Open the dropdown
    await page.click("#country--country")
    await page.wait_for_timeout(500)

    # Click the option matching the selected country (use role="option" to avoid matching the button)
    await page.get_by_role("option", name=country, exact=True).click()
    await page.wait_for_timeout(500)

    # Step 3: Fill "First Name" text input
    first_name_input = page.locator("#name--legalName--firstName")
    await first_name_input.click()
    # Select all existing text and replace
    await page.keyboard.press("Control+A")
    await first_name_input.fill(first_name)
    await page.wait_for_timeout(300)

    # Step 4: Fill "Last Name" text input
    last_name_input = page.locator("#name--legalName--lastName")
    await last_name_input.click()
    # Select all existing text and replace
    await page.keyboard.press("Control+A")
    await last_name_input.fill(last_name)
    await page.wait_for_timeout(300)

    # Step 5: Fill "Address Line 1" if provided
    if address_line_1:
        await page.fill('input[placeholder="Address Line 1"]', address_line_1)
        await page.wait_for_timeout(300)

    # Step 6: Fill "City" if provided
    if city:
        await page.fill('input[placeholder="City"]', city)
        await page.wait_for_timeout(300)

    # Step 7: Fill "State" dropdown if provided
    if state:
        await page.click('button[id*="state"][id*="state"]')
        await page.wait_for_timeout(500)
        await page.get_by_role("option", name=state, exact=True).click()
        await page.wait_for_timeout(500)

    # Step 8: Fill "Postal Code" if provided
    if postal_code:
        await page.fill('input[placeholder="Postal Code"]', postal_code)
        await page.wait_for_timeout(300)

    # Step 9: Fill "Phone Device Type" dropdown
    await page.click("#phoneNumber--phoneType")
    await page.wait_for_timeout(500)

    # Click the phone type option (use role="option" to avoid matching the button)
    await page.get_by_role("option", name=phone_device_type, exact=True).click()
    await page.wait_for_timeout(500)


    await clear_chip_field_by_input_id(page, "phoneNumber--countryPhoneCode")
    await page.wait_for_timeout(300)
    # Step 10: Handle "Country Phone Code" searchable dropdown
    # Click on the country code input/dropdown (use input xpath for reliability)
    country_code_input = page.locator("#phoneNumber--countryPhoneCode")
    await country_code_input.wait_for(state="visible", timeout=5000)
    await country_code_input.click()
    await page.wait_for_timeout(500)

    # Type to search for the country code
    search_term = country_phone_code.split("(")[0].strip().lower()
    await country_code_input.fill(search_term)
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(500)

    # # Click the matching option (use filter with has_text for flexibility)
    # dropdown_option = page.locator("div[role='option']").filter(has_text=country_phone_code).first
    # await dropdown_option.click()
    # await page.wait_for_timeout(500)

    # Step 11: Fill "Phone Number" text input
    phone_input = page.locator("#phoneNumber--phoneNumber")
    await phone_input.click()
    # Select all existing text and replace
    await page.keyboard.press("Control+A")
    await phone_input.fill(phone_number)
    await page.wait_for_timeout(300)

    # Step 12: Fill "Phone Extension" if provided
    if phone_extension:
        phone_extension_input = page.locator("#phoneNumber--phoneExtension")
        await phone_extension_input.fill(phone_extension)
        await page.wait_for_timeout(300)

    # Step 13: Submit the form by clicking "Save and Continue" button
    await page.click('button:has-text("Save and Continue")')
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
                # Navigate to the job application URL
                url = "https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1/apply/autofillWithResume?source=&source=Appcast_Indeed"
                await page.goto(url, wait_until="load")
                await page.wait_for_timeout(1500)

                # Call the automation function with default parameters
                await fill_job_application_info(page)

                # Keep the browser open for 5 seconds to see the result
                await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"Error during automation: {e}")
                raise
            finally:
                await browser.close()

    asyncio.run(main())
