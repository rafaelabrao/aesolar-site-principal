"""A capa (/), para quem já ouviu falar da AESOLAR e quer saber se é séria (decisão D19, 26/10/2026).
A usina real ocupa a primeira tela, com o título curto e o número em reais logo ali; o simulador fica ao lado no
computador e logo abaixo no celular. Depois, a prova com contas de clientes e o resto da página. Só fotos reais."""
import blocos as b
import capas
import perguntas

CAMINHO = '/'
TITULO = 'AESOLAR | Energia solar por assinatura em Goiás'
DESCRICAO = ('Energia solar por assinatura para empresas e condomínios de Goiás: até 30% de economia na parte da energia, '
             'sem obra e sem investimento.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = True
CLASSE_BODY = 'capa-v2'
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
PRELOAD = capas.preload('vereda-entardecer-larga', ('vereda-entardecer-retrato', 699))
SPRITE_EXTRA = capas.sprite_extra
FAQ = ['precisa-instalar', 'continuo-pagando', 'quanto-economizo', 'quando-comeca', 'quem-pode', 'contrato-prazo',
       'mercado-livre']


def corpo(d):
    return (
        capas.topo_v2(d, CAMINHO)
        + b.secao(capas.numeros(d), 'sec-num', 'numeros', 't-numeros')
        + b.secao(f'<div class="revela">{capas.caso(d)}</div>', '', 'caso', 't-caso')
        + b.secao(f'<div class="revela">{capas.passos(d)}</div>'
                  f'<div class="contas2 revela" data-sem-barra><div><h3>Como fica a sua conta</h3><p><strong>Você continua '
                  f'pagando a Equatorial.</strong> A conta dela fica menor e chega uma segunda, da AESOLAR, com o desconto. '
                  f'A soma das duas é que fica mais barata.</p></div>{capas.contas_espelho(d)}'
                  f'<p class="contas2-bt">{b.wa(d, b.MSG_FATURA, "capa:conta", "Quero o cálculo da minha conta")}</p></div>',
                  'sec-clara', 'como-funciona', 't-passos')
        + capas.usina_v2(d)
        + b.secao(f'<div class="revela">{capas.vantagens(d)}</div>', '', 'vantagens', 't-vant')
        + b.secao(f'<div class="revela">{capas.mapa(d)}</div>', 'sec-escura sec-mapa', 'onde', 't-mapa')
        + b.secao(f'<div class="revela">{capas.para_quem_v2(d)}</div>', 'sec-clara', 'para-quem', 't-quem')
        + b.secao(capas.quem(d), 'sec-escura sec-quem', 'quem-somos', 't-somos')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ)), '', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'vereda-ceu', 'Fileira de painéis do Complexo Vereda sob céu de nuvens, em Goiás',
                      f'Sua conta, em reais, em até {d.of["proposta_horas"]} horas.',
                      'Mande uma foto da última conta da Equatorial. A gente devolve quanto você paga hoje e quanto vai '
                      'pagar com a AESOLAR.')
    )


def schema(d):
    return [
        {'@type': 'WebSite', '@id': f'{d.site}/#site', 'url': f'{d.site}/', 'name': 'AESOLAR', 'inLanguage': 'pt-BR',
         'publisher': {'@id': f'{d.site}/#organizacao'}},
        b.servico(d, CAMINHO),
        b.faq_schema(perguntas.escolhe(d, FAQ)),
    ]
