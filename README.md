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

# Worflow do funcionamento do teste

Abaixo, está exemplificado em um worflow qual será o funcionamento do software.

![Workflow](API Stress Test Flow.png)

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

Exemplo de configuração:

```python
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
```

# Output da aplicação

O output da aplicação irá informar os seguintes dados:

- URL - Método HTTP - Status HTTP - Tempo em ms
- Total de requisições enviadas
- Disponibilidade (total de sucessos pelo total de requisições)
- Total de sucessos
- Total de falhas

```shell
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 15.4375ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 500 - 23.203125ms - ERROR
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 15.3125ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 15.484375ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 16.03125ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 15.53125ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 400 - 16.265625ms - ERROR
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 15.953125ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 28.765625ms
https://teste-api.herokuapp.com/api/auth/token - POST - Resposta: 200 - 15.4375ms
Total: 5000
Disponibilidade: 85.3%
Sucessos: 4265
Falhas: 735
```

# Autor

- Victor Hugo Negrisoli
- Desenvolvedor de Software Back-End
