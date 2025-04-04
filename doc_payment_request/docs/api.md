# Documentação do Robô de Solicitação de Pagamento :dollar: :robot_face:

# Integração com a Graph Microsoft API

## Visão Geral

Com a Graph Microsoft API permite que o nosso projeto se conecte aos serviços da Microsoft, como o Microsoft 365, para realizar tarefas como envio de e-mails e download de anexos de e-mail. 

## Requisitos Prévios
Antes de começar a usar a Graph Microsoft API, é necessário atender aos seguintes requisitos:

* Conta Microsoft: Certifique-se de ter uma conta Microsoft válida, que pode ser usada para autenticar e autorizar solicitações à API.

* Registro do Aplicativo: Você deve registrar seu aplicativo na Plataforma de Aplicativos da Microsoft, o que lhe fornecerá as credenciais necessárias para autenticar seu aplicativo com a API.

## Autenticação
Para usar a Graph Microsoft API, seu aplicativo precisa ser autenticado. Siga estas etapas para autenticar seu aplicativo:

* Registre seu aplicativo na Plataforma de Aplicativos da Microsoft.

* Obtenha as credenciais de autenticação, incluindo o ID do Aplicativo e o Segredo do Cliente.

* Implemente a autenticação OAuth2 no seu aplicativo para obter um token de acesso.

Referência usada no projeto de como realizar o passo a passo acima: 

https://documentation.botcity.dev/plugins/ms365/auth-credentials/

## Exemplos de Uso

### Envio de E-mails

Para enviar e-mails usando a Graph Microsoft API, você pode fazer uma solicitação HTTP POST para a seguinte URL:

> POST https://graph.microsoft.com/v1.0/me/sendMail

Para maiores detalhes, por favor consultar o módulo do projeto:

> send_email_tracert/send_tracert.py


### Download de Anexos de E-mail

Para baixar anexos de e-mails usando a Graph Microsoft API, você pode fazer uma solicitação HTTP GET para a URL do anexo desejado. 

Exemplo:

> GET https://graph.microsoft.com/v1.0/me/messages/{id-da-mensagem}/attachments/{id-do-anexo}

Para maiores detalhes, por favor consultar o módulo do projeto:

> download_pdf_from_email/new_extract_pdf_email_msal.py

## Referências de Doc usada no projeto

* https://learn.microsoft.com/en-us/graph/overview
* https://documentation.botcity.dev/plugins/ms365/auth-credentials/
* https://github.com/O365/python-o365
* https://www.youtube.com/playlist?list=PL3JVwFmb_BnT9Ti0MMRj5nPF7XoN-4MQx