"""
Playwright automation script for Expedia job application sign-in.

This script automates the process of signing into the Expedia job application
portal using provided credentials.
"""

import asyncio
import os
from playwright.async_api import async_playwright


async def sign_in_to_expedia_job_portal(
    page,
    email: str = "inverseui.official@gmail.com",
    password: str = "@Aa12345678"
) -> None:
    """
    Sign in to the Expedia job application portal.

    This function automates the sign-in process for the Expedia job application
    portal at the Principal Software Development Engineer position.

    Args:
        page: Playwright page object
        email: Email address for sign-in. Default: "inverseui.official@gmail.com"
        password: Password for sign-in. Default: "@Aa12345678"

    Returns:
        None
    """
    # Navigate to the job application page
    await page.goto(
        "https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1/apply/autofillWithResume?source=&source=Appcast_Indeed",
        wait_until="load"
    )

    # Wait for the page to fully load
    await page.wait_for_timeout(1500)

    # Scroll down to view the sign-in form
    await page.wait_for_timeout(300)

    # Click on the "Sign In" button to switch to the sign-in tab
    await page.get_by_role("button", name="Sign In").click()

    # Wait for the sign-in form to appear
    await page.wait_for_timeout(500)

    # Fill in the email address field
    email_field = page.get_by_role("textbox", name="Email Address*")
    await email_field.fill(email)

    # Fill in the password field
    password_field = page.get_by_role("textbox", name="Password*")
    await password_field.fill(password)

    # Wait for form processing
    await page.wait_for_timeout(300)

    # Click the Sign In button to submit the form
    await page.get_by_role("button", name="Sign In").click()

    # Wait for the sign-in to complete
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
                # Call the sign-in function
                await sign_in_to_expedia_job_portal(page)
            finally:
                await browser.close()

    asyncio.run(main())
