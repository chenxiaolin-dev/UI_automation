
import pytest
from playwright.sync_api import expect

BASE = "https://www.saucedemo.com"


@pytest.fixture
def login(page):
    """已登录的页面，需要直接用"""
    page.goto(BASE)
    page.get_by_role("textbox",name="Username").fill("standard_user")
    page.get_by_role("textbox",name="Password").fill("secret_sauce")
    page.get_by_role("button",name="Login").click()
    expect(page.get_by_text("Products")).to_be_visible()
    return page

