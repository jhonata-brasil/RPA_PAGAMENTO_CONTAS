from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pyautogui
from selenium.webdriver.chrome.options import Options
import os
import time
import glob
import math

# Importações necessárias
import os
import xml.etree.ElementTree as ET
from lxml import etree

import os
import time
import zipfile
import shutil


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from helpers.utilities import Utilities, Utilities1
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

load_dotenv()

path_download_zip =os.getenv('PATH_DOWNLOADED_INVOICES_PDF')
download_dir = os.getenv('PATH_DOWNLOADED_INVOICES_PDF')


class Fluig:
    __slots__ = "robot", "logger", "slack"

    def __init__(self, log, slack) -> None:
        self.robot = Utilities()
        self.logger = log
        self.slack = slack

    def start_browser(self):
        try:
            self.robot.open_chrome()
        except Exception as e:
            self.logger.error(f" :::Erro ao abrir o navegador {e}")
            self.slack.post_message(f" :::Erro ao abrir o navegador {e}")
            raise

    def select_url(self, url):
        try:
            self.robot.browser.get(url)
            self.robot.browser.delete_all_cookies()
        except Exception as e:
            self.logger.error(f" ::: Erro ao abrir a página. {e}")
            self.slack.post_message(f" ::: Erro ao abrir a página. {e}")
            raise

    def login(self, user, passwd):
        element_input_username = '//*[@id="username"]'
        element_input_passwd = '//*[@id="password"]'
        element_btn_confirm = '//*[@id="submitLogin"]'

        self.robot.wait_element(element_input_username)
        self.robot.wait_element(element_input_passwd)

        try:
            self.robot.browser.find_element(By.XPATH, element_input_username).send_keys(
                user
            )
            self.logger.info(f"Digitou o Usuário {user}")
            sleep(2)
            self.robot.browser.find_element(By.XPATH, element_input_passwd).send_keys(
                passwd
            )
            self.logger.info("Digitou a senha....")
            sleep(2)

            self.robot.browser.find_element(By.XPATH, element_btn_confirm).click()

            sleep(2)
            self.logger.info("Realizando Login...")

            self.robot.browser.refresh()
            #Quando for utilizar o ambiente de Homologação desabilite a linha abaixo
            # self.robot.wait_element("//a[contains(@href, 'https://csc.findes.org.br/portal/p/1/home')]")

            self.logger.info("Login realizado com sucesso!")

        except Exception as e:
            self.logger.error(f"Erro ao realizar login {e}")
            self.slack.post_message(f"Erro ao realizar login {e}")
            raise

    def go_to_payment_request(self):
        element_icon_homepage = "//li//a[contains(@href, '/portal/p/1/home')]"
        element_btn_payment_request = (
            "//*[contains(text(), 'Solicitação de Pagamento')]"
        )
        self.robot.wait_element(element_icon_homepage)
        try:
            self.robot.browser.find_element(By.XPATH, element_icon_homepage).click()

            self.robot.wait_element(element_btn_payment_request)

            sleep(1)
            self.robot.browser.find_element(By.XPATH, element_btn_payment_request).click()
        except Exception as e:
            self.logger.error(f'  :::Erro ao ir para o btn de Solicitação de Pagamento. {e}')
            self.slack.post_message(f'  ::: Erro ao ir para o btn de Solicitação de pagamento. {e}')
            raise

    def go_to_input_and_insert_value(self, type_element, value):
        try:
            self.robot.wait_element(type_element)
            input_element_coligada = self.robot.browser.find_element(
                By.XPATH, type_element
            )
            input_element_coligada.click()
            input_element_coligada.clear()
            input_element_coligada.send_keys(value)
            sleep(10)
            input_element_coligada.send_keys(Keys.ENTER)
            self.logger.info(f"Valor inserido com sucesso! {value}")
        except Exception as e:
            self.logger.error(f" :::Erro ao inserir valor em campo {e}")
            self.slack.post_message(f' :::Erro ao inserir valor em campo {e}')
            raise

    def go_to_input_coligada(self, coligada):
        element_coligada = "/html/body/div/form/div[2]/div[2]/div[2]/div[2]/span/span[1]/span/ul/li/input"

        self.go_to_input_and_insert_value(element_coligada, coligada)

    def go_to_input_branch(self, branch):
        element_branch = "/html/body/div/form/div[2]/div[2]/div[2]/div[4]/span/span[1]/span/ul/li/input"

        self.go_to_input_and_insert_value(element_branch, branch)

    def go_to_input_cpf_cnpj(self, cnpj):
        element_cnpj = "/html/body/div/form/div[2]/div[2]/div[3]/div[1]/span/span[1]/span/ul/li/input"

        self.go_to_input_and_insert_value(element_cnpj, cnpj)

    def go_to_input_departament(self, departament):
        element_departament = "/html/body/div/form/div[2]/div[2]/div[4]/div[2]/span/span[1]/span/ul/li/input"

        self.go_to_input_and_insert_value(element_departament, departament)

    def go_to_input_cost_center(self, cost_center):
        element_cost_center = "/html/body/div/form/div[2]/div[2]/div[4]/div[4]/span/span[1]/span/ul/li/input"

        self.go_to_input_and_insert_value(element_cost_center, cost_center)
    #Função juros 
    def go_to_value_juros(self, juros):
        element_value_juros = '//*[@id="TMOV_T_VALOREXTRA1"]'
        self.robot.wait_element(element_value_juros)
        input_element_value_juros = self.robot.browser.find_element(
            By.XPATH, element_value_juros
        )
        input_element_value_juros.click()
        input_element_value_juros.send_keys(juros)

        

    #Função Multa 
    def go_to_value_multa(self, multa):
        element_value_multa = '//*[@id="TMOV_T_VALOREXTRA2"]'
        self.robot.wait_element(element_value_multa)
        input_element_value_multa = self.robot.browser.find_element(
            By.XPATH, element_value_multa
        )
        input_element_value_multa.click()
        input_element_value_multa.send_keys(multa)    
    




    def select_dropdown_value(self, element_xpath, value):
        try:
            # Espera até que o elemento esteja presente na página
            WebDriverWait(self.robot.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, element_xpath))
            )
            # Encontra o elemento e seleciona o valor desejado
            select_element = Select(self.robot.browser.find_element(By.XPATH, element_xpath))
            select_element.select_by_visible_text(value)
        except Exception as e:
            self.logger.error(f" ::: Erro ao selecionar o valor no dropdown. {e}")
            self.slack.post_message(f" ::: Erro ao selecionar o valor no dropdown. {e}")
            raise

    def Select_movimentarassinatura(self):
        element_select_movimentar = '//*[@id="nextActivity"]'
        #var_atividade = 'Ajuste do Solicitante'
        var_atividade ='Provisionado?'
        self.select_dropdown_value(element_select_movimentar, var_atividade)
      
 

    def go_to_input_payament_type(self, payament_type):
        element_payament_type = "/html/body/div/form/div[2]/div[2]/div[6]/div[1]/span/span[1]/span/ul/li/input"
        # '//*[@id="TAREFA"]'

        self.robot.browser.find_element(By.XPATH, element_payament_type).click()
        self.go_to_input_and_insert_value(element_payament_type, payament_type)

    def go_to_value_total(self, value_total):
        element_value_total = '//*[@id="TMOV_T_VALORBRUTO"]'
        self.robot.wait_element(element_value_total)
        input_element_value_total = self.robot.browser.find_element(
            By.XPATH, element_value_total
        )
        input_element_value_total.click()
        input_element_value_total.send_keys(value_total)

    def go_to_numero_documento(self, numeroNota):
        element_numero_doc = "//input[@id='TMOV_T_SEGUNDONUMERO']"
        self.robot.wait_element(element_numero_doc)

        input_element_numero_doc = self.robot.browser.find_element(
        By.XPATH, element_numero_doc
        )
        input_element_numero_doc.click()
        input_element_numero_doc.send_keys(Keys.BACKSPACE)
        input_element_numero_doc.send_keys(numeroNota)


    def go_to_date_competence(self, dateCompetence):
        element_date_competence = (
            "/html/body/div[1]/form/div[2]/div[2]/div[6]/div[3]/input"
        )


        date_today = datetime.strptime(dateCompetence, "%d/%m/%Y").strftime("%Y-%m-%d")
        print(date_today)

        input_element_data_competence = self.robot.browser.find_element(
            By.XPATH, element_date_competence
        )
        self.robot.browser.execute_script(
            "arguments[0].value = arguments[1]",
            input_element_data_competence,
            date_today,
        )

    def go_to_historical(self, value_historical):
        element_historical = '//*[@id="HIST_COMPLEMENTAR"]'

        input_element_historical = self.robot.browser.find_element(
            By.XPATH, element_historical
        )
        input_element_historical.send_keys(value_historical)
    

    def verificar_Rateio(self, Possui_rateio,Departamento_rateio1,Centro_de_Custo_rateio1,Percentual_rateio1,Departamento_rateio2,Centro_de_Custo_rateio2,Percentual_rateio2,Departamento_rateio3,Centro_de_Custo_rateio3,Percentual_rateio3):
        if Possui_rateio =="Sim":
            #Clicar em Itens
            self.clicar_itens_rateio()
            # Rolar a página para baixo em 500 pixels (ajuste o valor conforme necessário)
            self.robot.browser.execute_script("window.scrollBy(0, 500);")   
            #Clicar em Rateio
            self.clicar_btn_rateio()
            # sleep(20)
            if (Departamento_rateio1 is not None  # Verifica se não é None
                and Departamento_rateio1 != ''  # Verifica se não é uma string vazia
                and not (isinstance(Departamento_rateio1, str) and Departamento_rateio1.strip().lower() == "nan")  # Verifica se não é "nan" (string)
                and not (isinstance(Departamento_rateio1, float) and math.isnan(Departamento_rateio1))  # Verifica se não é NaN (float)
            ):
                #1° inserir o departamento
                element_departament_1, type_element_input = self.departamento_rateio1()
                self.logger.info(f" :::Departamento_rateio1 localizado {Departamento_rateio1}")
                self.go_to_input_insert_value_department(element_departament_1,Departamento_rateio1,type_element_input)

                #2° inserir o centro do custo
                element_centro_custo = self.centro_de_custo_rateio1()
                self.logger.info(f" :::Departamento_rateio1 localizado {Departamento_rateio1}")
                self.go_to_input_insert_value_centro_de_custo(element_centro_custo,Centro_de_Custo_rateio1,element_centro_custo)
                self.logger.info(f" :::Centro_de_Custo_rateio1 localizado {Centro_de_Custo_rateio1}")

                #3° Percentual do rateio
                element_percentual_rateio1 = self.percentual_rateio1()
                self.logger.info(f" :::Departamento_rateio1 localizado {Departamento_rateio1}")
                self.go_to_input_insert_value_percentual(element_percentual_rateio1,Percentual_rateio1,element_percentual_rateio1)
                sleep(2)
                
            else:
                self.logger.error(f" :::Departamento_rateio1 não localizado {Departamento_rateio1}")
                self.slack.post_message(f' :::Departamento_rateio1 não localizado {Departamento_rateio1}')
            

            if (Departamento_rateio2 is not None  # Verifica se não é None
                and Departamento_rateio2 != ''  # Verifica se não é uma string vazia
                and not (isinstance(Departamento_rateio2, str) and Departamento_rateio2.strip().lower() == "nan")  # Verifica se não é "nan" (string)
                and not (isinstance(Departamento_rateio2, float) and math.isnan(Departamento_rateio2))  # Verifica se não é NaN (float)
            ): 

                #Clicar em Incluir
                self.clicar_incluir_rateio()
                #1° inserir o departamento
                element_departament_1, type_element_input = self.departamento_rateio2()
                self.logger.info(f" :::Departamento_rateio1 localizado {Departamento_rateio2}")
                self.go_to_input_insert_value_department(element_departament_1,Departamento_rateio2,type_element_input)

                #2° inserir o centro do custo
                element_centro_custo = self.centro_de_custo_rateio2()
                self.logger.info(f" :::Departamento_rateio1 localizado {Departamento_rateio2}")
                self.go_to_input_insert_value_centro_de_custo(element_centro_custo,Centro_de_Custo_rateio2,element_centro_custo)
                self.logger.info(f" :::Centro_de_Custo_rateio1 localizado {Centro_de_Custo_rateio2}")

                #3° Percentual do rateio
                element_percentual_rateio1 = self.percentual_rateio2()
                self.logger.info(f" :::Departamento_rateio1 localizado {Departamento_rateio2}")
                self.go_to_input_insert_value_percentual(element_percentual_rateio1,Percentual_rateio2,element_percentual_rateio1)
                sleep(1)
                
            else:
                self.logger.error(f" :::Departamento_rateio2 não localizado {Departamento_rateio2}")
                self.slack.post_message(f' :::Departamento_rateio2 não localizado {Departamento_rateio2}')

            if (Departamento_rateio3 is not None  # Verifica se não é None
                and Departamento_rateio3 != ''  # Verifica se não é uma string vazia
                and not (isinstance(Departamento_rateio3, str) and Departamento_rateio3.strip().lower() == "nan")  # Verifica se não é "nan" (string)
                and not (isinstance(Departamento_rateio3, float) and math.isnan(Departamento_rateio3))  # Verifica se não é NaN (float)
            ):           
                #Clicar em Incluir
                self.clicar_incluir_rateio()
                #1° inserir o departamento
                element_departament_1, type_element_input = self.departamento_rateio3()
                self.logger.info(f" :::Departamento_rateio3 localizado {Departamento_rateio3}")
                self.go_to_input_insert_value_department(element_departament_1,Departamento_rateio3,type_element_input)

                #2° inserir o centro do custo
                element_centro_custo = self.centro_de_custo_rateio3()
                self.logger.info(f" :::Centro_de_Custo_rateio3 localizado {Departamento_rateio3}")
                self.go_to_input_insert_value_centro_de_custo(element_centro_custo,Centro_de_Custo_rateio3,element_centro_custo)
                self.logger.info(f" :::Centro_de_Custo_rateio3 localizado {Centro_de_Custo_rateio3}")

                #3° Percentual do rateio
                element_percentual_rateio1 = self.percentual_rateio3()
                self.logger.info(f" :::Percentual_rateio3 localizado {Departamento_rateio3}")
                self.go_to_input_insert_value_percentual(element_percentual_rateio1,Percentual_rateio3,element_percentual_rateio1)
                sleep(1)
                
            else:
                self.logger.error(f" :::Departamento_rateio3 não localizado {Departamento_rateio3}")
                self.slack.post_message(f' :::Departamento_rateio3 não localizado {Departamento_rateio3}')
        else:
            print("Não existe Rateio para Fatura")
        self.logger.info(f" Etapa de verificar_Rateio concluido com sucesso")
  

    def clicar_itens_rateio(self):
        #Clicar em Itens
        element_itens = '//*[@id="tabItems"]'
        self.robot.wait_element(element_itens)
        input_element_itens = self.robot.browser.find_element(
        By.XPATH, element_itens
        )
        input_element_itens.click()
        sleep(2)

    def clicar_btn_rateio(self):
        #Clicar em Rateio
        element_numero_doc = '//*[@id="apportionments___1"]'
        self.robot.wait_element(element_numero_doc)
        input_element_numero_doc = self.robot.browser.find_element(
        By.XPATH, element_numero_doc
        )
        input_element_numero_doc.click() 
    
    def clicar_incluir_rateio(self):
        #Clicar em incluir
        element_numero_doc = '//*[@id="buttonTblApportionmentsItems"]'
        self.robot.wait_element(element_numero_doc)
        input_element_numero_doc = self.robot.browser.find_element(
        By.XPATH, element_numero_doc
        )
        input_element_numero_doc.click()


    def departamento_rateio1(self):
        element_departament_1 ='//*[@id="trApportionmentsItems___1"]/td[3]/span/span[1]/span/ul/li[1]/span'
        type_element_input ='//*[@id="trApportionmentsItems___1"]/td[3]/span/span[1]/span/ul/li/input'
        return element_departament_1, type_element_input
    
    def departamento_rateio2(self):
        element_departament_1 ='//*[@id="trApportionmentsItems___2"]/td[3]/span/span[1]/span/ul/li/input'
        type_element_input ='//*[@id="trApportionmentsItems___2"]/td[3]/span/span[1]/span/ul/li/input'
        return element_departament_1, type_element_input
    
    def departamento_rateio3(self):
        element_departament_1 ='//*[@id="trApportionmentsItems___3"]/td[3]/span/span[1]/span/ul/li/input'
        type_element_input ='//*[@id="trApportionmentsItems___3"]/td[3]/span/span[1]/span/ul/li/input'
        return element_departament_1, type_element_input
    
    def centro_de_custo_rateio1(self):
        element_centro_custo ='//*[@id="trApportionmentsItems___1"]/td[4]/span/span[1]/span/ul/li/input'
        return element_centro_custo
    
    def centro_de_custo_rateio2(self):
        element_centro_custo ='//*[@id="trApportionmentsItems___2"]/td[4]/span/span[1]/span/ul/li/input'       
        return element_centro_custo
    
    def centro_de_custo_rateio3(self):
        element_centro_custo ='//*[@id="trApportionmentsItems___3"]/td[4]/span/span[1]/span/ul/li/input'       
        return element_centro_custo
    
    def percentual_rateio1(self):
        element_percentual_rateio1 ='//*[@id="PERCENTUAL___1"]'
        return element_percentual_rateio1
    
    def percentual_rateio2(self):
        element_percentual_rateio1 ='//*[@id="PERCENTUAL___2"]'
        return element_percentual_rateio1
    
    def percentual_rateio3(self):
        element_percentual_rateio1 ='//*[@id="PERCENTUAL___3"]'
        return element_percentual_rateio1
    
    def go_to_input_insert_value_department(self, type_element,Departamento_rateio,type_element_input):
        try:
            self.robot.wait_element(type_element)
            input_element_departamento = self.robot.browser.find_element(
                By.XPATH, type_element
            )
            input_element_departamento.click()

            self.robot.wait_element(type_element_input)
            input_element_departamento_text = self.robot.browser.find_element(
                By.XPATH, type_element_input
            )

            # input_element_departamento.clear()
            input_element_departamento_text.send_keys(Departamento_rateio)
            sleep(10)
            input_element_departamento_text.send_keys(Keys.ENTER)
            self.logger.info(f"Valor inserido com sucesso! {Departamento_rateio}")
        except Exception as e:
            self.logger.error(f" :::Erro ao inserir valor em campo {e}")
            self.slack.post_message(f' :::Erro ao inserir valor em campo {e}')
            raise

    def go_to_input_insert_value_centro_de_custo(self, type_element,Centro_de_Custo_rateio,type_element_input):
        try:
            self.robot.wait_element(type_element)
            input_element_departamento = self.robot.browser.find_element(
                By.XPATH, type_element
            )
            input_element_departamento.click()

            self.robot.wait_element(type_element_input)
            input_element_departamento_text = self.robot.browser.find_element(
                By.XPATH, type_element_input
            )

            # input_element_departamento.clear()
            input_element_departamento_text.send_keys(Centro_de_Custo_rateio)
            sleep(10)
            input_element_departamento_text.send_keys(Keys.ENTER)
            self.logger.info(f"Valor inserido com sucesso! {Centro_de_Custo_rateio}")
        except Exception as e:
            self.logger.error(f" :::Erro ao inserir valor em campo Centro_de_Custo_rateio1 {e}")
            self.slack.post_message(f' :::Erro ao inserir valor em campo Centro_de_Custo_rateio1 {e}')
            raise
    
    def go_to_input_insert_value_percentual(self, type_element,percentual,type_element_input):
        try:
            self.robot.wait_element(type_element)
            input_element_percentual = self.robot.browser.find_element(
                By.XPATH, type_element
            )
            input_element_percentual.click()

            input_element_percentual.clear()
            sleep(2)
            input_element_percentual.click()

            # Converte para string, remove o ponto e converte para inteiro
            percentual_sem_ponto = str(percentual).replace('.', '0') 
            percentual = int(percentual_sem_ponto)
            input_element_percentual.send_keys(percentual)
            sleep(2)
            self.logger.info(f"Valor inserido com sucesso! {percentual}")
        except Exception as e:
            self.logger.error(f" :::Erro ao inserir valor em campo percentual {e}")
            self.slack.post_message(f' :::Erro ao inserir valor em campo percentual {e}')
            raise
    
    # def centro_de_custo_rateio1(self):
    #     element_centro_custo ='//*[@id="trApportionmentsItems___1"]/td[4]/span/span[1]/span/ul/li/input'
    #     return element_centro_custo
    
    # def centro_de_custo_rateio2(self):
    #     element_centro_custo ='//*[@id="trApportionmentsItems___2"]/td[4]/span/span[1]/span/ul/li/input'       
    #     return element_centro_custo
    
    # def centro_de_custo_rateio3(self):
    #     element_centro_custo ='//*[@id="trApportionmentsItems___3"]/td[4]/span/span[1]/span/ul/li/input'       
    #     return element_centro_custo

    def go_to_form_of_payment(self, value_form_of_payment):
        element_form_of_payment = (
            '//*[@id="financial"]/div/div[3]/span/span[1]/span/ul/li/input'
        )
#//*[@id="financial"]/div/div[3]/span/span[1]/span/ul/li/input
#/html/body/div[1]/form/div[2]/div[2]/div[11]/div/div/div[1]/div/div[3]/span/span[1]/span/ul/li/input
        self.go_to_input_and_insert_value(
            element_form_of_payment, value_form_of_payment
        )

    def go_to_conta(self, value_conta):
        element_conta = '//*[@id="financial"]/div/div[2]/span/span[1]/span/ul/li/input'

        self.go_to_input_and_insert_value(element_conta, value_conta)

    def go_to_attach_file(self):
        element_attach_file = '//*[@id="tab-attachments"]/a'

        self.robot.browser.switch_to.default_content()  # sai do iframe e retorna para documento html princiál
        self.robot.wait_element(element_attach_file)
        self.robot.browser.find_element(By.XPATH, element_attach_file).click()

    def upload_file_to_fluig(self, file):
        try:
            # Espere até que o formulário e o elemento de upload estejam visíveis
            wait = WebDriverWait(self.robot.browser, 10)
            form = wait.until(
                EC.presence_of_element_located((By.ID, "ecm_navigation_fileupload"))
            )
            upload_input = wait.until(
                EC.presence_of_element_located((By.ID, "ecm-navigation-inputFile-clone"))
            )

            # Agora você pode usar o elemento de upload para enviar o arquivo
            upload_input.send_keys(file)
        except Exception as e:
            self.slack.post_message(f' :::Erro ao fazer upload do arquivo {file}. Erro {e}')
            raise

    def send_payament_request_to_confirm(self):
        try:
            element_btn_send = '//*[@id="workflowActions"]/button[1]'
            self.robot.wait_element(element_btn_send)
            self.robot.browser.find_element(By.XPATH, element_btn_send).click()
        except Exception as e:
            self.logger.error(f"  :::Erro ao enviar solicitação de pagamento {e}")
            self.slack.post_message(f'  ::: Erro ao enviar solicitação de pagamento {e}')
            raise

    def send_payament_request_to_confirm_2(self):
        try:
            # element_btn_send = '//*[@id="workflowActions"]/button[1]'
            element_btn_send ='//*[@id="moviment-button"]'
            
            self.robot.wait_element(element_btn_send)
            self.robot.browser.find_element(By.XPATH, element_btn_send).click()
        except Exception as e:
            self.logger.error(f"  :::Erro ao enviar solicitação de pagamento {e}")
            self.slack.post_message(f'  ::: Erro ao enviar solicitação de pagamento {e}')
            raise
            
    def get_number_request_fluig(self):
        try:
            element_confirm_request_number = '//*[@id="message-page"]/div/div[1]'
            
            self.robot.wait_element(element_confirm_request_number)
            
            if self.robot.browser.find_element(By.XPATH, element_confirm_request_number):
            
                number_request = self.robot.browser.find_element(By.XPATH, '//*[@id="message-page"]/div/div[1]/span/a').text
                sleep(2)
                self.robot.browser
                return number_request   
        except Exception as e:
            self.slack.post_message(f'  :::Erro na etapa de verificar número de solicitação {e}')
            raise
            
    def insert_input_to_generate_payment_request(
        self,
        coligada,
        branch,
        cnpj,
        departament,
        cost_center,
        value_total,
        payament_type,
        historical_complement,
        value_conta,
        form_of_payment,
        file,
        numeroNota,
        dataEmissao,
        Possui_rateio,
        Departamento_rateio1,
        Centro_de_Custo_rateio1,
        Percentual_rateio1,
        Departamento_rateio2,
        Centro_de_Custo_rateio2,
        Percentual_rateio2,
        Departamento_rateio3,
        Centro_de_Custo_rateio3,
        Percentual_rateio3,
        juros,
        multa
        
    ):
        self.robot.wait_element('//*[@id="workflowView-cardViewer"]')
        iframe_screen_inputs = self.robot.browser.find_element(
            By.XPATH, '//*[@id="workflowView-cardViewer"]'
        )
        self.robot.browser.switch_to.frame(iframe_screen_inputs)

        # Insere valor no campo de Coligada
        self.go_to_input_coligada(coligada)

        # Inserir valor no campo de Filial
        self.go_to_input_branch(branch)

        # Inserir valor no campo de CPJ/CNPJ
        self.go_to_input_cpf_cnpj(cnpj)

        # Inserir valor no campo de Departamento
        self.go_to_input_departament(departament)

        # Inserir Centro de Custo
        self.go_to_input_cost_center(cost_center)

        # Inserir Numero Nota
        self.go_to_numero_documento(numeroNota)

        # Inserir Valor Total
        self.go_to_value_total(value_total)

        # Inserir juros
        self.go_to_value_juros(juros)

        # Inserir multa
        self.go_to_value_multa(multa)

        # Inserir Tipo de Pagamento
        self.go_to_input_payament_type(payament_type)

        # Inserir data de competência
        self.go_to_date_competence(dataEmissao)

        # inserir historico competencia
        self.go_to_historical(historical_complement)

        # Inserir conta
        self.go_to_conta(value_conta)

        # Inserir forma de pagamento
        self.go_to_form_of_payment(form_of_payment)


        self.verificar_Rateio(Possui_rateio,Departamento_rateio1,Centro_de_Custo_rateio1,Percentual_rateio1,Departamento_rateio2,Centro_de_Custo_rateio2,Percentual_rateio2,Departamento_rateio3,Centro_de_Custo_rateio3,Percentual_rateio3)


        # Vai para a tela para anexar o arquivo
        self.go_to_attach_file()

        # Anexar arquivo
        self.upload_file_to_fluig(file)

        sleep(10)

        # Confirma solicitação de pagamento (Clique em btn Enviar)
        self.send_payament_request_to_confirm()
        sleep(3)

        self.Select_movimentarassinatura()
        sleep(3)

        # self.Select_movimentarassinatura()
        self.send_payament_request_to_confirm_2()
        sleep(5)
        
        return self.get_number_request_fluig()
    

class EDPLINK:
    __slots__ = "robot", "logger", "slack"

    def __init__(self, log, slack) -> None:
        self.robot = Utilities1()
        self.logger = log
        self.slack = slack


    def start_browser1(self):
        try:
            self.robot.open_chrome1()
        except Exception as e:
            self.logger.error(f" :::Erro ao abrir o navegador {e}")
            self.slack.post_message(f" :::Erro ao abrir o navegador {e}")
            raise

    def select_url_1(self, link_extraido):
        try:
            self.robot.browser.get(link_extraido)
            self.robot.browser.delete_all_cookies()
        except Exception as e:
            self.logger.error(f" ::: Erro ao abrir a página. {e}")
            self.slack.post_message(f" ::: Erro ao abrir a página. {e}")
            raise
    


    def open_extracted_link(self, link_extraido):
        """
        Abre o link extraído no navegador.
        """
        try:
            # Verifica se o navegador já está aberto
            if not hasattr(self.robot, 'browser'):
                self.start_browser()  # Abre o navegador se não estiver aberto

            # Navega até o link extraído
            self.logger.info(f"Abrindo o link extraído: {link_extraido}")
            self.select_url_1(link_extraido)

            # Aguarda um tempo para garantir que a página carregue
            sleep(5)  # Ajuste o tempo conforme necessário

            self.logger.info("Link aberto com sucesso no navegador.")

        except Exception as e:
            self.logger.error(f"Erro ao abrir o link extraído: {e}")
            self.slack.post_message(f"Erro ao abrir o link extraído: {e}")
            raise





    def downloadEDP_contaslink(self):
        """
        Encontra e clica no checkbox e, em seguida, clica no botão de download.
        """
        # Definição dos elementos
        element_checkbox = '//*[@id="checkAll"]'
        # element_btn_download = '/html/body/form/table/tbody/tr[14]/td[1]/input'

        try:
            # Aguarda o checkbox estar visível e clicável
            self.logger.info("Aguardando o checkbox estar disponível...")
            checkbox = WebDriverWait(self.robot.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, element_checkbox)))

            # Clica no checkbox
            self.logger.info("Clicando no checkbox...")
            checkbox.click()

            # Aguarda o botão de download estar visível e clicável
            # self.logger.info("Aguardando o botão de download estar disponível...")
            # btn_download = WebDriverWait(self.robot.browser, 20).until(
            #     EC.element_to_be_clickable((By.XPATH, element_btn_download)))
                    # Encontra o botão de download pelo value="Download"
            self.logger.info("Buscando o botão de download...")
            btn_download = WebDriverWait(self.robot.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@value="Download"]')))

            # Clica no botão de download
            self.logger.info("Clicando no botão de download...")
            btn_download.click()

            # Aguarda um tempo para garantir que a janela "Salvar Como" seja aberta
            time.sleep(5)  # Ajuste o tempo conforme necessário

            # Pressiona Enter para confirmar a janela "Salvar Como"
            self.logger.info("Pressionando Enter para confirmar a janela 'Salvar Como'...")
            pyautogui.press('enter')  # Simula o pressionamento de Enter na janela "Salvar Como"

            # Aguarda o download ser iniciado e finalizado
            time.sleep(25)  # Ajuste o tempo conforme necessário

            # Verificar se o arquivo .zip foi baixado
            download_dir_ZIP = os.getenv('PATH_DOWNLOADED_ZIP')  # Pasta onde o .zip é baixado
            downloaded_file = self.wait_for_zip_download(download_dir_ZIP)

            if downloaded_file:
                self.logger.info(f"Arquivo .zip encontrado: {downloaded_file}")
                
                # Pasta onde os arquivos serão extraídos
                download_dir = os.getenv('PATH_DOWNLOADED_INVOICES_PDF')
                
                # Extrair o conteúdo do arquivo .zip para o diretório de destino
                self.logger.info("Extraindo o conteúdo do arquivo .zip...")
                self.extract_zip(os.path.join(download_dir_ZIP, downloaded_file), download_dir)
                self.logger.info("Conteúdo extraído com sucesso.")
                
                # Função para excluir arquivos .zip
                self.delete_zip_file(prefix="documentos_edp_")
                # Chame o método corretamente, passando apenas o prefixo

                self.renomear_arquivos(download_dir)




                # Após a extração, podemos fechar o navegador
                self.robot.browser.quit()

            else:
                self.logger.error("Nenhum arquivo .zip encontrado.")

        except Exception as e:
            self.logger.error(f"Erro ao tentar realizar o download: {e}")
            # self.slack.post_message(f"Erro ao tentar realizar o download: {e}")
            raise


    def wait_for_zip_download(self, download_dir_ZIP, timeout=60):
        """
        Verifica se o download de um arquivo .zip foi concluído na pasta especificada.
        Aguarda até que um arquivo .zip apareça na pasta de downloads.
        """
        elapsed_time = 0
        downloaded_files = os.listdir(download_dir_ZIP)

        # Aguarda o download ser concluído ou o tempo limite ser atingido
        while elapsed_time < timeout:
            time.sleep(1)  # Aguarda 1 segundo
            downloaded_files = os.listdir(download_dir_ZIP)

            # Filtra arquivos .zip
            zip_files = [f for f in downloaded_files if f.endswith('.zip')]

            if zip_files:
                # Ordena os arquivos por data de modificação e pega o último
                return sorted(zip_files, key=lambda x: os.path.getmtime(os.path.join(download_dir_ZIP, x)))[-1]

            elapsed_time += 1

        return None  # Retorna None se o tempo expirar sem encontrar o arquivo


    def extract_zip(self, zip_file_path, extract_to_dir):
        """
        Extrai o conteúdo de um arquivo .zip para o diretório especificado.
        """
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_dir)  # Extrai todos os arquivos para o diretório de destino
            self.logger.info(f"Arquivos extraídos para {extract_to_dir}")

        except zipfile.BadZipFile:
            self.logger.error(f"O arquivo {zip_file_path} não é um arquivo ZIP válido.")
        except Exception as e:
            self.logger.error(f"Erro ao extrair o arquivo ZIP: {e}")

    

    def delete_zip_file(self,prefix):
        """
        Função para excluir arquivos .zip que começam com um prefixo específico
        no diretório definido pela variável de ambiente 'PATH_DOWNLOADED_ZIP'.

        :param prefix: Prefixo do nome do arquivo (ex: 'documentos_edp_').
        """
        # Obtém o diretório de download da variável de ambiente
        download_dir_ZIP = os.getenv('PATH_DOWNLOADED_ZIP')

        if not download_dir_ZIP:
            print("Variável de ambiente 'PATH_DOWNLOADED_ZIP' não está definida.")
            return

        # Busca por arquivos que começam com o prefixo e terminam com .zip
        zip_files = glob.glob(os.path.join(download_dir_ZIP, f"{prefix}*.zip"))

        if not zip_files:
            print(f"Nenhum arquivo .zip encontrado com o prefixo '{prefix}' no diretório '{download_dir_ZIP}'.")
            return

        for zip_file in zip_files:
            try:
                os.remove(zip_file)
                print(f"Arquivo .zip excluído com sucesso: {zip_file}")
            except Exception as e:
                print(f"Erro ao excluir o arquivo {zip_file}: {e}")




    def renomear_arquivos(self,download_dir):
        # Listar todos os arquivos no diretório de downloads
        for filename in os.listdir(download_dir):

            # Verificar se o arquivo é XML
            if filename.endswith(".xml"):
                # Remover a extensão .xml para mostrar apenas o nome do arquivo
                nome_sem_extensao = os.path.splitext(filename)[0]  # Nome sem a extensão .xml
                print(f"Processando XML: {nome_sem_extensao}")

                # Definir o caminho completo do arquivo XML
                xml_file_path = os.path.join(download_dir, filename)
                print(f"Caminho completo do XML: {xml_file_path}")

                try:
                    # Definir o parser com codificação iso-8859-1
                    parser = etree.XMLParser(encoding="iso-8859-1")
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()

                    # Definir os namespaces
                    namespaces = {
                        'nf3e': 'http://www.portalfiscal.inf.br/nf3e',
                        'ds': 'http://www.w3.org/2000/09/xmldsig#'
                    }

                    # Procurar o <idAcesso> com o namespace correto
                    id_acesso_elem = root.find('.//nf3e:idAcesso', namespaces)
                    
                    if id_acesso_elem is not None:
                        id_acesso = id_acesso_elem.text
                        print(f"ID de Acesso encontrado: {id_acesso}")
                    else:
                        print(f"ID de Acesso não encontrado no arquivo {filename}. Pulando o arquivo.")
                        continue  # Pula para o próximo arquivo XML caso o idAcesso não seja encontrado

                    # Renomear o arquivo PDF correspondente
                    for pdf_filename in os.listdir(download_dir):
                        if pdf_filename.endswith(".pdf") and f"_{id_acesso}_" in pdf_filename:
                            pdf_file_path = os.path.join(download_dir, pdf_filename)
                            novo_nome_pdf = f"NEX{nome_sem_extensao}.pdf"
                            novo_caminho_pdf = os.path.join(download_dir, novo_nome_pdf)

                            # Verificar se o arquivo já existe
                            if os.path.exists(novo_caminho_pdf):
                                print(f"Arquivo {novo_nome_pdf} já existe. Pulando...")
                                continue  # Pula para o próximo arquivo PDF

                            # Renomear o arquivo PDF
                            os.rename(pdf_file_path, novo_caminho_pdf)
                            print(f"Arquivo PDF renomeado para: {novo_nome_pdf}")

                except etree.XMLSyntaxError:
                    print(f"Erro ao parsear o arquivo XML: {filename}. Ignorando o arquivo.")
                    continue


