"""
Workday Job Application Resume Upload Automation

This script automates the job application process for Workday applications:
- Navigating to job application URL
- Clicking the Apply button
- Autofilling with a resume
- Uploading the resume file
- Completing the application flow
"""

import os
from playwright.async_api import Page


async def open_job_application_url(page: Page, url: str) -> None:
    """
    Navigate to the job application page.

    Args:
        page: Playwright page object
        url: URL of the job application page
    """
    await page.goto(url, wait_until="load")
    await page.wait_for_timeout(1500)


async def upload_resume(
    page: Page,
    resume_path: str = "resume.pdf",
) -> None:
    """
    Upload resume and autofill the job application form.

    Args:
        page: Playwright Page object from the workflow (already navigated to job page)
        resume_path: Path to the resume file (DOC, DOCX, HTML, PDF, or TXT). Defaults to "resume.pdf"

    Returns:
        None

    Raises:
        FileNotFoundError: If the resume file does not exist
        TimeoutError: If elements don't load within timeout
    """
    # Convert relative path to absolute path for file upload
    abs_resume_path = os.path.abspath(resume_path)

    # Verify resume file exists
    if not os.path.isfile(abs_resume_path):
        raise FileNotFoundError(f"Resume file not found at: {abs_resume_path}")

    # Step 1: Click "Autofill with Resume" option
    print("Clicking Autofill with Resume option...")
    autofill_button = page.locator('xpath=/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div/a')
    await autofill_button.click()
    await page.wait_for_timeout(1000)  # Wait for autofill form to load

    # Step 2: Directly upload resume to file input
    print(f"Uploading resume from: {abs_resume_path}")
    file_input = page.locator('input[type="file"]')
    await file_input.set_input_files(abs_resume_path)

    # Step 3: Wait for file upload to complete and form to validate
    await page.wait_for_timeout(2000)

    # Step 4: Wait for Continue button to become enabled
    print("Waiting for form validation...")
    continue_button = page.locator('xpath=//div[@id="root"]/div/div/div[2]/div/main/div/div[3]/div[2]/div/div/button')

    # Wait up to 5 seconds for the button to be enabled
    try:
        await continue_button.wait_for(state="visible", timeout=5000)
        button_state = await continue_button.is_enabled()
        if button_state:
            print("Clicking Continue button...")
            await continue_button.click()
            await page.wait_for_timeout(1000)
            print("Resume upload completed successfully!")
        else:
            print("WARNING: Continue button is disabled. Manual intervention may be required.")
    except Exception as e:
        print(f"Continue button interaction encountered an issue: {e}")


async def apply_with_resume(page: Page, resume_path: str = "resume.pdf") -> None:
    """
    Upload resume and continue with the application process.

    This is an alias for upload_resume for backward compatibility.

    Args:
        page: Playwright page object
        resume_path: Path to the resume file to upload (default: "resume.pdf")
    """
    # Wait for the file upload section to be visible
    file_input = page.locator('input[type="file"]').first
    await file_input.wait_for(state="attached", timeout=5000)

    # Upload the resume file
    abs_resume_path = os.path.abspath(resume_path)
    await file_input.set_input_files(abs_resume_path)
    await page.wait_for_timeout(1000)

    # Click the Continue button
    continue_button = page.locator("button:has-text('Continue')")
    await continue_button.click()
    await page.wait_for_timeout(1500)

    # Wait for the page to load and stabilize after clicking Continue
    await page.wait_for_timeout(2000)
