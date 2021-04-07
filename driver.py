from selenium import webdriver
from selenium.webdriver.chrome.options import Options

Instance = None


def Initialize():
    global Instance
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    Instance = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    Instance.maximize_window()
    return Instance


def CloseDriver():
    global Instance
    Instance.quit()
