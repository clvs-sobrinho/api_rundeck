'''
Funções para exportar e importar jobs do Rundeck
Author: Cleverson Ezequiel Silva Sobrinho
Date: 2023-02-02
Update: 2023-02-10
'''

import requests
import os
import json
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
    url = "{host}/api/33/job/{id}".format(host=HOST, id=id)

    # Realiza a solicitação GET
    response = requests.get(url, headers=headers)

    # Verifica se a resposta é válida
    if response.status_code == 200:
        #retorna a estrutura do job em XML
        return {id: response.text}
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}")

def pull_job(project='TESTE', job='', id=''):
    '''
    Função que recebe o XML do job e importa para o projeto informado
    '''
    
    #Cabeçalho da solicitação
    headers = {
        "X-Rundeck-Auth-Token": TOKEN,
        "Accept": "application/json"
    }

    # URL da API do Rundeck
    url = "{host}/api/33/project/{project}/jobs/import".format(host=HOST, project=project)

    # Fazer uma solicitação POST para a API do Rundeck com o XML do job
    data = {
        "xmlBatch": job,
        "Content-Type": "x-www-form-urlencoded",
        "uuidOption": "remove",
        "uuidOption": "preserve"
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
            with open(id+'.xml', 'w') as outfile:
                outfile.write(job)
            with open('failed.log', 'a') as outfile:
                outfile.write(msg + "\n")
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}")

def alter_job(project='TESTE', job='', id=''):
    #Cabeçalho da solicitação
    headers = {
        "X-Rundeck-Auth-Token": TOKEN,
        "Accept": "application/json"
    }

    # URL da API do Rundeck
    url = "{host}/api/33/project/{project}/jobs/import".format(host=HOST, project=project)

    # Fazer uma solicitação POST para a API do Rundeck com o XML do job
    data = {
        "xmlBatch": job,
        "Content-Type": "x-www-form-urlencoded",
        "dupeOption": "update"
        }
    response = requests.post(url, headers=headers, data=data)

    # Verifica se a resposta é válida
    if response.status_code == 200:
        # Anlisa a resposta para verificar se o job foi importado com sucesso
        if response.json()["succeeded"]:
            msg = f'Job alterado com sucesso: {id} --> Novo id: {response.json()["succeeded"][0]["id"]}'
            print(msg)
            with open('succeeded.log', 'a') as outfile:
                outfile.write(msg + "\n")
        else:
            msg = f'Erro ao importar o job: {id}'
            print(msg)
            with open(id+'.json', 'w') as outfile:
                json.dump(response.json(), outfile, indent=4)
            with open(id+'.xml', 'w') as outfile:
                outfile.write(job)
            with open('failed.log', 'a') as outfile:
                outfile.write(msg + "\n")
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}")

def export_job(id='', group='', project='jobs_xml'):
    #obtem o job em XML
    job = get_job(id)
    if group:
        subfolder = group.split('/')
    else:
        subfolder = []
    pwd = os.getcwd()
    pwd = os.path.join(pwd, project)
    if not os.path.exists(pwd):
        os.makedirs(pwd)
    for folder in subfolder:
        pwd = os.path.join(pwd, folder)
        if not os.path.exists(pwd):
            os.makedirs(pwd)

    #salva o job em um arquivo XML
    with open(os.path.join(pwd,id+'.xml'), 'w') as outfile:
        outfile.write(job[id])
    print(f'Job exportado com sucesso: {id}')

def delete_job(id=''):
    #Cabeçalho da solicitação
    headers = {
        "X-Rundeck-Auth-Token": TOKEN,
        "Accept": "application/json"
    }

    # URL da API do Rundeck
    url = "{host}/api/33/job/{id}".format(host=HOST, id=id)

    # Fazer uma solicitação DELETE para a API do Rundeck
    response = requests.delete(url, headers=headers)

    # Verifica se a resposta é válida
    if response.status_code == 204:
        # Anlisa a resposta para verificar se o job foi importado com sucesso
        if response.json()["succeeded"]:
            msg = f'Job excluído com sucesso: {id}'
            print(msg)
            with open('succeeded.log', 'a') as outfile:
                outfile.write(msg + "\n")
        else:
            msg = f'Erro ao excluir o job: {id}'
            print(msg)
            with open(id+'.json', 'w') as outfile:
                json.dump(response.json(), outfile, indent=4)
            with open('failed.log', 'a') as outfile:
                outfile.write(msg + "\n")
    else:
        # Exibe a mensagem de erro
        raise Exception(f"Erro: {response.status_code}")