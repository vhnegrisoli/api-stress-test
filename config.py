from ast import arg
import sys

args = sys.argv
concorrencia_default = 10
tempo_default = 3

requisicao = {
    'metodo': 'GET',
    'url': 'http://localhost:8080/api/v1/cep/86050523/',
    'dados': '{}',
    'headers': {
        'content-type': 'application/json'
    }
}


def gerar_config():
    concorrencia = concorrencia_default
    tempo = tempo_default
    if len(args) == 3 and isNumeric(args[1]) and isNumeric(args[2]):
        concorrencia = int(args[1])
        tempo = int(args[2])
    else:
        print('Os parâmetros informados não estão no formato numérico válido, serão utilizados os valores default.')
    return {
        'concorrencia': concorrencia,
        'tempo': tempo,
        'requisicao': requisicao
    }


def isNumeric(value):
    try:
        int(value)
        return True
    except:
        return False
