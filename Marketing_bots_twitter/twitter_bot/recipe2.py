from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import csv
import datetime
import pandas as pd

# Change this to control how many people followed per day
no_followed_today = 0

# Create an instance of this class to login


class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://twitter.com/login')
        sleep(5)

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector(
            "input[name='session[username_or_email]']")
        password_input = self.browser.find_element_by_css_selector(
            "input[name='session[password]']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = browser.find_element_by_xpath(
            "//span[text()='Log in']")
        login_button.click()
        print("Logged in")
        sleep(5)


def check_user(browser, user):
    try:
        browser.get(f'https://twitter.com/{user}/')
        sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        primary_column = soup.find(
            'div', attrs={'data-testid': 'primaryColumn'})
        follows_you = False
        try:
            follows_you = browser.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/span[text()="Follows you"]')
        except:
            pass
        if not follows_you:
            print(f'{user} doesn\'t follow you')
            unfollow_button = browser.find_element_by_css_selector(
                "div[data-testid='placementTracking'] span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0")
            unfollow_button.click()
            unfollow_confirm_button = browser.find_element_by_css_selector(
                "div[data-testid='confirmationSheetConfirm'] span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0")
            unfollow_confirm_button.click()
            print(f'{user} unfollowed')
            sleep(30)
            return True
        else:
            print(f'{user} follows you')
            return False
    except Exception as e:
        print(e)


def main(browser):
    login_page = LoginPage(browser)
    login_page.login("testishaank1", "Abcd@1234")
    followed_accounts = []
    with open(r'C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\botsfolio_internship_main\\botsfolio_internship\\Marketing_bots_twitter\\twitter_bot\\AccountsFollowed.csv', 'rt') as f:
        reader = csv.DictReader(f)
        # Change the following variable to alter the no. of days after which no-follow users are unfollowed
        days_to_unfollow = 4
        print(
            f'Getting list of unchecked users followed before {days_to_unfollow} days ')
        days_diff = datetime.timedelta(days=days_to_unfollow)
        req_date_unformatted = datetime.datetime.now() - days_diff
        req_date = req_date_unformatted.strftime("%x")
        for raw in reader:
            x = raw['Date_Followed']
            # x = x[:-2] + '20' + x[-2:]
            x = datetime.datetime.strptime(x, '%m/%d/%y').strftime('%x')
            if x < req_date:
                followed_accounts.append(raw['Username'])
    for user in followed_accounts:
        print(f'Checking {user}')
        a = check_user(browser, user)
        if a:
            # Adding name to DontFollow.csv
            with open(r'C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\botsfolio_internship_main\\botsfolio_internship\\Marketing_bots_twitter\\twitter_bot\\DontFollow.csv', 'a', newline='') as f:
                print(f'Adding {user} to DontFollow.csv')
                writer = csv.writer(f)
                writer.writerow([user, datetime.datetime.now()])
            # Delete line from accountsfollowed.csv
            print(f'Deleting {user} from AccountsFollowed.csv')
            df1 = pd.read_csv(
                r'C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\botsfolio_internship_main\\botsfolio_internship\\Marketing_bots_twitter\\twitter_bot\\AccountsFollowed.csv', index_col="Username")
            df1.drop([user], inplace=True)
            df1.to_csv(r'C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\botsfolio_internship_main\\botsfolio_internship\\Marketing_bots_twitter\\twitter_bot\\AccountsFollowed.csv')


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\botsfolio_internship_main\\botsfolio_internship\\Marketing_bots_twitter\\twitter_bot\\geckoDriver\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
