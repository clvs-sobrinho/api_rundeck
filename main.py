'''
Script para exportar os jobs de projeto no Rundeck para outro e arnazenar em um arquivo .JSON
Author: Cleverson Ezequiel Silva Sobrinho
Date: 2023-02-02
'''

import functions
"""
Note que ao importar o arquivo functions.py, as bibliotecas requests e json são importadas automaticamente
mas para acessar as funções e/ou constantes/variáveis é necessário utilizar o nome do arquivo seguido do nome do objeto
Ex:
functions.get_job()
functions.pull_job()
functions.requests.get()
functions.TOKEN
functions.HOST

"""

# URL da API do Rundeck
url = "{host}/api/33/project/{project}/jobs".format(host=functions.HOST, project=functions.SRC_PROJECT)

#Cabeçalho da solicitação
headers = {
    "Accept": "application/json",
    "X-Rundeck-Auth-Token": functions.TOKEN
}

# Realiza a solicitação GET
response = functions.requests.get(url, headers=headers)
jobs_list = []

# Verifica se a resposta é válida
if response.status_code == 200:
    # Exporta os dados retornados pela API
    jobs = response.json()
    with open('jobs.json', 'w') as outfile:
        functions.json.dump(jobs, outfile, indent=4)

    for job in jobs:
        job_xml = functions.get_job(job["id"])
        jobs_list.append(job_xml)
        print(f'"{job["id"]}" obtido com sucesso!')
        functions.pull_job(project=functions.DST_PROJECT, job=job_xml[job["id"]], id=job["id"])

    with open('jobs_structure_xml.json', 'w') as outfile:
        functions.json.dump(jobs_list, outfile, indent=4)
    print("Jobs exportados com sucesso!")

else:
    # Exibe a mensagem de erro
    print(f"Erro: {response.status_code}")
