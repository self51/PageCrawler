# **Page crawler**

<br/>

#### About
This is a pet-project, it should not be used for commercial purposes!
<br/>Page Crawler is a script to automatically collect data from web pages, 
<br/>and send it to a Telegram channel.

##### Technology stack:
* Python 3.8;
* Redis;

##### Getting Started
* Clone the repository;
* Go to the project directory;
* Make sure you have Redis installed, set up Redis;
* Set up Telegram API;
  * You need to have: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID;
* Make sure you have a www.tesmanian.com account 
  * (you need a password and email address in .env)
* Create your .env file;
  * File must contain: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, 
  * REDIS_HOST, REDIS_PORT, PASSWORD, EMAIL;
* `$ pip install -r requirements.txt`.

Made by `Self`.