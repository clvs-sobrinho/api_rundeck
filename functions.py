'''
Funções para exportar e importar jobs do Rundeck
Author: Cleverson Ezequiel Silva Sobrinho
Date: 2023-02-02
'''

import requests
import os
import json
import yaml
from xml.etree import ElementTree
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Define as informações de autenticação
TOKEN = os.getenv("TOKEN")
HOST = os.getenv("HOST")
SRC_PROJECT = os.getenv("SRC_PROJECT")
DST_PROJECT = os.getenv("DST_PROJECT")

def get_job(id):
    #Cabeçalho da solicitação
    headers = {
    "Accept": "application/xml",
    "X-Rundeck-Auth-Token": TOKEN
    }

    # URL da API do Rundeck
    url = HOST+"/api/33/job/{id}".format(id=id)

    # Realiza a solicitação GET
    response = requests.get(url, headers=headers)

    # Verifica se a resposta é válida
    if response.status_code == 200:
        #retorna o job em XML
        return {id: response.text}
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}")

def pull_job(project='TESTE', job='', id=''):
    #Cabeçalho da solicitação
    headers = {
        "X-Rundeck-Auth-Token": TOKEN,
        "Accept": "application/json"
    }

    # URL da API do Rundeck
    url = HOST + "/api/33/project/{project}/jobs/import".format(project=project)

    # Fazer uma solicitação POST para a API do Rundeck com o XML do job
    data = {
        "xmlBatch": job,
        "Content-Type": "x-www-form-urlencoded",
        "uuidOption": "remove"
        }
    response = requests.post(url, headers=headers, data=data)

    # Verifica se a resposta é válida
    if response.status_code == 200:
        # Anlisa a resposta para verificar se o job foi importado com sucesso
        if response.json()["succeeded"]:
            msg = f'Job importado com sucesso: {id} --> Novo id: {response.json()["succeeded"][0]["id"]}'
            print(msg)
            with open('succeeded.log', 'a') as outfile:
                outfile.write(msg + "\n")
        else:
            msg = f'Erro ao importar o job: {id}'
            print(msg)
            with open(id+'.json', 'w') as outfile:
                json.dump(response.json(), outfile, indent=4)
            with open(id+'-import.xml', 'w') as outfile:
                outfile.write(job)
            with open('failed.log', 'a') as outfile:
                outfile.write(msg + "\n")
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}\n{url}")
