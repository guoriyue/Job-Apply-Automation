"""
Playwright automation script for filling out a Figma job application form.

This script automates the process of completing a job application with:
- Country selection (phone country code)
- Phone number entry
- Location selection
"""

import asyncio
import os
from playwright.async_api import async_playwright


async def fill_job_application(
    country: str = "China +86",
    phone: str = "11 122 233 33",
    location: str = "San Francisco, California, United States"
) -> None:
    """
    Fill out the Figma job application form with the provided information.

    Args:
        country: Country and phone code (e.g., "China +86")
        phone: Phone number (e.g., "11 122 233 33")
        location: City/location (e.g., "San Francisco, California, United States")
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to the job application page
            await page.goto(
                "https://job-boards.greenhouse.io/figma/jobs/5660873004?gh_jid=5660873004",
                wait_until="load"
            )
            await page.wait_for_timeout(1500)

            # Scroll to the phone section (if needed)
            await page.evaluate("window.scrollBy(0, 2282)")
            await page.wait_for_timeout(500)

            # ===== Country Selection (Custom Dropdown) =====
            # Click on the country dropdown to open it
            country_button = page.locator(
                "xpath=//form[@id='application-form']/div[1]/div[4]/fieldset/div[1]/div/div/div/div[1]/div/div[2]/button"
            )
            await country_button.click()
            await page.wait_for_timeout(500)

            # Fill the country input with the phone code
            country_input = page.locator("xpath=//input[@id='country']")
            await country_input.fill("+86")
            await page.wait_for_timeout(500)

            # Click the matching country option in the dropdown
            option = page.locator("[role='option']").filter(has_text=country).first
            await option.click()
            await page.wait_for_timeout(500)

            # ===== Phone Number Entry =====
            phone_input = page.locator("xpath=//input[@id='phone']")
            await phone_input.fill(phone)
            await page.wait_for_timeout(500)

            # ===== Location Selection (Custom Dropdown) =====
            # Click on the location dropdown to open it
            location_input = page.locator("xpath=//input[@id='candidate-location']")
            await location_input.click()
            await page.wait_for_timeout(500)

            # Type to filter locations
            await location_input.fill("San fran")
            await page.wait_for_timeout(500)

            # Click the matching location option
            location_option = page.locator("[role='option']").filter(has_text=location).first
            await location_option.click()
            await page.wait_for_timeout(500)

            print("✓ Job application form filled successfully")

        except Exception as e:
            print(f"✗ Error filling application form: {e}")
            raise
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(fill_job_application())
