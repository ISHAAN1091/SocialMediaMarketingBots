from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
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


def get_post_links(browser, no_of_likes, keyword):
    try:
        browser.get(f'https://www.instagram.com/explore/tags/{keyword}/')
        delay('short')
        post_links = list()
        prev_last_post = 0
        while True:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            primary_column = soup.find(
                'article', attrs={'class': 'KC1QD'})
            posts = primary_column.find_all('a')[9:]
            a = -1
            if prev_last_post in posts:
                a = posts.index(prev_last_post)
            if a != -1:
                posts = posts[a:]
            for post in posts:
                if len(post_links) < no_of_likes:
                    link = post['href'][1:]
                    post_links.append(link)
                    prev_last_post = post
                else:
                    break
            if len(post_links) >= no_of_likes:
                break
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            delay('short')
        return post_links
    except Exception as e:
        print(e)
        return[]


def like_post(browser, link):
    try:
        browser.get(f'https://instagram.com/{link}')
        like_btn = browser.find_element_by_css_selector(
            'svg[aria-label="Like"]')
        like_btn.click()
        delay('short')
    except Exception as e:
        print(e)


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("k10_coder", "Abcd@1234")
    login_page.clickNotNow()
    keywords = get_keywords()
    for keyword in keywords:
        no_of_likes = 4
        post_links = get_post_links(
            browser, no_of_likes, keyword)
        for index, link in enumerate(post_links):
            like_post(browser, link)
            print(
                f'Liked post no. {index+1} of {no_of_likes}')
        print(f"Liked posts for {keyword}")


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta_bots\\gecko\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
