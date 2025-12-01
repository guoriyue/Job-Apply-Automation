"""
Greenhouse Job Application Automation Script

This script automates submitting a resume to a Greenhouse job application form.
It navigates to the job posting, uploads a resume file, and completes the application process.
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


async def upload_resume_to_greenhouse(
    page: Page,
    resume_path: str = "resume.pdf"
) -> None:
    """
    Upload a resume to a Greenhouse job application form.

    This function navigates to the job posting page, scrolls to the Resume/CV section,
    and uploads the provided resume file.

    Args:
        page: Playwright Page object for browser interaction
        resume_path: Path to the resume file (relative or absolute). Defaults to "resume.pdf"

    Raises:
        FileNotFoundError: If the resume file does not exist
        TimeoutError: If page elements are not found within timeout period
    """

    # Convert relative path to absolute path
    abs_resume_path = os.path.abspath(resume_path)

    # Verify file exists
    if not os.path.exists(abs_resume_path):
        raise FileNotFoundError(f"Resume file not found: {abs_resume_path}")

    # Wait for the page to load
    await page.wait_for_timeout(1500)

    # Scroll to the Resume/CV section (scroll position was at y: 2426.5)
    await page.evaluate("window.scrollBy(0, 2426)")
    await page.wait_for_timeout(500)

    # Click the "Attach" button for Resume/CV field
    # Using the first xpath which is the most reliable
    attach_button = page.locator(
        "//form[@id='application-form']/div[1]/div[6]/div/div[2]/div/div[1]/div/button"
    )
    await attach_button.click()
    await page.wait_for_timeout(300)

    # Locate and interact with the file input
    # Using the input ID which is the most stable selector
    file_input = page.locator("input#resume")

    # Set the file - Playwright handles the file upload automatically
    await file_input.set_input_files(abs_resume_path)

    # Wait for the file to be processed
    await page.wait_for_timeout(1000)


async def apply_to_figma_job(
    resume_path: str = "sample-resume.pdf",
    headless: bool = True
) -> None:
    """
    Complete a Figma job application on Greenhouse job board.

    This is the main automation function that:
    1. Launches a browser
    2. Navigates to the job posting
    3. Uploads a resume file
    4. Completes the application process

    Args:
        resume_path: Path to the resume PDF file to upload
        headless: Whether to run the browser in headless mode (default: True)

    Example:
        await apply_to_figma_job(resume_path="my_resume.pdf")
    """

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=headless)

        # Create a new context and page
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to the job posting
            job_url = "https://job-boards.greenhouse.io/figma/jobs/5660873004?gh_jid=5660873004"
            await page.goto(job_url, wait_until="load")

            # Set viewport to match the recorded session
            await page.set_viewport_size({"width": 1508, "height": 859})

            # Wait for page to fully load
            await page.wait_for_timeout(1500)

            # Upload the resume
            await upload_resume_to_greenhouse(page, resume_path)

            # Wait for completion
            await page.wait_for_timeout(1000)

            print(f"✓ Resume uploaded successfully: {resume_path}")

        finally:
            # Cleanup
            await context.close()
            await browser.close()


if __name__ == "__main__":
    # Example usage: Run the automation with a resume file
    # Make sure the resume file exists in the current directory or provide the full path

    import sys

    # Get resume path from command line argument or use default
    resume_file = sys.argv[1] if len(sys.argv) > 1 else "sample-resume.pdf"

    # Run the automation
    asyncio.run(apply_to_figma_job(resume_path=resume_file, headless=False))
