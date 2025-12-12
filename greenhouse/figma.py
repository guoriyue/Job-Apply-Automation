"""
Figma Job Application Automation Script

This script automates the completion and submission of a job application for
the Distribution Partner Manager position at Figma via Greenhouse.

The script navigates to the application page, fills in all required fields,
uploads a resume, and completes the form.
"""

import os
import asyncio
from playwright.async_api import async_playwright
import re

async def apply_for_figma_job(
    page,
    first_name: str = "s",
    last_name: str = "a",
    email: str = "s",
    phone_country: str = "United States +1",
    phone_number: str = "(333) 444-5555",
    location: str = "San Fransisco, Balearic Islands, Spain",
    why_join: str = "i love figma",
    work_location: str = "san fransisco, CA",
    authorized_to_work: str = "Yes",
    worked_before: str = "No",
    resume_path: str = "sample-resume.pdf"
):
    """
    Complete and submit a Figma job application.

    Args:
        page: Playwright page object
        first_name: Applicant's first name
        last_name: Applicant's last name
        email: Applicant's email address
        phone_country: Country for phone number. Options: United States +1,
            Afghanistan +93, Åland Islands +358, Albania +355, Algeria +213,
            American Samoa +1, Andorra +376, Angola +244, Anguilla +1,
            Antigua & Barbuda +1, Argentina +54, Armenia +374, Aruba +297,
            Ascension Island +247, Australia +61, Austria +43, Azerbaijan +994,
            Bahamas +1, Bahrain +973, Bangladesh +880, Barbados +1, Belarus +375,
            Belgium +32, Belize +501, Benin +229, Bermuda +1, Bhutan +975,
            Bolivia +591, Bosnia & Herzegovina +387, Botswana +267, Brazil +55,
            British Indian Ocean Territory +246, British Virgin Islands +1,
            Brunei +673, Bulgaria +359, Burkina Faso +226, Burundi +257,
            Cambodia +855, Cameroon +237, Canada +1, Cape Verde +238,
            Caribbean Netherlands +599, Cayman Islands +1, Central African Republic +236,
            Chad +235, Chile +56, China +86, Christmas Island +61,
            Cocos (Keeling) Islands +61, Colombia +57, Comoros +269,
            Congo - Brazzaville +242, Congo - Kinshasa +243, Cook Islands +682,
            Costa Rica +506, Côte d'Ivoire +225, Croatia +385, Cuba +53,
            Curaçao +599, Cyprus +357, Czechia +420, Denmark +45, Djibouti +253,
            Dominica +1, Dominican Republic +1, Ecuador +593, Egypt +20,
            El Salvador +503, Equatorial Guinea +240, Eritrea +291, Estonia +372,
            Eswatini +268, Ethiopia +251, Falkland Islands +500, Faroe Islands +298,
            Fiji +679, Finland +358, France +33, French Guiana +594,
            French Polynesia +689, Gabon +241, Gambia +220, Georgia +995,
            Germany +49, Ghana +233, Gibraltar +350, Greece +30, Greenland +299,
            Grenada +1, Guadeloupe +590, Guam +1, Guatemala +502, Guernsey +44,
            Guinea +224, Guinea-Bissau +245, Guyana +592, Haiti +509,
            Honduras +504, Hong Kong SAR China +852, Hungary +36, Iceland +354,
            India +91, Indonesia +62, Iran +98, Iraq +964, Ireland +353,
            Isle of Man +44, Israel +972, Italy +39, Jamaica +1, Japan +81,
            Jersey +44, Jordan +962, Kazakhstan +7, Kenya +254, Kiribati +686,
            Kosovo +383, Kuwait +965, Kyrgyzstan +996, Laos +856, Latvia +371,
            Lebanon +961, Lesotho +266, Liberia +231, Libya +218,
            Liechtenstein +423, Lithuania +370, Luxembourg +352,
            Macao SAR China +853, Madagascar +261, Malawi +265, Malaysia +60,
            Maldives +960, Mali +223, Malta +356, Marshall Islands +692,
            Martinique +596, Mauritania +222, Mauritius +230, Mayotte +262,
            Mexico +52, Micronesia +691, Moldova +373, Monaco +377, Mongolia +976,
            Montenegro +382, Montserrat +1, Morocco +212, Mozambique +258,
            Myanmar (Burma) +95, Namibia +264, Nauru +674, Nepal +977,
            Netherlands +31, New Caledonia +687, New Zealand +64, Nicaragua +505,
            Niger +227, Nigeria +234, Niue +683, Norfolk Island +672,
            North Korea +850, North Macedonia +389, Northern Mariana Islands +1,
            Norway +47, Oman +968, Pakistan +92, Palau +680,
            Palestinian Territories +970, Panama +507, Papua New Guinea +675,
            Paraguay +595, Peru +51, Philippines +63, Poland +48, Portugal +351,
            Puerto Rico +1, Qatar +974, Réunion +262, Romania +40, Russia +7,
            Rwanda +250, Samoa +685, San Marino +378, São Tomé & Príncipe +239,
            Saudi Arabia +966, Senegal +221, Serbia +381, Seychelles +248,
            Sierra Leone +232, Singapore +65, Sint Maarten +1, Slovakia +421,
            Slovenia +386, Solomon Islands +677, Somalia +252, South Africa +27,
            South Korea +82, South Sudan +211, Spain +34, Sri Lanka +94,
            St. Barthélemy +590, St. Helena +290, St. Kitts & Nevis +1,
            St. Lucia +1, St. Martin +590, St. Pierre & Miquelon +508,
            St. Vincent & Grenadines +1, Sudan +249, Suriname +597,
            Svalbard & Jan Mayen +47, Sweden +46, Switzerland +41, Syria +963,
            Taiwan +886, Tajikistan +992, Tanzania +255, Thailand +66,
            Timor-Leste +670, Togo +228, Tokelau +690, Tonga +676,
            Trinidad & Tobago +1, Tunisia +216, Turkey +90, Turkmenistan +993,
            Turks & Caicos Islands +1, Tuvalu +688, U.S. Virgin Islands +1,
            Uganda +256, Ukraine +380, United Arab Emirates +971,
            United Kingdom +44, Uruguay +598, Uzbekistan +998, Vanuatu +678,
            Vatican City +39, Venezuela +58, Vietnam +84, Wallis & Futuna +681,
            Western Sahara +212, Yemen +967, Zambia +260, Zimbabwe +263
        phone_number: Applicant's phone number
        location: Work location city. Options: San Fransisco, Balearic Islands, Spain,
            Hacienda San Fransisco, Ancash, Peru
        why_join: Why applicant wants to join Figma (3-4 sentences)
        work_location: City and state where applicant intends to work
        authorized_to_work: Work authorization status. Options: Yes, No
        worked_before: Previous work at Figma. Options: Yes, No
        resume_path: Path to resume file (pdf, doc, docx, txt, rtf)
    """

    try:
        # Navigate to the Figma job posting
        await page.goto(
            "https://job-boards.greenhouse.io/figma/jobs/5660873004?gh_jid=5660873004",
            wait_until="load"
        )
        await page.wait_for_timeout(1500)

        # Click Apply button to open the application form
        apply_button = page.get_by_role("button", name="Apply")
        await apply_button.click()
        await page.wait_for_timeout(500)

        # Fill First Name
        first_name_field = page.get_by_role("textbox", name="First Name", exact=True)
        await first_name_field.click()
        await first_name_field.fill(first_name)
        await page.wait_for_timeout(300)

        # Fill Last Name
        last_name_field = page.get_by_role("textbox", name="Last Name")
        await last_name_field.click()
        await last_name_field.fill(last_name)
        await page.wait_for_timeout(300)

        # Fill Email
        email_field = page.get_by_role("textbox", name="Email")
        await email_field.click()
        await email_field.fill(email)
        await page.wait_for_timeout(300)

        # Select Phone Country (custom dropdown)
        # Click to open the country dropdown
        country = page.get_by_role("combobox", name="Country")
        await country.click()
        await page.wait_for_timeout(500)

        # Select the country option
        country_option = page.get_by_role("option", name=phone_country)
        await country_option.click()
        await page.wait_for_timeout(300)

        # Fill Phone Number
        phone_field = page.get_by_role("textbox", name="Phone")
        await phone_field.click()
        await phone_field.fill(phone_number)
        await page.wait_for_timeout(500)

        # Select Location (City) - Autocomplete combobox
        location_field = page.get_by_role("combobox", name="Location (City)")
        await location_field.click()
        await location_field.fill(location)
        await page.wait_for_timeout(500)

        # Click the location option
        location_option = page.get_by_role("option", name=location)
        await location_option.click()
        await page.wait_for_timeout(500)

        # Scroll down to see Resume/CV section
        await page.wait_for_timeout(300)

        # Upload Resume - Click Attach button
        attach_button = page.get_by_role("button", name="Attach")
        await attach_button.click()
        await page.wait_for_timeout(300)

        # Set the file input
        file_input = page.locator('input[type="file"]#resume')
        await file_input.set_input_files(os.path.abspath(resume_path))
        await page.wait_for_timeout(1000)

        # Scroll down to see more fields
        await page.wait_for_timeout(300)

        # Fill Why do you want to join Figma?
        why_join_field = page.get_by_role("textbox", name="Why do you want to join Figma?")
        await why_join_field.click()
        await why_join_field.fill(why_join)
        await page.wait_for_timeout(300)

        # Scroll down to work location field
        await page.wait_for_timeout(300)

        # Fill From where do you intend to work?
        work_location_field = page.get_by_role("textbox", name="From where do you intend to work?")
        await work_location_field.click()
        await work_location_field.fill(work_location)
        await page.wait_for_timeout(300)

        # Scroll down to authorization fields
        await page.wait_for_timeout(300)

        # Select "Are you authorized to work in the country for which you applied?"
        auth_dropdown = page.get_by_role("combobox", name="Are you authorized to work in the country for which you applied?")
        await auth_dropdown.click()
        await page.wait_for_timeout(500)

        auth_option = page.get_by_role("option", name=authorized_to_work)
        await auth_option.click()
        await page.wait_for_timeout(300)

        # Select "Have you ever worked for Figma before, as an employee or a contractor/consultant?"
        worked_before_dropdown = page.get_by_role("combobox", name="Have you ever worked for Figma before, as an employee or a contractor/consultant?")
        await worked_before_dropdown.click()
        await page.wait_for_timeout(500)

        worked_before_option = page.get_by_role("option", name=worked_before)
        await worked_before_option.click()
        await page.wait_for_timeout(300)

        # Scroll to Submit button
        await page.wait_for_timeout(500)

        # Submit the application
        submit_button = page.get_by_role("button", name="Submit application")
        await submit_button.click()
        await page.wait_for_timeout(1000)

        print("✓ Application submitted successfully")

    except Exception as e:
        print(f"✗ Error during application submission: {str(e)}")
        raise


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

            # Call the automation function
            await apply_for_figma_job(
                page,
                first_name="s",
                last_name="a",
                email="s",
                phone_country="United States +1",
                phone_number="(333) 444-5555",
                location="San Fransisco, Balearic Islands, Spain",
                why_join="i love figma",
                work_location="san fransisco, CA",
                authorized_to_work="Yes",
                worked_before="No",
                resume_path="sample-resume.pdf"
            )

            await browser.close()

    asyncio.run(main())
