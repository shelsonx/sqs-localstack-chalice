import requests
import json
from datetime import datetime
import sys
from time import sleep
from generate_passwords import generate_mixed_passwords
AMOUNT = 10

url = 'https://6girhtoq4e.execute-api.localhost.localstack.cloud:4566/api/cadastro'

def send_message_queue():
    headers = {
        'Content-Type': 'application/json'
    }
    passwords = generate_mixed_passwords(AMOUNT)
    for i in range(AMOUNT):
        data = {
            'name': str(datetime.now()),
            'password': passwords[i],
            'email': 'shelsonx@gmail.com'
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            print(f'Mensagem {i+1} enviada com sucesso!')
        else:
            print(f'Falha ao enviar mensagem: {i}', response.text)
        sleep(.5)

if __name__ == '__main__':
    send_message_queue()