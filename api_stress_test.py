import requests
import threading
import time
import random
from config import gerar_config

config = gerar_config()
requisicao = config['requisicao']
concorrencia = config['concorrencia']
tempo = config['tempo']
totais = []
threads = []

def criar_thread(name):
    thread_name = 'Thread {}'.format(name)
    threads.append(thread_name)
    realizar_chamada_http()
    threads.remove(thread_name)


def realizar_chamada_http():
    metodo = requisicao['metodo']
    url = requisicao['url']
    response = ''
    tempo_inicial = time.process_time()
    if metodo == 'GET':
        response = requests.get(
            requisicao['url'], headers=requisicao['headers'])
    if metodo == 'POST':
        response = requests.post(requisicao['url'], headers=requisicao['headers'], data=requisicao['dados'])
    tempo_total = time.process_time() - tempo_inicial
    response_status = response.status_code
    if response_status >= 200 and response_status < 300:
        totais.append('Sucesso')
        print('{} - {} - Resposta: {} - {}ms'.format(url, metodo, response_status, tempo_total))
    else:
        totais.append('Falha')
        print('{} - {} - Resposta: {} - {}ms - ERROR'.format(url, metodo, response_status, tempo_total))
    return response_status


if __name__ == "__main__":
    for segundo in range(tempo):
        time.sleep(1)
        for usuario in range(concorrencia):
            thread = threading.Thread(target=criar_thread, args=(usuario,))
            thread.start()
    while (len(threads) > 0):
        pass

    total = len(totais)
    sucessos = len(list(filter(lambda x: x == 'Sucesso', totais)))
    falhas = len(list(filter(lambda x: x == 'Falha', totais)))
    disponibilidade = (sucessos / total) * 100

    print('Total: {}'.format(total))
    print('Disponibilidade: {}%'.format(disponibilidade))
    print('Sucessos: {}'.format(sucessos))
    print('Falhas: {}'.format(falhas))
