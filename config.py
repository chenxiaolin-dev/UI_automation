# -*- coding: utf-8 -*-
"""全局配置：环境地址和测试账号集中放这里，不要散落在用例里"""

BASE_URL = "https://www.saucedemo.com"
# 登录后才允许访问的页面 —— storageState 复用登录态时必须直接来这里
INVENTORY_URL = BASE_URL + "/inventory.html"

USERS = {
    "standard": ("standard_user", "secret_sauce"),
    "locked": ("locked_out_user", "secret_sauce"),
    "problem": ("problem_user", "secret_sauce"),
}
