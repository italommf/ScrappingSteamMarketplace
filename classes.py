from selenium import webdriver
from datetime import datetime

class SeleniumBrowser:
    def __init__(self):
        self.driver = None

    def open_browser(self, c_options):
        self.driver = webdriver.Chrome(options=c_options)
        return self.driver

class Utils:
    @staticmethod
    def data_hora():
        now = datetime.now()
        data_hora = now.strftime("%d/%m/%y - %H:%M:%S")
        return data_hora

    @staticmethod
    def hora():
        now = datetime.now()
        hora = now.strftime("%H:%M:%S")
        return hora
    @staticmethod
    def data():
        now = datetime.now()
        data = now.strftime("%d/%m/%y")
        return data



