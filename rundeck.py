import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

class RundeckAPI:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("TOKEN")
        self.HOST = os.getenv("HOST")
        self.SRC_PROJECT = os.getenv("SRC_PROJECT")
        self.DST_PROJECT = os.getenv("DST_PROJECT")
        self.VERSION = os.getenv("VERSION")
        self.URL_1 = f"{self.HOST}/api/{self.VERSION}/job/"
        self.URL_2 = f"{self.HOST}/api/{self.VERSION}/project/{self.DST_PROJECT}/jobs/import"
        self.header = {
            "X-Rundeck-Auth-Token": self.TOKEN,
            "Accept": "application/json"
        }

    #define getter e setter para o header da API
    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, type='json'):
        self._header = {
            "X-Rundeck-Auth-Token": self.TOKEN,
            "Accept": f"application/{type}"
        }

    def get_job(self, id, type='xml'):
        #Cabeçalho da solicitação
        self.header = type
        headers = self.header

        # URL da API do Rundeck
        url = self.URL_1 + id

        # Realiza a solicitação GET
        response = requests.get(url, headers=headers)

        # Verifica se a resposta é válida
        if response.status_code == 200:
            #retorna a estrutura do job em XML
            return {id: response.text}
        else:
            # Exibe a mensagem de erro
            raise Exception(f"Erro: {response.status_code} \n {self.header}")

    def pull_job(self, project='TESTE', job='', id=''):
        '''
        Função que recebe o XML do job e importa para o projeto informado
        '''

        #Cabeçalho da solicitação
        headers = self.header

        # URL da API do Rundeck
        url = self.URL_2

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
                with open(id+'.xml', 'w') as outfile:
                    outfile.write(job)
                with open('failed.log', 'a') as outfile:
                    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    outfile.write(f'{time}: {msg}\n')
        else:
            # Exibe a mensagem de erro
            raise Exception(f"Erro: {response.status_code}")

    def alter_job(self, project='TESTE', job='', id=''):
        #Cabeçalho da solicita
        headers = self.header

        # URL da API do Rundeck
        url = self.URL_2

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
                    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    outfile.write(f'{time}: {msg}\n')
            else:
                msg = f'Erro ao importar o job: {id}'
                print(msg)
                with open(id+'.json', 'w') as outfile:
                    json.dump(response.json(), outfile, indent=4)
                with open(id+'.xml', 'w') as outfile:
                    outfile.write(job)
                with open('failed.log', 'a') as outfile:
                    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    outfile.write(f'{time}: {msg}\n')
        else:
            # Exibe a mensagem de erro
            raise Exception(f"Erro: {response.status_code}")

    def export_job(self, id='', type='xml', project='jobs_xml'):
        #obtem o job em XML
        job = self.get_job(id, type)
        pwd = os.getcwd()
        pwd = os.path.join(pwd, project)
        if not os.path.exists(pwd):
            os.makedirs(pwd)

        #salva o job em um arquivo YAML
        with open(os.path.join(pwd,id+'.yaml'), 'w') as outfile:
            outfile.write(job[id])
        print(f'Job exportado com sucesso: {id}')
        with open('export.log', 'a') as outfile:
            time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            outfile.write(f'export : {id} --> {pwd} {time}' + "\n")

    def delete_job(self, id=''):
        #Cabeçalho da solicitação
        headers = self.header

        # URL da API do Rundeck
        url = self.URL_1 + id

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
