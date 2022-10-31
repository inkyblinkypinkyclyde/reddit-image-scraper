from selenium import webdriver
from selenium.webdriver.common.by import By
import requests, time, os



options = webdriver.FirefoxOptions()
headless = None
if os.path.exists('reddit_images'):
    pass
else:
    os.mkdir('reddit_images')
while True:
    headless = input("Do you want to run the scraper headless? (y/n): ")
    if headless == "y":
        options.add_argument("--headless")
        break
    elif headless == "n":
        break
    else:
        print("Please enter a valid option.")


options.add_argument('--headless')

pages = int(input('How many pages? '))
subreddit = input('Subreddit? ')
if os.path.exists('reddit_images/' + subreddit):
    pass
else:
    os.mkdir('reddit_images/' + subreddit)
while True:
    top = input("Top, Hot, New, or Rising? (t/h/n/r): ")
    after = ""
    if top == "t":
        top = "top"
        after = input("After what time? (day/week/month/year/all): ")  
        if after == "d":
            after = ""
            break
        elif after == "w":
            after = "&t=week"
            break
        elif after == "m":
            after = "&t=month"
            break
        elif after == "y":
            after = "&t=year"
            break
        elif after == "a":
            after = "&t=all"
            break
        else:
            print("Please enter a valid option.")        
        break
    elif top == "h":
        top = "hot"
        break
    elif top == "n":
        top = "new"
        break
    elif top == "r":
        top = "rising"
        break
    elif top == "c":
        top = "controversial"
        break
    else:
        print("Please enter a valid option.")

url = 'https://www.reddit.com/r/' + subreddit + '/' + top.lower() + '/?count=25&after=t3_' + after.lower()
print(f'Retrieving {pages + 1} pages from {url}')
print('Please wait...')
driver = webdriver.Firefox(options=options, executable_path='./geckodriver')


driver.get(url)


### cookies accepter
print('finding button')
try:
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[1]/section/div/section[2]/section[1]/form/button').click()
    print('found and clicked button')
except:
    print('no button')
### cookies accepter

if headless == "n":
    input('Press enter to continue')


if pages > 0:
    for i in range(pages):
        print('scrolling...')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('waiting for loads...')
        time.sleep(5)

all_links = driver.find_elements(By.TAG_NAME, 'a')
print('found ' + str(len(all_links)) + ' links')
link_list = []
for post in all_links:
    try:
        post = post.get_attribute('href')
        if post.startswith(f'https://www.reddit.com/r/{subreddit}/comments/'):
            link_list.append(post)
    except:
        pass

link_set = set(link_list)
print('found ' + str(len(link_set)) + ' posts')

print('getting images...')
image_number = 1
for page in link_set:
    try:
        print(f'getting page {str(image_number)} of {str(len(link_set))}')
        print(page)
        save_name = str(page).split('/')[7]
        driver.get(page)
        links_list = driver.find_elements(By.TAG_NAME, 'a')
        for link in links_list:
            link = link.get_attribute('href')
            if link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif') or link.endswith('.jpeg') or link.endswith('.gifv') or link.endswith('.mp4') or link.endswith('.webm'):
                print('saving image...')
                r = requests.get(link)
                if link.endswith('.jpg'):
                    with open(f'reddit_images/{subreddit}/{save_name}.jpg', 'wb') as f:
                        f.write(r.content)
                elif link.endswith('.png'):
                    with open(f'reddit_images/{subreddit}/{save_name}.png', 'wb') as f:
                        f.write(r.content)
                elif link.endswith('.gif'):
                    with open(f'reddit_images/{subreddit}/{save_name}.gif', 'wb') as f:
                        f.write(r.content)
                elif link.endswith('.jpeg'):
                    with open(f'reddit_images/{subreddit}/{save_name}.jpeg', 'wb') as f:
                        f.write(r.content)
                elif link.endswith('.gifv'):
                    with open(f'reddit_images/{subreddit}/{save_name}.gif', 'wb') as f:
                        f.write(r.content)
                elif link.endswith('.mp4'):
                    with open(f'reddit_images/{subreddit}/{save_name}.mp4', 'wb') as f:
                        f.write(r.content)
                elif link.endswith('.webm'):
                    with open(f'reddit_images/{subreddit}/{save_name}.webm', 'wb') as f:
                        f.write(r.content)
                else:
                    print('could not save image')
                    pass
                print(f'saved image as {save_name}')
                break
            else:
                pass
    except Exception as e:
        print(e)
        pass
    image_number += 1




print('script complete')
# driver.quit()

