import asyncio
from playwright.async_api import async_playwright

async def scrape_with_playwright(url, output_file):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set to False to see the browser
        page = await browser.new_page()

        print(f"Opening page: {url}")
        await page.goto(url)
        await page.wait_for_selector('mat-sidenav-content')  # Wait for main content to load

        # Scroll to the bottom of the page
        retries = 5
        last_scroll_height = 0

        while retries > 0:
            scroll_height = await page.evaluate(
                "document.querySelector('mat-sidenav-content').scrollTop"
            )
            await page.evaluate(
                "document.querySelector('mat-sidenav-content').scrollBy(0, 500)"
            )
            await asyncio.sleep(0.7)  # Wait for content to load

            new_scroll_height = await page.evaluate(
                "document.querySelector('mat-sidenav-content').scrollTop"
            )

            if new_scroll_height == scroll_height:  # No more scrolling possible
                retries -= 1
            else:
                retries = 5  # Reset retries if content is loading
                last_scroll_height = new_scroll_height

        print("Scrolling completed.")

        # Extract all EIK values after scrolling finishes
        elements = await page.query_selector_all("//span[contains(text(), 'ЕИК')]")
        eik_values = {
            (await el.text_content()).strip().replace('ЕИК', '').strip()
            for el in elements
        }

        # Save EIK values to file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(",".join(eik_values))

        print(f"Scraping completed for {url}. Data saved to {output_file}")

        await browser.close()

# Main entry point
async def main():
    url = "https://taxireg.infosys.bg/pub/register"
    output_file = "eik_data.txt"
    await scrape_with_playwright(url, output_file)

if __name__ == "__main__":
    asyncio.run(main())
