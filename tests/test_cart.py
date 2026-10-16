# -*- coding: utf-8 -*-
"""需要登录态的测试：全部用 logged_page，一次登录 UI 都不走"""
from playwright.sync_api import expect

from pages import InventoryPage


def test_add_to_cart(logged_page):
    """加购一件，角标显示 1"""
    inventory = InventoryPage(logged_page)
    inventory.add_to_cart("Sauce Labs Backpack")
    expect(inventory.cart_count()).to_have_text("1")


def test_add_two_items(logged_page):
    """加购两件，角标显示 2 —— 用例自己准备数据、不依赖别的用例"""
    inventory = InventoryPage(logged_page)
    inventory.add_to_cart("Sauce Labs Backpack").add_to_cart("Sauce Labs Bike Light")
    expect(inventory.cart_count()).to_have_text("2")


def test_sort_price_low_to_high(logged_page):
    """按价格从低到高排序，第一件必须是 $7.99"""
    inventory = InventoryPage(logged_page)
    inventory.sort_by("lohi")
    expect(inventory.prices().first).to_have_text("$7.99")


def test_cart_page_keeps_item(logged_page):
    """加购后进购物车，商品还在里面（跨页面流转）"""
    cart = InventoryPage(logged_page).add_to_cart("Sauce Labs Backpack").go_to_cart()
    expect(cart.item_names).to_have_text("Sauce Labs Backpack")
    expect(cart.checkout_button).to_be_visible()
