from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import shutil
from pathlib import Path
import os
from dotenv import load_dotenv

from selenium import webdriver




# Classe responsavel por conter as funções genéricas / que são reutilizaveis.

class Utilities:
    __slots__ = 'browser'

    def __init__(self):
        self.browser = None

    def open_chrome(self):
        options = Options()
        options.headless = True
        options.add_argument("--incognito")

        #options.add_argument('--headless')# options.add_argument("--incognito")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)


        options.add_argument('--disable-gpu')
        options.add_argument("--disable-web-security")  # adiciona a opção de desabilitar a segurança
        options.add_argument("--allow-running-insecure-content")  # permite a execução de conteúdo inseguro (HTTP) em sites HTTPS
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--lang=pt-BR")
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('log-level=3')
        prefs = {
            'download.default_directory': os.getcwd(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option('prefs', prefs)

        options.add_argument('--acceptInsecureCerts')

        #self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),  options=options)
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()

    def wait_element(self, element, time = 120):
        print(f'Aguardando elemento... {element}')
        WebDriverWait(self.browser, time).until(EC.visibility_of_element_located((By.XPATH, element))
)
        


class Utilities1:
    __slots__ = 'browser'

    def __init__(self):
        self.browser = None

    def open_chrome1(self):

        options = Options()
        options.headless = True
        options.add_argument("--incognito")
        path_download_zip = os.getenv('PATH_DOWNLOADED_INVOICES_PDF')


        #options.add_argument('--headless')# options.add_argument("--incognito")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)


        options.add_argument('--disable-gpu')
        options.add_argument("--disable-web-security")  # adiciona a opção de desabilitar a segurança
        options.add_argument("--allow-running-insecure-content")  # permite a execução de conteúdo inseguro (HTTP) em sites HTTPS
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--lang=pt-BR")
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('log-level=3')
        options.add_argument(f'--download.default_directory={path_download_zip}')
        options.add_experimental_option('prefs', {
            'download.prompt_for_download': False,  # Desabilita o prompt de "Salvar Como"
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })

        options.add_argument('--acceptInsecureCerts')

        #self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),  options=options)
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()

    def wait_element(self, element, time = 120):
        print(f'Aguardando elemento... {element}')
        WebDriverWait(self.browser, time).until(EC.visibility_of_element_located((By.XPATH, element))
)