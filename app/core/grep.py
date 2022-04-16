from time import sleep
import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By

from app import config
import app.utils.db as db_utils

from app.parsers.grab_news_belgorod import *
from app.parsers.vmo24 import *

def get_browser_aws(browser):
    if browser is None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("window-size=1400,1500")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        
        #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)
        #options.add_argument('--disable-blink-features=AutomationControlled')

        browser = webdriver.Chrome(options=options)
    
    return browser

def get_browser(browser):
    if browser is None:
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)
        chromeOptions.add_argument("--incognito")
        #chromeOptions.add_argument("--headless")
        s=Service('/Users/ihor/Documents/Py/Yay/ChromeDriver')
        browser = webdriver.Chrome(options=chromeOptions,service=s)
        #browser.set_window_position(400, 0)
        wait = ui.WebDriverWait(browser,15)
        browser.implicitly_wait(3)
        
    return browser    

def get_news():
    browser = None
    
    while True:
        try:
            browser = get_browser_aws(browser)
            get_news_belgorod(browser)
            get_news_vmo24(browser)
                
        except Exception as e:
            logging.error(e)
            browser = None
        
        sleep(config.grab_delay)
    
if __name__ == "__main__":
    get_news()
