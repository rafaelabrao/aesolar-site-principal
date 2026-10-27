"""/representante/: público separado do cliente. É "Representante Autorizado AESOLAR", nunca "AESOLAR" solto."""
import blocos as b

CAMINHO = '/representante/'
TITULO = 'Seja Representante Autorizado AESOLAR em Goiás'
DESCRICAO = ('Conhece empresários e síndicos em Goiás? Você apresenta a AESOLAR; a gente faz a proposta, o contrato e a '
             'gestão. Comissão por cliente fechado.')
CABECALHO = 'completo'
SEGMENTO = 'representante'
SIMULADOR = False
MIGALHAS = [('Início', '/'), ('Seja representante', None)]
MSG = 'Quero ser Representante Autorizado AESOLAR.'


def corpo(d):
    lista = lambda xs: '<ul class="lista-check">' + ''.join(f'<li>{b.icone("check")}<span>{x}</span></li>' for x in xs) + '</ul>'
    quem = ['Corretores, consultores e contadores que atendem empresas.', 'Administradoras de condomínio e síndicos profissionais.',
            'Quem vende para empresas em Goiás e tem uma boa rede de contatos.']
    divisao = [('pessoas', 'Você', 'Apresenta a AESOLAR, pega a fatura e acompanha o cliente até a assinatura.'),
               ('calculadora', 'A AESOLAR', 'Faz o cálculo, a proposta em reais, o contrato e a gestão da energia todo mês.'),
               ('recibo', 'A comissão', 'Por cliente fechado, com a regra por escrito no seu contrato.')]
    cartoes = ''.join(f'<li class="cartao">{b.icone(i, "ic ic-cartao")}<h3>{t}</h3><p>{x}</p></li>' for i, t, x in divisao)
    recebe = ['Kit de apresentação com o seu nome, foto, cidade, WhatsApp e link próprio.',
              'Treinamento da Academia AESOLAR.', 'Acesso ao app para acompanhar os seus clientes e propostas.']
    regras = ['Atende só Goiás, inclusive o Entorno do DF atendido pela Equatorial Goiás.',
              'Apresenta-se sempre como Representante Autorizado AESOLAR.',
              f'Fala em economia de até {b.pct(d.of["desconto_max_pct"])}, nunca em percentual fixo ou garantido.']
    return (
        b.cabeca_pagina('Para representantes', 'Seja Representante Autorizado AESOLAR',
                        'Você conhece empresários e síndicos em Goiás. A gente tem a usina, o sistema e a proposta em reais. '
                        'Juntos, a conversa fica fácil.', MIGALHAS)
        + b.secao(f'<h2 id="t-divisao">Quem faz o quê</h2><ul class="cartoes cartoes-3">{cartoes}</ul>', '', 'divisao', 't-divisao')
        + b.secao(f'<div class="duas-col"><div><h2 id="t-perfil">Para quem é</h2>{lista(quem)}</div>'
                  f'<div><h2>O que você recebe</h2>{lista(recebe)}</div></div>', 'sec-clara', 'perfil', 't-perfil')
        + b.secao(f'<div class="estreito"><h2 id="t-regras">As regras do jogo</h2>{lista(regras)}</div>', '', 'regras', 't-regras')
        + b.secao(f'<div class="cta"><h2>Quer conversar?</h2><p>Chame no WhatsApp e diga a sua cidade e com que tipo de '
                  f'cliente você trabalha.</p><div class="cta-bt">'
                  f'{b.wa(d, MSG, "representante:final", "Quero ser representante")}</div></div>', 'sec-escura')
    )


def schema(d):
    return [b.migalhas_schema(d, MIGALHAS)]
