import os
import openpyxl
import pyautogui
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from interface import Ui_MainWindow, QMainWindow, QApplication
import sys

class MyApp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # uic.loadUi('minerador.ui', self)  # Carregue o arquivo .ui gerado pelo Qt Designer

        self.btn_iniciar = self.findChild(QPushButton, 'btn_iniciar')
        self.btn_fechar = self.findChild(QPushButton, 'btn_fechar')
        
        self.btn_iniciar.clicked.connect(self.run_program)
        self.btn_fechar.clicked.connect(self.close_program)

    def run_program(self):
        self.collect_data()

    def close_program(self):
        self.close()

    def collect_data(self):
        pasta_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
        nome_arquivo = os.path.join(pasta_downloads, 'dados_raspagem.xlsx')

        # Criação do DataFrame consolidado (caso você tenha múltiplas iterações)
        resultados = []


        # # # chromedriver_1140573590
        driver_path = 'https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br'
        service = Service(driver_path)


        # Informações de Login
        EMAIL = 'comercial03@lupafiscal.com.br'
        PASSWORD = 'Akiklijim@1'

        driver = webdriver.Chrome()
        driver.get('https://plat.econodata.com.br/?_gl=1*aefotu*_gcl_au*MzgwNDM1MTQyLjE3MjQ5NzUxNTM.*_ga*MTk3MTAyMzk5MS4xNzI0OTc1MTU0*_ga_BFMKLBFXM8*MTcyNDk3NTE1My4xLjAuMTcyNDk3NTE1My42MC4wLjA.#/login')
        sleep(5)


        # INPUT DAS INFORMAÇÕES DE LOGIN
        email_info = driver.find_element(By.XPATH, '//input[@id="E-mail"]')
        sleep(1)
        email_info.send_keys(EMAIL)
        sleep(1)
        senha_info = driver.find_element(By.XPATH, '//input[@id="Senha"]')
        sleep(1)
        senha_info.send_keys(PASSWORD)
        sleep(2)
        botao = driver.find_element(
            By.XPATH, '//button[@id="plat-login-botao-entrar"]')
        sleep(2)
        botao.click()
        sleep(10)
        botao_pesquisa = driver.find_element(
            By.XPATH, '//i[@class="nav-icon icon-magnifier"]')
        botao_pesquisa.click()
        sleep(10)
        ultima_pesquisa = driver.find_element(
            By.XPATH, '//div[@class="busca-text text-oneline"]')
        sleep(2)
        ultima_pesquisa.click()
        sleep(5)

        # SELEÇÃO DA QUANTIDADE DE ITENS POR PÁGINA. TENTEI COM TEMPOS MENORES MAS NÃO FOI POSSÍVEL
        button_select = driver.find_element(
            By.XPATH, '//select[@class="custom-select"]')
        button_select.click()
        sleep(2)

        pyautogui.hotkey('2', '5', '0')
        sleep(3)

        button_select = driver.find_element(
            By.XPATH, '//select[@class="custom-select"]')
        button_select.click()
        sleep(10)


          

            


        bloco_informacoes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//tr[@class="ecdt-tr"]'))
        )



        for bloco in bloco_informacoes:
            sleep(1)

            bloco.click()

            sleep(1)

            # RASPAGEM DAS INFORMAÇÕES DO POPUP

            popup_informacoes = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@class="tw-w-full tw-mb-8 tw-px-2"]/div'))
            )
            
            field_dict = {}

            for info in popup_informacoes:
                linhas = info.text.split('\n')
                for linha in linhas:
                    if ':' in linha:
                        chave, valor = linha.split(':', 1)
                        field_dict[chave] = valor.strip()
                    else:
                        chave = f'info_{len(field_dict)+1}'
                        field_dict[chave] = linha.strip()    


            botao_fechar_popup = driver.find_element(
                By.XPATH, '//i[@class="fa fa-close fa-lg text-dark"]')
            botao_fechar_popup.click()

            numero_telefone = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="d-flex align-items-center text-nowrap table-font-lg mb-0 telefone-alta"]'))
            )
            
            if numero_telefone:
                field_dict['telefone'] = numero_telefone.text
                print(numero_telefone.text)

            resultados.append(field_dict)
            sleep(1)


            df = pd.DataFrame(resultados)

            df.to_excel(nome_arquivo, index=False)

            QMessageBox.information(self, 'Informação', 'Arquivo salvo na pasta Download')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())    