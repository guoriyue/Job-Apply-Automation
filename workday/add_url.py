"""
NVIDIA Job Application Automation Script

This script automates the NVIDIA job application process, specifically handling
the "My Experience" section with website URLs and other profile information.

The automation:
1. Navigates to the job application page
2. Adds website URLs (LinkedIn and GitHub) to the application
3. Submits the form by clicking "Save and Continue"
"""

import asyncio
from playwright.async_api import async_playwright, Page

CDP_URL = "http://localhost:9222"


async def fill_nvidia_job_application(
    linkedin_url: str = "linkedin.com/in/johndoe",
    github_url: str = "github.com/johndoe",
) -> None:
    """
    Fill and submit the NVIDIA job application form with website URLs.

    This function automates the job application process for the Senior Manager,
    Robotics Quality Assurance position. It adds website URLs to the application
    and advances to the next step.

    Args:
        linkedin_url: The LinkedIn profile URL to add (default: "linkedin.com/in/johndoe")
        github_url: The GitHub profile URL to add (default: "github.com/johndoe")

    Returns:
        None

    Raises:
        TimeoutError: If elements or navigation timeouts occur
        Exception: For any other automation errors

    Example:
        await fill_nvidia_job_application(
            linkedin_url="linkedin.com/in/yourprofile",
            github_url="github.com/yourprofile"
        )
    """

    # Application URL
    app_url = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US,-CA,-Santa-Clara/Senior-Manager--Robotics-Quality-Assurance_JR2003248/apply/autofillWithResume"

    async with async_playwright() as playwright:
        # Attach to existing Chrome via CDP
        browser = await playwright.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        page: Page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        try:
            # Navigate to the job application page
            print(f"Navigating to {app_url}...")
            await page.goto(app_url, wait_until="load")
            await page.wait_for_timeout(1500)  # Wait for dynamic content

            # Scroll down to the Websites section
            print("Scrolling to Websites section...")
            await page.wait_for_timeout(500)

            # Click "Add Another" button to add first website
            print(f"Adding first website: {linkedin_url}")
            add_button = page.locator(
                "xpath=//div[@id='root']/div/div/div[2]/div/main/div/div[3]/div[1]/div[2]/div[9]/div[3]/div/div/button"
            )
            await add_button.click()
            await page.wait_for_timeout(800)  # Wait for form to update

            # Fill in the first website URL (LinkedIn)
            linkedin_input = page.locator("xpath=//input[@id='webAddress-141--url']")
            await linkedin_input.click()
            await linkedin_input.fill(linkedin_url)
            await page.wait_for_timeout(500)

            # Click "Add Another" to add second website
            print(f"Adding second website: {github_url}")
            add_another_btn = page.locator(
                "xpath=//div[@id='root']/div/div/div[2]/div/main/div/div[3]/div[1]/div[2]/div[9]/div[4]/div/div/button"
            )
            await add_another_btn.click()
            await page.wait_for_timeout(800)  # Wait for form to update

            # Scroll to see the new website field
            await page.wait_for_timeout(500)

            # Fill in the second website URL (GitHub)
            github_input = page.locator("xpath=//input[@id='webAddress-143--url']")
            await github_input.click()
            await github_input.fill(github_url)
            await page.wait_for_timeout(500)

            # Click "Save and Continue" button to submit the form
            print("Submitting form by clicking 'Save and Continue'...")
            save_button = page.locator(
                "xpath=//div[@id='root']/div/div/div[2]/div/main/div/div[3]/div[2]/div[3]/div/button"
            )

            # Wait for button to be enabled and clickable
            await save_button.wait_for(state="visible", timeout=5000)
            await page.wait_for_timeout(300)  # Brief pause before clicking

            await save_button.click()
            await page.wait_for_timeout(2000)  # Wait for form submission and navigation

            print("Application form submitted successfully!")

        except Exception as e:
            print(f"Error during automation: {str(e)}")
            raise

        # Don't close browser - it's the user's Chrome


async def main() -> None:
    """
    Main entry point for the automation script.

    Executes the NVIDIA job application automation with default parameters.
    """
    try:
        await fill_nvidia_job_application()
        print("✓ Automation completed successfully!")
    except Exception as e:
        print(f"✗ Automation failed: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
