from O365 import Account, FileSystemTokenBackend
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

import os

load_dotenv()

def generate_token(slack):
    try:
        CREDENTIALS = (os.getenv('ID_CLIENT'), os.getenv('SECRET_TD'))

        token_backend = FileSystemTokenBackend(token_path=os.getenv('LOCAL_TOKEN_PATH'), token_filename=os.getenv('TOKEN_FILENAME'))
        account = Account(CREDENTIALS, token_backend=token_backend)

        if not account.is_authenticated:
            account.authenticate(scopes=['basic', 'calendar_all', 'onedrive_all', 'message_all'])

        expires_at = account.connection.token_backend.get_token()['expires_at']

        expires_at = datetime.fromtimestamp(expires_at)

        if expires_at - timedelta(minutes=5) <= datetime.now():
            # slack.post_message('O Token de acesso está perto de expirar! Gerando novo Token.')
            account.connection.refresh_token()
            # time.sleep(10)
            # slack.post_message('Token renovado :)!')
        else:
            # slack.post_message('O Token de acesso ao email ainda é válido...')
            print("O Token de acesso ao email ainda é válido..")
            
        token_acess = account.connection.token_backend.get_token()['access_token']
        
        return token_acess
    except Exception as e:
        # slack.post_message(f'Erro na geração de Token de acesso {e}')
        print(f"Erro na geração de Token de acesso {e}")



# from O365 import Account, FileSystemTokenBackend
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import time
# import os

# load_dotenv()

# def generate_token(slack):
#     try:
#         # Verifique se as credenciais estão sendo carregadas corretamente
#         client_id = os.getenv('ID_CLIENT')
#         client_secret = os.getenv('SECRET_TD')
#         token_path = os.getenv('LOCAL_TOKEN_PATH')
#         token_filename = os.getenv('TOKEN_FILENAME')

#         if not client_id or not client_secret or not token_path or not token_filename:
#             raise ValueError("Uma ou mais variáveis de ambiente estão ausentes.")

#         print(f"ID_CLIENT: {client_id}, SECRET_TD: {client_secret}, LOCAL_TOKEN_PATH: {token_path}, TOKEN_FILENAME: {token_filename}")

#         CREDENTIALS = (client_id, client_secret)

#         # Defina o backend para armazenamento do token
#         token_backend = FileSystemTokenBackend(token_path=token_path, token_filename=token_filename)
#         account = Account(CREDENTIALS, token_backend=token_backend)

#         if not account.is_authenticated:
#             print("Autenticando o usuário...")
#             account.authenticate(scopes=['basic', 'calendar_all', 'onedrive_all', 'message_all'])

#         # Obter a data de expiração do token
#         expires_at = account.connection.token_backend.get_token()['expires_at']
#         expires_at = datetime.fromtimestamp(expires_at)

#         # Verificar se o token está prestes a expirar
#         if expires_at - timedelta(minutes=5) <= datetime.utcnow():
#             print("Token perto de expirar, renovando...")
#             account.connection.refresh_token()
#             time.sleep(10)
#             # slack.post_message('Token renovado :)!')
#         else:
#             slack.post_message('O Token de acesso ao email ainda é válido...')

#         # Obter o token de acesso
#         token_acess = account.connection.token_backend.get_token()['access_token']
#         return token_acess

#     except Exception as e:
#         print(f"Erro na geração de Token de acesso: {e}")
#         import traceback
#         traceback.print_exc()  # Exibe detalhes completos do erro


