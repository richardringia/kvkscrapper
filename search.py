import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from url import Url
from post import Post


class Search:
    zip = ""
    title = ""
    url = None
    pages = []
    posts = []
    navigation_items = []
    contentId = "js-search-results"

    def __init__(self, zip, title):
        self.zip = zip
        self.title = title
        self.url = Url(zip, title)
        self.scrap()

    def get_page_posts(self):
        for page in self.pages:
            soup = BeautifulSoup(page, 'lxml')
            # soup
            for ultag in soup.find_all('ul', {'class': 'results'}):
                for litag in ultag.find_all('li', recursive=False):
                    if len(litag.attrs['class']) == 0:
                        if litag.find('div', {'class': 'handelsnaamHeaderWrapper'}):
                            self.posts.append(Post(litag.find('h3', {'class': 'handelsnaamHeader'}).text,
                                                   litag.find('ul', {'class': 'kvk-meta'}).find_all('li', {})[0].text))

    def scrap(self):
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

        driver = webdriver.Chrome(executable_path=DRIVER_BIN)
        driver.get(self.url.get())
        try:
            driver.implicitly_wait(10000)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, self.contentId)))
            print("Page is ready")
            self.get_total_pages(driver)
            self.get_pages(driver)
        except TimeoutException:
            print("Loading taked to long")
        finally:
            driver.close()
            self.get_page_posts()

    def get_total_pages(self, driver):
        navigation = driver.find_element_by_css_selector("nav[data-ui-test-class=pagination-navigation]")
        self.navigation_items = navigation.find_elements_by_class_name('nav-new__link')

    def get_pages(self, driver):
        self.pages.append(driver.page_source)
        # self.get_page_posts(driver)

        if len(self.navigation_items) > 1:
            for x in range(1, len(self.navigation_items)):
                navigation = self.navigation_items[x]
                navigation.click()
                # TODO MAKE THIS BETTER
                time.sleep(1)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#js-search-results .results li'))
                )
                self.pages.append(driver.page_source)
