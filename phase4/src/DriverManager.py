from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    @staticmethod
    def chrome_driver():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--kiosk")
        return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
