from selenium.webdriver.common.by import By

from test_appium.page.base_page import BasePage


class Login(BasePage):
    # 账号密码登录
    def on_login(self, phone, pwd):
        _login_linlk = (By.XPATH, '//*[@text="帐号密码登录"]')
        _name = (By.ID, 'login_account')
        _pwd = (By.ID, 'login_password')
        _submit = (By.ID, 'button_next')

        self.find(_login_linlk).click()
        self.find(_name).send_keys(phone)
        self.find(_pwd).send_keys(pwd)
        self.find(_submit).click()
        return self
    def is_login(self):
        _err = (By.ID, "md_content")
        return self.find(_err).text
