# run_tasks.py

import time
import random
import logging
import argparse
from utils import start_browser, stop_browser, random_sleep, hover_and_click
from playwright.sync_api import Page, Browser

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

def smooth_scroll(page: Page, distance: int, steps: int = 25, delay: float = 0.04):
    step = distance / steps
    direction = "down" if distance > 0 else "up"
    logger.info(f"Start smooth scroll {direction}: total {distance}px in {steps} steps")
    for i in range(1, steps + 1):
        page.mouse.wheel(0, step)
        logger.debug(f"  Step {i}/{steps}: moved {step:.1f}px")
        time.sleep(delay)
    logger.info(f"Finished smooth scroll {direction}")

def open_saucedemo(browser: Browser):
    logger.info("Opening new page and navigating to saucedemo")
    page = browser.new_page()
    page.goto("https://www.saucedemo.com")
    logger.info(f"Page title: {page.title()}")
    login(page)
    return page

def login(page: Page):
    logger.info("Starting login process")
    raw = page.locator("#login_credentials").inner_text()
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    usernames = lines[1:]
    if "locked_out_user" in usernames:
        logger.info("Removing locked_out_user from candidates")
        usernames.remove("locked_out_user")
    logger.info(f"Available usernames: {usernames}")

    random_user = random.choice(usernames)
    logger.info(f"Selected random username: {random_user}")

    passwords_raw = page.locator(".login_password").inner_text()
    passwords = [p.strip() for p in passwords_raw.splitlines() if p.strip()]
    logger.info(f"Passwords list: {passwords}")

    login_input = page.locator(".input_error.form_input").nth(0)
    password_input = page.locator(".input_error.form_input").nth(1)
    logger.info("Filling login field")
    login_input.fill(random_user)
    random_sleep(1, 3)
    logger.info("Filling password field")
    password_input.fill(passwords[1])
    random_sleep(1, 2)

    submit = page.locator(".submit-button.btn_action")
    logger.info("Hovering and clicking Submit")
    hover_and_click(page, submit)
    random_sleep(2, 3)

    logger.info("Scrolling page down and up")
    smooth_scroll(page, 1000)
    random_sleep(1, 2)
    smooth_scroll(page, -1000)
    random_sleep(1, 2)
    logger.info("Login flow completed")


def do_screenshot(page: Page, filename: str):
    logger.info(f"Taking screenshot: {filename}")
    page.screenshot(path=filename)
    random_sleep(2, 3)
    logger.info(f"Screenshot saved: {filename}")

def main():
    breakpoint()
    parser = argparse.ArgumentParser(description="Run saucedemo flow")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="If set, runs browser in headless mode"
    )
    args = parser.parse_args()

    logger.info(f"Starting browser (headless={args.headless})")
    pw, browser = start_browser(headless=args.headless)

    try:
        page = open_saucedemo(browser)
        time.sleep(2)
    finally:
        if args.headless:
            logger.info("Taking screenshot in headless mode")
            do_screenshot(page, "saucedemo_headless.png")
        else:
            logger.info("Taking screenshot in headed mode")
            do_screenshot(page, "saucedemo.png")
        logger.info("Stopping browser")
        stop_browser(pw, browser)

if __name__ == "__main__":
    main()
