import os

from selenium import webdriver
# from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options

Instance = None


def Initialize():
    global Instance
    options = Options()
    working_directory = os.getcwd() + "\downloads"
    options.add_experimental_option("prefs", {
        "download.default_directory": working_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    })
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    Instance = webdriver.Chrome('config/chromedriver.exe', chrome_options=options)

    Instance.maximize_window()
    return Instance


def CloseDriver():
    global Instance
    Instance.quit()
