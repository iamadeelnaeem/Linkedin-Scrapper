from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
service = Service("./chromedriver")
driver = webdriver.Chrome(options=options,service=service)

driver.get('https://www.linkedin.com/login/')

# Gets email and password from config.txt file
file = open('config.txt')
lines = file.readlines()
EMAIL =lines[0] 
PASSWD=lines[1]

# Logs in
emailForm = driver.find_element(By.ID, 'username')
emailForm.send_keys(EMAIL)
passwdForm = driver.find_element(By.ID, 'password')
passwdForm.send_keys(PASSWD)
loginButton = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[3]/button')
loginButton.click()


# Gets URL from command line
url = "http://www.linkedin.com/in/simon-crease-92a5a110"
driver.get(url)

# # Gets source code of the page, loads it with BeautifulSoup
src = driver.page_source
soup = BeautifulSoup(src, 'html.parser')

try:
    Name_section = soup.find('div', class_="ph5 pb5").get_text().strip()
except:
    Name_section = ""

try:
    aboutMeDiv = soup.find('div', class_="display-flex ph5 pv3")
    aboutMe = aboutMeDiv.find('span').get_text().strip()
except:
    aboutMe = ""
data=Name_section + aboutMe
try:
    all_headings = soup.find_all('div', class_="pvs-header__container")
    all_sections = soup.find_all('div', class_="pvs-list__outer-container")
    for i in range(0,10):
        if i<8:
            data+=all_headings[i].get_text().strip()
        data+=all_sections[i].get_text().strip()
except:
    data = ""

with open("file.txt","w") as file:
    file.write(data)
