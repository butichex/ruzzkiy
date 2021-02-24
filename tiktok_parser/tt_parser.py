import os
import sys
import json
import random
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from exceptions import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from threading import Thread
from bs4 import BeautifulSoup as bs4
from utils import download_video_by_id
import requests
import re
import json

from selenium import webdriver
import time


class TikTok:
    def __init__(self, username):
        self.username = username
        self.profile_url = f"https://www.tiktok.com/@{self.username}"
        self.user_data = {}
        self.tiktoks_data = {}

        # define chromedriver executable
        executable = "chromedriver"
        if os.name == "nt":
            executable += ".exe"

        self.chrome_options = Options()
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        self.chrome_options.add_argument("--ignore-ssl-errors")
        """self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')"""

        # start webdriver
        self.driver = webdriver.Chrome("chromedriver.exe", options=self.chrome_options)
        if not os.path.exists(self.username):
            os.mkdir(self.username)

    def __del__(self):
        self.driver.quit()

    def parse_user_data(self):
        try:
            self.driver.get(self.profile_url)
            self.driver.implicitly_wait(5)
            first_last_name = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/header/div[1]/div/h1"
            ).text
            avatar_url = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/header/div[1]/span/img"
            )
            following = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/header/h2[1]/div[1]/strong"
            ).text
            followers = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/header/h2[1]/div[2]/strong"
            ).text
            likes = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/header/h2[1]/div[3]/strong"
            ).text
            status = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[2]/div[2]/div/header/h2[2]"
            ).text
            self.user_data = {
                "name_and_surname": first_last_name,
                "avatar_url": None,
                "following": following,
                "followers": followers,
                "likes": likes,
                "status": status,
            }
            with open(
                f"{self.username}\{self.username}_user_data.json", "w", encoding="utf-8"
            ) as file:
                file.write(json.dumps(self.user_data, ensure_ascii=False))
            return self.user_data
        except Exception as error:
            return error

    def scroll_to_bottom(self):
        try:

            old_position = 0
            new_position = None

            while new_position != old_position:
                # Get old scroll position
                old_position = self.driver.execute_script(
                    (
                        "return (window.pageYOffset !== undefined) ?"
                        " window.pageYOffset : (document.documentElement ||"
                        " document.body.parentNode || document.body);"
                    )
                )
                # Sleep and Scroll
                time.sleep(1)
                self.driver.execute_script(
                    (
                        "var scrollingElement = (document.scrollingElement ||"
                        " document.body);scrollingElement.scrollTop ="
                        " scrollingElement.scrollHeight;"
                    )
                )
                # Get new position
                new_position = self.driver.execute_script(
                    (
                        "return (window.pageYOffset !== undefined) ?"
                        " window.pageYOffset : (document.documentElement ||"
                        " document.body.parentNode || document.body);"
                    )
                )

            return self.driver.page_source
        except Exception as error:
            return error

    def parse_shortcodes(self):
        try:
            account_page_source = self.scroll_to_bottom()
            soup = bs4(account_page_source, "lxml")
            if soup.find("p", attrs={"class": re.compile(r"jsx-[0-9]{10} title")}):
                raise noVideos(self.username)
            tiktoks_items = soup.findAll(
                "div", attrs={"class": re.compile(r"jsx-[0-9]{10} video-feed-item")}
            )
            for item in tiktoks_items:
                tiktok_url = item.find("a")["href"]
                shortcode = tiktok_url.split("/")[5]
                tiktok_views = item.find(
                    "strong", attrs={"class": re.compile(r"jsx-[0-9]{10} video-count")}
                ).text
                self.tiktoks_data[shortcode] = {
                    "views": tiktok_views,
                    "comments": None,
                    "likes": None,
                    "description": None,
                    "audio_name": None,
                    "reposts": None,
                    "date": None,
                    "tiktok_source_url": None,
                }
        except noVideos as error:
            return error
        except Exception as error:
            return error

    def parse_tiktoks(self, download=False):
        try:
            self.driver.get(self.profile_url)
            self.parse_shortcodes()
            for shortcode, data in self.tiktoks_data.items():
                self.driver.get(
                    f"https://www.tiktok.com/@{self.username}/video/{shortcode}"
                )
                self.driver.implicitly_wait(1.5)
                likes = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[4]/div[2]/div[1]/strong"
                ).text
                comments = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[4]/div[2]/div[2]/strong"
                ).text
                audio_name = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[3]/h4/a/div"
                ).text
                description = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[2]/strong[1]"
                ).text
                date = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[1]/a[2]/h4"
                ).text
                reposts = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[4]/div[2]/div[3]/strong"
                ).text
                tiktok_source_url = self.driver.find_element_by_xpath(
                    "//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[4]/div[1]/a/div/div/video"
                ).get_attribute("src")
                self.tiktoks_data[shortcode]["comments"] = comments
                self.tiktoks_data[shortcode]["likes"] = likes
                self.tiktoks_data[shortcode]["description"] = description
                self.tiktoks_data[shortcode]["audio_name"] = audio_name
                self.tiktoks_data[shortcode]["date"] = date.split(" · ")[1]
                self.tiktoks_data[shortcode]["reposts"] = reposts
                self.tiktoks_data[shortcode]["tiktok_source_url"] = tiktok_source_url
                with open(
                    f"{self.username}\{shortcode}.json", "w", encoding="utf-8"
                ) as file:
                    file.write(
                        json.dumps(self.tiktoks_data[shortcode], ensure_ascii=False)
                    )
                if download: 
                    thread = Thread(
                        target=download_video_by_id, args=(self.username, shortcode,)
                    )
                    thread.start()
            with open(
                f"{self.username}\{self.username}_tiktoks_data.json",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(json.dumps(self.tiktoks_data, ensure_ascii=False))
            return self.tiktoks_data
        except Exception as error:
            return error