# -*- coding: utf-8 -*-
"""登录本身的测试：用全新 page（未登录态），这里才需要真的走登录 UI"""
import pytest
from playwright.sync_api import expect


from pages import LoginPage



@pytest.mark.parametrize("user,pwd,expect_ok", [
    ("standard_user",  "secret_sauce" ,True),  #正常用户
    ("locked_out_user", "secret_sauce" ,False), #被锁定
    ("problem_user", "secret_sauce" ,True),   # 图片异常但能登录
    ("error_user",  "secret_sauce" ,  True), #慢用户
    ("standard_user", "wrong_password" , False),  #密码错误（用空密码位区分)
    ("standard_user", "", False),
],ids=[
    "normal",
    "locked",
    "problem",
    "error",
    "wrong-password",
    "qingshurumima"
])
def test_login(page, user, pwd, expect_ok):
    """登录参数化：5组数据走同一条流程，只有数据和期望不同"""
    login_page = LoginPage(page).open()
    inventory = login_page.login(user, pwd) #接住返回值（商品页对象)

    if expect_ok:
        expect(inventory.title).to_be_visible() #成功：看到products标题

    else:
        expect(login_page.error()).to_be_visible()  #失败，看到红色错误条
