# Documentação do Robô de Solicitação de Pagamento :dollar: :robot_face:

# Execução Do Projeto

## Instale o Python

> Certifique-se de que o Python esteja instalado no sistema. Possível baixá-lo no *python.org*

## Crie um Ambiente Virtual

> É necessário criar um ambiente virtual para isolar as dependências do projeto. É recomendável que user o virtualenv. 

Caso não tenha instalado o virtualenv, segue exemplo:
> pip install virtualenv

Exemplo usando *venv*:
> virtualenv venv

Para ativar o Ambiente Virtual no Windows:
> venv\Scripts\activate

## Instale as Dependências do Projeto:

Use o 'pip' para instalar as bibliotecas necessárias para o projeto. As dependências instaladas no projeto estão no requirements.txt

Exemplo de como instalar as dependências:

> pip install -r requirements.txt

## Configuras as Váriaveis de Ambiente 

Para o funcionamento correto do projeto é necessário criar um arquio no raiz do projeto chamado '.env', nesse arquivo irá conter todas as variáveis de ambientes usadas no projeto. 

Exemplo: 

No raiz do projeto é possível encontrar um arquivo chamado 'sample.env' na qual vai estar todas as variavis de ambiente criada para o projeto. Necessário copiar as variáveis de ambiente desse arquivo SAMPLE, e colar dentro do arquivo .env, após isso, mudar os valores das variáveis para o cenário real de deploy. 

> .env

## Setar Planilha de Configuração

Necessário ter a planilha de configuração dentro do diretório *dealerships_xlsx*. A planilha irá conter todos os dados necessários que o robô inserir dentro do processo de Solicitação de Pagamento do Fluig. 

Nome recomendável da planilha: 

> concessionarias_infos.xlsx

Observação: A planilha usada pelo robô pode ser encontrada com o time de Análise de Processos ou com o Financeiro.

## Geração do Arquivo de Token Graph API 

Com o módulo generate_token_acess.py é possível gerar o Token de acesso, para acesso a API da Microsoft, que será responsável pela interação com o email. 

Após geração do Token um arquivo será gerado no raiz do projeto. Exemplo:

> O365_token.txt

## Execução

Após realizar todos os passos acima. Apenas é necessário executar o *main.py*. Exemplo:

> python main.py








