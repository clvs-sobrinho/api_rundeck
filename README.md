# RUNDECK-DEV 
Script para acessar o ENDPOINT do Rundeck - DEV, exportar os jobs do projeto BIGDATA e importar no projeto BIGDATA-PREPROD.

# Dependências
Este script utiliza duas bibliotecas requests 2.28.2 e python-dotenv 0.21.1, e foi utilizado o pip para instala-lás.
```bash:
pip install requests==2.28.2
```

```bash:
pip install python-dotenv==0.21.1
```


# Variáveis de ambiente

O script utiliza a biblioteca python-dotenv para usar as variáveis de ambiente para acessar o Rundeck DEV e importar os jobs no Rundeck PREPROD. Para isso, é necessário criar um arquivo .env na raiz do projeto e adicionar as seguintes variáveis:


```bash:
TOKEN = <TOKEN>
HOST =  <HOST>
SRC_PROJECT = BIGDATA
DST_PROJECT = BIGDATA-PREPROD
```


# API Rundeck

O script utiliza a API do Rundeck através de token, é necessário possuir um token de acesso no Rundeck DEV e adicionar na variável TOKEN do arquivo .env. A requisição é feita através do método GET, utilizando o header Authorization com o token de acesso.

# Estrutura do projeto

O projeto possui a seguinte estrutura:

```bash:
├── .env
├── .gitignore
├── README.md
├── main.py
├── functions.py
```

O arquivo main.py é o arquivo principal do projeto, onde é feita a chamada das funções do arquivo functions.py, este arquivo requisita a lista de jobs e em seguida requisita a estutura destes jobs através do id e após faz o post no projeto de destino. O arquivo functions.py possui as funções que fazem a requisição para o Rundeck DEV e importam os jobs no Rundeck PREPROD. O arquivo .env possui as variáveis de ambiente que são utilizadas no projeto. O arquivo .gitignore possui os arquivos que não devem ser versionados no repositório.

# Como utilizar

Para utilizar o script, é necessário ter o python instalado na máquina. Após isso, basta executar o script main.py na raiz do projeto.

```bash:
python .\main.py
```


