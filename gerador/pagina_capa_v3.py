"""Protótipo v3 da capa (sessão A3): "a conta em reais".

O simulador é o topo: a pessoa digita a conta e vê a economia antes de qualquer outra coisa, com as duas contas
lado a lado; o passo seguinte, "mande a foto da fatura", vem desenhado como uma conversa. Usa fotos de banco
(provisórias, marcadas em dados.json) para Goiânia e para os segmentos.
Não indexada, fora do sitemap e dos menus; o --producao recusa publicar com ela no site.
"""
import blocos as b
import capas
import pagina_capa
import perguntas

CAMINHO = '/prototipos/capa-v3/'
TITULO = 'Protótipo v3 da capa: a conta em reais | AESOLAR'
DESCRICAO = pagina_capa.DESCRICAO
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = True
SEMPRE_NOINDEX = True
PROTOTIPO = True
CLASSE_BODY = 'capa-v3'
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
SPRITE_EXTRA = capas.sprite_extra
FAQ = pagina_capa.FAQ


def corpo(d):
    return (
        capas.topo_v3(d, CAMINHO)
        + b.pendente_bloco('D1', 'Aprovar o título do topo (proposta da A3).')
        + b.secao(f'<div class="revela">{capas.conversa_v3(d, CAMINHO)}</div>', 'sec-clara', 'como-funciona', 't-passos')
        + b.secao(f'<div class="revela">{capas.provas_v3(d)}</div>', '', 'provas', 't-provas')
        + b.secao(f'<div class="revela">{capas.mapa_v3(d)}</div>', 'sec-escura sec-mapa', 'onde', 't-mapa')
        + b.secao(f'<div class="revela">{capas.para_quem_v3(d)}</div>', 'sec-clara', 'para-quem', 't-quem')
        + b.secao(f'<div class="revela">{capas.muda(d)}</div>', '', 'letra-miuda', 't-miuda')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ)), 'sec-clara', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'goiania-noite', 'Céu de fim de tarde sobre os prédios de Goiânia',
                      'Sua economia em reais, com a sua conta de verdade.',
                      f'Mande a foto da fatura pelo WhatsApp. Em até {d.of["proposta_horas"]} horas, o cálculo completo, '
                      f'sem compromisso.')
    )


def schema(d):
    return [b.servico(d, CAMINHO), b.faq_schema(perguntas.escolhe(d, FAQ))]
