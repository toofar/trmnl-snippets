#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 800, 'height': 480})
        await page.context.grant_permissions(['local-fonts'])
        with open("base.html") as f:
            await page.set_content(f.read())
        await page.screenshot(path='image.png')
        await browser.close()

# TODO:
# * to 1 bit png

asyncio.run(main())
