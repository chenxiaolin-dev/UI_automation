# -*- coding: utf-8 -*-
# @File    : test_my_login_pom.py
# @Time    : 2026/10/16 16:37
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
"""我的 POM 版登录用例（3 条）—— 用例里搜不到一个定位器字符串"""
from playwright.sync_api import expect

from config import USERS
from pages import LoginPage


def test_login_success(page):
    """标准用户登录成功：login() 返回商品页对象，用它的标题做断言"""
    inventory = LoginPage(page).open().login(*USERS["standard"])
    expect(inventory.title).to_be_visible()


def test_locked_out_user(page):
    """锁定用户登录失败：留在登录页，取红色提示条"""
    login = LoginPage(page).open()
    login.login(*USERS["locked"])
    expect(login.error()).to_contain_text("locked out")


def test_wrong_password(page):
    """密码错误：一个正确账号 + 一个错密码"""
    login = LoginPage(page).open()
    login.login(USERS["standard"][0], "wrong_password")
    expect(login.error()).to_contain_text("do not match")
