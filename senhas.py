#! /usr/bin/env python3

from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

url = 'http://seat.ind.br/processo-seletivo/desafio-2017-03.php'
values = {'nome' : 'Pedro Guilherme Siqueira Moreira'}

data = urlencode(values)
full_url = url + '?' + data # http://minha.url.com/etc?param1=val1&param2=val2...

# leitura dos dados
req = Request(full_url)
with urlopen(req) as response:
    resp = json.loads(response.read().decode('utf-8')) # o resultado da requisição está em JSON
    senhas = resp['input'] # lista com as senhas desordenadas
    chave = resp['chave'] # a chave de envio
    post_to = resp['postTo'] # url de envio POST e os parâmetros necessários
    nome = resp['nome'] # o nome de quem envia

# dump das senhas
with open('dump_senhas', 'w') as fp:
    for senha in senhas:
        fp.write(str(senha) + '\n')

# primeiro milestone
## ordenando pela hora de emissão
lista_ordenada = sorted(senhas, key = lambda x: int(x['emissao']))

# segundo milestone
for i in range(len(lista_ordenada)):
    lista_ordenada[i]['naFrente'] = i

# requisição POST final
values = {'nome': nome, 'chave': chave, 'resultado': lista_ordenada}
data = urlencode(values).encode()

req = Request(post_to['url'], data)
with urlopen(req) as response:
    resp = response.read().decode('utf-8')
    with open('resultado.html', 'w') as resp_formatted:
        resp_formatted.write('<html><head><title>Resultado</title></head><body>' + resp + '</body></html>')
