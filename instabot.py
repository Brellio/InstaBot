import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint

#OPENS CHROME AND NAVIGATES TO THE INSTAGRAM LOG IN PAGE
chromedriver_path = '/Users/Bruce/Desktop/chromedriver'
webdriver = webdriver.Chrome(executable_path= chromedriver_path)
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(5)

#LOGS IN TO INSTA ACCOUNT
username = webdriver.find_element_by_name('username')
username.send_keys('USERNAME')
password = webdriver.find_element_by_name('password')
password.send_keys('PASSWORD')

button_login = webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(3) > button')
button_login.click()
sleep(3)

#NOT NOW FOR THE 'TURN ON NOTIFICATIONS' POP-UP
notnow = webdriver.find_element_by_css_selector('body > div:nth-child(12) > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
notnow.click()

hashtag_list = ['beach', 'beachbum', 'bikini', 'sand', 'seaside']

prev_user_list = [] #only for first run
#prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
#prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0



for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

    first_thumbnail.click()
    sleep(randint(1,2))

    try:
        for x in range(1,20):
            username = webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text

            if username not in prev_user_list:
                # If we already follow, do not unfollow
                if webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                    webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                    new_followed.append(username)
                    followed += 1

                    # Liking the picture
                    button_like = webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')

                    button_like.click()
                    likes += 1
                    sleep(randint(10,20))

                    webdriver.find_element_by_link_text('Next').click()
                    sleep(randint(15,29))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(20,26))
    except:
        continue

for n in range(0,len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('users_followed_list.csv')
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))

exit()
