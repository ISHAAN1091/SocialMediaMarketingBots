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


def login(browser):
    url = "https://medium.com/m/callback/email?token=3ead218a1742&operation=login&state=medium"
    browser.get(url)
    print('Logged In')
    delay('short')


def search_url(keyword):
    keyword = keyword.replace(" ", "%20")
    keyword = keyword.replace('#', '%23')
    return keyword


def get_users(browser, no_of_users):
    try:
        user_profiles = set()
        while len(user_profiles) != no_of_users:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            all_links = soup.find_all('a')
            for link in all_links:
                if len(user_profiles) == no_of_users:
                    break
                if "https://medium.com/@" in link['href']:
                    profile = link['href'][20:-19]
                    user_profiles.add(profile)
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            delay('short')
        print('Recorded user profiles')
        return user_profiles
    except Exception as e:
        print(e)


def follow(browser, user):
    try:
        browser.get(f'https://medium.com/@{user}')
        follow_btn = browser.find_element_by_xpath(
            '//*[@id="root"]/div/section/div[1]/div[2]/div[2]/div[2]/div/div[1]/button')
        follow_btn.click()
        with open('AccountsFollowed.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [user, datetime.datetime.now().strftime("%x")])
        print(f'Followed {user}')
        delay('long')
    except Exception as e:
        print(e)


def clap(browser, no_of_claps):
    # try:
    posts = set()
    no_of_claps_count = 0
    last_clap = None
    while no_of_claps_count <= no_of_claps:
        temp = browser.find_elements_by_css_selector('div.n.o')
        # print(temp)
        for post in temp:
            # post = post.find_element_by_css_selector('div.n.o')
            post = post.find_elements_by_css_selector("*")
            # print(post)
            post = post[0]
            # post = post.find_elements_by_css_selector("*")
            # print(post)
            # post = post[0]
        # print(temp)
        if len(temp) > 0 and temp[-1] == last_clap:
            break
        for post in temp:
            if len(posts) == no_of_claps:
                break
            posts.add(post)
        # print(posts)
        for post in posts:
            if no_of_claps_count == no_of_claps:
                break
            post.click()
            post.click()
            no_of_claps_count += 1
            print(f'Clapped posts {no_of_claps_count} of {no_of_claps}')
            delay('short')
        if no_of_claps_count == no_of_claps:
            break
        if len(temp) > 0:
            last_clap = temp[-1]
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        delay('short')
        # print(no_of_claps_count)
    # except Exception as e:
    #     print(e)


def get_twitter_handle(browser, user):
    try:
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_links = soup.find_all('a')
        twitter_link = None
        for link in all_links:
            if 'https://twitter.com/' in link['href']:
                twitter_link = link
                break
        if twitter_link == None:
            print('Twitter handle link not found ')
        else:
            with open('TwitterHandles.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    [user, twitter_link['href'][20:]])
            print(f'Recorded twitter handle of {user}')
    except Exception as e:
        print(e)


def follow_publications(browser, no_of_publications):
    try:
        follow_btns = set()
        no_of_follows_count = 0
        while no_of_follows_count <= no_of_publications:
            temp = browser.find_elements_by_css_selector('span')
            for follow_btn in temp:
                if len(follow_btns) == no_of_publications:
                    break
                if follow_btn.text == 'Follow':
                    follow_btns.add(follow_btn)
            for follow_btn in follow_btns:
                if no_of_follows_count == no_of_publications:
                    break
                try:
                    follow_btn.click()
                except:
                    pass
                delay('long')
                no_of_follows_count += 1
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            delay('short')
        print('Publications followed')
    except Exception as e:
        print(e)


def main(browser):
    login(browser)
    keyword = "bots #trading"
    key = search_url(keyword)
    browser.get(f'https://medium.com/search/users?q={key}')
    user_profiles = get_users(browser, 50)
    for index, user in enumerate(user_profiles):
        if index == 0:
            continue
        follow(browser, user)
        get_twitter_handle(browser, user)
        no_of_claps = 2
        clap(browser, no_of_claps)
    browser.get(f'https://medium.com/search/publications?q={key}')
    follow_publications(browser, 50)


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_medium\\medium_bots\\gecko\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
