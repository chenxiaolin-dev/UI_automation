# -*- coding: utf-8 -*-
"""全局 fixture：登录态只做一次，所有用例共享"""
import os

import pytest
from playwright.sync_api import expect

from config import INVENTORY_URL, USERS
from pages.login_page import LoginPage

AUTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth.json")


@pytest.fixture(scope="session")
def auth_file(browser):
    """登录态文件：整个测试会话只做一次真实 UI 登录，之后所有用例复用。

    第一次跑：真登录 → 把 cookie / localStorage 存成 auth.json
    之后每次跑：直接用现成的 auth.json，一次登录 UI 都不走
    """
    if os.path.exists(AUTH_FILE):
        return AUTH_FILE

    context = browser.new_context()
    page = context.new_page()
    LoginPage(page).open().login(*USERS["standard"])
    expect(page.get_by_text("Products")).to_be_visible()

    context.storage_state(path=AUTH_FILE)
    context.close()
    return AUTH_FILE


@pytest.fixture
def logged_page(browser, auth_file):
    """已登录的页面：给需要登录态的用例用。

    注意它和内置的 page fixture 的区别：
      page        —— 全新 context，未登录（用来测登录本身）
      logged_page —— 灌入 auth.json 的 context，一打开就是登录态
    """
    context = browser.new_context(storage_state=auth_file)
    page = context.new_page()
    # 关键：必须直接进「登录后才允许访问」的页面。
    # 回到首页 BASE_URL 没用 —— 首页是公开页，永远显示登录表单，
    # cookie 只有访问受保护页面时才会被真正用到。
    page.goto(INVENTORY_URL)
    yield page
    context.close()
