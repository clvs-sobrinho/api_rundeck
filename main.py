'''
Script para exportar os jobs de projeto no Rundeck para outro e arnazenar em um arquivo .JSON

'''

import functions

# URL da API do Rundeck
url = functions.HOST + "/api/33/project/{project}/jobs".format(project=functions.SRC_PROJECT)

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
    # Imprime os dados retornados pela API
    jobs = response.json()
    with open('jobs.json', 'w') as outfile:
        json.dump(jobs, outfile, indent=4)

    for job in jobs:
        job_xml = functions.get_job(job["id"])
        jobs_list.append(job_xml)
        print(f'"{job["id"]}" obtido com sucesso!')
        functions.pull_job(project=functions.DST_PROJECT, job=job_xml['id'], id=job["id"])

    with open('jobs_structure_xml.json', 'w') as outfile:
        functions.json.dump(jobs_list, outfile, indent=4)
    print("Jobs exportados com sucesso!")

else:
    # Exibe a mensagem de erro
    print(f"Erro: {response.status_code}")
