# -*- coding: utf-8 -*-
"""所有页面对象的基类：只放公共能力，不放任何业务"""
from playwright.sync_api import Page

from config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str = BASE_URL):
        """打开页面。返回 self，这样才能链式调用：LoginPage(page).open().login(...)"""
        self.page.goto(url)
        return self

    @property
    def url(self) -> str:
        return self.page.url

    def title(self) -> str:
        return self.page.title()
