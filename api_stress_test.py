import requests
import threading
import time
import random

concorrencia = 100
tempo = 20

totais = []
threads = []

requisicao = {
    'metodo': 'POST',
    'url': 'https://b2vn-auth-api.herokuapp.com/oauth/token',
    'dados': '"-----------------------------21370522132873121755771853860\r\nContent-Disposition: form-data; name=\"client_id\"\r\n\r\nb2vn-auth-api-client\r\n-----------------------------21370522132873121755771853860\r\nContent-Disposition: form-data; name=\"client_secret\"\r\n\r\nb2vn-auth-api-secret\r\n-----------------------------21370522132873121755771853860\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nvictorhugonegrisoli.ccs@gmail.com\r\n-----------------------------21370522132873121755771853860\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n123456\r\n-----------------------------21370522132873121755771853860\r\nContent-Disposition: form-data; name=\"grant_type\"\r\n\r\npassword\r\n-----------------------------21370522132873121755771853860--\r\n"',
    'headers': {
        'Authorization': 'Bearer 25e2221f-3bad-4225-9c67-12daf27dbfd1',
        'api-secret': 'correcao-api-tataia-base64-producao',
        'content-type': 'multipart/form-data; boundary=---------------------------21370522132873121755771853860'
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