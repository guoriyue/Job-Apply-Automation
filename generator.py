from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page17.get_by_role("group", name="Phone").get_by_label("Toggle flyout").click()
    page17.get_by_role("option", name="United States +").click()
    page17.get_by_label("Phone").fill("1112223333")
    page17.get_by_text("Location (City)*Locate me").click()
    page17.locator("div:nth-child(5) > .select > .select__container > .select-shell > div > .select__control > .select__value-container > .select__input-container").first.click()
    page17.get_by_label("Location (City)*").fill("san fransisco, cali")
    page17.get_by_label("Location (City)*").press("Meta+a")
    page17.get_by_label("Location (City)*").fill("San Fransisco")
    page17.get_by_role("option", name="San Fransisco, Balearic").click()
    page17.get_by_role("button", name="Attach").click()
    page17.get_by_role("button", name="Attach").set_input_files("sample-resume.pdf")
    page17.get_by_label("Why do you want to join Figma?").click()
    page17.get_by_label("Why do you want to join Figma?").fill("love")
    page17.get_by_label("From where do you intend to").click()
    page17.get_by_label("From where do you intend to").fill("CA")
    page17.locator("div:nth-child(9) > .select > .select__container > .select-shell > div > .select__control > .select__value-container > .select__input-container").click()
    page17.get_by_role("option", name="Yes").click()
    page17.locator("div:nth-child(10) > .select > .select__container > .select-shell > div > .select__control > .select__value-container > .select__input-container").click()
    page17.get_by_role("option", name="Yes").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
