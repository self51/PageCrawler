import time
import asyncio
import redis
import environ

import requests
from telegram import Bot
from bs4 import BeautifulSoup

# Set up environment variables
env = environ.Env()
environ.Env.read_env()

# Set up Redis
redis_client = redis.Redis(host=env('REDIS_HOST'), port=env('REDIS_PORT'), db=0)
redis_key = 'previous_titles'

# Set up Telegram bot
bot = Bot(token=env('TELEGRAM_BOT_TOKEN'))
chat_id = env('TELEGRAM_CHAT_ID')

# Set up persistent session
session = requests.Session()


def log_in():
    login_url = 'https://www.tesmanian.com/account/login?return_url=%2Faccount'
    response = session.post(login_url, data={'email': env('EMAIL'), 'password': env('PASSWORD')})

    if '_secure_session_id' not in session.cookies:
        print('Login failed')
    else:
        print('Login successful')

    return response


# Scrapes recent articles and add them to redis
def get_latest_article():
    # checks if you are logged in
    if '_secure_session_id' not in session.cookies:
        log_in()

    url = 'https://www.tesmanian.com/'
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    latest_article = set()
    for article in soup.select('blog-post-card'):
        title = article.find('p').find('a').text
        link = article.find('a')['href']
        if not redis_client.sismember(redis_key, link):
            latest_article.add((title, f'https://www.tesmanian.com{link}'))
            redis_client.sadd(redis_key, link)

    return latest_article


async def send_message():
    messages = get_latest_article()
    for message in messages:
        await bot.send_message(chat_id=chat_id, text=f'Title - {list(message)[0]}, Link - {list(message)[1]}')
        time.sleep(1)


def main():
    while True:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(send_message())
        time.sleep(15)


if __name__ == '__main__':
    main()
