import csv
import json
import requests
from bs4 import BeautifulSoup

lista_de_vagas = []
linkedin_url = "https://www.linkedin.com/jobs/search"
response = requests.get(
    linkedin_url,
    params={
        "keywords": "Desenvolvedor Junior",
        "location": "Brazil",
        "trk": "guest_homepage-basic_guest_nav_menu_jobs",
    },
)

contexto = BeautifulSoup(response.content, "html.parser")
seleciona_vagas = contexto.select(".jobs-search__results-list li")
for vaga in seleciona_vagas:
    titulo = vaga.select(".base-search-card__title")[0].text.strip()
    empresa = vaga.select(".base-search-card__subtitle")[0].text.strip()
    localidade = vaga.select(".job-search-card__location")[0].text.strip()
    data_publicacao = vaga.find("time").get("datetime")

    if len(vaga.select(".hidden-nested-link")) == 0:
        link = vaga.select(".base-card")[0].get("href")
    else:
        link = vaga.select(".hidden-nested-link")[0].get("href")

    print(f"Vaga: {titulo}")
    print(f"Empresa: {empresa}")
    print(f"Localidade: {localidade}")
    print(f"Data de publicação: {data_publicacao}")
    print(f"Link da vaga: {link}")
    print("########\n\n\n")

    info = {
        "vaga": titulo,
        "empresa": empresa,
        "localidade": localidade,
        "data_publicacao": data_publicacao,
        "link": link,
    }

    lista_de_vagas.append(info)

with open("vagas.json", "w") as arquivo_json:
    arquivo_json.write(json.dumps(lista_de_vagas))

with open("vagas.csv", mode="w") as arquivo_csv:
    cabecalho = ["vaga", "empresa", "localidade", "data_publicacao", "link"]
    gerador_csv = csv.DictWriter(arquivo_csv, fieldnames=cabecalho)
    gerador_csv.writeheader()
    gerador_csv.writerows(lista_de_vagas)
