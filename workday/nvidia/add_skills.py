"""
Playwright automation script for filling job application with skills.

This script automates the process of adding skills to a Workday job application form.
"""

from playwright.async_api import Page


async def add_skills(page: Page, skills: list[str]) -> None:
    """
    Add skills to the job application form.

    Args:
        page: Playwright Page object
        skills: List of skills to add (e.g., ["OpenCV", "Parallelism", "Python"])

    Example:
        await add_skills(page, ["OpenCV", "Parallelism", "Python"])
    """
    for skill in skills:
        # Click on the skills input field
        skills_input = page.locator('xpath=//input[@id="skills--skills"]')
        await skills_input.click()
        await page.wait_for_timeout(500)

        # Type the skill into the input field
        await skills_input.fill(skill)
        await page.wait_for_timeout(500)

        # Press Enter to confirm input
        await skills_input.press("Enter")
        await page.wait_for_timeout(1000)

        # Wait for dropdown to appear
        await page.wait_for_timeout(500)

        # Find and click the matching skill from the dropdown options
        option_selector = '[role="option"]'
        options = page.locator(option_selector)

        # Look for the option that matches the skill
        for i in range(await options.count()):
            option = options.nth(i)
            text = await option.inner_text()
            if skill.lower() in text.lower():
                await option.click()
                await page.wait_for_timeout(500)
                break

        # Wait before processing next skill for human-like pacing
        await page.wait_for_timeout(300)

    print(f"Successfully added {len(skills)} skills to the application")
