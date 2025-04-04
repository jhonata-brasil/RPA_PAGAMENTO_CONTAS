import win32com.client as win32
import os

from dotenv import load_dotenv

load_dotenv()

def instance_microsoft_outlook(logger):
 
    """
    Função responsável por criar instÂncia da aplicação Microsoft Outlook. 
    Representa o Namespace do sistema de mensagens do Outlook.
    
    Returns:
        win32com.gen_py.Namespace: Um objeto COM que permite acessar pastas e itens de e-mail no Outlook.
    """
    try:
        outlook = win32.Dispatch('outlook.application')
        namespace = outlook.GetNamespace('MAPI')
        
        return namespace
    except Exception as e:
        logger.error(f'  :::Erro ao se conectar com o Microsoft Outlook {e}')

def get_account_shared(logger):
    
    """
    Função responsável por retornar caixa de entrada de Concessionárias.

    Returns:
        shared_acconut.Folders: Um objeto que permite acessar a pasta Caixa de Entrada de Concessionárias
    """
    try:
        namespace = instance_microsoft_outlook(logger)
        
        shared_acconut = namespace.Folders('Concessionárias')

        inbox = shared_acconut.Folders('Caixa de Entrada')
        
        return inbox
    except Exception as e:
        logger.error(f'  :::Erro ao retornar pasta de caixa de entrada {e}')

def download_invoice(email: str, logger):
    """
    Função responsável por verificar se o email existe anexo, caso o email tenha anexo, o processo irá salvar o PDF em um caminho passado em .env

    Args:
        email (str): Email 
    """
    if email.Attachments.Count > 0:
        for anexo in email.Attachments:
            try:
                if str(anexo).endswith('pdf'):
                    logger.info(f'Baixando arquivo pdf... {anexo}')
                    anexo.SaveAsFile(os.getenv('PATH_DOWNLOADED_INVOICES_PDF') + '\\' + anexo.Filename)
                    logger.info(f'Arquivo PDF baixado: {anexo.Filename}')
            except Exception as e:
                logger.error(f'  :::Erro ao baixar arquivo. {e}')

    
def get_invoice_pdf(email: str, keyword: str, type_invoice: str, logger):
    """
    Função responsável por realizar o download das faturas.  

    Args:
        email (str): email
        keyword (str): descrição do assunto
        type_invoice (str): tipo da fatura
    """
    subject = email.Subject
    if keyword in subject:
        logger.info(f'ENCONTRADO FATURA PARA: {type_invoice}')
        download_invoice(email, logger)

                
def extract_pdf_from_email(logger) -> None:
    """
    Função responsável por realizar a captura de PDFs em email.
    
    """
    
    subject_invoices = [
        ("Agência Virtual - Remanejamento de Fatura Virtual", "CESAN"),
        ("Fatura Mensal EDP", "EDP"),
        ("Envio da Conta de Energia", "ELFSM"),
        ("Fatura de água e esgoto", "SAAE"),
        ("Fatura digital - SAAE - LINHARES,SAAE")
    
    ]    

    inbox = get_account_shared(logger)

    unread_emails = [email for email in inbox.Items if email.UnRead]
    
    if len(unread_emails) == 0:
        logger.info('Não existe faturas para ser baixadas.')

    for email in unread_emails:
        for subject_keyword, invoice_type in subject_invoices:
            get_invoice_pdf(email, subject_keyword, invoice_type, logger)