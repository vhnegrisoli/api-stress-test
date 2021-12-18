concorrencia = 10
tempo = 3

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

def gerar_config():
  return {
    'concorrencia': concorrencia,
    'tempo': tempo,
    'requisicao': requisicao
  }
