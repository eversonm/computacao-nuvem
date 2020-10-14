import requests
import json

def dynamodb_get():
    url = "https://*****.execute-api.*******/*******/mineracao"

    response = requests.get(url=url)
    return response.json()

def dynamodb_post(nome="tabela", horario="01/01/2020 00:00:00", link="www.kaggle.com/"):
    url = "https://*****.execute-api.*******/*******/mineracao"
    payload = {
        "nometabela": nome,
        "horarioacesso": horario,
        "link": link
    }
    response = requests.post(url=url, data=json.dumps(payload))
    return response
