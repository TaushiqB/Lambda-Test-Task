from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def open_amazon(playwright):
    browser = playwright.chromium.launch(headless=False) 
    page = browser.new_page()
    page.wait_for_timeout(5000)
    page.goto("https://www.amazon.in/")
    search_bar_xpath = '//*[@id="twotabsearchtextbox"]'
    page.wait_for_selector(search_bar_xpath)
    page.fill(search_bar_xpath, "iphone")
    page.press(search_bar_xpath, "Enter")
    page.wait_for_selector("div.s-main-slot", timeout=10000)
    page.wait_for_timeout(2000)
    
    
    product_title_locator = page.locator('h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal')
    
    if product_title_locator.count() > 0:
        product_title_text = product_title_locator.first.inner_text().strip()
        print("Title:", product_title_text)
        if "iphone" in product_title_text.lower():
            print("Title has iphone")
        else:
            print("No 'iphone'.")
    else:
        print("No product Title")

    page.wait_for_timeout(5000)
    browser.close()

with sync_playwright() as playwright:
    open_amazon(playwright)