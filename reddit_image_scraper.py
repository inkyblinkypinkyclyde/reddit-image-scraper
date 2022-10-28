from selenium import webdriver
from selenium.webdriver.common.by import By
import requests, time, shutil, os
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# options = webdriver.FirefoxOptions()
# options.add_argument('-headless')


driver.get("https://www.reddit.com/r/pics/")
# time.sleep(5)
print('finding button')
try:
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[1]/section/div/section[2]/section[1]/form/button').click()
    print('found and clicked button')
except:
    print('no button')
# driver.switch_to.alert.accept()
input("Press enter to continue")
pages = int(input('How many pages? '))
pages_list = []
image_urls = []
for i in range(pages):
    print('scrolling...')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('waiting for loads...')
    time.sleep(5)
posts = driver.find_elements(By.XPATH, '//img[@alt="Post image"]')

for i in range(len(posts)):
    try:
        print('getting post url...')
        xpath_string = f'/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[4]/div[1]/div[4]/div[{i+3}]/div/div/div[3]/div[3]/div/div[2]/div/a'
        post_url = driver.find_element(By.XPATH, xpath_string).get_attribute('href')
        print('adding to list...')
        pages_list.append(post_url)
    except:
        print('no post url found')
        pass


print('found ' + str(len(pages_list)) + ' image posts')
for page in pages_list:
    print(page)
    save_name = str(page).split('/')[7]
    breakpoint()
    driver.get(page) # go to the post

    image_url = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[5]/div/a').get_attribute('href') # gets the image URL from the post page

    res = requests.get(image_url)
    try:
        res.raise_for_status()
        print('image found')
        image_urls.append(image_url)
        print('image url added to list')
        image_file = open(os.path.join('reddit_images', os.path.basename(save_name + '.jpg')), 'wb')
        print(f'image file opened as {save_name}')
        # image_file = open(f'reddit_images/{save_name}', 'wb')
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
        print(f'image saved as {save_name}')
        image_file.close()
        print(f'image file closed')
    except Exception as exc:
        print(exc)
        pass
    print('moving to next post \n \n')


print('found ' + str(len(image_urls)) + ' image urls')
for url in image_urls:
    print(url)


# /html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[3]
print('script complete')
# driver.quit()

