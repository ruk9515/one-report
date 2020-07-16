import requests
import json
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

CURRENT_PATH = r'C:\Users\u8645622\Desktop\one'

URL = 'https://one.prat.idf.il/api/Attendance/InsertPersonalReport'
DRIVER_PATH = os.path.join(CURRENT_PATH, 'chromedriver.exe')
COOKIE_PATH = os.path.join(CURRENT_PATH, 'cookie.txt')

def get_codes():
    res = requests.get('http://ruk9515.pythonanywhere.com/')
    return res.json()

def main():
    if(not os.path.exists(COOKIE_PATH)):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get('https://one.prat.idf.il/login')
        wait = WebDriverWait(driver, 120)
        wait.until(lambda driver: driver.current_url != "https://one.prat.idf.il/login")
        cookies = driver.get_cookies()
        cookie = '; '.join([f'{cookie["name"]}={cookie["value"]}' for cookie in cookies])
        with open(COOKIE_PATH, 'w') as f:
            f.write(cookie)
    else:
        with open(COOKIE_PATH, 'r') as f:
            cookie = f.read()

    codes = get_codes()
    main_code = codes['MAIN_CODE']
    secondary_code = codes['SECONDARY_CODE']
    note = '' # Note 
    data = f"------WebKitFormBoundaryBlITUYglfWe1bh0t\r\nContent-Disposition: form-data; name=\"MainCode\"\r\n\r\n{main_code}\r\n------WebKitFormBoundaryBlITUYglfWe1bh0t\r\nContent-Disposition: form-data; name=\"SecondaryCode\"\r\n\r\n{secondary_code}\r\n------WebKitFormBoundaryBlITUYglfWe1bh0t--\r\nContent-Disposition: form-data; name=\"Note\"{note}------WebKitFormBoundaryOusvJ63bzvSAgVzX--"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "access-control-allow-origin": "*",
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryBlITUYglfWe1bh0t",
        "crossdomain": "true",
        "pragma": "no-cache",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin", 
        "cookie": cookie
    }
    
    res = requests.post(URL, headers=headers, data=data)


if(__name__ == '__main__'):
    main()