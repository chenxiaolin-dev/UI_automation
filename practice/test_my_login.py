# -*- coding: utf-8 -*-
# @File    : test_my_login.py
# @Time    : 2026/10/15 15:42
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm


from playwright.sync_api import Page,expect

BASE = "https://www.saucedemo.com"


#操作
#正常场景
def test_login_success(page: Page):
    page.goto(BASE)
    page.get_by_role("textbox", name="Username").fill("standard_user")
    page.get_by_role("textbox", name="Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    #断言
    expect(page.get_by_text("Products")).to_be_visible()

#失败场景
def test_locked_out_user(page: Page):
    page.goto(BASE)
    page.get_by_role("textbox", name="Username").fill("locked_out_user")
    page.get_by_role("textbox", name="Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("locked out")).to_be_visible()

#失败路径
def test_wrong_password(page: Page):
    page.goto(BASE)
    page.get_by_role("textbox", name="Username").fill("standard_user")
    page.get_by_role("textbox", name="Password").fill("wrong_password")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("Username and password do not match")).to_be_visible()



