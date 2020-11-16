from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import csv
import datetime
import pandas as pd
import random

# Change this to control how many people followed per day
no_followed_today = 0


environment = 'test'  # development or test


def delay(duration):
    if environment == 'test':
        sleep(3)
        return
    elif environment == 'development':
        if duration == 'short':
            a = 5
            b = 15
            x = random.randint(a, b+1)
            sleep(x)
            return
        elif duration == 'long':
            a = 10
            b = 30
            x = random.randint(a, b+1)
            sleep(x)
            return


# Create an instance of this class to login
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


# Create an instance of this class to get followers of competitor , check follower profiles for conditions and to follow them
class ProfilePage:
    def __init__(self, browser, username):
        self.browser = browser
        self.browser.get(f'https://twitter.com/{username}/followers')
        print(f'Opened profile of competitor : {username}')
        delay('short')

    def get_followers(self, scroll_limit):
        try:
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

    def check_follower(self, min_followers, min_tweets, user):
        try:
            follower_profile_link = self.browser.get(
                f'https://twitter.com/{user}/')
            print(f'Checking follower : {user}')
            delay('short')
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            primary_column = soup.find(
                'div', attrs={'data-testid': 'primaryColumn'})
            no_of_followers_str = primary_column.find(
                "a", attrs={'href': f'/{user}/followers'}).get_text()
            no_of_followers = ""
            while no_of_followers_str[0] != " ":
                if no_of_followers_str[0] == ',':
                    no_of_followers_str = no_of_followers_str[1:]
                    continue
                no_of_followers += no_of_followers_str[0]
                last_letter_follower = no_of_followers_str[0]
                no_of_followers_str = no_of_followers_str[1:]
            if last_letter_follower == 'K':
                no_of_followers = no_of_followers[:len(no_of_followers)-1]
                no_of_followers = float(no_of_followers)
                no_of_followers *= 1000
            elif last_letter_follower == 'M':
                no_of_followers = no_of_followers[:len(no_of_followers)-1]
                no_of_followers = float(no_of_followers)
                no_of_followers *= 1000000
            no_of_followers = int(no_of_followers)
            a = True
            if no_of_followers < min_followers:
                a = False
            no_of_tweets_str = primary_column.find('div', attrs={
                'class': 'css-901oao css-bfa6kz r-1re7ezh r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-bcqeeo r-qvutc0'}).get_text()
            no_of_tweets = ""
            while no_of_tweets_str[0] != " ":
                if no_of_tweets_str[0] == ',':
                    no_of_tweets_str = no_of_tweets_str[1:]
                    continue
                no_of_tweets += no_of_tweets_str[0]
                last_letter_tweet = no_of_tweets_str[0]
                no_of_tweets_str = no_of_tweets_str[1:]
            if last_letter_tweet == 'K':
                no_of_tweets = no_of_tweets[:len(no_of_tweets)-1]
                no_of_tweets = float(no_of_tweets)
                no_of_tweets *= 1000
            elif last_letter_tweet == 'M':
                no_of_tweets = no_of_tweets[:len(no_of_tweets)-1]
                no_of_tweets = float(no_of_tweets)
                no_of_tweets *= 1000000
            no_of_tweets = int(no_of_tweets)
            if no_of_tweets < min_tweets:
                a = False
            try:
                user_desc = primary_column.find("div", attrs={'data-testid':'UserDescription'}).get_text()
                garbage_words = get_garbage_words()
                for word in garbage_words:
                    if word.lower() in user_desc.lower():
                        a = False
                        break
            except:
                pass
            if a == True:
                print(f'{user} profile verification status: Success')
                follow_div = primary_column.find('div', attrs={
                    'data-testid': 'placementTracking'
                })
                follow_status = follow_div.find('span', attrs={
                    'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'
                }).get_text()
                if follow_status == 'Follow':
                    blacklisted_users = list()
                    with open('DontFollow.csv', 'rt') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            blacklisted_users.append(row['Username'])
                    if user not in blacklisted_users:
                        follow_button = self.browser.find_element_by_css_selector(
                            "div[data-testid='placementTracking'] span.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0")
                        follow_button.click()
                        global no_followed_today
                        no_followed_today += 1
                        print(f'Following {user}')
                        with open('AccountsFollowed.csv', 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(
                                [user, datetime.datetime.now().strftime("%x")])
                        print(f'Starting liking tweets of {user}')
                        like_tweets(self.browser, 2, user)
                        print("Liked tweets")
                    else:
                        print(f'{user} blacklisted in DontFollow.csv')
                else:
                    print(f'{user} already followed')
            else:
                print(f'{user} profile verification status: Fail')
            delay('long')
        except Exception as e:
            print(e)


def get_garbage_words():
    try:
        garbage_words = list()
        with open('GarbageWords.csv', 'rt') as f:
            reader = csv.DictReader(f)
            for row in reader:
                garbage_words.append(row['Word'])
        return garbage_words
    except Exception as e:
        print(e)
        return []


def like_tweets(browser, no_of_likes, user):
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
        if len(tweets) == 0:
            break
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
    # continuation_index = None
    # filename = None
    # with open('position.csv', 'rt') as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         continuation_index = int(row['Index'])
    #         filename = row['Filename']
    # if continuation_index == -1:
    #     competitors_list = []
    #     with open("Competitors.csv", 'rt') as f:
    #         reader = csv.DictReader(f)
    #         for raw in reader:
    #             competitors_list.append(raw['Competitors'])
    #     for comp in competitors_list:
    #         profile_page = ProfilePage(browser, comp)
    #         # Change this variable to change how much of competitor's followers list is scraped/ to define the no. of scrolls to be made while scraping competitor's followers list
    #         scroll_limit = 40
    #         follower_list = profile_page.get_followers(scroll_limit)
    #         with open(f'{comp}_followers.csv', 'wt', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow(['Username'])
    #             for uname in follower_list:
    #                 writer.writerow(
    #                     [uname])
    #         df1 = pd.read_csv('Competitors.csv', index_col="Competitors")
    #         df1.drop([comp], inplace=True)
    #         df1.to_csv('Competitors.csv')
    #         with open('ProcessedCompetitors.csv', 'a', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow([comp])
    #         for index,user in enumerate(follower_list):
    #             if no_followed_today >= 3:
    #                 with open('position.csv', 'wt', newline='') as f:
    #                     writer = csv.writer(f)
    #                     writer.writerow(['Index', 'Filename'])
    #                     writer.writerow([index, f'{comp}_followers.csv'])
    #                 break
    #             if user == follower_list[-1]:
    #                 with open('position.csv', 'wt', newline='') as f:
    #                     writer = csv.writer(f)
    #                     writer.writerow(['Index', 'Filename'])
    #                     writer.writerow([-1, f'{comp}_followers.csv'])
    #             # Change this variable to change the minimum no. of followers a user should have to be followed
    #             min_no_followers = 0
    #             # Change this variable to change the minimum no. of tweets a user should have to be followed
    #             min_no_tweets = 0
    #             profile_page.check_follower(min_no_followers, min_no_tweets, user)
    #         if no_followed_today >= 3:
    #             break
    #         competitors_list.remove(comp)
    # else:
    #     followers_list = []
    #     with open(filename, 'rt') as f:
    #         reader = csv.DictReader(f)
    #         for raw in reader:
    #             followers_list.append(raw['Username'])
    #     followers_list = followers_list[continuation_index:]
    #     profile_page = ProfilePage(browser, 'botsfolio')
    #     for index, user in enumerate(followers_list):
    #         if no_followed_today >= 3:
    #             with open('position.csv', 'wt', newline='') as f:
    #                 writer = csv.writer(f)
    #                 writer.writerow(['Index', 'Filename'])
    #                 writer.writerow([index + continuation_index, filename])
    #             break
    #         # Change this variable to change the minimum no. of followers a user should have to be followed
    #         min_no_followers = 0
    #         # Change this variable to change the minimum no. of tweets a user should have to be followed
    #         min_no_tweets = 0
    #         profile_page.check_follower(
    #             min_no_followers, min_no_tweets, user)
    #         if user == followers_list[-1]:
    #             with open('position.csv', 'wt', newline='') as f:
    #                 writer = csv.writer(f)
    #                 writer.writerow(['Index', 'Filename'])
    #                 writer.writerow([-1, filename])
    #             main(browser)
    profile_page = ProfilePage(browser, 'botsfolio')
    profile_page.check_follower(0, 0, 'MKBHD')
    profile_page.check_follower(0, 0, 'IshaanKamra')
    profile_page.check_follower(0, 0, 'Nicholacrypto')


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_twitter\\twitter_bot\\geckoDriver\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    # browser.close()


# git branch
# git checkout -b branch_name
# git checkout branch_name
# git add file_name / git add -A .
# git commit -m "commit msg"
# git push origin branch name (currently use branch_name= master)
# git pull origin branch_name