import pytest
import yaml

from test_appium.page.app import App


class TestSearch:
    def setup(self):
        self.main = App().start().main()

    # todo: 参数化,可结合yaml文件做数据驱动 done
    # @pytest.mark.parametrize("key, stock_type, price", [
    #     # ("albb", "BABA", 100),
    #     ("JD", "JD", 20),
    # ])

    @pytest.mark.parametrize("key, stock_type, price",
                             yaml.safe_load(open("/home/chent/PycharmProjects/mmj/test_appium/yaml/search_data.yaml")))
    def test_search(self, key, stock_type, price):
        assert self.main.goto_search().search(key).get_price(stock_type) > price
    # 测试步骤的数据驱动
    def test_search_dd(self):
        App().start().main().goto_search().search2("jd")

    def test_zixuan(self):
        assert "已添加" in self.main.goto_search().search("JD").get_cho().get_msg()


