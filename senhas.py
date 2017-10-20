#! /usr/bin/env python3

"""Arquivo com as soluções dos milestones do desafio
para o processo seletivo da SEAT."""

from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

def ordenar_senhas(senhas):
    """Ordena as senhas respeitando a prioridade de atendimento."""

    senhas = [senha for senha in senhas if 'chamada' not in senha.keys()]

    senhas_preferenciais = [senha for senha in senhas if senha['prioridade'] == 'preferencial']
    senhas_preferenciais = sorted(senhas_preferenciais, key = lambda x: int(x['emissao']))

    senhas_gerais = [senha for senha in senhas if senha['prioridade'] == 'geral']
    senhas_gerais = sorted(senhas_gerais, key = lambda x: int(x['emissao']))

    ## atendimento preferencial primeiro
    lista_ordenada = senhas_preferenciais + senhas_gerais

    return lista_ordenada

def senhas_na_frente(senhas):
    """Cria o campo 'naFrente' informando quantas senhas estão na frente
    (assume-se que as senhas estão ordenadas)."""

    for i in range(len(senhas)):
        senhas[i]['naFrente'] = i
    return senhas

def tempo_de_espera(senhas):
    """Cria-se o campo 'espera' com o tempo estimado de espera
    com base no tempo de espera da senha anterior mais o intervalo
    entre as emissões entre as senhas se esta for positiva."""

    senhas[0]['espera'] = 0
    for i in range(1, len(senhas)):
        senhas[i]['espera'] = senhas[i-1]['espera'] + max(0, senhas[i]['emissao'] - senhas[i-1]['emissao'])
    return senhas

def histograma(senhas):
    """Impressão do histograma de espera."""

    bins = {}
    for senha in senhas:
        key = senha['espera'] // (5 * 60 * 1000) # 5 mins em ms
        try:
            bins[key].append(senha)
        except:
            bins[key] = [senha]

    for b in range(max(bins.keys())):
        try:
            qtde = len(bins[b])
        except:
            qtde = 0
        else:
            print('< %03d mins: ' % ((b+1)*5) + '#' * qtde + ' ' + str(qtde))

def dump_das_senhas(senhas, arquivo='dump_senhas'):
    """Rotina que imprime as senhas em um arquivo para
    auxiliar na depuração."""

    with open(arquivo, 'w') as fp:
        for senha in senhas:
            fp.write(str(senha) + '\n')

if __name__ == "__main__":
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

    #----- Início do desafio -----#

    senhas = ordenar_senhas(senhas) # primeiro milestone
    senhas = senhas_na_frente(senhas) # segundo milestone
    senhas = tempo_de_espera(senhas) # terceiro milestone
    #histograma(senhas) # quarto milestone

    #----- Fim do desafio -----#

    dump_das_senhas(senhas)

    # requisição POST final
    resultado = json.dumps(senhas)
    values = {'nome': nome, 'chave': chave, 'resultado': resultado}
    data = urlencode(values).encode('utf-8')

    print(data)
    print(post_to['url'])

    post_to_url = post_to['url']

    req = Request(post_to_url, data)
    with urlopen(req) as response:
        resp = response.read().decode('utf-8')
        with open('resultado.html', 'w') as resp_formatted:
            resp_formatted.write('<html><head><title>Resultado</title></head><body>' + resp + '</body></html>')
