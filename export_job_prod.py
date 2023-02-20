'''
Script para exportar os jobs de projeto no Rundeck para outro e arnazenar em um arquivo .JSON
Author: Cleverson Ezequiel Silva Sobrinho
Date: 2023-20-02
'''

from rundeck import RundeckAPI, requests, json
"""

"""
rd = RundeckAPI()

# URL da API do Rundeck
url = f"{rd.HOST}/api/{rd.VERSION}/project/{rd.SRC_PROJECT}/jobs"

#Cabeçalho da solicitação
headers = rd.header

# Realiza a solicitação GET
response = requests.get(url, headers=headers)
jobs_list = []

# Verifica se a resposta é válida
if response.status_code == 200:
    # Exporta os dados retornados pela API
    jobs = response.json()
    with open('jobs.json', 'w') as outfile:
        json.dump(jobs, outfile, indent=4)

    for job in jobs:
        job_xml = rd.get_job(job["id"], type="yaml")
        # verifica se o job contém o comando "cd $SCRIPTS_DIR/ingestions/" 
        # se sim, adiciona o job na lista jobs_list
        if "cd $SCRIPTS_DIR/ingestions/" in job_xml[job["id"]]:
            jobs_list.append(job_xml)
            print(f'"{job["id"]}" obtido com sucesso!')
            rd.export_job(
                id=job["id"],
                group=job["group"],
                project=rd.SRC_PROJECT
            )

    with open('jobs_prod_ingestions_xml.json', 'w') as outfile:
        json.dump(jobs_list, outfile, indent=4)
    print("Jobs exportados com sucesso!")

else:
    # Exibe a mensagem de erro
    print(f"Erro: {response.status_code}")
