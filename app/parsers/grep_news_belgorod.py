from selenium.webdriver.common.by import By
from time import sleep
from app import config
import app.utils.db as db_utils
import logging


def get_news_belgorod(browser):
    source='https://yandex.ru/news/region/belgorod'
    browser.get(source)
    browser.implicitly_wait(5)
    
    news = browser.find_elements(By.CLASS_NAME,'mg-card__title')
    logging.info(f'Reading {len(news)} news from main page')
    records=[]
    for li in news:
        record={}
        record['href'] = li.find_element(By.TAG_NAME,'a').get_attribute('href')
        record['title'] = li.text
        record['source'] = source
        records.append(record)
        logging.info(record['title'])
        
    if len(records)>0:
        conn = db_utils.create_mysql_connector(config.db_news)
        db_utils.insert_records_to_table("news",records,'title', conn)
    else:
        browser = None
        logging.warning(f'Failed to read news from {source}')
                
        