'''
Script para exportar a estrutura de cada job do projeto BIGDATA do Rundeck para um arquivo .JSON
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
        #Elimina as tags 'id' e 'uuid' do XML para evitar conflitos
        root = ElementTree.fromstring(response.text)
        for parent in root.findall('.//id..'):
            parent.clear()
        for parent in root.findall('.//uuid'):
            parent.clear()
        job_xml = ElementTree.tostring(root, encoding='unicode')
        return {id: job_xml}
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}")

def pull_job(project, job, id):
    #Cabeçalho da solicitação
    headers = {
        "X-Rundeck-Auth-Token": TOKEN,
        "Accept": "application/json"
    }

    # URL da API do Rundeck
    url = HOST + "/api/33/project/{project}/jobs/import".format(project=project)

    # Fazer uma solicitação POST para a API do Rundeck com o YAML do job
    data = {
        "xmlBatch": job,
        "Content-Type": "x-www-form-urlencoded"
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
            with open('failed.log', 'a') as outfile:
                outfile.write(msg + "\n")
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}\n{url}")
