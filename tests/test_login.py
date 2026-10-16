# -*- coding: utf-8 -*-
"""登录本身的测试：用全新 page（未登录态），这里才需要真的走登录 UI"""
from playwright.sync_api import expect

from config import USERS
from pages import LoginPage


def test_login_success(page):
    """正常用户能登录进商品页"""
    inventory = LoginPage(page).open().login(*USERS["standard"])
    expect(inventory.title).to_be_visible()


def test_locked_out_user(page):
    """被锁用户登录失败，提示 locked out"""
    login = LoginPage(page).open()
    login.login(*USERS["locked"])
    expect(login.error()).to_contain_text("locked out")


def test_wrong_password(page):
    """密码错误提示不匹配"""
    login = LoginPage(page).open()
    login.login(USERS["standard"][0], "wrong_password")
    expect(login.error()).to_contain_text("do not match")
