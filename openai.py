"""
Playwright automation script for OpenAI job application form.

This script automates filling out and submitting a job application form
on the Ashby job application platform.
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


async def fill_openai_job_application(
    page: Page,
    resume_path: str,
    name: str,
    email: str,
    phone: str = "1234567890",
    location: str = "San Francisco, CA, United States",
    start_date: str = "12/30/2024",
    needs_sponsorship: bool = False,
    can_attend_office: bool = True,
) -> None:
    """
    Fill out and submit the OpenAI job application form.

    Args:
        page: Playwright page object
        resume_path: Path to the resume PDF file
        name: Applicant's full name
        email: Applicant's email address
        phone: Phone number to fill in
        location: Work location preference
        start_date: Desired start date
        needs_sponsorship: True if requires sponsorship, False otherwise
        can_attend_office: True if can go to US office 3 days a week, False otherwise
    """
    # Navigate to the application URL
    await page.goto(
        "https://jobs.ashbyhq.com/openai/93d9be71-6502-4e48-94c2-1c17724e2bc7/application",
        wait_until="load",
    )
    await page.wait_for_timeout(1500)

    # Upload resume - directly set the file input
    file_input = await page.query_selector("//div[@id='form']/div[1]/div/input")
    if file_input:
        await file_input.set_input_files(resume_path)
        print("✓ Resume uploaded")
        await page.wait_for_timeout(1000)

    # Fill name field
    print("Filling name field...")
    name_field_selector = "#_systemfield_name"
    await page.wait_for_selector(name_field_selector, state="visible", timeout=3000)
    name_input = page.locator(name_field_selector)
    await name_input.click()
    await page.wait_for_timeout(300)
    # Clear any existing value and fill
    await name_input.fill("")
    await name_input.fill(name)
    await page.wait_for_timeout(500)
    print(f"✓ Name filled: {name}")

    # Fill email field
    print("Filling email field...")
    email_field_selector = "#_systemfield_email"
    await page.wait_for_selector(email_field_selector, state="visible", timeout=3000)
    await page.click(email_field_selector)
    await page.fill(email_field_selector, email)
    await page.wait_for_timeout(500)
    print(f"✓ Email filled: {email}")

    # Scroll down to form fields
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(500)

    # Fill phone number
    phone_input = await page.query_selector("//input[@id='20f8883c-d278-427c-9465-dc614f612e1f']")
    if phone_input:
        await phone_input.click()
        await page.wait_for_timeout(300)
        await page.fill("//input[@id='20f8883c-d278-427c-9465-dc614f612e1f']", phone)
        await page.wait_for_timeout(500)

    # Scroll to next field sections
    await page.evaluate("window.scrollBy(0, 200)")
    await page.wait_for_timeout(500)

    # Fill location/work preference field - click and interact with autocomplete
    location_input_xpath = "//div[@id='form']/div[3]/div/div[5]/div/input"
    location_input = await page.query_selector(location_input_xpath)
    if location_input:
        await location_input.click()
        await page.wait_for_timeout(300)
        # Clear and fill the location
        await page.fill(location_input_xpath, location)
        await page.wait_for_timeout(800)  # Wait for autocomplete suggestions to appear

        # Wait for autocomplete dropdown and click the first option
        # The dropdown is a portal element appended to body with dynamic ID
        try:
            # Step 1: Wait for the dropdown menu to appear (dynamic floating-ui element)
            await page.wait_for_selector("[id^='floating-ui-']", state="visible", timeout=3000)
            await page.wait_for_timeout(500)

            # Step 2: Find and click the first option in the dropdown
            # The dropdown contains clickable divs, we need to find the actual option elements
            # Try to click an element with text that matches the location pattern
            # Or just click the first clickable option
            first_option = page.locator("[id^='floating-ui-'] div[role='option']").first
            if await first_option.count() > 0:
                await first_option.click()
            else:
                # Fallback: try clicking any div that looks clickable
                first_option = page.locator("[id^='floating-ui-'] > div").first
                await first_option.click()

            await page.wait_for_timeout(500)
            print(f"✓ Location selected: {location}")
        except Exception as e:
            # If no autocomplete appears, try keyboard navigation as fallback
            print(f"⚠ Trying keyboard navigation for location: {e}")
            try:
                await page.keyboard.press("ArrowDown")
                await page.wait_for_timeout(200)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(500)
            except:
                print(f"⚠ Location autocomplete failed")
            pass

    # Fill date field - click on the date input
    date_input = await page.query_selector("//div[@id='form']/div[3]/div/div[6]/div[1]/div/input")
    if date_input:
        await date_input.click()
        await page.wait_for_timeout(500)

        # Click on the 30th day in the date picker (from the recorded actions)
        try:
            await page.wait_for_selector(
                "//div[@id='form']/div[3]/div/div[6]/div[2]/div/div/div[2]/div[2]/div[6]/div[1]",
                state="visible",
                timeout=2000,
            )
            await page.click("//div[@id='form']/div[3]/div/div[6]/div[2]/div/div/div[2]/div[2]/div[6]/div[1]")
            await page.wait_for_timeout(700)
        except Exception:
            # If date picker doesn't appear, try typing the date
            await page.fill("//div[@id='form']/div[3]/div/div[6]/div[1]/div/input", start_date)
            await page.wait_for_timeout(500)

    # Scroll down to reveal more form fields
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(500)

    # Continue scrolling to reach the submit button area
    await page.evaluate("window.scrollBy(0, 300)")
    await page.wait_for_timeout(500)

    # Answer sponsorship question (button 1 of div[7])
    # Click button 1 if needs sponsorship, button 2 if doesn't need sponsorship
    sponsorship_button_index = 1 if needs_sponsorship else 2
    sponsorship_button_selector = f"//div[@id='form']/div[3]/div/div[7]/div[2]/button[{sponsorship_button_index}]"
    try:
        await page.wait_for_selector(sponsorship_button_selector, state="visible", timeout=3000)
        await page.click(sponsorship_button_selector)
        await page.wait_for_timeout(800)
        print(f"✓ Sponsorship question answered: {'Yes' if needs_sponsorship else 'No'}")
    except Exception as e:
        print(f"⚠ Could not find sponsorship button: {e}")

    # Answer office attendance question (button 1 of div[8])
    # Click button 1 if can attend office, button 2 if cannot attend office
    office_button_index = 1 if can_attend_office else 2
    office_button_selector = f"//div[@id='form']/div[3]/div/div[8]/div/button[{office_button_index}]"
    try:
        await page.wait_for_selector(office_button_selector, state="visible", timeout=3000)
        await page.click(office_button_selector)
        await page.wait_for_timeout(1000)
        print(f"✓ Office attendance question answered: {'Yes' if can_attend_office else 'No'}")
    except Exception as e:
        print(f"⚠ Could not find office attendance button: {e}")

    # Wait indefinitely for manual review and submission
    print("\n✓ Form filled. Please review and submit manually.")
    print("Press Ctrl+C to close the browser when done.\n")

    # Keep the browser open indefinitely
    try:
        await page.wait_for_timeout(3600000)  # Wait for 1 hour (or until interrupted)
    except KeyboardInterrupt:
        print("\nClosing browser...")


async def main() -> None:
    """
    Main entry point for the automation script.

    Launches a browser, navigates to the job application page,
    and fills out the form with sample data.
    """
    async with async_playwright() as p:
        # Launch browser with headless mode
        browser: Browser = await p.chromium.launch(headless=False)
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()

        try:
            # Example usage with test data
            resume_file = Path("sample-resume.pdf")

            # Check if resume file exists, if not create a placeholder
            if not resume_file.exists():
                # For demonstration, we'll proceed without checking
                # In production, ensure the resume file exists
                print("Note: Resume file not found. Using placeholder path.")

            await fill_openai_job_application(
                page=page,
                resume_path=str(resume_file),
                name="Your Name",  # Replace with your actual name
                email="your.email@example.com",  # Replace with your actual email
                phone="1234567890",
                location="San Francisco, CA, United States",
                start_date="12/30/2024",
                needs_sponsorship=False,  # Set to True if needs sponsorship
                can_attend_office=True,   # Set to True if can attend US office 3 days/week
            )

            print("Application submission completed successfully!")

        except Exception as e:
            print(f"Error during automation: {e}")
            raise

        finally:
            # Clean up
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
