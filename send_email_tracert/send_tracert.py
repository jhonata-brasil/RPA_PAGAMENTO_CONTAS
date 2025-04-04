import requests
import datetime 

def get_message_greeting(type_service, name_coligada, name_filial, number_registration, number_request):
    
    current_time = datetime.datetime.now().time()
    
    limit_morning = datetime.time(5,0)
    limit_affertnoon = datetime.time(12,0)
    limit_evining = datetime.time(18,0)
    
    if limit_morning <= current_time < limit_affertnoon:
        greeting = 'bom dia'
    elif limit_affertnoon <= current_time < limit_evining:
        greeting = 'boa tarde'
    else:
        greeting = 'boa noite'
        
        
    message = f'''
       
        Olá, {greeting}. 
        
        <br><br>

        Informamos que a solicitação de pagamento de {type_service} para a coligada {name_coligada},
        filial {name_filial}, instalação n° {number_registration} foi gerada no Fluig por meio da 
        solicitação n° {number_request}.
        
    '''
    
    return message


def send_tracert_to_user(token_acess, logger, user_email, type_service, name_coligada, name_filial, number_registration, number_request):

    headers = {
        'Authorization': 'Bearer ' + token_acess
    }

        # Split the user_emails string by ';' and strip any extra whitespace
    email_list = [email.strip() for email in user_email.split(';') if email.strip()]

    # Build the list of recipient objects
    recipients = [{'emailAddress': {'address': email}} for email in email_list]

    request_body = {
        'message': {
            # recipient list
            'toRecipients': recipients,
            # email subject
            'subject': f'Solicitação de Pagamento n° {number_request} gerada ',
            'importance': 'normal',
            'body': {
                'contentType': 'HTML',
                'content': get_message_greeting(type_service, name_coligada, name_filial, number_registration, number_request)
            },
            
        }
    }

    GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'
    endpoint = GRAPH_ENDPOINT + '/me/sendMail'

    response = requests.post(endpoint, headers=headers, json=request_body)
    if response.status_code == 202:
        logger.info('Email enviado com sucesso.')
    else:
        logger.error(response.reason)