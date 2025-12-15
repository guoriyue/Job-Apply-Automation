"""Indeed job application automation - Resume selection and upload."""

import asyncio
import os
from playwright.async_api import async_playwright


async def upload_resume_to_indeed(page, resume_path: str = "resume.pdf", skip_navigation: bool = False):
    """
    Automate Indeed job application resume selection and upload.

    Navigates to the resume selection page, selects the upload option,
    uploads a resume file, and proceeds to the next step.

    Args:
        page: Playwright page object
        resume_path: Path to the resume file to upload (PDF, DOCX, RTF, or TXT)
        skip_navigation: If True, skip page navigation (for workflow use)
    """
    if not skip_navigation:
        # Navigate to the resume selection page
        await page.goto(
            "https://us.smartapply.indeed.com/beta/indeedapply/form/resume-selection-module/resume-selection",
            wait_until="load"
        )
    await page.wait_for_timeout(1500)

    # Click on "Upload a resume" option to select it
    # This is the second radio button option in the resume selection module
    await page.get_by_test_id("resume-selection-file-resume-upload-button-header-subtitle").click()
    await page.wait_for_timeout(500)

    # Click on the file input to open the file picker
    file_input = page.get_by_test_id("resume-selection-file-resume-upload-button-file-input")

    # Set the input files with the resume path
    # Using absolute path to ensure the file is found
    await file_input.set_input_files(os.path.abspath(resume_path))
    await page.wait_for_timeout(1000)

    # Wait for the upload to complete
    # The upload state indicator changes from "Uploading..." to completed state
    await page.wait_for_timeout(2000)

    # Scroll down to ensure the Continue button is visible
    await page.evaluate("window.scrollBy(0, 424)")
    await page.wait_for_timeout(500)

    # Click the Continue button to proceed to the next step
    await page.get_by_text("Continue").click()
    await page.wait_for_timeout(1500)


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
                # Call the upload resume function with your resume file path
                await upload_resume_to_indeed(page, resume_path="resume.pdf")
                print("Resume uploaded successfully!")
            except Exception as e:
                print(f"Error during resume upload: {e}")
            finally:
                await browser.close()

    asyncio.run(main())
