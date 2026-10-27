"""/usinas/: a prova de que a usina existe. Só foto real, do banco da Academia (sem GPS). Sem potência, capacidade
ou quantidade de usinas (regra da marca)."""
import blocos as b

CAMINHO = '/usinas/'
TITULO = 'Nossas usinas solares em Goiás | AESOLAR'
DESCRICAO = ('Conheça o Complexo Vereda, a principal usina solar da Boreal Solar, a cerca de 30 km de Goiânia: é de lá que '
             'vem a energia por assinatura da AESOLAR.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = False
MIGALHAS = [('Início', '/'), ('Nossas usinas', None)]
FOTO_TOPO = 'vereda-aerea'  # o maior bloco da tela no celular: pré-carregado

GALERIA = [
    ('vereda-paineis', 'Painéis solares do Complexo Vereda em operação, com céu aberto', 'Painéis em operação.'),
    ('vereda-entardecer', 'Fileira de painéis solares no fim da tarde', 'Fim de tarde na usina.'),
    ('vereda-inversores', 'Casa de inversores do Complexo Vereda, com a ligação à rede elétrica',
     'Casa de inversores e ligação com a rede da Equatorial.'),
    ('vereda-inversores-dentro', 'Inversores instalados na parede da casa de inversores',
     'Inversores: transformam a energia dos painéis na energia da rede.'),
]


def corpo(d):
    galeria = ''.join(
        f'<figure class="gal-item">{b.foto(n, alt, "(min-width: 900px) 520px, calc(100vw - 32px)")}<figcaption>{leg}</figcaption></figure>'
        for n, alt, leg in GALERIA)
    caminho = [('sol', 'A usina gera', 'Os painéis transformam o sol em energia elétrica.'),
               ('tomada', 'A energia entra na rede', 'A usina injeta a energia na rede da Equatorial.'),
               ('recibo', 'Vira crédito na sua conta', 'A Equatorial lança os créditos na conta da sua unidade.'),
               ('check', 'Sua conta cai', 'Você paga a energia à AESOLAR, com desconto.')]
    trilha = '<ol class="trilha">' + ''.join(
        f'<li>{b.icone(i, "ic ic-cartao")}<h3>{t}</h3><p>{x}</p></li>' for i, t, x in caminho) + '</ol>'
    return (
        b.cabeca_pagina('Nossas usinas', 'A usina é nossa, e fica em Goiás',
                        'A energia da AESOLAR vem de usinas da Boreal Solar em diversas regiões de Goiás. A principal é o '
                        'Complexo Vereda, a cerca de 30 km de Goiânia, em operação desde 2023.', MIGALHAS)
        + b.secao(f'<figure class="foto-grande">{b.foto("vereda-aerea", "Vista aérea do Complexo Vereda, usina solar da Boreal Solar em Goiás", lazy=False)}'
                  '<figcaption>Complexo Vereda, visto de cima. Todas as fotos desta página são reais e sem retoque.'
                  '</figcaption></figure>', 'sec-foto')
        + b.secao('<h2 id="t-caminho">Da usina até a sua conta</h2>' + trilha, '', 'caminho', 't-caminho')
        + b.secao(f'<h2 id="t-galeria">Por dentro da usina</h2><div class="galeria">{galeria}</div>', 'sec-clara',
                  'galeria', 't-galeria')
        + b.secao('<div class="estreito"><h2 id="t-porque">Por que ter usina própria importa</h2>'
                  '<p>Quem tem a usina responde por ela. As usinas são da Boreal Solar, a mesma empresa que opera a '
                  'AESOLAR.</p><p>Para você, isso quer dizer saber de onde vem a energia da sua empresa e com quem falar se '
                  'algo não sair como combinado.</p></div>', '', 'por-que', 't-porque')
        + b.cta_final(d, CAMINHO)
    )


def schema(d):
    return [b.migalhas_schema(d, MIGALHAS)]
