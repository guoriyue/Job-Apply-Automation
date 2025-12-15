"""
Indeed Job Application Automation - Job Experience Entry Module

This script automates the job experience entry form on Indeed's SmartApply platform.
It fills in job title and company name fields with autocomplete selection.
"""

import asyncio
from playwright.async_api import async_playwright


async def fill_job_experience(
    page,
    job_title: str = "security officer",
    company_name: str = "warner bros",
    skip_navigation: bool = False,
):
    """
    Fill in job experience information on Indeed's SmartApply form.

    This function navigates through the job title and company name fields with
    autocomplete dropdown selection and continues to the next step.

    Args:
        page: Playwright page object
        job_title: Job title to enter. Options: Security Officer, Software Engineer, etc.
        company_name: Company name to enter. Options: Warner Bros, Apple, Google, etc.
        skip_navigation: If True, skip page navigation (for workflow use)
    """

    if not skip_navigation:
        # Navigate to the job experience entry page
        await page.goto(
            "https://us.smartapply.indeed.com/beta/indeedapply/form/resume-selection-module/privacy-settings",
            wait_until="load"
        )
    await page.wait_for_timeout(1500)

    # Click Continue button on privacy settings page
    await page.get_by_text("Continue").click()
    await page.wait_for_timeout(1000)

    # Wait for the job title input field to be visible
    await page.wait_for_selector('[data-testid="job-title-input"]', state="visible", timeout=3000)

    # Fill in job title field
    job_title_input = page.get_by_test_id("job-title-input")
    await job_title_input.click()
    await job_title_input.fill(job_title)
    await page.wait_for_timeout(500)  # Wait for dropdown to appear

    # Select the job title from dropdown
    # The dropdown shows matching job titles based on input
    await page.get_by_role("option", name=job_title.title()).click()
    await page.wait_for_timeout(500)

    # Fill in company name field
    company_input = page.get_by_test_id("company-name-input")
    await company_input.click()
    await company_input.fill(company_name)
    await page.wait_for_timeout(500)  # Wait for dropdown to appear

    # Select the company from dropdown
    # Match the exact company name from the dropdown options
    await page.get_by_role("option", name=company_name.title()).click()
    await page.wait_for_timeout(500)

    # Click Continue button to proceed to next step
    await page.get_by_test_id("continue-button").click()
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
                # Call the automation function
                await fill_job_experience(page)
                print("Job experience form filled successfully!")
            except Exception as e:
                print(f"Error during automation: {e}")
                raise
            finally:
                await browser.close()

    asyncio.run(main())
