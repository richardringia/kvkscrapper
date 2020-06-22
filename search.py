import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
    # navigation_items = []
    total_pages = 0
    post_per_page = 10
    contentId = "searchpage"

    def __init__(self, zip, title):
        self.zip = zip
        self.title = title
        self.url = Url(zip, title)
        self.scrap()

    def get_page_posts(self):
        for page in self.pages:
            soup = BeautifulSoup(page, 'lxml')
            print(page)
            # soup
            # todo when header has hoofdvestigingTag class then not add
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
                            if postcode[:4] == str(self.zip):
                                self.posts.append(Post(naam, kvk, address, postcode, city))

    def scrap(self):
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

        driver = webdriver.Chrome(executable_path=DRIVER_BIN)
        driver.get(self.url.get())
        try:
            # wait = WebDriverWait(driver, 30)
            # print('test')
            # wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))
            # print('test2')
            # driver.implicitly_wait(1000)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".searchpage")))
            print("Page is ready")
            # print(driver.find_element_by_id('js-search-results'))

            try:
                driver.find_element_by_id('js-search-results').find_elements_by_class_name('results')
                # print('test1')
            except NoSuchElementException:
                print('failed')

            self.get_total_pages(driver)
            self.get_pages(driver)

        except TimeoutException:
            print("Loading taked to long")

        finally:
            driver.close()
            self.get_page_posts()

    def get_total_pages(self, driver):
        # navigation = driver.find_element_by_css_selector("nav[data-ui-test-class=pagination-navigation]")
        # self.navigation_items = navigation.find_elements_by_class_name('nav-new__link')
        navigation = driver.find_element_by_css_selector("ul.default-search")
        self.total_pages = len(navigation.find_elements_by_tag_name('li')) - 2

    def get_pages(self, driver):
        self.pages.append(driver.page_source)
        # self.get_page_posts(driver)

        if self.total_pages > 1:
            for x in range(1, self.total_pages):
                driver.get(self.url.get_start(self.post_per_page * x))
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".searchpage")))
                self.pages.append(driver.page_source)
                # navigation = self.navigation_items[x]
                # navigation.click()
                # # TODO MAKE THIS BETTER
                # time.sleep(1)
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, '#js-search-results .results li'))
                # )
                # self.pages.append(driver.page_source)
