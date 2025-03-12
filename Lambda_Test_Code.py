import json
import os
import urllib
import subprocess

from playwright.sync_api import sync_playwright

capabilities = {
    'browserName': 'Chrome',  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    'browserVersion': 'latest',
    'LT:Options': {
        'platform': 'Windows 10',
        'build': 'Playwright Python Build',
        'name': 'Playwright Test',
        'user': 'taushiqbalamurugan',
        'accessKey': 'LT_cDORzpIj7rx0zIl6NoteCB68mhHSfNAt9IGPNHdVyBxUSrt',
        'network': True,
        'video': True,
        'console': True,
        'tunnel': False,  # Add tunnel configuration if testing locally hosted webpage
        'tunnelName': '',  # Optional
        'geoLocation': '', # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    }
}


def run(playwright):
    playwrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
    capabilities['LT:Options']['playwrightClientVersion'] = playwrightVersion

    lt_cdp_url = 'wss://cdp.lambdatest.com/playwright?capabilities=' + urllib.parse.quote(
        json.dumps(capabilities))
    browser = playwright.chromium.connect(lt_cdp_url)
    page = browser.new_page()
    try:
        page.goto("https://www.amazon.in/")
        page.wait_for_timeout(3000)
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

    except Exception as err:
        print("Error:: ", err)
        set_test_status(page, "failed", str(err))


    browser.close()



def set_test_status(page, status, remark):
    page.evaluate("_ => {}",
                  "lambdatest_action: {\"action\": \"setTestStatus\", \"arguments\": {\"status\":\"" + status + "\", \"remark\": \"" + remark + "\"}}");


with sync_playwright() as playwright:
    run(playwright)