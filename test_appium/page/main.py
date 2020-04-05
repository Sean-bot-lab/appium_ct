from time import sleep

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from test_appium.page.base_page import BasePage
from test_appium.page.login import Login
from test_appium.page.search import Search


class Main(BasePage):

    def setup(self):
        pass

    def goto_search(self):
        _emt_homesearch = (MobileBy.ID, 'home_search')
        # self.find(_emt_homesearch).click()
        self.steps("/home/chent/PycharmProjects/mmj/test_appium/steps_yaml/search_data.yaml")
        return Search(self._driver)

    def goto_stocks(self):
        pass

    def goto_trade(self):
        pass

    def goto_profile(self):
        _emt_mine = (By.XPATH, "//*[@text='我的' and contains(@resource-id,'tab_name')]")
        self.find(_emt_mine).click()
        return Login(self._driver)
        pass

    def goto_message(self):
        pass
