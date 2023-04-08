import os
import re
import subprocess
from win32com.client import Dispatch
import requests
try:
    from selenium import webdriver
except:
    os.system('py -m pip install selenium')

class buffTraffic:
    def __init__(self):
        self.driver = self.open_chromedriver()
    
    # install chrome driver
    def check_chrome_version(self):
        paths = [r"C:/Program Files/Google/Chrome/Application/chrome.exe",
                r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"]
        parser = Dispatch("Scripting.FileSystemObject")
        # Get the version of Google Chrome installed on your machine
        for path in paths:
            try:
                version = parser.GetFileVersion(path)
                return version
            except:
                continue

    def find_chrome_version(self):
        # Send a GET request to the website
        response = requests.get("https://chromedriver.chromium.org/downloads")
        # Get the content of the response
        content = response.content.decode("utf-8")
        # Extract the available versions of ChromeDriver from the content using regex
        versions = re.findall(r'ChromeDriver \d+\.\d+\.\d+.\d+', content)
        # Remove the prefix "ChromeDriver " from the versions
        versions = [version.replace("ChromeDriver ", "") for version in versions]
        return versions

    def install_chromedriver(self, chrome_version):
        if chrome_version:
            for ver in self.find_chrome_version():
                if chrome_version.split('.')[0] == ver.split('.')[0]:
                    # Install the compatible version of ChromeDriver for the installed version of Google Chrome
                    os.system(f"curl https://chromedriver.storage.googleapis.com/{ver}/chromedriver_win32.zip -o chromedriver.zip")
                    subprocess.run(["powershell.exe", "-Command", "Expand-Archive chromedriver.zip -Force"])
                    os.remove("chromedriver.zip")
                    print(f"ChromeDriver version {ver} installed.")
                    return None
            print("Không tìm thấy chromedriver phù hợp với phiên bản google của bạn")

    def open_chromedriver(self):
        # option here
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # find chorme driver
        try:
            driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver', options=options)
        except:
            print('Không tìm thấy "chromedriver" tiến hành cài đặt.')
            self.install_chromedriver(self.check_chrome_version())
            driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver', options=options)
        return driver

    def buff_traffic(self, buffUrl, keyWord):
        self.driver.get("https://www.google.com")

        # find sreach bar
        search_box = self.driver.find_element_by_name("q")
        self.driver.execute_script("arguments[0].click();", search_box)

        # find key word and submit
        search_box.send_keys(keyWord)
        search_box.submit()

        # find your website
        while True:
            # Tìm tất cả các liên kết trong kết quả tìm kiếm
            links = self.driver.find_elements_by_css_selector("div.g a")
            for link in links:
                # Nếu liên kết chứa địa chỉ của trang hellotruyen.com thì click vào liên kết đó
                if buffUrl in link.get_attribute("href"):
                    link.click()
                    # Thoát khỏi vòng lặp và đóng trình duyệt
                    self.driver.quit()
                    exit()
            
            # Nếu không tìm thấy trang hellotruyen.com ở trang hiện tại thì chuyển sang trang kế tiếp
            try:
                next_button = self.driver.find_element_by_css_selector("#pnnext")
                next_button.click()
            except:
                # Nếu không có nút chuyển trang kế tiếp thì thoát khỏi vòng lặp và đóng trình duyệt
                self.driver.quit()
                exit()