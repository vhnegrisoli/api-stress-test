import requests
import threading
import time
import random

concorrencia = 100
tempo = 50

totais = []
threads = []

requisicao = {
    'metodo': 'POST',
    'url': 'https://teste-api.herokuapp.com/api/auth/token',
    'dados': '{"usuario":"teste@teste.com","senha":"123456"}',
    'headers': {
        'Authorization': 'Bearer 25e2221f-3bad-4225-9c67-12daf27dbfd1',
        'api-secret': 'correcao-teste-base64',
        'content-type': 'application/json'
    }
}

def criar_thread(name):
  thread_name = 'Thread {}'.format(name)
  threads.append(thread_name)
  call_http_request()
  threads.remove(thread_name)

def call_http_request():
  metodo = requisicao['metodo']
  url = requisicao['url']
  response = ''
  start = time.process_time()
  if (metodo == 'GET'):
    response = requests.get(requisicao['url'], headers=requisicao['headers'])
  if (metodo == 'POST'):
    response = requests.post(requisicao['url'], headers=requisicao['headers'], data=requisicao['dados'])
  response_time = time.process_time() - start
  response_status = response.status_code
  if (response_status >= 200 and response_status < 300):
    totais.append('Sucesso')
    print('{} - {} - Resposta: {} - {}ms'.format(url, metodo, response_status, response_time))
  else:
    totais.append('Falha')
    print('{} - {} - Resposta: {} - {}ms - ERROR'.format(url, metodo, response_status, response_time))
  return response_status

if __name__ == "__main__":
  for segundo in range(tempo):
    time.sleep(1)
    for usuario in range(concorrencia):
      thread=threading.Thread(target=criar_thread, args=(usuario,))
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
