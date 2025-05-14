from playwright.sync_api import sync_playwright
import random, time 

def start_browser(headless: bool = False):
    """
    Запускає Playwright і браузер, повертає tuple (playwright, browser).
    """
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless)
    return pw, browser

def stop_browser(pw, browser):
    """
    Закриває браузер і зупиняє Playwright.
    """
    browser.close()
    pw.stop()

def random_sleep(f, t):
    time.sleep(random.randint(f, t))

def hover_and_click(page, element):
    """
    Наводить курсор на елемент і клікає на нього.
    """
    element.hover()
    element.click()

