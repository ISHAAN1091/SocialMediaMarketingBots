from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
import datetime
import pandas as pd
import random

environment = 'development'  # development or test


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


def get_followers(browser, scroll_limit, username):
    try:
        browser.get(f'https://www.instagram.com/{username}/')
        followers_btn = browser.find_element_by_css_selector(
            "a.-nal3")
        followers_btn.click()
        delay('short')
        scroll_time = 1
        usernames = []
        # created this variable to track the last recorded username
        prev_last_usernames = 0
        while scroll_time <= scroll_limit:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            primmary_column = soup.find('div', attrs={'class': 'PZuss'})
            index_prev_last_usernames = -1
            # unprocessed_usernames = primmary_column.find_all(
            #     "a", attrs={'class': 'FPmhX notranslate _0imsa'})
            unprocessed_usernames = list()
            user_boxes = primmary_column.find_all("li")
            for user_box in user_boxes:
                follow_status = user_box.find('button').get_text()
                if follow_status == 'Following':
                    username = user_box.find(
                        "a", attrs={'class': 'FPmhX notranslate _0imsa'})
                    unprocessed_usernames.append(username)
            for index, span in enumerate(unprocessed_usernames):
                temp_text = span['href']
                if prev_last_usernames == temp_text:
                    index_prev_last_usernames = index
                    break
            if index_prev_last_usernames != -1:
                unprocessed_usernames = unprocessed_usernames[index_prev_last_usernames+2:]
            if len(unprocessed_usernames) == 0:
                break
            for user in unprocessed_usernames:
                temp_text = user['href']
                uname = temp_text[1:len(temp_text)-1]
                usernames.append(uname)
            div_profile = browser.find_element_by_css_selector(
                'div.PZuss')
            b = div_profile.find_elements_by_tag_name('button')
            status = b[-1].text
            if status == 'Follow':
                last_profile = browser.find_elements_by_css_selector(
                    "button.sqdOP.L3NKy.y3zKF")[-1]
                last_profile.send_keys('')
                delay('short')
                last_profile = browser.find_elements_by_css_selector(
                    "button.sqdOP.L3NKy.y3zKF")[-1]
                last_profile.send_keys('')
            elif status == 'Following':
                last_profile = browser.find_elements_by_css_selector(
                    "button.sqdOP.L3NKy._8A5w5")[-1]
                last_profile.send_keys('')
                delay('short')
                last_profile = browser.find_elements_by_css_selector(
                    "button.sqdOP.L3NKy._8A5w5")[-1]
                last_profile.send_keys('')
            delay('short')
            scroll_time += 1
            prev_last_usernames = '/' + usernames[len(usernames)-1] + '/'
        print('Recorded followers')
        return usernames
    except Exception as e:
        print(e)
        return []


def get_messaged_accounts():
    try:
        messaged_accounts_list = list()
        with open('MessagedAccounts.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                messaged_accounts_list.append(row['Username'])
        return messaged_accounts_list
    except Exception as e:
        print(e)
        return []


def get_accounts_to_be_messaged(no_of_messages, followers_list, messaged_accounts_list):
    try:
        messaging_list = list()
        for follower in followers_list:
            if len(messaging_list) >= no_of_messages:
                break
            if follower not in messaged_accounts_list:
                messaging_list.append(follower)
        return messaging_list
    except Exception as e:
        print(e)
        return []


def get_welcome_message():
    try:
        welcome_messages = list()
        with open('Welcome.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                welcome_messages.append(row['Message'])
        return welcome_messages
    except Exception as e:
        print(e)
        return []


def send_message(browser, user, welcome_messages):
    try:
        print(f'Sending message to {user}')
        browser.get(f'https://www.instagram.com/{user}/')
        delay('short')
        message_btn = browser.find_element_by_css_selector(
            'button.sqdOP.L3NKy._4pI4F._8A5w5')
        message_btn.click()
        message_input = browser.find_element_by_css_selector(
            'textarea[placeholder="Message..."]')
        welcome_message = random.choice(welcome_messages)
        message_input.send_keys(welcome_message)
        delay('short')
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
    scroll_limit = 10000
    followers_list = get_followers(browser, scroll_limit, 'k10_coder')
    messaged_accounts_list = get_messaged_accounts()
    no_of_messages = 15
    messaging_list = get_accounts_to_be_messaged(
        no_of_messages, followers_list, messaged_accounts_list)
    welcome_messages = get_welcome_message()
    for user in messaging_list:
        send_message(browser, user, welcome_messages)
        with open('MessagedAccounts.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user, datetime.datetime.now()])


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta\\gecko\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
