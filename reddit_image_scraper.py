from selenium import webdriver
from selenium.webdriver.common.by import By
import requests, time, os



options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options, executable_path='/Users/richardgannon/geckodriver')
# pages = int(input('How many pages? '))
pages = 10
# subreddit = input('Subreddit? ')
subreddit = 'pics'
driver.get(f'https://www.reddit.com/r/{subreddit}/top/?t=all')


### cookies accepter
print('finding button')
try:
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[1]/section/div/section[2]/section[1]/form/button').click()
    print('found and clicked button')
except:
    print('no button')
### cookies accepter

# input('Press enter to continue')


if pages > 0:
    for i in range(pages):
        print('scrolling...')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('waiting for loads...')
        time.sleep(5)

try:
    print('getting post url...')
    all_links = driver.find_elements(By.TAG_NAME, 'a')
    print('found some posts')
except:
    print('...no post url found')
    pass



print('found ' + str(len(all_links)) + ' links')
link_list = []
for post in all_links:
    try:
        post = post.get_attribute('href')
        if post.startswith('https://www.reddit.com/r/pics/comments/'):
            link_list.append(post)
        print(f'added {post} to list')
    except:
        print('could not add to list')
        pass

link_set = set(link_list)
print('found ' + str(len(link_set)) + ' posts')
for post in link_set:
    print(post)


# breakpoint()
for page in link_set:
    try:
        print(page)
        save_name = str(page).split('/')[7]
        driver.get(page) # go to the post
        links_list = driver.find_elements(By.TAG_NAME, 'a') # get all the links
        for link in links_list:
            link = link.get_attribute('href')
            if link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif'):
                print('saving image...')
                r = requests.get(link)
                with open(f'reddit_images/{save_name}.jpg', 'wb') as f:
                    f.write(r.content)
                print('saved image')
                break
            else:
                print('...no image found')
                pass
    except Exception as e:
        print(e)
        pass



#     try:
#         res = requests.get(image_url)
#         res.raise_for_status()
#         print('image found')
#         # image_urls.append(image_url)
#         print('image url added to list')
#         image_file = open(os.path.join('reddit_images', os.path.basename(save_name + '.jpg')), 'wb')
#         print(f'image file opened as {save_name}')
#         # image_file = open(f'reddit_images/{save_name}', 'wb')
#         for chunk in res.iter_content(100000):
#             image_file.write(chunk)
#         print(f'image saved as {save_name}')
#         image_file.close()
#         print(f'image file closed')
#     except Exception as exc:
#         print(exc)
#         pass
#     print('moving to next post \n \n')


# print('found ' + str(len(image_urls)) + ' image urls')
# for url in image_urls:
#     print(url)


# /html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[3]
print('script complete')
# driver.quit()

