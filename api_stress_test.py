import requests
import threading
import time
from config import gerar_config
import uuid

config = gerar_config()
requisicao = config['requisicao']
concorrencia = config['concorrencia']
tempo = config['tempo']
url = requisicao['url']
metodo = requisicao['metodo']
headers = requisicao['headers']
dados = requisicao['dados']
totais = []
timer = []
requests_ids = []
metricas_tempo = []


def iniciar_timer():
    timer.append(1)
    contador = tempo
    while contador > 0:
        time.sleep(1)
        contador -= 1
    timer.clear()


def criar_thread_usuario():
    while(len(timer) > 0):
        try:
            realizar_chamada_http()
        except:
            print('Erro ao tentar relizar chamada HTTP')
            totais.append('Falha')


def realizar_chamada_http():
    request_id = str(uuid.uuid4())
    requests_ids.append(request_id)
    tempo_inicial = time.process_time()
    status_code = 0
    try:
        response = requests.request(
            method=metodo, url=url, headers=headers, data=dados)
        status_code = response.status_code
    except:
        status_code = 500
    tempo_total = round(time.process_time() - tempo_inicial, 2)
    metricas_tempo.append(tempo_total)
    exibir_resposta_requisicao(status_code, tempo_total)
    requests_ids.remove(request_id)


def exibir_resposta_requisicao(status_code, tempo_total):
    if isSuccess(status_code):
        totais.append('Sucesso')
        print('{} - {} - Resposta: {} - {}s'.format(url,
              metodo, status_code, tempo_total))
    else:
        totais.append('Falha')
        print('{} - {} - Resposta: {} - {}s - ERROR'.format(url,
              metodo, status_code, tempo_total))


def isSuccess(status_code):
    return status_code >= 200 and status_code < 300


def calcular_metricas():
    while (len(timer) > 0 or len(requests_ids) > 0):
        pass

    total = len(totais)
    sucessos = len(list(filter(lambda x: x == 'Sucesso', totais)))
    falhas = len(list(filter(lambda x: x == 'Falha', totais)))
    disponibilidade = (sucessos / total) * 100
    tempo_medio = round(sum(metricas_tempo) / len(metricas_tempo), 2)
    exibir_resultados(total, sucessos, falhas, disponibilidade, tempo_medio)


def exibir_resultados(total, sucessos, falhas, disponibilidade, tempo_medio):
    print('Total: {}'.format(total))
    print('Disponibilidade: {}%'.format(disponibilidade))
    print('Sucessos: {}'.format(sucessos))
    print('Falhas: {}'.format(falhas))
    print('Requisi????o mais r??pida: {}s'.format(min(metricas_tempo)))
    print('Requisi????o mais lenta: {}s'.format(max(metricas_tempo)))
    print('Tempo m??dio: {}s'.format(tempo_medio))


if __name__ == "__main__":
    threading.Thread(target=iniciar_timer).start()
    print('Disparando {} usu??rios durante {}s...'.format(concorrencia, tempo))
    threading.Thread(target=calcular_metricas).start()
    for usuario in range(concorrencia):
        threading.Thread(target=criar_thread_usuario).start()
