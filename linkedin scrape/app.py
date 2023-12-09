import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
                    Name_section = soup.find('div', class_="mt2 relative").get_text().strip()
                except:
                    Name_section = ""

                try:
                    aboutMeDiv = soup.find('div', class_="display-flex ph5 pv3")
                    aboutMe = aboutMeDiv.find('span').get_text().strip()
                except:
                    aboutMe = ""
                data = Name_section + aboutMe
                try:
                    all_headings = soup.find_all('div', class_="pvs-header__container")
                    all_sections = soup.find_all('div', class_="pvs-list__outer-container")
                    for i in range(0, 10):
                        if i < 8:
                            data += all_headings[i].get_text().strip()
                        data += all_sections[i].get_text().strip()
                except:
                    data = ""

                # Update the 'Account Info' field in the row with the extracted data
                row[header.index(output_header)] = data
                updated_data.append(row)

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(updated_data)
        
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


driver.get('https://www.linkedin.com/login/')

# Gets email and password from credentials.txt file
with open('credentials.txt') as config_file:
    EMAIL, PASSWD = config_file.read().splitlines()

# Logs in
emailForm = driver.find_element(By.ID, 'username')
emailForm.send_keys(EMAIL)
passwdForm = driver.find_element(By.ID, 'password')
passwdForm.send_keys(PASSWD)
loginButton = driver.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[3]/button')
loginButton.click()

file_path = 'Demo_Input_-_Sheet1.csv'  # Replace with the path to your CSV file
visit_and_update_profiles(file_path, 'Person Linkedin Url', 'Account info output')
