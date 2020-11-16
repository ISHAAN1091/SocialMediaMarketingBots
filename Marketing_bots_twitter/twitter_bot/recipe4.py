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


def get_followers(browser, scroll_limit, username):
    try:
        browser.get(f'https://twitter.com/{username}/followers')
        print(f'Opened profile of : {username}')
        delay('short')
        scroll_time = 1
        usernames = []
        # created this variable to track the last recorded username
        prev_last_usernames = 0
        while scroll_time <= scroll_limit:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            a = soup.find('div', attrs={'data-testid': 'primaryColumn'})
            index_prev_last_usernames = -1
            span_elements = a.find_all(
                "a", class_=["css-4rbku5", "css-18t94o4", "css-1dbjc4n", "r-1loqt21", "r-1wbh5a2", "r-dnmrzs", "r-1ny4l3l"])
            for index, span in enumerate(span_elements):
                temp_text = span['href']
                if prev_last_usernames == temp_text:
                    index_prev_last_usernames = index
                    break
            if index_prev_last_usernames != -1:
                span_elements = span_elements[index_prev_last_usernames+2:]
            if len(span_elements) == 0:
                break
            for index, span in enumerate(span_elements):
                if index % 2 == 0:
                    if ('https' not in span['href']) and ('follow' not in span['href']) and ('?q=' not in span['href']):
                        temp_text = span['href']
                        uname = temp_text[1:]
                        usernames.append(uname)
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            delay('short')
            scroll_time += 1
            prev_last_usernames = '/' + usernames[len(usernames)-1]
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
    welcome_message = random.choice(welcome_messages)
    browser.execute_script(
        "document.getElementsByClassName('notranslate public-DraftEditor-content')[0].scrollIntoView();")
    message_input.click()
    message_input_div.send_keys(welcome_message)
    delay('short')


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("testishaank1", "Abcd@1234")
    scroll_limit = 10000
    # followers_list = get_followers(browser, scroll_limit, 'botsfolio')
    # print(followers_list)
    # print(len(followers_list))
    # messaged_accounts_list = get_messaged_accounts()
    # no_of_messages = 15
    # messaging_list = get_accounts_to_be_messaged(
    #     no_of_messages, followers_list, messaged_accounts_list)
    # print(messaging_list)
    # print(len(messaging_list))
    welcome_messages = get_welcome_message()
    # for user in messaging_list:
    #     send_message(browser, user, welcome_messages)
    #     with open('MessagedAccounts.csv', 'a', newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow([user, datetime.datetime.now()])
    send_message(browser, 'IshaanKamra', welcome_messages)


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_twitter\\twitter_bot\\geckoDriver\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
