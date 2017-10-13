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

# primeiro milestone
## ordenando pela hora de emissão e separação
senhas_preferenciais = [senha for senha in senhas if senha['prioridade'] == 'preferencial']
senhas_preferenciais = sorted(senhas_preferenciais, key = lambda x: int(x['emissao']))

senhas_gerais = [senha for senha in senhas if senha['prioridade'] == 'geral']
senhas_gerais = sorted(senhas_gerais, key = lambda x: int(x['emissao']))

## atendimento preferencial primeiro
lista_ordenada = senhas_preferenciais + senhas_gerais

#-------------------------------------------------------------------------------

# segundo milestone
for i in range(len(lista_ordenada)):
    lista_ordenada[i]['naFrente'] = i

# dump das senhas
with open('dump_senhas', 'w') as fp:
    for senha in lista_ordenada:
        fp.write(str(senha) + '\n')

# requisição POST final
values = {'nome': nome, 'chave': chave, 'resultado': lista_ordenada}
data = urlencode(values).encode()

req = Request(post_to['url'], data)
with urlopen(req) as response:
    resp = response.read().decode('utf-8')
    with open('resultado.html', 'w') as resp_formatted:
        resp_formatted.write('<html><head><title>Resultado</title></head><body>' + resp + '</body></html>')

if __name__ == "__main__":
    pass
