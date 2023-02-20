import functions

# URL da API do Rundeck
url = "{host}/api/33/project/{project}/jobs".format(host=functions.HOST, project=functions.DST_PROJECT)

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
    with open('jobs{}.json'.format(functions.DST_PROJECT), 'w') as outfile:
        functions.json.dump(jobs, outfile, indent=4)

    for job in jobs:
        functions.export_job(
            id=job["id"], 
            group=job["group"], 
            project=functions.DST_PROJECT
            )


else:
    # Exibe a mensagem de erro
    print(f"Erro: {response.status_code}")

