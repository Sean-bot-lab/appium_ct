from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

from test_appium.page.base_page import BasePage


class Search(BasePage):

    def search(self, key: str):
        # todo:多平台,多版本,多个可能定位符,新老版本定位符
        _emt_search_input = (MobileBy.ID, "search_input_text")
        _emt_name = (MobileBy.ID, "name")
        self.find(_emt_search_input).send_keys(key)
        self.find(_emt_name).click()
        # 链式调用
        return self

    def search2(self, key: str):
        # todo:多平台,多版本,多个可能定位符,新老版本定位符
        self._params = {}
        self._params["key"] = key

        self.steps("/home/chent/PycharmProjects/mmj/test_appium/steps_yaml/search2_data.yaml")
        # 链式调用
        return self

    def get_price(self, key: str) -> float:
        _emt_price = (MobileBy.ID, "current_price")
        return float(self.find(_emt_price).text)

    def get_cho(self):
        _loc_cho = (By.ID, "follow_btn")
        self.find(_loc_cho).click()
        return self

    def get_msg(self):
        _loc_choed = (By.ID, "followed_btn")
        return self.find_and_get_text(_loc_choed)
