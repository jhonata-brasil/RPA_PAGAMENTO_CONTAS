from download_pdf_from_email.new_extract_pdf_email_msal import (
    main_process_download_attachments,process_edp_emails,
)
from download_pdf_from_email.generate_token_acess import generate_token
from send_email_tracert.send_tracert import send_tracert_to_user
from convert_pdf_to_txt.pdf_txt import filtered_extracted_data
from slack_monitoring.slack_notifier import SlackNotifier
from database.db import (
    connect_db_sqlite,
    create_table_params_filters,
    insert_filename_in_db,
    select_filename_in_db,
)

from log_data.logger import LogGenerator
from datetime import datetime
from rpa_fluig import Fluig, EDPLINK
from time import sleep
from pathlib import Path
from sharepoint.SharepointFunctions import Sharepoint

import shutil
import os
import sys
import config

from dotenv import load_dotenv
URL_MAIN_FLUIG = None

load_dotenv()

log_instance = LogGenerator()

slack = None
logger =None
# Criando uma instância da classe EDPLINK
edplink_instance = EDPLINK(logger,slack)

logger = log_instance.setup_logger()
conn = connect_db_sqlite(logger)
slack_notifier = SlackNotifier(
    os.getenv("ENDPOINT_SLACK"), os.getenv("CHANNEL_SLACK"), os.getenv("NAME_ALERT")
)

create_table_params_filters(conn)


def move_file_to_processed(path_file, path_destiny):
    try:
        shutil.move(path_file, path_destiny)
    except Exception as e:
        slack_notifier.post_message(
            f"  :::Erro ao mover arquivo {path_file} para pasta  {path_destiny} -> Processados {e}"
        )


def process_rpa_fluig(token):
    sleep(5)

    # shpt = Sharepoint()
    # shpt.DownloadPlanilha()
    df, juros, multa = filtered_extracted_data(logger)
    month_competence = datetime.today().strftime("%m/%Y")

    if df is None:
        logger.info("O df retornou None.")
        return

    sleep(5)

    for index, row in df.iterrows():
        filename = Path(row["PATH_FILE"]).stem
        result = select_filename_in_db(conn, filename, logger)

        if result:
            move_file_to_processed(
                row["PATH_FILE"], f'{os.getenv("PATH_PDFS_DUPLICATED")}{filename}.pdf'
            )
            

        else:
            fluig = Fluig(logger, slack_notifier)
            fluig.start_browser()
            # Deve ser usada em ambiente de homologação substitua
            # varURL ='https://hmgfluig.findes.org.br/portal/p/1/home'
            # fluig.select_url(varURL)
            fluig.select_url(os.getenv("URL_MAIN_FLUIG"))
            fluig.login(os.getenv("USER_FLUIG"), os.getenv("PASSWORD_FLUIG"))
            fluig.go_to_payment_request()

            HISTORICAL_COMPLEMENT = f"INSTALAÇÃO {row['INSTALAÇÃO/MATRÍCULA']} - FATURA {row['CONCESSIONÁRIO']} {row['DESCRIÇÃO DO DEPARTAMENTO']} - {month_competence}"
            # Deve ser usada em ambiente de homologação substitua a row["EMAIL USUARIO"] por varemailteste
            # varemailteste ='jhonata.alves@findes.org.br'
            # varemailteste ='jbravo@findes.org.br'

            number_request = fluig.insert_input_to_generate_payment_request(
                row["COLIGADA"],
                row["DESCRIÇÃO DA FILIAL"],
                row["CNPJ DO FORNECEDOR"],
                row["DESCRIÇÃO DO DEPARTAMENTO"],
                row["CENTRO DE CUSTO"],
                row["VALOR TOTAL"],
                row["TIPO DO SERVIÇO"],
                HISTORICAL_COMPLEMENT,
                row["CONTA/CAIXA"],
                row["FORMA DE PAGAMENTO"],
                row["PATH_FILE"],
                row["NUMERO NOTA"],
                row["DATA EMISSAO"],
                row['Possui rateio?'],
                row['Departamento rateio1'],
                row['Centro de Custo rateio1'],
                row['Percentual rateio1'],
                row['Departamento rateio2'],
                row['Centro de Custo rateio2'],
                row['Percentual rateio2'],
                row['Departamento rateio3'],
                row['Centro de Custo rateio3'],
                row['Percentual rateio3'],
                juros,
                multa
                    
            )

            send_tracert_to_user(
                token,
                logger,
                row["EMAIL USUARIO"],
                row["TIPO DO SERVIÇO"],
                row["COLIGADA"],
                row["DESCRIÇÃO DA FILIAL"],
                row["INSTALAÇÃO/MATRÍCULA"],
                number_request,
            )

            insert_filename_in_db(conn, filename, logger)

            #PÓS CONCLUSÃO DO PROCESSO MOVE O ARQUIVO PARA PROCESSADO
            move_file_to_processed(
                row["PATH_FILE"], f'{os.getenv("PATH_PDF_PROCESSEDS")}{filename}.pdf'
            )


if __name__ == "__main__":
    token = generate_token(slack_notifier)
    print(token)

    # Processa e-mails com anexos (função existente)
    amount_email_attachment = main_process_download_attachments(
        token, logger, slack_notifier
    )
        # Processa e-mails da EDP e baixa no formato .eml (nova função)
    path_download_eml = os.getenv('PATH_DOWNLOADED_INVOICES_PDF')
    process_edp_emails(token, logger, path_download_eml)

    process_rpa_fluig(token)
    sys.exit()

