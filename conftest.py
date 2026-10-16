# -*- coding: utf-8 -*-
"""全局 fixture：登录态只做一次，所有用例共享"""
import os

import pytest
from playwright.sync_api import expect

from config import INVENTORY_URL, USERS
from pages.login_page import LoginPage

AUTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth.json")
TRACE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-results")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """把每个阶段的执行结果挂到用例对象上，收尾时才知道它有没有失败。

    为什么要这一段：pytest 的 fixture 收尾（yield 之后）跑在用例执行完之后，
    但那时拿不到「刚才到底过没过」。先把结果存到 item 上，收尾里就能读了。
    """
    outcome = yield
    setattr(item, "rep_" + outcome.get_result().when, outcome.get_result())


def _save_trace_on_failure(context, request):
    """失败才留 trace：成功的不占地方，失败的必有据可查。

    ⚠️ 为什么不直接用 pytest 的 --tracing=retain-on-failure？
    因为那个开关只作用在 pytest-playwright 自带的 page / context fixture 上。
    而我们的 logged_page 是自己在 conftest 里 new_context(...) 建的，
    框架根本不认识它 —— 用参数跑一遍会发现 test-results 里什么都没有。
    所以自己建的 context，要自己开 trace。
    """
    failed = bool(getattr(request.node, "rep_call", None) and request.node.rep_call.failed)
    if failed:
        os.makedirs(TRACE_DIR, exist_ok=True)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in request.node.name)
        context.tracing.stop(path=os.path.join(TRACE_DIR, safe + "-trace.zip"))
    else:
        context.tracing.stop()


def _login_and_save(browser) -> str:
    """真实走一次 UI 登录，把登录态存进 auth.json"""
    context = browser.new_context()
    page = context.new_page()
    LoginPage(page).open().login(*USERS["standard"])
    expect(page.get_by_text("Products")).to_be_visible()

    context.storage_state(path=AUTH_FILE)
    context.close()
    return AUTH_FILE


def _storage_state_still_valid(browser) -> bool:
    """验货：拿缓存登录态去开受保护页，能看到商品列表才算有效。

    为什么不能只看文件在不在 —— 登录态是会过期的！
    saucedemo 的 session cookie 只有 10 分钟寿命，过期后 Playwright
    加载时会把失效 cookie 直接丢弃，等于没登录。真实系统的 session
    一样会过期，所以「复用前先验货、失效就重登」是框架的标准兜底。
    """
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    page.goto(INVENTORY_URL)
    try:
        expect(page.get_by_text("Products")).to_be_visible(timeout=5000)
        return True
    except AssertionError:
        return False
    finally:
        context.close()


@pytest.fixture(scope="session")
def auth_file(browser):
    """登录态文件：整个测试会话只做一次真实 UI 登录，之后所有用例复用。

    第一次跑：真登录 → 把 cookie / localStorage 存成 auth.json
    之后每次跑：先验货 —— 缓存还有效就直接用；过期就删掉重新登录
    """
    if os.path.exists(AUTH_FILE) and _storage_state_still_valid(browser):
        return AUTH_FILE

    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)  # 过期的缓存，留着没用
    return _login_and_save(browser)


@pytest.fixture
def logged_page(browser, auth_file, request):
    """已登录的页面：给需要登录态的用例用。

    注意它和内置的 page fixture 的区别：
      page        —— 全新 context，未登录（用来测登录本身）
      logged_page —— 灌入 auth.json 的 context，一打开就是登录态
    """
    context = browser.new_context(storage_state=auth_file)
    # 自己建的 context，要自己开 trace（截图 + DOM 快照 + 源码）
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    # 关键：必须直接进「登录后才允许访问」的页面。
    # 回到首页 BASE_URL 没用 —— 首页是公开页，永远显示登录表单，
    # cookie 只有访问受保护页面时才会被真正用到。
    page.goto(INVENTORY_URL)
    yield page
    _save_trace_on_failure(context, request)
    context.close()
