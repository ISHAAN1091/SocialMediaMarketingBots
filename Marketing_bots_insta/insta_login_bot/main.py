from selenium import webdriver
from time import sleep


class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com/')

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector(
            "input[name='username']")
        password_input = self.browser.find_element_by_css_selector(
            "input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = browser.find_element_by_xpath(
            "//button[@type='submit']")
        login_button.click()
        sleep(5)

    def clickNotNow(self):
        not_now_btn_1 = self.browser.find_element_by_css_selector(
            ".sqdOP.yWX7d.y3zKF")
        not_now_btn_1.click()
        sleep(5)
        not_now_btn_2 = self.browser.find_element_by_xpath(
            "/html/body/div[4]/div/div/div/div[3]/button[2]")
        not_now_btn_2.click()
        sleep(10)

# class ProfilePage:
#     def __init__(self,)


browser = webdriver.Firefox(
    executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta\\gecko\\geckodriver.exe")
browser.implicitly_wait(5)

login_page = LoginPage(browser)
login_page.login("k10_coder", "Abcd@1234")
login_page.clickNotNow()

browser.close()
