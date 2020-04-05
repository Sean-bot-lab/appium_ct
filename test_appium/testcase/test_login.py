import pytest

from test_appium.page.app import App


class TestLogin:
    def setup(self):
        self.main = App().start().main()

    @pytest.mark.parametrize('phone,pwd,rts', [
        ("15222225555", "123456", "用户名或"),
        ("15277775555", "123456", "用户名或")
    ])
    def test_unlogin(self, phone, pwd, rts):
        assert rts in self.main.goto_profile().on_login(phone, pwd).is_login()
