"""
Playwright automation for job application form.

This module contains automation for filling out a job application form with resume upload.
"""

import asyncio
import os
from playwright.async_api import async_playwright


async def apply_with_resume(page, resume_path: str = "resume.pdf"):
    """
    Automate job application form submission with resume upload.

    Navigates to a job application form, uploads a resume file, and continues
    with the application process.

    Args:
        page: Playwright page object
        resume_path: Path to the resume file to upload (default: "resume.pdf")
    """
    # Navigate to the job application page
    await page.goto(
        "https://expedia.wd108.myworkdayjobs.com/en-US/search/job/USA---California---San-Jose/Principal-Software-Development-Engineer_R-99477-1/apply/autofillWithResume?source=&source=Appcast_Indeed",
        wait_until="load"
    )
    await page.wait_for_timeout(1500)

    # Wait for the file upload section to be visible
    file_input = page.locator('input[type="file"]').first
    await file_input.wait_for(state="attached", timeout=5000)

    # Upload the resume file
    # Use absolute path to ensure the file can be found
    abs_resume_path = os.path.abspath(resume_path)
    await file_input.set_input_files(abs_resume_path)
    await page.wait_for_timeout(1000)

    # Click the Continue button
    # Using the xpath from the action to locate the button
    continue_button = page.locator("button:has-text('Continue')")
    await continue_button.click()
    await page.wait_for_timeout(1500)

    # Wait for the page to load and stabilize after clicking Continue
    await page.wait_for_timeout(2000)


if __name__ == "__main__":
    CDP_URL = None  # Set to "http://localhost:9222" to connect to existing browser

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
                # Call the automation function with default resume path
                # You can change the resume_path parameter to point to your actual resume file
                await apply_with_resume(page, resume_path="resume.pdf")
                print("Application form submission completed successfully!")
            except Exception as e:
                print(f"Error during automation: {e}")
            finally:
                await browser.close()

    asyncio.run(main())
