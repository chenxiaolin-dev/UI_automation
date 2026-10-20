# UI Automation · Playwright + pytest 自动化

基于 Playwright + pytest 的 UI 自动化示例：分层设计（页面对象）、
登录态复用、参数化登录用例，可接入 Jenkins 做持续集成。

## 技术栈
Python 3.13 / pytest 9.1.1 / Playwright 1.64 / pytest-playwright 0.10 / pytest-xdist / allure-pytest


## 目录结构
config.py       环境地址与测试账号（https://www.saucedemo.com）
pages/           页面对象：所有定位器只出现在这里
tests/           用例：只有步骤和断言，搜不到一个 CSS
conftest.py      共享 fixture：登录态缓存（失效自动重登）、失败时落 trace
practice/        Day8 手写练习，不参与 CI
pytest.ini       默认参数（testpaths / alluredir）
requirements.txt 依赖版本（钉死）

## 怎么跑
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 首次安装浏览器内核；国内网络下载慢时先设镜像
set PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright
.venv\Scripts\python.exe -m playwright install chromium

.venv\Scripts\python.exe -m pytest
期望结果：10 passed（登录 6 条参数化 + 购物车 4 条）

## 覆盖什么
- 登录：正常 / 锁定 / 图片异常 / 按钮异常 / 密码错误 / 空密码（参数化，带可读 ids）
- 购物车：加入、计数、移除、去结算页
- 分层：页面对象 + fixture 共享登录态，用例里没有定位器

## 不覆盖什么（已知边界）
- 只跑 Chromium，没有跨浏览器矩阵
- 被测站点是 saucedemo 演示站（第三方，可能改版导致失败）
- 登录态缓存的 cookie 只有 10 分钟寿命，跨天跑会自动重新登录
- 还没有重试策略，flaky 会直接是红灯
