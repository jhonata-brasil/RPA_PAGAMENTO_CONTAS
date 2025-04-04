
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from fsspec.implementations.local import LocalFileSystem
from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text
from io import StringIO
from pdfminer.pdfdocument import PDFPasswordIncorrect
from pathlib import Path
from dotenv import load_dotenv


import pandas as pd
import os
import re
from datetime import datetime

from lxml import etree
import xml.etree.ElementTree as ET
import logging

from rpa_fluig import EDPLINK  # Importando a classe EDPLINK




vartipo_concessionaria =None
load_dotenv()



import os
import pandas as pd

# file_path = os.getenv('DOWNLOAD_PATH')

def read_excel_dealerships(file_path):
    """
    Função responsável por realizar a leitura do arquivo XLSX onde estão contidas 
    todas as informações que precisam ser inseridas.

    Returns:
        pd.DataFrame: DataFrame contendo os dados do arquivo XLSX.
    """
    try:
        # Verifica se o caminho do arquivo está correto
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
        
        # Imprime o caminho do arquivo para depuração
        print(f"Caminho do arquivo: {file_path}")
        
        # Lê o arquivo XLSX
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Verifica se o DataFrame foi carregado corretamente
        if df is None:
            raise ValueError("Falha ao carregar o DataFrame.")
        
        # Remove os zeros à esquerda na coluna "INSTALAÇÃO/MATRÍCULA"
        df['INSTALAÇÃO/MATRÍCULA'] = df['INSTALAÇÃO/MATRÍCULA'].astype(str).str.lstrip('0')
        
        return df
    except FileNotFoundError as fnfe:
        print(f"Erro de arquivo não encontrado: {fnfe}")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except pd.errors.EmptyDataError as ede:
        print(f"Erro de dados vazios: {ede}")
    except pd.errors.ParserError as pe:
        print(f"Erro de parsing: {pe}")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
    return None




# file_path= os.getenv('DOWNLOAD_PATH')

# def read_excel_dealerships(file_path):
#     """
#     Função responsável por realizar a leitura do arquivo XLSX onde estão contindas 
#     todas as informações que precisam ser inseridas 

#     Returns:
#         _type_: _description_
#     """
#     df = pd.read_excel(file_path, engine='openpyxl')

#         # Remove os zeros à esquerda na coluna "INSTALAÇÃO/MATRÍCULA"
#     df['INSTALAÇÃO/MATRÍCULA'] = df['INSTALAÇÃO/MATRÍCULA'].astype(str).str.lstrip('0')
    
#     return df
    
#     #df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
#     df = df.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)

       
#     return df


def convert_pdf_to_text(path, password):
    
    text = extract_text(path, password)
    
    # text = text.split('\n')
    
    # new_list_lines = list(filter(lambda item: item.strip() != "", text))
    
    # return new_list_lines
        # Verifica se o texto não é None ou uma string vazia
    if not text:
        return []  # Retorna uma lista vazia caso o texto seja inválido ou vazio
    
    # Divide o texto em linhas
    text = text.split('\n')
    
    # Filtra as linhas, removendo aquelas que são vazias ou apenas espaços
    new_list_lines = list(filter(lambda item: item.strip() != "", text))
    
    return new_list_lines

def extrair_numeros_sem_zeros_a_esquerda(numero):
    # A expressão regular corresponde a qualquer sequência de dígitos 0 a 9 após os zeros à esquerda.
    # O "+" significa "um ou mais".
    padrao = r'^0*(\d+)$'

    # Use a função findall para encontrar todas as correspondências na string.
    correspondencias = re.findall(padrao, numero)

    # Se houver correspondências, retorne a primeira correspondência (a parte após os zeros à esquerda).
    # Caso contrário, retorne None.
    if correspondencias:
        return correspondencias[0]
    else:
        return None


def extract_text_from_pdf(file_path, logger):
    """
    Função responsável por retornar uma lista com os dados extraídos.

    Args:
        file_path (_type_): _description_

    Returns:
        list: Retorna uma lista com
    """
    instalacao = None
    
    try:
        output_string = StringIO()
        with open(file_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        lines = output_string.getvalue().split('\n')
        
        new_list_lines = list(filter(lambda item: item.strip() != "", lines))
        
        return new_list_lines, instalacao
    except PDFPasswordIncorrect as e:

        dict_passcnpj_instalacao = {
            
            '0000151086': '03810',
            '0000150260': '03810',
            '0000151087': '03810',
            '0000151939': '03810',
            '0160675179': '03810',
            '0160833913': '03810',
            '0000152278': '03810',
            '0160105645': '28151',
            '0000580129': '03810',
            '0000693854': '03810',
            '0160105634': '03810',
            '0160105636': '03810',
            '0160105637': '03810',
            '0160169810': '03810',
            '0160835222': '03810',
            '0160700520': '03810',
            '0160105642': '03810',
            '0160105630': '03810',
            '0160105625': '03810',
            '0160105620': '03810',
            '0000150330': '28483',
            '0000150112': '03810',
            '0160828231': '28151',
            '0000150112': '03810',
            '0000150630': '03810',
            '0000150743': '03810',
            '0000151087': '03810',
            '0160663084': '03810',
            '0161017641': '03810',
            '0000150489': '03810',
            '0160929836': '03810',
            '0001959730': '03810'
        }
        
        filename = Path(file_path).stem
        
        logger.info(f'Processando PDF que possui senha {filename}')
        try:
            instalacao = filename.split('_')[2]
            fileNameError = False
        except:
            fileNameError = True
        
        if fileNameError:
            possiblePasswords = ["28151", "03810", "28483"]
            for password in possiblePasswords:
                    try:
                        list_line = convert_pdf_to_text(file_path, password)
                        for item in list_line:
                            if "INSTALAÇÃO" in item:
                                instalacao = item.replace("INSTALAÇÃO: ", "").strip()
                                return list_line, instalacao
                    except:
                        continue
            

        for key, value in dict_passcnpj_instalacao.items():
            if key == instalacao:
                list_line = convert_pdf_to_text(file_path, value)
                
                return list_line, instalacao

def extract_data_cesan(list_lines, logger):   
    matricula = None
    valor_total = None
    juros =0
    multa = 0
    
    logger.info('Executando extração para fatura Cesan.')
    
    for i in range(len(list_lines) - 1):
        try:
            if "Matrícula" in list_lines[i]:
                matricula = list_lines[i + 1]
            elif "Total a pagar R$" in list_lines[i]:
                valor_total = list_lines[i + 1].strip()
            elif "Mês/Ano referência" in list_lines[i]:
                numeroNota = list_lines[i + 1].strip()
            elif "Data Leitura Atual" in list_lines[i]:
                dataEmissao = list_lines[i + 5].strip()
        except Exception as e:
            logger.error(f'  :::Erro ao extrair dados da Fatura Cesan {e}')
            
    logger.info(f'Retornado para Cesan > Matrícula {matricula} | Valor Total {valor_total}')
    # registration, value_total, numeroNota, dataEmissao, juros, multa
            
    return matricula, valor_total, numeroNota, dataEmissao, juros, multa


def extract_data_edp_com_senha(list_lines, instalacao, logger):
    valor_total = None
    
    
    for i in range(len(list_lines) - 1):
        try:
            if "RESERVADO AO FISCO" in list_lines[i]:
                valor_total = list_lines[i + 3]
        except Exception as e:
            logger.error(f'  :::Erro ao extrair dados da Fatura Santa Maria {e}')
                        
    return instalacao, valor_total

#TESTE----



#FIM TESTE---------------------------------------

#CODIGO DE PRODUÇÃO
def extract_data_edp(list_lines, logger, xmlPath = ""):
    # Criando uma instância da classe EDPLINK

        # Transformar a lista em uma única string
    if list_lines == "EDP_XML":
        juros =0,00
        multa =0,00
        varLiquido_formatado =0,00

        parser = etree.XMLParser(encoding="iso-8859-1")
        tree = etree.parse(xmlPath, parser)
        root = tree.getroot()
        namespaces = {
            'nf3e': 'http://www.portalfiscal.inf.br/nf3e',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
        # Acessa os valores dentro das tags específicas -valor_total
        valor_total_str = tree.find('.//nf3e:vNF', namespaces=namespaces).text.replace(".", ",")
        instalacao = tree.find('.//nf3e:idAcesso', namespaces=namespaces).text
        dataEmissaoXML = tree.find('.//nf3e:dhEmi', namespaces=namespaces).text
        dataEmissao = datetime.strptime(dataEmissaoXML, '%Y-%m-%dT%H:%M:%S%z').strftime("%d/%m/%Y")
        inf_nf3e = tree.find('.//nf3e:infNF3e', namespaces=namespaces).get("Id").replace("NF3e", "")
        numeroNota = inf_nf3e[25:34]

        # Inicialize as variáveis de JUROS e MULTA
        juros = None
        multa = None

        # Encontrar todos os elementos <det> no XML
        det_items = tree.xpath('//nf3e:det', namespaces=namespaces)

        # Percorrer todos os elementos <det>
        for det in det_items:
            # Encontrar o <xProd> e verificar se é "JUROS" ou "MULTA"
            xProd = det.xpath('.//nf3e:prod/nf3e:xProd', namespaces=namespaces)
            
            if xProd:
                xProd_text = xProd[0].text
                
                # Verificar se o xProd contém "JUROS" ou "MULTA"
                if "JUROS" in xProd_text:
                    juros = det.xpath('.//nf3e:prod/nf3e:vProd', namespaces=namespaces)[0].text if det.xpath('.//nf3e:prod/nf3e:vProd', namespaces=namespaces) else None
                elif "MULTA" in xProd_text:
                    multa = det.xpath('.//nf3e:prod/nf3e:vProd', namespaces=namespaces)[0].text if det.xpath('.//nf3e:prod/nf3e:vProd', namespaces=namespaces) else None

        # Exibir os resultados
        print(f"JUROS: {juros}")
        print(f"MULTA: {multa}")

        def converter_para_float(valor):
            # Substituir o ponto de milhares por nada
            valor = valor.replace(".", "")
            # Substituir a vírgula por ponto (caso seja separador decimal)
            valor = valor.replace(",", ".")
            return float(valor)


        # Corrigir e converter para float
        valor_total_float = converter_para_float(valor_total_str)
        print(valor_total_float)

        # # Encontrar os elementos que contêm as informações de JUROS e MULTA
        # juros_item = tree.xpath('//nf3e:det[@nItem="3"]/nf3e:detItem/nf3e:prod/nf3e:vProd', namespaces=namespaces)
        # multa_item = tree.xpath('//nf3e:det[@nItem="4"]/nf3e:detItem/nf3e:prod/nf3e:vProd', namespaces=namespaces)
  
        # Verificar se os valores foram encontrados
        # juros = juros_item[0].text if juros_item else None
        # multa = multa_item[0].text if multa_item else None

        # print(f'{juros} e Multa {multa}')

        # Aqui, vamos corrigir a formatação do valor_total que vem com a vírgula
        # valor_total_str = valor_total_str.replace(",", ".")  # Troca vírgula por ponto

        # Converte o valor_total_str para float
        #valor_total = float(valor_total_str)

        # Formatar o valor_total corretamente para exibição em reais
        valor_total_formatado = f"R$ {valor_total_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(valor_total_formatado)

        # Converte os valores para float e formata em reais
        if juros:
            juros_formatado = f"R$ {float(juros):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            juros_formatado = "R$ 0,00"
            
        if multa:
            multa_formatado = f"R$ {float(multa):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            multa_formatado = "R$ 0,00"

        # Atribui valores formatados
        juros = juros_formatado
        multa = multa_formatado
        valor_total = valor_total_formatado

        # Função para converter valores formatados de volta para float
        def converter_para_float(valor):
            return float(valor.replace("R$", "").replace(",", ".").strip())

        # Converte os valores para float
        #valor_total_float = converter_para_float(valor_total)
        juros_float = converter_para_float(juros)
        multa_float = converter_para_float(multa)

        # Cálculo do valor líquido
        varLiquido = valor_total_float - multa_float - juros_float

        # Formatar o valor líquido em reais
        varLiquido_formatado = f"R$ {varLiquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # Exibir os resultados
        print(f"JUROS: {juros}")
        print(f"MULTA: {multa}")
        print(f"VALOR TOTAL: {valor_total}")
        print(f"VALOR LIQUIDO: {varLiquido_formatado}")

        # Definir valor total como o valor líquido formatado
        valor_total = varLiquido_formatado

        # Retornar os valores
        return instalacao, valor_total, numeroNota, dataEmissao, juros, multa, varLiquido_formatado
        # # Acessa os valores dentro das tags específicas -valor_total
        # valor_total_str  = tree.find('.//nf3e:vNF', namespaces=namespaces).text.replace(".", ",")
        # instalacao = tree.find('.//nf3e:idAcesso', namespaces=namespaces).text
        # dataEmissaoXML = tree.find('.//nf3e:dhEmi', namespaces=namespaces).text
        # dataEmissao = datetime.strptime(dataEmissaoXML, '%Y-%m-%dT%H:%M:%S%z').strftime("%d/%m/%Y")
        # inf_nf3e = tree.find('.//nf3e:infNF3e', namespaces=namespaces).get("Id").replace("NF3e", "")
        # numeroNota = inf_nf3e[25:34]

        # # Encontrar os elementos que contêm as informações de JUROS e MULTA
        # juros_item = tree.xpath('//nf3e:det[@nItem="3"]/nf3e:detItem/nf3e:prod/nf3e:vProd', namespaces=namespaces)
        # multa_item = tree.xpath('//nf3e:det[@nItem="4"]/nf3e:detItem/nf3e:prod/nf3e:vProd', namespaces=namespaces)

        # # Verificar se os valores foram encontrados
        # juros = juros_item[0].text if juros_item else None
        # multa = multa_item[0].text if multa_item else None

        # print(f'{juros} e Multa{multa}')
       
        # # Aqui, vamos corrigir a formatação do valor_total que vem com a vírgula
        # valor_total_str = valor_total_str.replace(",", ".")  # Troca vírgula por ponto
        # valor_total = float(valor_total)  # Converte para float

        # # Formatar o valor_total corretamente para exibição em reais
        # valor_total_formatado = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        # #print(f"VALOR TOTAL FORMATADO: {valor_total_formatado}")
     
        # # Converte os valores para float e formata em reais
        # if juros:
        #     juros_formatado = f"R$ {float(juros):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        # else:
        #     juros_formatado = None
        
        # if multa:
        #     multa_formatado = f"R$ {float(multa):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        # else:
        #     multa_formatado = None
        
        # juros =juros_formatado
        # multa = multa_formatado
        # valor_total = valor_total_formatado
        
        # def converter_para_float(valor):
        #     return float(valor.replace("R$", "").replace(",", ".").strip())

        # # Converte os valores para float
        # valor_total_float = converter_para_float(valor_total)
        # juros_float = converter_para_float(juros)
        # multa_float = converter_para_float(multa)

        # # Cálculo do valor líquido
        # varLiquido = valor_total_float - multa_float - juros_float

        # # Formatar o valor líquido em reais
        # varLiquido_formatado = f"R$ {varLiquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # if juros == None:
        #     juros = 0,00
        # if multa == None:
        #     multa = 0,00

        # # Exibir os resultados
        # print(f"JUROS: {juros}")
        # print(f"MULTA: {multa}")
        # print(f"VALOR TOTAL: {valor_total}")
        # print(f"VALOR LIQUIDO: {varLiquido_formatado}")

        # valor_total = varLiquido_formatado

        # return instalacao, valor_total, numeroNota, dataEmissao, juros, multa, varLiquido_formatado
 
    data_string = ' '.join(list_lines)


    instalacao = re.search(r'\b\d{10}\b', data_string).group(0)
    numeroNota = re.search(r"N[°º] (\d{3})\.\d{3}\.\d{3}", data_string).group(0).replace("Nº", "").replace("N°", "").strip()
    dataEmissao = re.search(r"DATA DE EMISSÃO: (\d{2}\/\d{2}\/\d{4})", data_string).group(0).replace("DATA DE EMISSÃO: ", "").strip()
    # pattern = r'R\$ ([^\s]+)'
    # value_match = re.search(pattern, data_string).group(0)
    
    # valor_total = value_match.replace('R$', '')
    # pattern = r'Total:\s*([\d.,]+)'
    # Regex para encontrar o valor total
    pattern = r'TOTAL\D+(\d{1,3}(?:\.\d{3})*(?:,\d{2}))'
    match = re.search(pattern, data_string)

    if match:
        valor_total = match.group(1)
        print(f"Valor total encontrado: {valor_total}")
    else:
        print("Valor total não encontrado.")
    

  
    return instalacao, valor_total, numeroNota, dataEmissao

def extract_data_santa_maria(list_lines, logger):
    juros = 0
    multa = 0
    matricula = None
    valor_total = None
    
    logger.info('Executando extração para fatura Santa Maria.')
    
    for i in range(len(list_lines) - 1):
        try:
            if "IDENTIFICAÇÃO" in list_lines[i]:
                matricula = list_lines[i + 1]
            elif "TOTAL A PAGAR :" in list_lines[i]:
                valor_total = list_lines[i + 1].replace("R$", "").strip()

            numeroNota = None  # Inicializa a variável fora do loop
            dataEmissao = None  # Inicializa a variável para data de emissão

            for line in list_lines:
                if "NF3E nº" in line:
                    numeroNota = line.split('NF3E nº')[1].strip().split(' ')[0]
                if "DATA DE EMISSÃO" in line:
                    dataEmissao = line.split('DATA DE EMISSÃO :')[1].strip()
                if numeroNota and dataEmissao:
                    break

            print(f"NF3E Número: {numeroNota}")  # Imprime o número da NF3E encontrado
            print(f"Data de Emissão: {dataEmissao}")
        except Exception as e:
            logger.error(f'  :::Erro ao extrair dados da Fatura Santa Maria {e}')
            
    logger.info(f'Retornado para Santa Maria > Matrícula {matricula} | Valor Total {valor_total}')
            
    return matricula, valor_total,numeroNota, dataEmissao, multa, juros

def extract_data_saae_linhares(list_lines, logger):
    matricula = None
    valor_total = None
    numeroNota = None
    dataEmissao = None
    numero_guia =None
    
    logger.info('Executando extração para fatura SAAE.')
    logger.info(f'Retorno da lista: {list_lines}.')

    # Regex para capturar matrícula
    matricula_regex = r'CÓD\. LIGAÇÃO:\s*(\d{4}-\d)' 

    # Regex para capturar valor total (R$ ou ¤ seguido de valores decimais)
    valor_total_regex = r"[¤R$\u20AC£¥]\s?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)"

    # Regex para capturar número da nota (NR. GUIA)
    #numero_nota_regex = r"NR\. GUIA:\s*(\d+)"

    # Regex para capturar a data de competência
    data_competencia_regex = r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"


    for i in range(len(list_lines) - 1):
        try:
            # Procurar por matrícula utilizando regex
            if "LIGAÇÃO:" in list_lines[i]:
                match_matricula = re.search(matricula_regex, list_lines[i])
                if match_matricula:
                    matricula = match_matricula.group(1)  # Captura a matrícula

            # Procurar por valor total utilizando regex
            elif "VALOR A PAGAR" in list_lines[i]:
                match_valor = re.search(valor_total_regex, list_lines[i + 1].strip())
                if match_valor:
                    valor_total = match_valor.group(1)  # Captura o valor total
             # Procurar pelo número da nota ("GUIA:")
             # Procurar pelo número da nota ("MÊS/ANO:")

            # elif "MÊS/ANO:" in list_lines[i]:
            #     numeroNota = list_lines[i + 1]
                # match_numero_nota = re.search(numero_nota_regex, list_lines[i + 1].strip())
                # if match_numero_nota:
                #     numeroNota = match_numero_nota.group(1)  # Captura o número da nota

            elif "DATA LEITURA ATUAL" in list_lines[i]:
                dataEmissao = list_lines[i + 1]
            
            elif "NR. GUIA:" in list_lines[i]:
                numero_guia = list_lines[i + 1]

                        # Procurar pela data de competência
            if i == 5:  # Linha 005 (a partir de 0, ou seja, 6ª linha)
                match_data_competencia = re.search(data_competencia_regex, list_lines[i])
                if match_data_competencia:
                    dataEmissao = match_data_competencia.group(1)  # Captura a data de competência
                
        except Exception as e:
            logger.error(f'Erro ao extrair dados da Fatura SAAE: {e}')

    logger.info(f'Retornado para SAAE > Matrícula: {matricula} | Valor Total: {valor_total} | NR. GUIA: {numero_guia} | dataEmissao: {dataEmissao}')
    #print(f'Retornado para SAAE > Matrícula: {matricula} | Valor Total: {valor_total}')
    # dataEmissao,numero_guia
    return matricula, valor_total, None,None

def extract_data_saae_aracruz(list_lines, logger):
    matricula = None
    valor_total = None
    
    logger.info('Executando extração para fatura SAAE.')
    # logger.info(f'retorno da lista {list_lines}.')
    
    
    for i in range(len(list_lines) - 1):
        try:
            # LIGAÇÃO:
            if "Ligação" in list_lines[i]:
                matricula = list_lines[i + 1]
                # VALOR A PAGAR
            elif "Valor Total da Fatura:" in list_lines[i]:
                valor_total = list_lines[i + 1].strip()
        except Exception as e:
            logger.error(f'  :::Erro ao extrair dados da Fatura SAAE {e}')
            
    logger.info(f'Retornado para SAAE > Matrícula {matricula} | Valor Total {valor_total}')
    print(f'Retornado para SAAE > Matrícula {matricula} | Valor Total {valor_total}')
    
    return matricula, valor_total, None, None

def extract_data_sao_mateus(list_lines, logger):
    # juros = 0
    # multa = 0
    matricula = None
    valor_total = None
    
    logger.info('Executando extração para fatura SAAE.')
    
    
    for i in range(len(list_lines) - 1):
        try:
            if "Código do Cliente" in list_lines[i]:
                matricula = list_lines[i + 1]
            elif "Valor Total da Fatura:" in list_lines[i]:
                valor_total = list_lines[i + 1].strip()
            # elif "Código do Cliente" in list_lines[i]:
            #     numeroNota = list_lines[i + 1]
            # elif "DATA EMISSÃO" in list_lines[i]:
                # dataEmissao = list_lines[i + 1]
            # for line in list_lines:
            dataEmissao = None  # Inicializa a variável fora do loop

            for line in list_lines:
                if "Emitida em" in line:
                    dataEmissao = line.split('Emitida em')[1].strip().split(',')[0]
                    break

            print(dataEmissao)
            numeroNota = None  # Inicializa a variável fora do loop

            for line in list_lines:
                if "Nº da fatura:" in line:
                    numeroNota = line.split('Nº da fatura:')[1].strip()
                    break

            print(numeroNota) 



        except Exception as e:
            logger.error(f'  :::Erro ao extrair dados da Fatura SAAE {e}')
            
    logger.info(f'Retornado para SAAE > Matrícula {matricula} | Valor Total {valor_total}')
    
    return matricula, valor_total, numeroNota, dataEmissao

def extract_data_brk(list_lines, logger):    
    matricula = None
    valor_total = None
    numeroNota = None
    dataEmissao = None
    juros =0
    multa =0
    
    logger.info('Executando extração para fatura BRK.')
    
    for i in range(len(list_lines) - 1):
        try:
            if "CDC" in list_lines[i]:
                matricula = list_lines[i + 1]
            elif "VALOR TOTAL - R$" in list_lines[i]:
                valor_total = list_lines[i + 1].strip()
            elif "N° DA CONTA" in list_lines[i]:
                numeroNota = list_lines[i + 1]
            elif "DATA EMISSÃO" in list_lines[i]:
                dataEmissao = list_lines[i + 1]



        except Exception as e:
            logger.error(f'  :::Erro ao extrair dados da Fatura BRK {e}')
            
    logger.info(f'Retornado para BRK > Matrícula {matricula} | Valor Total {valor_total}')
    
    return matricula, valor_total, numeroNota, dataEmissao, juros, multa

def extract_data_sanear(list_lines, logger):

    return None, None, None, None
    

def generate_extract_data(lines, instalacao, logger, xmlPath = ""):   
    try:
        #Trocar None para numero da Nota/Data emissao quando for mapeado

        if any('cesan' in line.lower() for line in lines):
            return extract_data_cesan(lines, logger)
        if lines == "EDP_XML":
            return extract_data_edp(lines, logger, xmlPath)
        if  any('EDP' in line for line in lines):
            return extract_data_edp(lines, logger)
        if any('Empresa Luz e Força Santa Maria S/A' in line for line in lines):
            return extract_data_santa_maria(lines, logger)
        if any('SAAE - LINHARES' in line for line in lines):
            return extract_data_saae_linhares(lines, logger)
        if any('Website: saaeara.es.gov.br' in line for line in lines):
            return extract_data_saae_aracruz(lines, logger)
        if any('Website: www.saaesma.com.br' in line for line in lines):
            return extract_data_sao_mateus(lines, logger)        
        if any('BRK' in line for line in lines):
           return extract_data_brk(lines, logger)
        if any('SERVICO COL. DE SANEAMENTO AMBIENTAL' in line for line in lines):
            return extract_data_sanear(lines, logger)

    except Exception as e:
        logger.error(f'erro {e}')
    
    return None, None, None, None
      

def filtered_extracted_data(logger):
    
    fsl = LocalFileSystem()
    df = read_excel_dealerships(os.getenv('PATH_FILE_XLSX'))  
    files = fsl.glob(f'{os.getenv("PATH_GENERAL_FILES_PDF")}/*.pdf')
    filesXml = fsl.glob(f'{os.getenv("PATH_GENERAL_FILES_PDF")}/*.xml')
    files.extend(filesXml)

    files = [file for file in files if "NEX" not in file]
    juros =0
    multa = 0
    varLiquido_formatado = 0
    
    if len(files) == 0:
        logger.info('Sem arquivos PDF para ser processados.')

        return juros, multa, df
        
    for file in files:
        logger.info(f'Começando a extrair dados de arquivo: {Path(file).stem}')

        if not file.endswith(".xml"):
            text_extract_the_in_pdf, instalacao = extract_text_from_pdf(file, logger) 

        else:
            text_extract_the_in_pdf = "EDP_XML"
            instalacao = "EDP_XML"
        
        
        if text_extract_the_in_pdf != None:
            
            if text_extract_the_in_pdf == "EDP_XML": 
                registration, value_total, numeroNota, dataEmissao, juros, multa, varLiquido_formatado= generate_extract_data(text_extract_the_in_pdf, instalacao, logger, file)
                if juros is not None:
                    print(f'Conta contem Juros{juros}')
                if multa is not None:
                    print(f'Conta contem Multa{multa}')
                if varLiquido_formatado is not None:
                    print(f'Valor liquido{varLiquido_formatado}')
                #return juros, multa

            else:
                registration, value_total, numeroNota, dataEmissao, juros, multa = generate_extract_data(text_extract_the_in_pdf, instalacao, logger)
            
            logger.info(f'''
                  
                  >>> Matrícula|Instalação: {registration} 
                  
                  >>> Valor Total: {value_total}
                  
                  ''')
            
            if (registration, value_total, numeroNota, dataEmissao) == (None, None, None, None):
                logger.warning(f'Retornou None. Por favor, verificar. Arquivo {file}')
                return
            
            # Verificar se CNPJ e valor foram encontrados
            if registration and value_total:
                print(registration)
                # Remove os zeros à esquerda, mas preserva o hífen
                registration = re.sub(r"^0+(?=\d)", "", registration)
                # Procurar o CNPJ no DataFrame e filtrar pela linha correspondente
                linha_filtrada = df[df["INSTALAÇÃO/MATRÍCULA"] == registration]

                # Inserir o valor total na linha filtrada
                if not linha_filtrada.empty:
                    df.loc[linha_filtrada.index, "VALOR TOTAL"] = value_total

                    if text_extract_the_in_pdf == "EDP_XML":
                        splitedFile = file.split("/")
                        fileName = splitedFile[-1]
                        newFileName = "NEX" + fileName.replace("xml", "pdf")
                        newSplitedFile = splitedFile[:-1] + [newFileName]
                        newPath = os.path.join(*newSplitedFile)
                        newPath = newPath.replace("C:", "C:\\")

                        df.loc[linha_filtrada.index, "PATH_FILE"] = newPath
                    else:
                        df.loc[linha_filtrada.index, "PATH_FILE"] = file

                    if numeroNota == None or dataEmissao == None:
                        df.loc[linha_filtrada.index, "NUMERO NOTA"] = "0"
                        df.loc[linha_filtrada.index, "DATA EMISSAO"] = datetime.now().strftime('%d/%m/%Y')
                    else:
                        df.loc[linha_filtrada.index, "NUMERO NOTA"] = numeroNota.replace(".", "")
                        df.loc[linha_filtrada.index, "DATA EMISSAO"] = dataEmissao   
    
    
    if 'VALOR TOTAL' in df.columns:
        import numpy as np
        df.replace("nan", np.nan, inplace=True)
        df_filtrado = df[df["VALOR TOTAL"].notnull()]

    else:
        return
        
    
    return df_filtrado, juros, multa

class PDFUtilities:
    def extract_text_from_pdf_utilities(self, file_path, logger):

        instalacao = None
        
        try:
            output_string = StringIO()
            with open(file_path, 'rb') as in_file:
                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                rsrcmgr = PDFResourceManager()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)

            lines = output_string.getvalue().split('\n')
            
            new_list_lines = list(filter(lambda item: item.strip() != "", lines))
            
            return new_list_lines, instalacao
        except PDFPasswordIncorrect as e:

            dict_passcnpj_instalacao = {
                
                '0000151086': '03810',
                '0000150260': '03810',
                '0000151087': '03810',
                '0000151939': '03810',
                '0160675179': '03810',
                '0160833913': '03810',
                '0000152278': '03810',
                '0160105645': '28151',
                '0000580129': '03810',
                '0000693854': '03810',
                '0160105634': '03810',
                '0160105636': '03810',
                '0160105637': '03810',
                '0160169810': '03810',
                '0160835222': '03810',
                '0160700520': '03810',
                '0160105642': '03810',
                '0160105630': '03810',
                '0160105625': '03810',
                '0160105620': '03810',
                '0000150330': '28483',
                '0000150112': '03810',
                '0160828231': '28151',
                '0000150112': '03810',
                '0000150630': '03810',
                '0000150743': '03810',
                '0000151087': '03810',
                '0160663084': '03810',
                '0161017641': '03810',
                '0000150489': '03810',
                '0160929836': '03810',
                '0001959730': '03810'
            }
            
            filename = Path(file_path).stem
            
            logger.info(f'Processando PDF que possui senha {filename}')
            try:
                instalacao = filename.split('_')[2]
                fileNameError = False
            except:
                fileNameError = True
            
            if fileNameError:
                possiblePasswords = ["28151", "03810", "28483"]
                for password in possiblePasswords:
                        try:
                            list_line = convert_pdf_to_text(file_path, password)
                            for item in list_line:
                                if "INSTALAÇÃO" in item:
                                    instalacao = item.replace("INSTALAÇÃO: ", "").strip()
                                    return list_line, instalacao
                        except:
                            continue
                

            for key, value in dict_passcnpj_instalacao.items():
                if key == instalacao:
                    list_line = convert_pdf_to_text(file_path, value)
                    
                    return list_line, instalacao
    

    def extract_data_brk_utilites(self, list_lines, logger):            
        logger.info('Executando extração para fatura BRK.')
        
        for i in range(len(list_lines) - 1):
            try:
                if "CDC" in list_lines[i]:
                    matricula = list_lines[i + 1]
                elif "VALOR TOTAL - R$" in list_lines[i]:
                    valor_total = list_lines[i + 1].strip()
                elif "REFERÊNCIA" in list_lines[i]:
                    referencia = list_lines[i + 1]
                    


            except Exception as e:
                logger.error(f'  :::Erro ao extrair dados da Fatura BRK {e}')
                
        logger.info(f'Retornado para BRK > Matrícula {matricula} | Valor Total {valor_total}')
        
        return matricula, referencia
    
    def extract_data_saae_linhares(self, list_lines, logger):
        # Aqui o método recebe dois parâmetros: list_lines e logger
        matricula = None
        dataEmissao = None
        numero_guia = None

        logger.info('Executando extração para fatura SAAE.')
        logger.info(f'Retorno da lista: {list_lines}.')

        # Regex para capturar matrícula
        matricula_regex = r'CÓD\. LIGAÇÃO:\s*(\d{4}-\d)'

        # Regex para capturar a data de competência
        data_competencia_regex = r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"

        for i in range(len(list_lines) - 1):
            try:
                # Procurar por matrícula utilizando regex
                if "LIGAÇÃO:" in list_lines[i]:
                    match_matricula = re.search(matricula_regex, list_lines[i])
                    if match_matricula:
                        matricula = match_matricula.group(1)  # Captura a matrícula

                # Procurar pela data de emissão
                elif "DATA LEITURA ATUAL" in list_lines[i]:
                    dataEmissao = list_lines[i + 1]
                
                elif "NR. GUIA:" in list_lines[i]:
                    numero_guia = list_lines[i + 1]

                # Procurar pela data de competência
                if i == 5:  # Linha 005 (a partir de 0, ou seja, 6ª linha)
                    match_data_competencia = re.search(data_competencia_regex, list_lines[i])
                    if match_data_competencia:
                        dataEmissao = match_data_competencia.group(1)  # Captura a data de competência
                    
            except Exception as e:
                logger.error(f'Erro ao extrair dados da Fatura SAAE: {e}')

        return matricula, dataEmissao, numero_guia