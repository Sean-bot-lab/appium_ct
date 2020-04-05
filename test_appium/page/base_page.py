import yaml
from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
import logging


class BasePage:
    logging.basicConfig(level=logging.INFO)
    _driver: WebDriver
    # 定义五花八门的黑名单,当有弹框时候,点击掉,可添加多个黑名单
    _black_list = [
        (By.ID, "tv_agree"),  # 协议
        (By.XPATH, "//*[@text='确定']"),
        (By.ID, "image_cancel"),  # 升级框
        (By.XPATH, "//*[@text='下次再说']")  # 评价
    ]
    _err_max = 5
    _err_count = 0

    _params = {}

    def __init__(self, driver: WebDriver = None):
        self._driver = driver

    # todo:当有广告,协议,评价各种弹框出现,需处理异常情况 done
    def find(self, locator, value: str = None):
        # 用于调试
        logging.info(locator)
        logging.info(value)
        try:
            # 寻找控件,三木表达式
            element = self._driver.find_element(*locator) if isinstance(locator, tuple) else \
                self._driver.find_element(locator, value)
            # 如果成功,清空错误计数
            self._err_count = 0
            return element
            # if isinstance(locator, tuple):
            #     # 传入参数是否元组,如果是的话解析传入
            #     return self._driver.find_element(*locator)
            # else:
            #     return self._driver.find_element(locator, value)

            # 找不到元素的时候,查看页面是否有黑名单元素
        except Exception as e:
            # 定义最大循环次数,避免死循环,直接报错
            if self._err_count > self._err_max:
                raise e
            # 记录异常失败次数
            self._err_count += 1
            # 对黑名单里的弹框进行处理
            for emt in self._black_list:
                logging.info(emt)
                emts = self._driver.find_elements(*emt)
                # 如果找到有黑名单元素,click掉
                if len(emts) > 0:
                    emts[0].click()
                    # 再次递归调用find方法,注意参数[_ero_max]配置
                    return self.find(locator, value)
                # self._driver.back()

                # 所有(黑名单+传入的元素)元素都没找到,就抛出异常
                logging.warn("没找到黑名单元素")
                raise e
            # return self.find(locator, value)

    # todo:通用异常,通过装饰器让函数自动处理
    def find_and_get_text(self, locator, value: str = None):
        # 用于调试
        logging.info(locator)
        logging.info(value)
        try:
            # 寻找控件,三木表达式
            element = self._driver.find_element(*locator) if isinstance(locator, tuple) else \
                self._driver.find_element(locator, value)
            # 如果成功,清空错误计数
            self._err_count = 0
            return element.text
            # if isinstance(locator, tuple):
            #     # 传入参数是否元组,如果是的话解析传入
            #     return self._driver.find_element(*locator)
            # else:
            #     return self._driver.find_element(locator, value)

            # 找不到元素的时候,查看页面是否有黑名单元素
        except Exception as e:
            # 定义最大循环次数,避免死循环,直接报错
            if self._err_count > self._err_max:
                raise e
            # 记录异常失败次数
            self._err_count += 1
            # 对黑名单里的弹框进行处理
            for emt in self._black_list:
                logging.info(emt)
                emts = self._driver.find_elements(*emt)
                # 如果找到有黑名单元素,click掉
                if len(emts) > 0:
                    emts[self._err_count - 1].click()
                    # 再次递归调用find方法,注意参数[_ero_max]配置
                    return self.find_and_get_text(locator, value)
                # self._driver.back()
                # 所有(黑名单+传入的元素)元素都没找到,就抛出异常
            logging.warn("没找到黑名单元素")
            raise e
            # return self.find(locator, value)

    # 获取toast提示
    def get_toast(self):
        return self.find(By.XPATH, "//*[@class='android.widget.Toast']").text

    def text(self, key):
        return (By.XPATH, "//*[@text='%s']" % key)

    def find_by_text(self, key):
        return self.find(self.text(key))

    # todo: 测试步骤的数据驱动需要持续优化,兼容各种情况,可用于开发测试平台
    def steps(self, path):
        with open(path) as f:
            steps: list[dict] = yaml.safe_load(f)
            elemetnt: WebElement = None
            for step in steps:
                logging.info(step)
                if "by" in step.keys():
                    elemetnt = self.find(step["by"], step["locator"])
                if "action" in step.keys():
                    action = step["action"]
                    if step["action"] == "find":
                        pass
                    elif action == "click":
                        elemetnt.click()
                    elif action == "text":
                        elemetnt.text
                    elif action == "attribute":
                        elemetnt.get_attribute(step["value"])
                    elif action in ["send", "input"]:
                        # 参数化  yaml文件中的["key"]
                        content: str = step["value"]
                        for key in self._params.keys():
                            # 将传入的参数替换到yaml文件中的["key"]
                            content = content.replace("{%s}" % key, self._params[key])
                        elemetnt.send_keys(content)
