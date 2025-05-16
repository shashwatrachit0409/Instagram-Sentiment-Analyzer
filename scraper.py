from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_instagram_data(username):
    url = f"https://www.instagram.com/{username}/"
    driver = init_driver()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    posts = followers = following = "Unknown"
        
    try:
        spans = soup.find_all('span')
        for span in spans:
            text = span.get_text().replace(',', '').lower()
            if 'followers' in text:
                followers = text.split(' ')[0]
            elif 'following' in text:
                following = text.split(' ')[0]
    except Exception as e:
        print("Error extracting followers/following:", e)

    try:
        # Try extracting post count separately
        spans = soup.find_all('span')
        for span in spans:
            text = span.get_text().lower()
            if 'posts' in text:
                posts_text = text.split(' ')[0]
                posts = ''.join(filter(str.isdigit, posts_text))
                break
    except Exception as e:
        print("Error extracting posts:", e)
    post_links = []
    captions = []
    hashtags = []
    likes_list = []
    comments_list = []
    images = []
    engagement_rates = []

    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and "/p/" in href:
            post_url = "https://www.instagram.com" + href
            if post_url not in post_links:
                post_links.append(post_url)
            if len(post_links) >= 10:
                break

    def convert_to_int(value_str):
        try:
            value_str = value_str.strip().lower().replace(',', '')
            if 'k' in value_str:
                return int(float(value_str.replace('k', '')) * 1000)
            elif 'm' in value_str:
                return int(float(value_str.replace('m', '')) * 1000000)
            else:
                return int(float(value_str))
        except:
            return 0

    follower_count = convert_to_int(followers)

    for post_url in post_links:
        driver.get(post_url)
        time.sleep(3)
        post_soup = BeautifulSoup(driver.page_source, 'html.parser')

        caption = ""
        hash_tags = []
        try:
            desc_meta = post_soup.find('meta', property='og:description')
            if desc_meta:
                caption = desc_meta['content']
                hash_tags = [tag for tag in caption.split() if tag.startswith('#')]
        except:
            pass

        img_url = ""
        try:
            img_meta = post_soup.find('meta', property='og:image')
            if img_meta:
                img_url = img_meta['content']
        except:
            pass

        captions.append(caption)
        hashtags.append(hash_tags)
        images.append(img_url)

        likes = 0
        comments = 0

        try:
            spans = post_soup.find_all('span')
            for span in spans:
                if 'like' in span.text.lower():
                    text = span.text.strip().lower()
                    if 'k' in text:
                        likes = int(float(text.split()[0].replace('k', '')) * 1000)
                    elif 'm' in text:
                        likes = int(float(text.split()[0].replace('m', '')) * 1000000)
                    else:
                        likes = int(text.split()[0].replace(',', ''))
                    break
        except:
            pass

        try:
            comment_blocks = post_soup.find_all('ul')
            for block in comment_blocks:
                li_tags = block.find_all('li')
                comments = len(li_tags) - 1
                break
        except:
            pass

        likes_list.append(likes)
        comments_list.append(comments)

        if follower_count > 0:
            engagement = ((likes + comments) / follower_count) * 100
            engagement = round(min(engagement, 100.0), 2)
        else:
            engagement = 0.0
        engagement_rates.append(engagement)

    driver.quit()

    return {
        'username': username,
        'posts': int(float(posts)) if posts.isdigit() else 0,
        'followers': followers,
        'following': following,
        'post_links': post_links,
        'captions': captions,
        'hashtags': hashtags,
        'likes': likes_list,
        'comments': comments_list,
        'images': images,
        'engagement_rates': engagement_rates
    }