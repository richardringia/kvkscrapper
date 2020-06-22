import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from post import Post
from url import Url


class Search2:
    __zip = ""  # the zipcode for searching
    __title = ""  # title for the what to search
    __url = None  # the url for getting en editing
    __total_pages = 0  # len of total pages TODO: REMOVE!
    __posts_per_page = 10  # total posts per page
    __content_check = ".searchpage"  # what should be loaded if there are results
    __driver = None  # the selenium instance
    __pages = []  # all the pages
    __counter = 0
    __posts = []

    # init all the default variable
    def __init__(self, zip, title):
        self.__zip = zip
        self.__title = title
        self.__url = Url(zip, title)

        # Create and set the chrome instance for the selenium instance
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
        self.__driver = webdriver.Chrome(executable_path=DRIVER_BIN)

    # Change the default content check
    def set_content_check(self, content_check):
        self.__content_check = content_check

    # Change the default posts per page
    def set_posts_per_page(self, posts_per_page):
        self.__posts_per_page = posts_per_page

    #
    def scrap(self):
        self.__driver.get(self.__url.get_start(self.__posts_per_page * self.__counter))

        try:
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.__content_check)))

            # TODO: REMOVE!
            if self.__total_pages == 0 and len(self.__pages) == 0:
                try:
                    navigation = self.__driver.find_element_by_css_selector('ul.default-search')
                    self.__total_pages = len(navigation.find_elements_by_tag_name('li')) - 2
                except NoSuchElementException:
                    print('no results in ' + str(self.__zip))
                    self.__driver.close()
                    exit()

            self.__pages.append(self.__driver.page_source)
        except TimeoutException:
            print("Loading taked to long")

        self.__counter += 1
        if self.__counter < self.__total_pages:
            self.scrap()
        else:
            self.__driver.close()

    #
    def get_posts(self):
        for page in self.__pages:
            soup = BeautifulSoup(page, 'lxml')
            for ultag in soup.find_all('ul', {'class': 'results'}):
                for litag in ultag.find_all('li', recursive=False):
                    if len(litag.attrs['class']) == 0:
                        if litag.find('div', {'class': 'handelsnaamHeaderWrapper'}):
                            kvk_meta = litag.find('ul', {'class': 'kvk-meta'}).find_all('li', {})
                            naam = litag.find('h3', {'class': 'handelsnaamHeader'}).text
                            kvk = kvk_meta[0].text
                            address = kvk_meta[1].text
                            postcode = kvk_meta[2].text
                            city = kvk_meta[3].text
                            if postcode[:4] == str(self.__zip):
                                self.__posts.append(Post(naam, kvk, address, postcode, city))
        return self.__posts
