"""/perguntas-frequentes/: todas as perguntas de perguntas.py, por grupo."""
import blocos as b
import perguntas

CAMINHO = '/perguntas-frequentes/'
TITULO = 'Perguntas frequentes sobre energia por assinatura | AESOLAR'
DESCRICAO = ('Respostas diretas sobre a energia solar por assinatura da AESOLAR em Goiás: economia em reais, contas da '
             'Equatorial, prazos, contrato e quem pode contratar.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = False
MIGALHAS = [('Início', '/'), ('Perguntas frequentes', None)]


def corpo(d):
    todas = perguntas.todas(d)
    grupos = ''
    for gid, nome in perguntas.GRUPOS:
        itens = [x for x in todas if x['grupo'] == gid]
        grupos += (f'<div class="faq-grupo" id="g-{gid}">'
                   + b.perguntas_bloco(d, itens, nome, link=False, id_titulo=f't-{gid}').replace(
                       '<p class="olho">Dúvidas</p>', '') + '</div>')
    indice = '<nav class="faq-indice" aria-label="Grupos de perguntas"><ul>' + ''.join(
        f'<li><a href="#g-{gid}">{nome}</a></li>' for gid, nome in perguntas.GRUPOS) + '</ul></nav>'
    return (
        b.cabeca_pagina('Perguntas frequentes', 'Perguntas frequentes',
                        'O que todo empresário pergunta antes de assinar, respondido sem rodeio. Não achou a sua? Pergunte '
                        'pelo WhatsApp.', MIGALHAS)
        + b.secao(indice + grupos, '', 'perguntas', None)
        + b.cta_final(d, CAMINHO, 'Ficou alguma dúvida?', 'Mande a sua pergunta, ou a fatura, pelo WhatsApp. A análise é gratuita.')
    )


def schema(d):
    return [b.faq_schema(perguntas.todas(d)), b.migalhas_schema(d, MIGALHAS)]
