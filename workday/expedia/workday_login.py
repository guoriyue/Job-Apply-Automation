"""
Playwright automation script for Expedia job application form.

This script automates the account creation process during the job application.
"""

import asyncio
import os
from playwright.async_api import async_playwright


async def apply_to_job(
    page,
    email: str = "inverseui.official@gmail.com",
    password: str = "@Aa12345678",
    verify_password: str = "@Aa12345678",
) -> None:
    """
    Automate the Expedia job application account creation process.

    This function handles:
    - Clicking the Apply button
    - Selecting "Autofill with Resume" option
    - Filling email address
    - Setting password with required complexity
    - Confirming password
    - Checking privacy policy checkbox
    - Submitting the form

    Args:
        page: Playwright page object
        email: Email address for account creation. Default: inverseui.official@gmail.com
        password: Password that meets complexity requirements (must include special char,
                uppercase, lowercase, numeric, min 8 chars).
                Default: @Aa12345678
        verify_password: Password confirmation. Should match password parameter.
                        Default: @Aa12345678
    """

    # Step 1: Click the Apply button on the job listing page
    await page.locator("xpath=//div[@id='mainContent']/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/a").click()
    await page.wait_for_timeout(500)

    # Step 2: Click "Autofill with Resume" option in the modal
    await page.locator("xpath=/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div/a").click()
    await page.wait_for_timeout(1000)

    # Step 3: Fill email address field
    email_field = page.locator("#input-4")
    await email_field.click()
    await page.wait_for_timeout(300)
    await email_field.fill(email)
    await page.wait_for_timeout(500)

    # Step 4: Fill password field with required complexity
    password_field = page.locator("#input-5")
    await password_field.click()
    await page.wait_for_timeout(300)
    await password_field.fill(password)
    await page.wait_for_timeout(500)

    # Step 5: Scroll down to see more form fields
    await page.wait_for_timeout(300)

    # Step 6: Fill verify password field
    verify_password_field = page.locator("#input-6")
    await verify_password_field.click()
    await page.wait_for_timeout(300)
    await verify_password_field.fill(verify_password)
    await page.wait_for_timeout(500)

    # Step 7: Check the privacy policy checkbox
    privacy_checkbox = page.locator("#input-8")
    await privacy_checkbox.click()
    await page.wait_for_timeout(300)

    # Step 8: Click the Create Account button to submit the form
    create_account_button = page.locator(
        "xpath=/html/body/div[@id='root']/div/div[@class='css-qjy8kv']/div[@id='mainContent' and @class='css-u765ul']/div/main[@class='css-1o5upoi']/div[@class='css-inhirh']/div[@class='css-1j489tx']/div[@class='css-g7hkny']/div[@class='css-19ssb29']/div[@class='css-ecyovj']/div/form[@class='css-w0sgi8']/div[@class='css-1s1r74k']/div[@class='css-1s1r74k']/div/div[@class='css-1s1r74k']/div[@class='css-1s1r74k']/button[@class='css-a9u6na' and @type='submit']"
    )
    await create_account_button.click()
    await page.wait_for_timeout(2000)


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

            # Navigate to the job application page
            job_url = "https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1?source=&source=Appcast_Indeed"
            await page.goto(job_url, wait_until="load")
            await page.wait_for_timeout(1500)

            # Call the automation function
            await apply_to_job(page)

            # Keep the browser open briefly to verify completion
            await page.wait_for_timeout(1000)

            await browser.close()

    asyncio.run(main())
