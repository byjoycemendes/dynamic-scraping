import asyncio
import json
import logging
from pathlib import Path

from playwright.async_api import async_playwright


logging.basicConfig(level=logging.INFO)


class NetworkMonitor:

    def __init__(self):
        self.responses = []

    async def handle_response(self, response):

        try:

            content_type = response.headers.get(
                "content-type",
                ""
            )

            logging.info(
                f"[RESPONSE] {response.status} - {response.url}"
            )

            if "application/json" in content_type:

                data = await response.json()

                self.responses.append({
                    "url": response.url,
                    "status": response.status,
                    "data": data
                })

        except Exception as e:
            logging.error(e)


class AtlasScraper:

    def __init__(self, url):

        self.url = url

        self.browser = None
        self.context = None
        self.page = None

        self.monitor = NetworkMonitor()

    async def start(self):

        playwright = await async_playwright().start()

        self.browser = await playwright.chromium.launch(
            headless=False
        )

        self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

        self.page.on(
            "response",
            self.monitor.handle_response
        )

    async def navigate(self):

        logging.info("[INFO] Abrindo página")

        await self.page.goto(
            self.url,
            wait_until="domcontentloaded"
        )

    async def analyze_page(self):

        logging.info("[INFO] Coletando informações")

        title = await self.page.title()

        logging.info(f"[TITLE] {title}")

        cookies = await self.context.cookies()

        Path("output").mkdir(exist_ok=True)

        with open(
            "output/cookies.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                cookies,
                f,
                indent=4
            )

        await self.page.screenshot(
            path="output/page.png",
            full_page=True
        )

    async def run(self):

        await self.start()

        try:

            await self.navigate()

            await asyncio.sleep(10)

            await self.analyze_page()

        finally:

            await self.browser.close()


async def main():

    scraper = AtlasScraper(
        "https://frenqulabi.com/ig/atlas"
    )

    await scraper.run()


if __name__ == "__main__":
    asyncio.run(main())