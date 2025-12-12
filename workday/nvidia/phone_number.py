"""
Playwright automation script for NVIDIA job application form.

This script automates filling out the phone contact information section
of the NVIDIA Workday job application.
"""

from playwright.async_api import Page
from .utils import clear_chip_field_by_input_id


async def fill_phone_number(
    page: Page,
    phone_device_type: str = "Home",
    country_phone_code: str = "+1",
    phone_number: str = "3334445555",
) -> None:
    """
    Fill out the phone contact section of the job application.

    Args:
        page: Playwright Page object from the workflow
        phone_device_type: Type of phone device (default: "Home").
                          Options: "Home", "Home Cellular"
        country_phone_code: Country phone code prefix (default: "+1").
        phone_number: The phone number to enter (default: "3334445555")
    """
    # Step 1: Select Phone Device Type
    print("Selecting phone device type...")
    phone_type_button = page.locator('xpath=//button[@id="phoneNumber--phoneType"]')
    await phone_type_button.click()
    await page.wait_for_timeout(500)

    # Find and click the matching device type option
    device_option = page.locator(f'//li/div[text()="{phone_device_type}"]').first
    await device_option.click()
    await page.wait_for_timeout(300)

    # Step 2: Fill Country Phone Code
    print("Filling country phone code...")

    # Clear any existing country code chip first
    await clear_chip_field_by_input_id(page, "phoneNumber--countryPhoneCode")
    await page.wait_for_timeout(300)

    # Click on the country code input
    country_code_input = page.locator("//input[@id='phoneNumber--countryPhoneCode']")
    await country_code_input.click()
    await page.wait_for_timeout(500)

    # Type "united" to filter options and press Enter to search
    await country_code_input.fill("united")
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(500)

    # Step 3: Select from Country Dropdown
    print("Selecting country from dropdown...")
    dropdown_option = page.locator("//div[@role='option']").filter(has_text="United States of America (+1)").first
    await dropdown_option.click()
    print("Country code selected.")
    await page.wait_for_timeout(500)

    # Step 4: Fill Phone Number
    print("Entering phone number...")
    phone_number_input = page.locator('xpath=//input[@id="phoneNumber--phoneNumber"]')
    await phone_number_input.click()
    await page.wait_for_timeout(300)

    # Clear any existing content and type the phone number
    await phone_number_input.fill("")
    await phone_number_input.type(phone_number, delay=30)
    await page.wait_for_timeout(500)

    print("✓ Phone number filled successfully!")
    print(f"  - Phone Device Type: {phone_device_type}")
    print(f"  - Country Code: {country_phone_code}")
    print(f"  - Phone Number: {phone_number}")
