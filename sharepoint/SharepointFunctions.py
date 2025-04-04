import os
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
class Sharepoint:
    def __init__(self):
        self.SHAREPOINT_EMAIL = os.getenv('SHAREPOINT_EMAIL')
        self.SHAREPOINT_PASSWORD = os.getenv('SHAREPOINT_PASSWORD')
        self.SHAREPOINT_URL_SITE = os.getenv('SHAREPOINT_URL_SITE')
        self.SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')
        self.SHAREPOINT_DOC_LIBRARY = os.getenv('SHAREPOINT_DOC_LIBRARY')
        self.DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')

    def ConnectSharepoint(self):
        return ClientContext(self.SHAREPOINT_URL_SITE).with_credentials(UserCredential(self.SHAREPOINT_EMAIL, self.SHAREPOINT_PASSWORD))

    
    # def DownloadPlanilha(self):
    #     ctx = self.ConnectSharepoint()

    #     sharepointFilePath = f"{self.SHAREPOINT_DOC_LIBRARY}/concessionarias_infos.xlsx"
    #     fileSavePath = self.DOWNLOAD_PATH + "concessionarias_infos.xlsx"

    #     try:
    #         with open(fileSavePath, "wb") as local_file:
    #                 ctx.web.get_file_by_server_relative_url(sharepointFilePath).download(local_file).execute_query()
    #         return "Success"
    #     except Exception as e:
    #         return f"Error: {str(e)}"

    def DownloadPlanilha(self):
        # Aqui você carrega o dfUnidades (substitua com seu código real)
        file_path_unidades = os.getenv('DOWNLOAD_PATH') + r"concessionarias_infos.xlsx"
        fileSavePath = pd.read_excel(file_path_unidades)
        
        return "Success",fileSavePath