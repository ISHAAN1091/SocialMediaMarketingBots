from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
import datetime
import pandas as pd
import random

no_followed_today = 0

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
        delay('short')

    def clickNotNow(self):
        not_now_btn_1 = self.browser.find_element_by_css_selector(
            ".sqdOP.yWX7d.y3zKF")
        not_now_btn_1.click()
        delay('short')
        not_now_btn_2 = self.browser.find_element_by_css_selector(
            "button.aOOlW.HoLwm ")
        not_now_btn_2.click()
        print("Logged in")
        delay('short')


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
        follower_profile_link = browser.get(
            f'https://instagram.com/{user}/')
        print(f'Checking follower : {user}')
        delay('short')
        follow_button = browser.find_element_by_css_selector(
            "div.Igw0E.IwRSH.eGOV_._4EzTm  button._5f5mN.jIbKX._6VtSN.yZn4P")
        follow_button.click()
        global no_followed_today
        no_followed_today += 1
        with open('AccountsFollowed.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [user, datetime.datetime.now().strftime("%x")])
        print(f'Followed {user}')
    except Exception as e:
        print(e)


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
    try:
        print(f'Sending message to {user}')
        browser.get(f'https://www.instagram.com/{user}/')
        delay('short')
        message_btn = browser.find_element_by_css_selector(
            'button.sqdOP.L3NKy._4pI4F._8A5w5')
        message_btn.click()
        delay('short')
        message_input = browser.find_element_by_css_selector(
            'textarea[placeholder="Message..."]')
        influencer_message = influencer_messages[0]
        message_input.send_keys(influencer_message)
        message_bar = browser.find_element_by_css_selector('div.X3a-9')
        send_btn = message_bar.find_element_by_css_selector(
            'button.sqdOP.yWX7d.y3zKF')
        send_btn.click()
        print('Message sent')
        delay('long')
    except Exception as e:
        print(e)


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("k10_coder", "Abcd@1234")
    login_page.clickNotNow()
    influencer_accounts_list = get_influencer_accounts()
    influencer_messages = get_influencer_message()
    for user in influencer_accounts_list:
        follow(browser, user)
        send_message(browser, user, influencer_messages)


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta\\gecko\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    # browser.close()
