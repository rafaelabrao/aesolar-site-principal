"""Protótipo v2 da capa (sessão A3): "a usina em tela cheia".

A foto real do Complexo Vereda ocupa a primeira tela, com título curto e o número em reais logo ali; o simulador
fica ao lado no computador e logo abaixo no celular. Só fotos reais: esta versão não depende de banco de imagem.
Não indexada, fora do sitemap e dos menus; o --producao recusa publicar com ela no site.
"""
import blocos as b
import capas
import pagina_capa
import perguntas

CAMINHO = '/prototipos/capa-v2/'
TITULO = 'Protótipo v2 da capa: a usina em tela cheia | AESOLAR'
DESCRICAO = pagina_capa.DESCRICAO
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = True
SEMPRE_NOINDEX = True
PROTOTIPO = True
CLASSE_BODY = 'capa-v2'
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
PRELOAD = capas.preload('vereda-entardecer-larga', ('vereda-entardecer-retrato', 699))
SPRITE_EXTRA = capas.sprite_extra
FAQ = pagina_capa.FAQ


def corpo(d):
    return (
        capas.topo_v2(d, CAMINHO)
        + b.pendente_bloco('D1', 'Aprovar o título e o subtítulo do topo (proposta da A3).')
        + b.secao(capas.numeros(d), 'sec-num', 'numeros', 't-numeros')
        + b.secao(f'<div class="revela">{capas.passos(d)}</div>'
                  f'<div class="contas2 revela"><div><h3>Como fica a sua conta</h3><p><strong>Você continua pagando a '
                  f'Equatorial.</strong> A conta dela fica menor e chega uma segunda, da AESOLAR, com o desconto. A soma das '
                  f'duas é que fica mais barata.</p></div>{capas.contas_espelho(d)}</div>',
                  'sec-clara', 'como-funciona', 't-passos')
        + capas.usina_v2(d)
        + b.secao(f'<div class="revela">{capas.muda(d)}</div>', '', 'letra-miuda', 't-miuda')
        + b.secao(f'<div class="revela">{capas.para_quem_v2(d)}</div>', 'sec-clara', 'para-quem', 't-quem')
        + b.secao(capas.quem(d), 'sec-escura sec-quem', 'quem-somos', 't-somos')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ)), '', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'vereda-ceu', 'Fileira de painéis do Complexo Vereda sob céu de nuvens, em Goiás',
                      f'Sua conta, em reais, em até {d.of["proposta_horas"]} horas.',
                      'Mande uma foto da última conta da Equatorial. A gente devolve quanto você paga hoje e quanto vai '
                      'pagar com a AESOLAR.')
    )


def schema(d):
    return [b.servico(d, CAMINHO), b.faq_schema(perguntas.escolhe(d, FAQ))]
