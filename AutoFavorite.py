from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime
import bs4
import random
import chromedriver_binary

def now_time():
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%m/%d %H:%M') + ' '

# ログイン
username = "ohtaguchi_t"
password = "Ohtaguchi1202"

# ハッシュタグ
tagName = random.choice(['プログラミング', 'IT系', 'システムエンジニア'])
print(tagName)

# イイね数を設定する
likedMax = 100

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
print(now_time() + 'instagramにアクセスしました')
time.sleep(1)

driver.find_element(By.NAME, 'username').send_keys(username)
time.sleep(1)
driver.find_element(By.NAME, 'password').send_keys(password)
time.sleep(1)

driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click()
time.sleep(3)
print(now_time() + 'instagramにログインしました')
time.sleep(1)

# タグを検索する
instaurl = 'https://www.instagram.com/explore/tags/'
driver.get(instaurl + tagName)
time.sleep(3)
print(now_time() + 'タグで検索を行いました')
time.sleep(3)

# 直近の投稿ページへ移動する
target = driver.find_elements(By.CLASS_NAME, '_aagw')[10]
actions = ActionChains(driver)
actions.move_to_element(target)
actions.perform()
print(now_time() + '最新の投稿まで画面を移動しました。')
time.sleep(3)

# 過去にイイねをしたかを確認する
def check_Like():
    html = driver.page_source.encode('utf-8')
    soup = bs4.BeautifulSoup(html, 'lxml')
    a = soup.select('span._aamw')
    return not '取り消す' in str(a[0])

# 直近の投稿へイイねする
try:
    driver.find_elements(By.CLASS_NAME, '_aagw')[9].click()
    time.sleep(random.randint(3, 5))
    print(now_time() + '投稿をクリックしました')
    time.sleep(4)

    if check_Like():
        driver.find_element(By.CLASS_NAME, '_aamw').click()
        print(now_time() + '投稿をイイねしました（1回目）')
        time.sleep(random.randint(3, 5))
    else:
        print(now_time() + 'イイね済みA')

except WebDriverException:
    print(now_time() + 'error81')

# その他の投稿にイイねする
for i in range(likedMax - 1):
    try:
        driver.find_elements(By.XPATH, '//button[@class="_abl-"]')[1].click()
        print(now_time() + '次の投稿へ移動しました')
        time.sleep(random.randint(3, 5))

    except WebDriverException:
        print(now_time() + 'error91')
        time.sleep(random.randint(4, 10))

    try:
        if check_Like():
            driver.find_element(By.CLASS_NAME, '_aamw').click()
            print(now_time() + '投稿をイイねしました（{}回目）'.format(i + 2))
            time.sleep(random.randint(3, 5))
        else:
            print(now_time() + 'イイね済みB')

    except WebDriverException:
        print(now_time() + 'error103')

print(now_time() + 'イイね終了')
driver.close()
driver.quit()