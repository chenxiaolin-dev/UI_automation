# -*- coding: utf-8 -*-
"""登录页：只有这一个页面知道「登录按钮叫什么、用户名框怎么找」"""
from playwright.sync_api import Locator

from config import BASE_URL
from .base_page import BasePage
from .inventory_page import InventoryPage


class LoginPage(BasePage):
    def open(self):
        self.page.goto(BASE_URL)
        return self

    def login(self, username: str, password: str) -> InventoryPage:
        """登录。成功返回商品页对象，失败留在本页（用 error() 取提示）"""
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        return InventoryPage(self.page)

    def error(self) -> Locator:
        """登录失败的红色提示条"""
        return self.page.locator('[data-test="error"]')
