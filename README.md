# API Stress Test

Aplicação em Python para realizar testes de carga e estresse em sites e APIs utilizando client HTTP e multithreading.

# Tecnologias

- Python 3
- Requests
- Time
- Threading

# Executando

É possível executar de 2 maneiras diferentes:

* Rodando com valores padrões de concorrência e tempo
* Rodando com valores de concorrência e tempo especificados por parâmetro

### Executando com valores padrões

Basta rodar o comando:

`python api_stress_test.py`

A concorrência e o tempo serão os que estão setados no arquivo `config.py`, caso queira um valor default diferente, terá que alterar o arquivo.

### Executando com valores informados por parâmetro

Basta rodar o comando:

`python api_stress_test.py valor_concorrencia valor_tempo`

Exemplo:

`python api_stress_test.py 10 60` -> executará o teste de estresse com 10 usuários concorrentes por 60 segundos.

O valor `default`, caso não sejam informados os parâmetros, será de **10 usuários durante 3 segundos**.

# Worflow do funcionamento do teste

Abaixo, está exemplificado em um worflow qual será o funcionamento do software.

![Workflow](https://github.com/vhnegrisoli/api-stress-test/blob/master/API%20Stress%20Test%20Flow.png)

# Configurar teste

A configuração do teste fica no arquivo `config.py`.

Neste arquivo, existirão 3 objetos e uma função para exportá-los.

- concorrencia
- tempo
- requisicao

## Configuração do teste

Existem 2 configurações principais do teste de carga:

- Concorrência
- Duração

A concorrência será a quantidade de threads que serão criadas para simular requisições sendo enviadas, e a duração será a quantidade de segundos em que o total de threads criadas estará disparando requisições.

Cada thread irá simular um usuário realizando uma requisição ao servidor.

Exemplo:

```python
concorrencia = 100
tempo = 120
```

No exemplo acima, serão criadas 100 threads que farão loops de disparos durante 120 segundos (2 minutos). Cada thread irá disparar uma requisição após a outra em loop. Ao fim dos 120 segundos, as requisições não serão mais disparadas, e a aplicação irá aguardar as restantes (caso existam) para realizar o cálculo das métricas.

## Configuração da requisição

O objeto requisicao é um dicionário contendo método, url, dados (body) e headers, que também é um dicionário contendo um par chave/valor.

Exemplo de configuração (dados fictícios):

```python
requisicao = {
    'metodo': 'POST',
    'url': 'http://localhost:8080/api/v1/user/save',
    'dados': '{"usuario":"teste@teste.com","senha":"123456"}',
    'headers': {
        'content-type': 'application/json'
    }
}
```

# Output da aplicação

O output da aplicação irá informar os seguintes dados:

- URL - Método HTTP - Status HTTP - Tempo em ms
- Total de requisições enviadas
- Disponibilidade (total de sucessos pelo total de requisições)
- Total de sucessos
- Total de falhas
- Tempo médio

```shell
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.2s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.25s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.08s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.22s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.25s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.16s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.14s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.16s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.23s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.27s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.3s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.33s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.33s
http://localhost:8080/api/v1/cep/86010580/ - POST - Resposta: 200 - 0.19s
Total: 256
Disponibilidade: 100.0%
Sucessos: 256
Falhas: 0
Requisição mais rápida: 0.06s
Requisição mais lenta: 0.66s
Tempo médio: 0.19s
```

# Autor

- Victor Hugo Negrisoli
- Desenvolvedor de Software Back-End
