from random import weibullvariate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import urllib.parse
import time
import json
driver = webdriver.Chrome()
driver.implicitly_wait(7)


loading_component_selector = 'div[data-visualcompletion="loading-state"]'
feed_selector = 'div[role="feed"]'
username_selector = "a strong span"
comments_selector = "div.j83agx80.cbu4d94t.ew0dbk1b.irj2b8pg > div > span"
date_selector = "span[class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi b1v8xokw m9osqain hzawbc8m'] >  span > span:nth-child(2) > span > a > span"
base_path = "https://web.facebook.com/"
print_button_id = "#ctl00_ContentPlaceHolder1_ButtonPrint"
cmts= []
dts=[]
usrs=[]
def login():
   #target username
   email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
   password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

   #enter username and password
   email.clear()
   email.send_keys("dlwvctr@gmail.com")
   password.clear()
   password.send_keys("ilovemum")

   #target the login button and click it
   button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
def fetch_post_coment(commentElement):
   text=""
   length = len(commentElement.find_elements_by_css_selector("div > div"))
   for i in range(length):
      comment = commentElement.find_elements_by_css_selector("div > div")[i].text
      if comment != 'See more':
         text += comment
   return text
def fetch_comments():
   comments = []
   comments_length = len(driver.find_elements_by_css_selector(comments_selector))
   print(f'comment comments_length: {comments_length}')
   for i in range(comments_length):
      comment = fetch_post_coment(driver.find_elements_by_css_selector(comments_selector)[i])
      print(f'comment: {comment}')
      comments.append(comment)
   return comments
def fetch_usernames():
   usernames= []
   username_elements = driver.find_elements_by_css_selector(username_selector)
   length = len(username_elements)
   for i in range(length):
      username = username_elements[i].text
      usernames.append(username)
   return usernames
def fetch_dates():
   dates = []
   length = len(driver.find_elements_by_css_selector(date_selector))
   for i in range(length):
      date = driver.find_elements_by_css_selector(date_selector)[i].text
      dates.append(date)
   return dates
def search_term(term):
   encoded_term = urllib.parse.quote(term)
   url = f'https://web.facebook.com/search/posts/?q={encoded_term}'
   print(url)
   driver.get(url)
def get_dates():
   jsScript = """
   const outputDate=[];
   const dates = document.querySelectorAll("span[class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi b1v8xokw m9osqain hzawbc8m'] >  span > span:nth-child(2) > span > a > span");
   for(let i =0; i < dates.length; i++){
      outputDate.push(dates[i].innerText);
   }
   return outputDate;
   """
   print(jsScript.strip())
   return driver.execute(jsScript.strip())
def get_usernames():
   userScript = """
   const names = document.querySelectorAll("a > strong > span");
   const result = [];
   for(let i = 0; i < names.length; i++){
      result.push(names[i].innerText);
   }
   return result;
   """
   print(userScript.strip())
   return driver.execute(userScript.strip())

def get_coments():
   commentScript = '''
   let result = [];
   const comments = document.querySelectorAll('div[data-ad-preview="message"] div  div span');
   for(let i = 0; i < comments.length; i++){
      let comment = "";
      const texts = comments[0].querySelectorAll("div[dir='auto']");
      for(let j = 0; j< texts.length; j++){
         comment += texts[j].innerText;
      }
      result.push(comment);
   }
   return result;
   '''
   return driver.execute_script(commentScript.strip())
   
def scroll_to_end():
   max_scroll = 5
   length = 0
   scroll_count = 0
   while True or scroll_count < max_scroll:
      scroll_count+=1
      lastPostSelector = f'{feed_selector} > div:last-child'
      length = len(driver.find_elements_by_css_selector(f'{feed_selector} > div'))
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(6)
      newlength = len(driver.find_elements_by_css_selector(f'{feed_selector} > div'))
      print(f'length {length}; newlength: {newlength}; scroll count: {scroll_count} ')
      if newlength == length and scroll_count > 34:
         break
   print("Done Scrolling")

def scrape_posts():
   print('Scrapping posts now .....')
   comments = get_coments()
   print('gotten comments... ')
   print(comments)
   time.sleep(2);
   usernames = get_usernames()
   print('gotten usernames... ')
   print(usernames)

   time.sleep(2)
   dates = get_dates()
   print('gotten dates... ')
   print(dates)
   commentcount = len(comments)
   usernamecount = len(usernames)
   datescount = len(dates)
   cmts.extend(comments)
   dts.extend(dates)
   usrs.extend(usernames)
   print(f' added { commentcount} comments, {usernamecount} users, {datescount} dates') 
   
def save_data():
   data_dict = { "comments": cmts, "usernames": usrs, "dates": dts}
   file = open(f'fb/{term}.json', 'w')
   data_json = json.dumps(data_dict)
   file.write(data_json)
   print(f'finished scrapping "{term}" ')

      


      



driver.get(base_path)
driver.implicitly_wait(4)
login()
driver.implicitly_wait(20)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search Facebook']")))
term = "igbo presidency"
search_term(term)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, feed_selector)))
driver.implicitly_wait(8)
scroll_to_end()
scrape_posts()
save_data()





