from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import csv,os,time
import pandas as pd

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def scrape(shortURL):
    driver = webdriver.Chrome('path/to/chromedriver',options=set_chrome_options())
    # Do stuff with your driver
    url = f"https://www.instagram.com/p/{shortURL}"
    driver.get(url)
    time.sleep(4)
    parse_html= BeautifulSoup(driver.page_source,"html.parser") # Scrape url
    date = parse_html.find(class_="_aaqe")
    author = parse_html.find("a",class_= "x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp xqnirrm xj34u2y x568u83 x3nfvp2" )
    like= parse_html.find(class_="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")
    content = parse_html.find(class_ ="_aacl _aaco _aacu _aacx _aad7 _aade")
    date = BeautifulSoup(str(date),'html.parser').text # remove html tags
    author = BeautifulSoup(str(author),'html.parser').text
    like = BeautifulSoup(str(like),'html.parser').text.replace('likes','')
    content = BeautifulSoup(str(content),'html.parser').text
    print(f"Date:{date}\n Author: {author}\n Likes: {like}\n Text: {content}")
    data = {"Date":[date],"Author":[author],"LikeCount":[like],"info":[content],"URL":[url]}

    df = pd.DataFrame(data)
    currentPath = os.getcwd()
    file_path = f'{currentPath}/data.csv'
    if os.path.isfile(file_path) == False:
        with open(file_path, 'w', newline='') as f:
            header = ["Date","Author","LikeCount","Info","URL"]
            writer = csv.writer(f)
            writer.writerow(header)
    df.to_csv(file_path, mode='a', index=False,header=False)
    df = readCSV(file_path)
    driver.close()
    return df


def readCSV(file_path):
   df = pd.read_csv(file_path,encoding="UTF-8")
   return df



