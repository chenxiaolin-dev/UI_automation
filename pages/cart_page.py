# -*- coding: utf-8 -*-
"""购物车页"""
from playwright.sync_api import Locator

from .base_page import BasePage


class CartPage(BasePage):
    @property
    def items(self) -> Locator:
        return self.page.locator(".cart_item")

    @property
    def item_names(self) -> Locator:
        # 必须限定在 .cart_item 里面：页面切换的瞬间，上一页的 DOM 还没被替换掉，
        # 全页面搜 .inventory_item_name 会同时命中两个页面的元素 → strict mode 直接失败
        return self.page.locator(".cart_item .inventory_item_name")

    @property
    def checkout_button(self) -> Locator:
        return self.page.get_by_role("button", name="Checkout")
