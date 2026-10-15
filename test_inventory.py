# -*- coding: utf-8 -*-
# @File    : test_inventory.py
# @Time    : 2026/10/15 21:10
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm

from playwright.sync_api import expect

#加入购物车
def test_add_to_cart(login):
    login.get_by_role("button",name="Add to cart").first.click()
    expect(login.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")


def test_sort_by_price(login):
    login.get_by_role("combobox").select_option("lohi")
    expect(login.locator('[data-test="inventory-item-price"]').first).to_have_text("$7.99")