"""
Implementação de Captura de PDFs anexado ao E-mail usando a API do Microsoft Graph.
Ess alternativa foi usada, para poder acessar o E-mail via Outlook Web.

"""
from dotenv import load_dotenv
import datetime
from time import sleep
from convert_pdf_to_txt.pdf_txt import PDFUtilities

import os
import requests
import re
import config



from email import policy
from email.parser import BytesParser
import quopri
import chardet

from rpa_fluig import EDPLINK
from slack_monitoring.slack_notifier import SlackNotifier

import hashlib
import os

# Adicionando a função para gerar o hash com salt
def gerar_hash_com_salt(input_string):
    salt = os.urandom(16)  # Gerando um salt único (16 bytes aleatórios)
    input_string_with_salt = input_string.encode() + salt  # Concatenando a string com o salt
    hash_with_salt = hashlib.sha256(input_string_with_salt).hexdigest()  # Gerando o hash
    return hash_with_salt


load_dotenv()

class EmailManager:
    def __init__(self, access_token, api_endpoint):
        self.GRAPH_API_ENDPOINT = api_endpoint
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }
    


    def download_attachments(self, message_id, save_folder, logger, slack, edp = False, brk = False, varNameConc =False):
        try:
            response = requests.get(
                f"{self.GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments",
                headers=self.headers
            )
            

            attachment_items = response.json()['value']
            for attachment in attachment_items:
                if edp:
                    
                    file_name = attachment['name']
                    attachment_id = attachment['id']
                    attachment_content = requests.get(
                        f"{self.GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments/{attachment_id}/$value", headers=self.headers
                    )
                    
                    logger.info(f'Salvando arquivo: {file_name}...')

                    if str(attachment['name']).endswith('pdf'):
                        file_name = "EDP_TEMPPDF.pdf"

                    with open(os.path.join(save_folder, file_name), 'wb') as _f:
                        _f.write(attachment_content.content)
                    
                    if str(attachment['name']).endswith('xml'):
                        newFileName = f"NEX{file_name.replace('xml', 'pdf')}"
                        fullFilePath = os.path.join(save_folder, newFileName)

                        os.rename(os.path.join(save_folder, "EDP_TEMPPDF.pdf"), fullFilePath)
                    continue
                

                if brk:
                    if str(attachment['name']).endswith('pdf'):
                        file_name = attachment['name']
                        attachment_id = attachment['id']
                        attachment_content = requests.get(
                            f"{self.GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments/{attachment_id}/$value", headers=self.headers
                        )
                        
                        sleep(1)
                        logger.info(f'Salvando arquivo: {file_name}...')
                        with open(os.path.join(save_folder, file_name), 'wb') as _f:
                            _f.write(attachment_content.content)
                        
                        pdf = PDFUtilities()
                        pdfText = pdf.extract_text_from_pdf_utilities(os.path.join(save_folder, file_name), logger)
                        matricula, referencia = pdf.extract_data_brk_utilites(pdfText[0], logger)

                        referencia = referencia.replace("/", ".")
                        
                        os.rename(f"{save_folder}/{file_name}", f"{save_folder}/{matricula} - {referencia}.pdf")
                        continue
                
                if varNameConc:
                    if str(attachment['name']).endswith('pdf'):
                        file_name = attachment['name']
                        attachment_id = attachment['id']
                        attachment_content = requests.get(
                            f"{self.GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments/{attachment_id}/$value", headers=self.headers
                        )
                        
                        sleep(1)
                        logger.info(f'Salvando arquivo: {file_name}...')
                        varRemove = file_name

                        #TESTANDO LINHA 104
                        with open(os.path.join(save_folder, file_name), 'wb') as _f:
                            _f.write(attachment_content.content)
                        
                        # Instanciando a classe PDFUtilities
                        pdf = PDFUtilities()

                        # Extraindo o texto do PDF
                        pdfText = pdf.extract_text_from_pdf_utilities(os.path.join(save_folder, file_name), logger)

                        # Extraindo os dados do PDF
                        matricula, dataEmissao, numero_guia = pdf.extract_data_saae_linhares(pdfText[0], logger)
                        print(dataEmissao)
                        varDataemissao = dataEmissao

                        dataEmissao = dataEmissao.replace("/", ".")

                        # Verificando se os dados necessários foram extraídos corretamente
                        if matricula and dataEmissao and numero_guia:
                            file_name = f"{matricula}-{numero_guia}-{dataEmissao}.pdf"

                            #Salvar o arquivo 
                            with open(os.path.join(save_folder, file_name), 'wb') as _f:
                                _f.write(attachment_content.content)
                            # Renomeando o arquivo com os dados extraídos
                            os.rename(
                                os.path.join(save_folder, file_name),
                                os.path.join(save_folder, f"{matricula}-{numero_guia}-{dataEmissao}.pdf")
                            )
                            file_name = f"{matricula}-{numero_guia}-{dataEmissao}.pdf"
                            # Remove o arquivo após salvá-lo
                            
                            os.remove(os.path.join(save_folder, varRemove))
                            dataEmissao = varDataemissao
                            print(f'Data atualizada {dataEmissao}')


                            continue
                        else:
                            logger.error("Erro: Dados faltando para renomear o arquivo.")


                if str(attachment['name']).endswith('pdf'):
                    file_name = attachment['name']
                    attachment_id = attachment['id']
                    attachment_content = requests.get(
                        f"{self.GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments/{attachment_id}/$value", headers=self.headers
                    )

                    sleep(1)
                    
                    logger.info(f'Salvando arquivo: {file_name}...')
                    with open(os.path.join(save_folder, file_name), 'wb') as _f:
                        _f.write(attachment_content.content)
                                       
                    # pdf = PDFUtilities()
                    # pdfText = pdf.extract_text_from_pdf_utilities(os.path.join(save_folder, file_name), logger)
                    #matricula, dataEmissao = pdf.extract_data_saae_linhares(pdfText[0], logger)

                    # # Gerar o timestamp para renomear o arquivo
                    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                    
                    # # Criar um novo nome de arquivo com timestamp
                    # new_file_name = f"{file_name} - {timestamp}.pdf"
                    
                    # # Renomear o arquivo para incluir o timestamp
                    # os.rename(os.path.join(save_folder, file_name), os.path.join(save_folder, new_file_name))

                    # logger.info(f"Arquivo renomeado para: {new_file_name}")
                    # file_name = new_file_name
                    # try:
                    #     if str(attachment['name']).startswith('Fatura'):
                    #         file_name = f"documento_{matricula}_{referencia}.pdf"  # Nome único com data e hora
                    # except:
                    #     print("Erro ao Renomear faturar")
                    #     continue
                    
                    # logger.info(f'Salvando arquivo: {file_name}...')
                    # with open(os.path.join(save_folder, file_name), 'wb') as _f:
                    #     _f.write(attachment_content.content)
                    
                    # logger.info(f'Salvando arquivo: {file_name}...')
                    # with open(os.path.join(save_folder, file_name), 'wb') as _f:
                    #     _f.write(attachment_content.content)


                        
            return True
        except Exception as e:
            slack.post_message(f'Erro ao realizar download de arquivo {e}')
            return False

    def mark_as_read(self, message_id, logger):
        try:
            update_data = {
                "isRead": True
            }
            response = requests.patch(
                f"{self.GRAPH_API_ENDPOINT}/me/messages/{message_id}",
                headers=self.headers,
                json=update_data
            )
            response.raise_for_status()
            logger.info(f"Email marcado como lido.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to mark email {message_id} as read:", e)
            return False
    
    def get_invoice_pdf(self, email, keyword, type_invoice, email_id, path_download_pdfs, logger, slack,varNameConc):
        subject = email['subject']
        if keyword in subject:
            logger.info(f'ENCONTRADO FATURA PARA: {type_invoice}')
            if "EDP" in subject:
                    return self.download_attachments(
                    email_id,
                    path_download_pdfs, logger, slack, edp=True
                    )
            
            if "BRK" in subject:
                return self.download_attachments(
                    email_id,
                    path_download_pdfs, logger, slack, brk=True
                    )
            if varNameConc in subject:
                
                return self.download_attachments(
                    email_id,
                    path_download_pdfs, logger, slack, varNameConc=True
                    )

            else:
                return self.download_attachments(
                    email_id,
                    path_download_pdfs, logger, slack
                    )


def main_process_download_attachments(access_token, logger, slack):
    
    api_endpoint = os.getenv('GRAPH_API_ENDPOIN')
    path_download_pdfs = os.getenv('PATH_DOWNLOADED_INVOICES_PDF')
    
    email_manager = EmailManager(access_token, api_endpoint)
    

    params = {
        'top': 25,
        'select': 'subject,hasAttachments',
        'filter': 'hasAttachments eq true and isRead eq false',
        'count': 'true'

    }

    response = requests.get(
        f"{email_manager.GRAPH_API_ENDPOINT}/me/mailFolders/inbox/messages",
        headers=email_manager.headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(response.json())

    response_json = response.json()
    emails = response_json['value']
    
    if len(emails) == 0:
        logger.info('Não existe faturas para ser baixadas.')

    for email in emails:
        if email['hasAttachments']:
            email_id = email['id']
            varNameConc = 'Fatura digital - SAAE - LINHARES'
            
            subject_invoices = [
                 ("Agência Virtual - Remanejamento de Fatura Virtual", "CESAN"),
                ("Agência Virtual Cesan - Remanejamento de Fatura", "CESAN-ATUALIZADO"),
                ("CESAN ", "CESAN-ATUALIZADO 2"),
                ("Fatura Mensal EDP", "EDP"),
                ("EDP", "EDP"),
                ("SANTA MARIA", "Santa Maria"),
                ("Envio da Conta de Energia", "ELFSM"),
                ("Minha BRK - Fatura Digital", "BRK"),
                ("Fatura de água e esgoto", "SAAE"),
                ("Fatura digital - SAAE", "LINHARES"),
                ("Fatura digital - SAAE", varNameConc)
            ] 
            for subject_keyword, invoice_type in subject_invoices:
                           
                email_manager.get_invoice_pdf(email, subject_keyword, invoice_type, email_id, path_download_pdfs, logger, slack,varNameConc)

            email_manager.mark_as_read(email_id, logger)

    return emails


#FUNÇÃO DE TESTE

# def extract_edp_link_from_email(email_body):
#     """
#     Extrai o link do corpo do e-mail que contém a frase "Basta clicar neste link".
#     """
#     # Expressão regular para encontrar o link
#     link_pattern = r'Basta clicar neste link\s*<a[^>]*href="([^"]+)"'
#     match = re.search(link_pattern, email_body)
    
#     if match:
#         return match.group(1)  # Retorna o link encontrado
#     return None




def extract_edp_link_from_email(email_body):
    """
    Extrai o link do corpo do e-mail que contém a frase "Basta clicar neste link".
    """
    # Expressão regular para encontrar o link
    link_pattern = r'Basta clicar neste link\s*<a[^>]*href="([^"]+)"'
    match = re.search(link_pattern, email_body, re.IGNORECASE)
    
    if match:
        return match.group(1)  # Retorna o link encontrado
    return None

def download_email_as_eml(email_id, access_token, path_download_eml, logger):
    """
    Baixa o e-mail no formato .eml e salva no diretório especificado.
    """
    api_endpoint = os.getenv('GRAPH_API_ENDPOINT', 'https://graph.microsoft.com/v1.0')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Faz a requisição para baixar o e-mail no formato .eml
    response = requests.get(
        f"{api_endpoint}/me/messages/{email_id}/$value",
        headers=headers,
        stream=True
    )

    if response.status_code != 200:
        logger.error(f"Erro ao baixar o e-mail {email_id}: {response.status_code}")
        return False

    # Salva o e-mail no formato .eml
    eml_filename = os.path.join(path_download_eml, f"EDP - FATURAS_Link.eml")
    with open(eml_filename, 'wb') as eml_file:
        for chunk in response.iter_content(chunk_size=8192):
            eml_file.write(chunk)

    logger.info(f"E-mail baixado e salvo como: {eml_filename}")
    # Extrai o link do arquivo .eml
    link_extraido = extract_link_from_eml(eml_filename)

    if link_extraido:
        print(f"Link extraído: {link_extraido}")

        # Cria uma instância da classe EDPLINK
        edp_link = EDPLINK(logger, SlackNotifier)

        edp_link.start_browser1()

        # Abre o link extraído no navegador
        edp_link.open_extracted_link(link_extraido)
        # Executa a função para clicar no checkbox e no botão de download
        edp_link.downloadEDP_contaslink()
        

        # Atualiza a variável global var_edp_link
        config.var_edp_link = True

        
        
    else:
        print("Nenhum link encontrado no arquivo .eml.")
        # Atualiza a variável global var_edp_link
        config.var_edp_link = False

        # main_process_download_attachments(email_id, access_token, path_download_eml, logger)

    return True, link_extraido,config.var_edp_link

def process_edp_emails(access_token, logger, path_download_eml):
    api_endpoint = os.getenv('GRAPH_API_ENDPOIN')
    email_manager = EmailManager(access_token,api_endpoint)

    """
    Busca e-mails não lidos com o assunto 'EDP - FATURAS' e baixa o e-mail no formato .eml.
    """
    api_endpoint = os.getenv('GRAPH_API_ENDPOINT', 'https://graph.microsoft.com/v1.0')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Parâmetros para buscar e-mails não lidos com o assunto específico
    params = {
        'top': 25,
        'select': 'subject,body',
        'filter': "isRead eq false and subject eq 'EDP - FATURAS'",
        'count': 'true'
    }

    # Faz a requisição para buscar os e-mails
    response = requests.get(
        f"{api_endpoint}/me/mailFolders/inbox/messages",
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(response.json())

    response_json = response.json()
    emails = response_json['value']
    
    if len(emails) == 0:
        logger.info('Não existem e-mails não lidos com o assunto "EDP - FATURAS".')
        return []

    # Processa cada e-mail encontrado
    for email in emails:
        email_id = email['id']
        email_body = email['body']['content']  # Corpo do e-mail

        # Extrai o link do corpo do e-mail
        link_edp = extract_edp_link_from_email(email_body)
        
        if link_edp:
            logger.info(f"Link EDP encontrado: {link_edp}")
            # Baixa o e-mail no formato .eml
            download_email_as_eml(email_id, access_token, path_download_eml, logger)
        else:
            logger.info("Nenhum link encontrado no e-mail da EDP.")
            download_email_as_eml(email_id, access_token, path_download_eml, logger)

    email_manager.mark_as_read(email_id, logger)


    return emails





def decode_quoted_printable(text):
    """
    Decodifica texto codificado em quoted-printable.
    """
    return quopri.decodestring(text).decode('utf-8', errors='ignore')

def detect_encoding(content):
    """
    Detecta a codificação do conteúdo usando a biblioteca chardet.
    """
    result = chardet.detect(content)
    return result.get('encoding', 'utf-8')

def extract_link_from_eml(eml_file_path):
    """
    Lê o arquivo .eml, detecta a codificação, decodifica o conteúdo e extrai o link desejado.
    """
    try:
        # Abre o arquivo .eml e lê o conteúdo em modo binário
        with open(eml_file_path, 'rb') as file:
            raw_content = file.read()

        # Detecta a codificação do conteúdo
        encoding = detect_encoding(raw_content)

        # Decodifica o conteúdo para texto usando a codificação detectada
        decoded_content = raw_content.decode(encoding, errors='ignore')

        # Decodifica o conteúdo quoted-printable
        decoded_body = decode_quoted_printable(decoded_content)

        # Expressão regular para encontrar o link específico
        link_pattern = r'https://contasporemail\.edpbr\.com\.br/webcontasEdp/acessoDocsEdp\?i=\d{8}-\d{8}-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}'
        match = re.search(link_pattern, decoded_body)

        if match:
            return match.group(0)  # Retorna o link encontrado
        else:
            return None  # Retorna None se nenhum link for encontrado

    except Exception as e:
        print(f"Erro ao processar o arquivo .eml: {e}")
        return None

