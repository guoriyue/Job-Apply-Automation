"""
Playwright automation script for Figma job application form.

This script automates filling out the Figma job application with employment
authorization, work history, and location information.
"""

import asyncio
from playwright.async_api import async_playwright


async def fill_figma_job_application(
    authorized_to_work: str = "Yes",
    worked_for_figma_before: str = "No",
) -> None:
    """
    Fill out the Figma job application form with employment details.

    Args:
        authorized_to_work: Response to authorization to work in country (Yes/No)
        worked_for_figma_before: Whether previously worked at Figma (Yes/No)
        work_location: City and state for work location (e.g., "San Francisco, CA")
    """
    async with async_playwright() as p:
        # Launch browser
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

            # Scroll to the form section with employment questions
            await page.evaluate("window.scrollBy(0, 3179)")
            await page.wait_for_timeout(500)

            # ==========================================
            # Question 1: Authorization to work
            # ==========================================
            # Click on the authorization dropdown to open it
            auth_dropdown_input = page.locator('xpath=//input[@id="question_14250644004"]')
            await auth_dropdown_input.click()
            await page.wait_for_timeout(500)

            # Fill the input with the selection value and wait for dropdown to appear
            await auth_dropdown_input.fill(authorized_to_work)
            await page.wait_for_timeout(500)

            # Click the matching option in the dropdown menu
            auth_menu = page.locator(
                f"//form[@id='application-form']/div[2]/div[8]//div[@role='listbox'] //div[@role='option'] | "
                f"//form[@id='application-form']/div[2]/div[8]//button[contains(text(), '{authorized_to_work}')]"
            ).first
            await auth_menu.click()
            await page.wait_for_timeout(500)

            # ==========================================
            # Question 2: Previous Figma employment
            # ==========================================
            # Click on the Figma employment history dropdown
            figma_dropdown_input = page.locator('xpath=//input[@id="question_14250644004"]')
            await page.wait_for_timeout(300)

            # Locate and click the second dropdown (previous Figma employment)
            # Using xpath relative to form structure
            figma_dropdown = page.locator(
                'xpath=//form[@id="application-form"]/div[2]/div[9]//input[@type="text"]'
            ).first
            await figma_dropdown.click()
            await page.wait_for_timeout(500)

            # Fill and select the Figma employment option
            await figma_dropdown.fill(worked_for_figma_before)
            await page.wait_for_timeout(500)

            # Click the matching option
            figma_menu = page.locator(
                f"//form[@id='application-form']/div[2]/div[9]//div[@role='listbox'] //div[@role='option'] | "
                f"//form[@id='application-form']/div[2]/div[9]//button[contains(text(), '{worked_for_figma_before}')]"
            ).first
            await figma_menu.click()
            await page.wait_for_timeout(500)

        finally:
            # Clean up
            await context.close()
            await browser.close()


if __name__ == "__main__":
    # Example usage: Run the automation with default values
    asyncio.run(
        fill_figma_job_application(
            # authorized_to_work="No",
            # worked_for_figma_before="Yes"
        )
    )