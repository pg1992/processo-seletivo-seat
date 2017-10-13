#! /usr/bin/env python3

from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

url = 'http://seat.ind.br/processo-seletivo/desafio-2017-03.php'
values = {'nome' : 'Pedro Guilherme Siqueira Moreira'}

data = urlencode(values)
full_url = url + '?' + data
req = Request(full_url)
with urlopen(req) as response:
    resp = json.loads(response.read().decode('utf-8'))
    senhas = resp['input']
    chave = resp['chave']
    post_to = resp['postTo']
    nome = resp['nome']
for senha in senhas:
    print(senha)
print('\nTotal de %d senhas' % len(senhas))
print('Chave: %s' % chave)
print('Postar para %s' % str(post_to))
print('Nome: "%s"' % nome)
