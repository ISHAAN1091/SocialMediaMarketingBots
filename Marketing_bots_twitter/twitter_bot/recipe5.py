from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
import datetime
import pandas as pd
import random

environment = 'test'  # development or test


def delay(duration):
    if environment == 'test':
        sleep(3)
        return
    elif environment == 'development':
        if duration == 'short':
            a = 5
            b = 10
            x = random.randint(a, b+1)
            sleep(x)
            return
        elif duration == 'long':
            a = 30
            b = 60
            x = random.randint(a, b+1)
            sleep(x)
            return


class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://twitter.com/login')
        delay('short')

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector(
            "input[name='session[username_or_email]']")
        password_input = self.browser.find_element_by_css_selector(
            "input[name='session[password]']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = browser.find_element_by_xpath(
            "//span[text()='Log in']")
        delay('short')
        login_button.click()
        print("Logged in")
        delay('long')


def get_influencer_accounts():
    try:
        influencer_accounts_list = list()
        with open('Influencers.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                influencer_accounts_list.append(row['Username'])
        return influencer_accounts_list
    except Exception as e:
        print(e)
        return []


def follow(browser, user):
    try:
        follower_profile_link = self.browser.get(
            f'https://twitter.com/{user}/')
        print(f'Checking follower : {user}')
        delay('short')
        follow_button = self.browser.find_element_by_css_selector(
            "div[data-testid='placementTracking'] span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0")
        follow_button.click()
        global no_followed_today
        no_followed_today += 1
        with open('AccountsFollowed.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [user, datetime.datetime.now().strftime("%x")])
        print(f'Followed {user}')


def get_influencer_message():
    try:
        influencer_messages = list()
        with open('InfluencerMessages.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                influencer_messages.append(row['Message'])
        return influencer_messages
    except Exception as e:
        print(e)
        return []


def send_message(browser, user, influencer_messages):
    browser.get(f'https://twitter.com/{user}/')
    delay('short')
    message_btn = browser.find_element_by_css_selector(
        "div[aria-label='Message']")
    message_btn_precise = message_btn.find_element_by_css_selector(
        "svg.r-13gxpu9.r-4qtqp9.r-yyyyoo.r-1q142lx.r-50lct3.r-dnmrzs.r-bnwqim.r-1plcrui.r-lrvibr.r-1srniue")
    message_btn_precise.click()
    delay('short')
    message_input_div = browser.find_element_by_css_selector(
        "div.DraftEditor-editorContainer")
    message_input = message_input_div.find_element_by_css_selector(
        "span")
    focus_assist_message_input = browser.find_element_by_xpath(
        "/html/body/div/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/div/div/div/aside/div[2]/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div/span")
    influencer_message = random.choice(influencer_messages)
    browser.execute_script(
        "document.getElementsByClassName('notranslate public-DraftEditor-content')[0].scrollIntoView();")
    message_input.click()
    message_input_div.send_keys(influencer_message)
    delay('short')


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("testishaank1", "Abcd@1234")
    influencer_accounts_list = get_influencer_accounts()
    influencer_messages = get_influencer_message()
    for user in influencer_accounts_list:
        follow(browser, user)
        send_message(browser, user, influencer_messages)


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_twitter\\twitter_bot\\geckoDriver\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
