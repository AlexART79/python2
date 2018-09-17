class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def go(self, url):
        self.driver.get(url)

    def is_title_contains(self, title):
        return title in self.driver.title