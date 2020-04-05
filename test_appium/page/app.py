import datetime
from time import sleep

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from test_appium.page.base_page import BasePage
from test_appium.page.main import Main


class App(BasePage):
    _appPackage = "com.xueqiu.android"
    _appActivity = ".view.WelcomeActivityAlias"

    # def __init__(self,driver:WebDriver):

    def start(self):
        if self._driver is None:
            caps = {}
            caps["platformName"] = "android"
            caps["deviceName"] = "hgwz"
            caps["appPackage"] = self._appPackage
            caps["appActivity"] = self._appActivity
            # caps["noReset"] = True
            caps["chromedriverExecutable"] = "/soft_ct/chrome/chrome_driver/chromedriver"
            # 配置Appium等待多少时间未接收到来自客户端的新命令时终止整个会话，默认60秒
            caps["newCommandTimeout"] = 600
            self._driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
            self._driver.implicitly_wait(5)
            return self
        else:
            print(self._driver)
            # todo: kill app start app
            self._driver.start_activity(self._appPackage, self._appActivity)

    def restart(self):
        pass

    def stop(self):
        pass

    def main(self) -> Main:
        # todo:广告点击 done
        # print("chent:"+self._driver.page_source)
        # 当页面加载出[我的]或者[同意],后续代码才走
        def wait_load(driver):
            print(datetime.datetime.now())
            source = self._driver.page_source
            if "我的" in source:
                return True
            if "同意" in source:
                return True
            if "image_cancel" in source:
                return True
            return False

        # WebDriverWait(self._driver, 10).until(lambda x: 'com.xueqiu.android:id/logo' in self._driver.page_source)
        WebDriverWait(self._driver, 10).until(wait_load)
        return Main(self._driver)
