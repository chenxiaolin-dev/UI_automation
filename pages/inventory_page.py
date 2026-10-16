# -*- coding: utf-8 -*-
"""商品列表页：定位器全在这里，用例里看不到一个 CSS"""
from playwright.sync_api import Locator

from .base_page import BasePage
from .cart_page import CartPage


class InventoryPage(BasePage):
    @property
    def title(self) -> Locator:
        """页面标题「Products」—— 用来断言「确实登录进来了」"""
        return self.page.get_by_text("Products")

    def item(self, item_name: str) -> Locator:
        """按商品名拿到那一整张商品卡片（而不是猜第几个 div）"""
        return self.page.locator(".inventory_item").filter(has_text=item_name)

    def add_to_cart(self, item_name: str):
        self.item(item_name).get_by_role("button", name="Add to cart").click()
        return self

    def cart_count(self) -> Locator:
        """购物车角标（加购后才会出现）"""
        return self.page.locator('[data-test="shopping-cart-badge"]')

    def sort_by(self, value: str):
        """value 取 az / za / lohi / hilo"""
        self.page.get_by_role("combobox").select_option(value)
        return self

    def prices(self) -> Locator:
        return self.page.locator(".inventory_item_price")

    def go_to_cart(self) -> CartPage:
        self.page.locator('[data-test="shopping-cart-link"]').click()
        return CartPage(self.page)
