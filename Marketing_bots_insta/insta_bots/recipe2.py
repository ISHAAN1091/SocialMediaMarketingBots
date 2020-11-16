from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
import datetime
import pandas as pd
import random

no_unfollowed_today = 0


environment = 'test'  # development or test


# Create an instance of this class to login
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
            unprocessed_usernames = primmary_column.find_all(
                "a", attrs={'class': 'FPmhX notranslate _0imsa'})
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


def unfollow_user(browser, username):
    try:
        browser.get(f'https://www.instagram.com/{username}/')
        delay('short')
        unfollow_btn = browser.find_element_by_css_selector(
            "span[aria-label='Following']")
        unfollow_btn.click()
        unfollow_confirm_btn = browser.find_element_by_css_selector(
            "button.aOOlW.-Cab_")
        unfollow_confirm_btn.click()
        delay('long')
    except Exception as e:
        print(e)


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("k10_coder", "Abcd@1234")
    login_page.clickNotNow()
    scroll_limit = 10000
    followers_list = get_followers(browser, scroll_limit, 'k10_coder')
    followed_accounts = []
    with open('AccountsFollowed.csv', 'rt') as f:
        reader = csv.DictReader(f)
        # Change the following variable to alter the no. of days after which no-follow users are unfollowed
        days_to_unfollow = 4
        print(
            f'Getting list of unchecked users followed before {days_to_unfollow} days ')
        days_diff = datetime.timedelta(days=days_to_unfollow)
        req_date_unformatted = datetime.datetime.now() - days_diff
        req_date = req_date_unformatted.strftime("%x")
        for raw in reader:
            x = raw['Date']
            x = datetime.datetime.strptime(x, '%m/%d/%y').strftime('%x')
            if x < req_date:
                followed_accounts.append(raw['Username'])
    for user in followed_accounts:
        print(f'Checking {user}')
        if user not in followers_list:
            print('Verification : Fail')
            unfollow_user(browser, user)
            print(f'{user} unfollowed')
            # Adding name to DontFollow.csv
            with open('DontFollow.csv', 'a', newline='') as f:
                print(f'Adding {user} to DontFollow.csv')
                writer = csv.writer(f)
                writer.writerow([user, datetime.datetime.now()])
            # Delete line from accountsfollowed.csv
            print(f'Deleting {user} from AccountsFollowed.csv')
            df1 = pd.read_csv('AccountsFollowed.csv', index_col="Username")
            df1.drop([user], inplace=True)
            df1.to_csv('AccountsFollowed.csv')


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta\\gecko\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    browser.close()
