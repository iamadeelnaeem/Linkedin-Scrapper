import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
service = Service("./chromedriver")
options = webdriver.ChromeOptions()
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


def find_link_column_index(header_row, target_header):
    for index, header in enumerate(header_row):
        if target_header in header:
            return index
    return None

def visit_and_update_profiles(file_path, target_header, output_header):
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        link_column_index = find_link_column_index(header, target_header)
        if link_column_index is None:
            print(f"'{target_header}' column was not found in the CSV file headers.")
            return

        updated_data = []
        for row in csv_reader:
            link = row[link_column_index]
            if link:
                driver.get(link)
                # Gets source code of the page, loads it with BeautifulSoup
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

                data = Name_section + aboutMe

                try:
                    all_sections = soup.find_all('section', class_="artdeco-card ember-view relative break-words pb3")
                    for section in all_sections:
                        data += section.get_text().strip()
                except:
                    pass

                print(data)
                row.append(f'{data}')
                updated_data.append(row)

    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header + [output_header])
        csv_writer.writerows(updated_data)

# Example usage


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

file_path = 'datafile.csv'  # Replace with the path to your CSV file
visit_and_update_profiles(file_path, 'Person Linkedin Url', 'Account info output')



