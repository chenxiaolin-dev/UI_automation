import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.get_by_test_id("username").click()
    page.get_by_test_id("username").fill("standatd_user")

    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    page.get_by_test_id("username").click()
    page.get_by_test_id("username").press("ArrowRight")
    page.get_by_test_id("username").fill("standard_user")
    page.get_by_test_id("login-button").click()
    page.get_by_test_id("add-to-cart-sauce-labs-bike-light").click()
    page.get_by_test_id("shopping-cart-link").click()
