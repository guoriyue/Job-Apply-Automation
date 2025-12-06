import asyncio
from playwright.async_api import async_playwright, Page

CDP_URL = "http://localhost:9222"


async def apply_to_nvidia_job_with_skills(
    skills: list[str] | None = None,
) -> None:
    """
    Automates filling in the NVIDIA Senior Manager - Robotics Quality Assurance
    job application with selected skills.

    This function navigates to the job application page and adds skills from a
    customizable list.

    Args:
        skills: List of skills to add to the application (e.g., ["OpenCV", "Parallelism"]).
                Defaults to ["OpenCV", "Parallelism"] if not provided.

    Example:
        await apply_to_nvidia_job_with_skills(
            skills=["OpenCV", "Parallelism", "Python"]
        )
    """
    if skills is None:
        skills = ["OpenCV", "Parallelism"]

    async with async_playwright() as p:
        # Attach to existing Chrome via CDP
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0] if browser.contexts else await browser.new_context()
        page: Page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        try:
            # Navigate to the job application page
            job_url = (
                "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/"
                "US,-CA,-Santa-Clara/Senior-Manager--Robotics-Quality-Assurance_JR2003248/"
                "apply/autofillWithResume"
            )
            await page.goto(job_url, wait_until="load")
            await page.wait_for_timeout(1500)

            # Process each skill in the list
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
                option_selector = f'[role="option"]'
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

            # Wait to ensure all changes are processed
            await page.wait_for_timeout(1000)

            print(f"Successfully added {len(skills)} skills to the application")

        # Don't close browser - it's the user's Chrome


if __name__ == "__main__":
    # Example usage with default skills (OpenCV and Parallelism)
    asyncio.run(apply_to_nvidia_job_with_skills())

    # Example with custom skills
    # asyncio.run(apply_to_nvidia_job_with_skills(
    #     skills=["Python", "Machine Learning", "CUDA"]
    # ))
