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


def get_keywords():
    try:
        keywords = list()
        with open('Keywords.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                keywords.append(row['Keywords'])
        return keywords
    except Exception as e:
        print(e)
        return []


def search(browser, keyword):
    keyword = keyword.replace(" ", "%20")
    keyword = keyword.replace('#', '%23')
    browser.get(
        f'https://twitter.com/search?q={keyword}&src=typed_query&f=live')
    delay('short')


def like_tweets(browser, no_of_likes):
    prev_last_tweet = 0
    likes = 0
    while True:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        primary_column = soup.find(
            'div', attrs={'data-testid': 'primaryColumn'})
        tweets = primary_column.find_all(
            'div', attrs={'data-testid': 'like'})
        a = -1
        if prev_last_tweet in tweets:
            a = tweets.index(prev_last_tweet)
        if a != -1:
            tweets = tweets[a:]
        for tweet in tweets:
            if likes < no_of_likes:
                tweet_like_button = browser.find_element_by_css_selector(
                    "div[data-testid='like'] svg.r-4qtqp9.r-yyyyoo.r-1xvli5t.r-dnmrzs.r-bnwqim.r-1plcrui.r-lrvibr.r-1hdv0qi")
                tweet_like_button.click()
                likes += 1
                delay('short')
                print(f'Liked tweet no. {likes} of {no_of_likes}')
                prev_last_tweet = tweet
            else:
                break
        if likes >= no_of_likes:
            break
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        delay('short')


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("testishaank1", "Abcd@1234")
    keywords = get_keywords()
    for keyword in keywords:
        search(browser, keyword)
        # Set no of likes you want before moving to the next keyword/ending the program
        no_of_likes = 3
        like_tweets(browser, no_of_likes)


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_twitter\\twitter_bot\\geckoDriver\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
