# from selenium import webdriver
# from time import sleep
# from bs4 import BeautifulSoup
# import csv
# import datetime
# import pandas as pd
# import random

# no_followed_today = 0

# environment = 'test'  # development or test


# def delay(duration):
#     if environment == 'test':
#         sleep(3)
#         return
#     elif environment == 'development':
#         if duration == 'short':
#             a = 5
#             b = 10
#             x = random.randint(a, b+1)
#             sleep(x)
#             return
#         elif duration == 'long':
#             a = 30
#             b = 60
#             x = random.randint(a, b+1)
#             sleep(x)
#             return


# class LoginPage:
#     def __init__(self, browser):
#         self.browser = browser
#         self.browser.get('https://www.instagram.com/')

#     def login(self, username, password):
#         username_input = self.browser.find_element_by_css_selector(
#             "input[name='username']")
#         password_input = self.browser.find_element_by_css_selector(
#             "input[name='password']")
#         username_input.send_keys(username)
#         password_input.send_keys(password)
#         login_button = browser.find_element_by_xpath(
#             "//button[@type='submit']")
#         login_button.click()
#         delay('short')

#     def clickNotNow(self):
#         not_now_btn_1 = self.browser.find_element_by_css_selector(
#             ".sqdOP.yWX7d.y3zKF")
#         not_now_btn_1.click()
#         delay('short')
#         not_now_btn_2 = self.browser.find_element_by_css_selector(
#             "button.aOOlW.HoLwm ")
#         not_now_btn_2.click()
#         print("Logged in")
#         delay('short')


# def get_influencer_accounts():
#     try:
#         influencer_accounts_list = list()
#         with open('Influencers.csv', 'rt') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 influencer_accounts_list.append(row['Username'])
#         return influencer_accounts_list
#     except Exception as e:
#         print(e)
#         return []


# def follow(browser, user):
#     global no_followed_today
#     try:
#         follower_profile_link = browser.get(
#             f'https://instagram.com/{user}/')
#         print(f'Checking follower : {user}')
#         delay('short')
#         follow_button = browser.find_element_by_css_selector(
#             "div.Igw0E.IwRSH.eGOV_._4EzTm  button._5f5mN.jIbKX._6VtSN.yZn4P")
#         follow_button.click()
#         no_followed_today += 1
#         with open('AccountsFollowed.csv', 'a', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(
#                 [user, datetime.datetime.now().strftime("%x")])
#         print(f'Followed {user}')
#     except Exception as e:
#         try:
#             follow_button = browser.find_element_by_css_selector(
#                 "div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm  button.sqdOP.L3NKy.y3zKF")
#             something += 1
#             follow_button.click()
#             # global no_followed_today
#             no_followed_today += 1
#             with open('AccountsFollowed.csv', 'a', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(
#                     [user, datetime.datetime.now().strftime("%x")])
#             print(f'Followed {user}')
#         except:
#             print("Error in follow()")


# def get_influencer_message():
#     try:
#         influencer_messages = list()
#         with open('InfluencerMessages.csv', 'rt') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 influencer_messages.append(row['Message'])
#         return influencer_messages
#     except Exception as e:
#         print(e)
#         return []


# def send_message(browser, user, influencer_messages):
#     try:
#         print(f'Sending message to {user}')
#         browser.get(f'https://www.instagram.com/{user}/')
#         delay('short')
#         message_btn = browser.find_element_by_css_selector(
#             'button.sqdOP.L3NKy._4pI4F._8A5w5')
#         message_btn.click()
#         delay('short')
#         message_input = browser.find_element_by_css_selector(
#             'textarea[placeholder="Message..."]')
#         influencer_message = influencer_messages[0]
#         message_input.send_keys(influencer_message)
#         message_bar = browser.find_element_by_css_selector('div.X3a-9')
#         send_btn = message_bar.find_element_by_css_selector(
#             'button.sqdOP.yWX7d.y3zKF')
#         send_btn.click()
#         print('Message sent')
#         delay('long')
#     except Exception as e:
#         print(e)


# def main(browser):
#     login_page = LoginPage(browser)
#     login_page.login("k10_coder", "Abcd@1234")
#     login_page.clickNotNow()
#     influencer_accounts_list = get_influencer_accounts()
#     influencer_messages = get_influencer_message()
#     for user in influencer_accounts_list:
#         follow(browser, user)
#         send_message(browser, user, influencer_messages)


# if __name__ == '__main__':
#     browser = webdriver.Firefox(
#         executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta\\gecko\\geckodriver.exe")
#     browser.implicitly_wait(5)
#     main(browser)
#     browser.close()


from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import csv
import datetime
import pandas as pd
import random

# Change this to control how many people followed per day
no_followed_today = 0

# Create an instance of this class to login

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


class ProfilePage:
    def __init__(self, browser, username):
        self.browser = browser
        self.browser.get(f'https://www.instagram.com/{username}/')

    def get_followers(self, scroll_limit):
        try:
            followers_btn = self.browser.find_element_by_css_selector(
                "a.-nal3")
            followers_btn.click()
            delay('short')
            scroll_time = 1
            usernames = []
            # created this variable to track the last recorded username
            prev_last_usernames = 0
            while scroll_time <= scroll_limit:
                html = self.browser.page_source
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
                div_profile = self.browser.find_element_by_css_selector(
                    'div.PZuss')
                b = div_profile.find_elements_by_tag_name('button')
                status = b[-1].text
                if status == 'Follow':
                    last_profile = self.browser.find_elements_by_css_selector(
                        "button.sqdOP.L3NKy.y3zKF")[-1]
                    last_profile.send_keys('')
                    delay('short')
                    last_profile = self.browser.find_elements_by_css_selector(
                        "button.sqdOP.L3NKy.y3zKF")[-1]
                    last_profile.send_keys('')
                elif status == 'Following':
                    last_profile = self.browser.find_elements_by_css_selector(
                        "button.sqdOP.L3NKy._8A5w5")[-1]
                    last_profile.send_keys('')
                    delay('short')
                    last_profile = self.browser.find_elements_by_css_selector(
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

    def check_follower(self, min_followers, min_posts, no_of_likes, user):
        try:
            follower_profile_link = self.browser.get(
                f'https://instagram.com/{user}/')
            print(f'Checking follower : {user}')
            delay('short')
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            primary_column = soup.find('ul', attrs={'class': 'k9GMp'})
            no_of_followers = None
            try:
                no_of_followers_holder = primary_column.find(
                    "a", attrs={'href': f'/{user}/followers/'})
                no_of_followers_str = no_of_followers_holder.find(
                    "span", attrs={'class': 'g47SY'}).get_text()
                no_of_followers = ""
                for i in no_of_followers_str:
                    if i != ',':
                        no_of_followers += i
                last_letter_follower = no_of_followers[len(no_of_followers)-1]
                if last_letter_follower == 'k':
                    no_of_followers = no_of_followers[:len(no_of_followers)-1]
                    no_of_followers = float(no_of_followers)
                    no_of_followers *= 1000
                elif last_letter_follower == 'M':
                    no_of_followers = no_of_followers[:len(no_of_followers)-1]
                    no_of_followers = float(no_of_followers)
                    no_of_followers *= 1000000
            except:
                no_of_followers = 0
            no_of_followers = int(no_of_followers)
            a = True
            if no_of_followers < min_followers:
                a = False
            no_of_posts_holder = primary_column.find(
                "span", attrs={'class': '-nal3'})
            no_of_posts_str = no_of_posts_holder.find('span', attrs={
                'class': 'g47SY'}).get_text()
            no_of_posts = ""
            for i in no_of_posts_str:
                if i != ',':
                    no_of_posts += i
            last_letter_post = no_of_posts[len(no_of_posts)-1]
            if last_letter_post == 'K':
                no_of_posts = no_of_posts[:len(no_of_postts)-1]
                no_of_posts = float(no_of_posts)
                no_of_posts *= 1000
            elif last_letter_post == 'M':
                no_of_posts = no_of_posts[:len(no_of_posts)-1]
                no_of_posts = float(no_of_posts)
                no_of_posts *= 1000000
            no_of_posts = int(no_of_posts)
            if no_of_posts < min_posts:
                a = False
            try:
                desc_section  = soup.find("section", attrs={'class':'zwlfE'})
                user_desc = desc_section.find('div', attrs={'class':'-vDIg'}).get_text()
                print(user_desc)
                garbage_words = get_garbage_words()
                print(garbage_words)
                for word in garbage_words:
                    if word.lower() in user_desc.lower():
                        a = False
                        break
            except:
                pass
            if a == True:
                print(f'{user} profile verification status: Success')
                try:
                    follow_div_1 = soup.find('div', attrs={'class': 'BY3EC'})
                    follow_div_2 = follow_div_1.find('span', attrs={
                        'class': 'bqE32'
                    })
                    follow_status = follow_div_2.find('span', attrs={
                        'class': 'vBF20 _1OSdk'
                    }).get_text()
                except:
                    follow_status = "Following"
                if follow_status == 'Follow':
                    blacklisted_users = list()
                    with open('DontFollow.csv', 'rt') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            blacklisted_users.append(row['Username'])
                    if user not in blacklisted_users:
                        follow_button = self.browser.find_element_by_css_selector(
                            "div.Igw0E.IwRSH.eGOV_._4EzTm  button._5f5mN.jIbKX._6VtSN.yZn4P")
                        follow_button.click()
                        global no_followed_today
                        no_followed_today += 1
                        print(f'Following {user}')
                        with open('AccountsFollowed.csv', 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(
                                [user, datetime.datetime.now().strftime("%x")])
                        print(f'Starting liking posts of {user}')
                        post_links = get_post_links(
                            self.browser, no_of_likes, user)
                        for index, link in enumerate(post_links):
                            print(
                                f'Liking post no. {index+1} of {no_of_likes}')
                            like_post(self.browser, link)
                        print("Liked posts")
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


def get_post_links(browser, no_of_likes, user):
    try:
        browser.get(f'https://instagram.com/{user}/')
        delay('short')
        post_links = list()
        prev_last_post = 0
        while True:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            primary_column = soup.find(
                'article', attrs={'class': 'ySN3v'})
            posts = primary_column.find_all('a')
            a = -1
            if prev_last_post in posts:
                a = tweets.index(prev_last_post)
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
    # try:
    login_page = LoginPage(browser)
    login_page.login("k10_coder", "Abcd@1234")
    login_page.clickNotNow()
    # except:
    #     pass
    # continuation_index = None
    # filename = None
    # with open('position.csv', 'rt') as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         continuation_index = int(row['Index'])
    #         filename = row['Filename']
    # if continuation_index == -1:
    #     competitors_list = []
    #     with open("target.csv", 'rt') as f:
    #         reader = csv.DictReader(f)
    #         for raw in reader:
    #             competitors_list.append(raw['Username'])
    #     for comp in competitors_list:
    #         profile_page = ProfilePage(browser, comp)
    #         # Change this variable to change how much of competitor's followers list is scraped/ to define the no. of scrolls to be made while scraping competitor's followers list
    #         scroll_limit = 100
    #         follower_list = profile_page.get_followers(scroll_limit)
    #         with open(f'{comp}_followers.csv', 'wt', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow(['Username'])
    #             for uname in follower_list:
    #                 writer.writerow(
    #                     [uname])
    #         df1 = pd.read_csv('target.csv', index_col="Username")
    #         df1.drop([comp], inplace=True)
    #         df1.to_csv('target.csv')
    #         with open('ProcessedCompetitors.csv', 'a', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow([comp])
    #         for index, user in enumerate(follower_list):
    #             if no_followed_today >= 199:
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
    #             min_no_followers = 10
    #             # Change this variable to change the minimum no. of tweets a user should have to be followed
    #             min_no_posts = 5
    #             # Change this variable to change the no. of posts liked on the users profile upon follow
    #             no_of_likes = 2
    #             profile_page.check_follower(
    #                 min_no_followers, min_no_posts, no_of_likes, user)
    #         if no_followed_today >= 199:
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
    #         if no_followed_today >= 199:
    #             with open('position.csv', 'wt', newline='') as f:
    #                 writer = csv.writer(f)
    #                 writer.writerow(['Index', 'Filename'])
    #                 writer.writerow([index + continuation_index, filename])
    #             break
    #         # Change this variable to change the minimum no. of followers a user should have to be followed
    #         min_no_followers = 10
    #         # Change this variable to change the minimum no. of tweets a user should have to be followed
    #         min_no_posts = 5
    #         # Change this variable to change the no. of posts liked on the users profile upon follow
    #         no_of_likes = 2
    #         profile_page.check_follower(
    #             min_no_followers, min_no_posts, no_of_likes, user)
    #         if user == followers_list[-1]:
    #             with open('position.csv', 'wt', newline='') as f:
    #                 writer = csv.writer(f)
    #                 writer.writerow(['Index', 'Filename'])
    #                 writer.writerow([-1, filename])
    #             main(browser)
    profile_page = ProfilePage(browser, 'botsfolio')
    profile_page.check_follower(0, 0, 2, 'ishaan_kamra1091')
    profile_page.check_follower(0, 0, 2, 'skillinit225')
    profile_page.check_follower(0, 0, 2, 'botsfolio')


if __name__ == '__main__':
    browser = webdriver.Firefox(
        executable_path="C:\\Users\\ISHAAN KAMRA\\VScode_temporary\\Marketing_bots_insta\\insta_bots\\gecko\\geckodriver.exe")
    browser.implicitly_wait(5)
    main(browser)
    # browser.close()

