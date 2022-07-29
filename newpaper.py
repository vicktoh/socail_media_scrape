from random import weibullvariate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
import urllib.parse
import csv
import time
import json
driver = webdriver.Chrome()
driver.implicitly_wait(7)
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
#guardian_url = "https://guardian.ng/tag/aisha-yesufu/"
guardian_url = "https://guardian.ng/tag/oby-ezekwesili/"
def fetch_guardian():
   file = open(f"general/guardianObby.csv", "w")
   writter = csv.writer(file)
   writter.writerow(["title", "link", "article"])
   driver.get(guardian_url)
   while driver.find_element_by_css_selector("button.load-more-button"):
      try:
         driver.find_element_by_css_selector("button.load-more-button").click()
      except:
         break
      driver.implicitly_wait(5)

   articles = driver.find_elements_by_css_selector(".item.design-article")
   for i in range(len(articles) - 1):
      headerElement = driver.find_element_by_css_selector(f".item.design-article:nth-child({i+1}) span.title a")
      headline = headerElement.get_attribute("innerText")
      link = headerElement.get_attribute("href")
      req = requests.get(link, headers)
      soup = BeautifulSoup(req.content, 'html.parser')
      element = soup.find("article")
      paragraps = [p.text for p in element.find_all("p")]
      content = " ".join(paragraps)
      writter.writerow([headline, link, content])
      print(f"fetched {headline} and link {link}")
def fetch_punch(term):
    encoded_term = urllib.parse.quote(term)
    maxpage = 49
    file = open(f"general/punch{term}.csv", "a")
    writter = csv.writer(file)
    writter.writerow(["title", "link", "article"])
    for i in range(6, maxpage):
      url = f"https://punchng.com/page/{i}/?s={encoded_term}"
      print(f"fetching {url}")
      req = requests.get(url, headers)
      soup = BeautifulSoup(req.content, 'html.parser')
      elementList = soup.find(class_="latest-news-timeline-section")
      articles = elementList.find_all("article")
      for article in articles:
         name = article.select_one(".post-title a")
         title = name.text
         link = name['href']
         r = requests.get(link, headers)
         content_soup = BeautifulSoup(r.content, 'html.parser')
         contents = content_soup.find(class_="post-content")
         pararaphs = [p.text for p in contents.find_all("p")]
         content = " ".join(pararaphs)
         print(f"Writing {title}, {link}")
         writter.writerow([title, link, content])
fetch_guardian()
# fetch_punch("oby ezekwesili")