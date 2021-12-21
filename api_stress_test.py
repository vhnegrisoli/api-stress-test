import requests
import threading
import time
import random
from config import gerar_config
import uuid

config = gerar_config()
requisicao = config['requisicao']
concorrencia = config['concorrencia']
tempo = config['tempo']
totais = []
timer = []
requests_ids = []


def iniciar_timer(name):
    timer.append(1)
    contador = tempo
    for segundo in range(contador):
        time.sleep(1)
        contador -= 1
    timer.clear()


def criar_thread(name):
    while(len(timer) > 0):
        realizar_chamada_http()


def realizar_chamada_http():
    request_id = str(uuid.uuid4())
    requests_ids.append(request_id)
    metodo = requisicao['metodo']
    url = requisicao['url']
    response = ''
    tempo_inicial = time.process_time()
    response = requests.request(
        method=metodo, url=requisicao['url'], headers=requisicao['headers'], data=requisicao['dados'])
    tempo_total = time.process_time() - tempo_inicial
    response_status = response.status_code
    if response_status >= 200 and response_status < 300:
        totais.append('Sucesso')
        print('{} - {} - Resposta: {} - {}ms'.format(url,
                                                     metodo, response_status, round(tempo_total, 2)))
    else:
        totais.append('Falha')
        print('{} - {} - Resposta: {} - {}ms - ERROR'.format(url,
                                                             metodo, response_status, round(tempo_total, 2)))
    requests_ids.remove(request_id)


if __name__ == "__main__":
    threading.Thread(target=iniciar_timer, args=('',)).start()
    print('Disparando {} usuários durante {}s...'.format(concorrencia, tempo))
    time.sleep(1)
    for usuario in range(concorrencia):
        threading.Thread(target=criar_thread, args=(usuario,)).start()

    while (len(timer) > 0 or len(requests_ids) > 0):
        pass

    total = len(totais)
    sucessos = len(list(filter(lambda x: x == 'Sucesso', totais)))
    falhas = len(list(filter(lambda x: x == 'Falha', totais)))
    disponibilidade = (sucessos / total) * 100

    print('Total: {}'.format(total))
    print('Disponibilidade: {}%'.format(disponibilidade))
    print('Sucessos: {}'.format(sucessos))
    print('Falhas: {}'.format(falhas))
