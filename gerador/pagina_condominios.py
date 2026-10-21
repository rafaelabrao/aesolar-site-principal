"""/condominios/: amostra da fase 2 (páginas por segmento). Em "previa_paginas" até o Rafael aprovar o texto."""
import blocos as b
import perguntas

CAMINHO = '/condominios/'
TITULO = 'Energia solar por assinatura para condomínios | AESOLAR'
DESCRICAO = ('Reduza a conta de luz das áreas comuns do condomínio com energia solar por assinatura, sem obra. Proposta em '
             'reais para o síndico levar à assembleia.')
CABECALHO = 'completo'
SEGMENTO = 'condominio'
SIMULADOR = True
MIGALHAS = [('Início', '/'), ('Condomínios', None)]
FAQ_CONDO = [
    {'id': 'condo-assembleia', 'p': 'Precisa de aprovação em assembleia?',
     'r': '<p>Depende da convenção do condomínio. Em muitos casos a decisão passa pela assembleia ou pelo conselho, e a '
          'proposta em reais é feita para essa conversa.</p>'},
    {'id': 'condo-moradores', 'p': 'Muda alguma coisa para os moradores?',
     'r': '<p>Não. A assinatura vale para a conta do condomínio (áreas comuns). As contas dos apartamentos e a instalação do '
          'prédio continuam iguais.</p>'},
    {'id': 'condo-sindico', 'p': 'E se o síndico mudar?',
     'r': '<p>O contrato é do condomínio, não do síndico. A troca de síndico não muda nada na assinatura.</p>'},
]
FAQ = ['continuo-pagando', 'quando-comeca', 'contrato-prazo']


def corpo(d):
    itens = FAQ_CONDO + perguntas.escolhe(d, FAQ)
    lista = lambda xs: '<ul class="lista-check">' + ''.join(f'<li>{b.icone("check")}<span>{x}</span></li>' for x in xs) + '</ul>'
    return (
        b.topo(d, CAMINHO, 'Para condomínios de Goiás', 'Energia solar por assinatura para condomínios',
               f'A conta das áreas comuns até {b.pct(d.of["desconto_max_pct"])} mais barata na parte da energia, sem obra no '
               f'prédio. A proposta sai em reais, pronta para o síndico levar à assembleia.',
               'Quanto o condomínio economiza, em reais')
        + b.secao('<div class="duas-col"><div><p class="olho">Para o síndico</p><h2 id="t-sindico">O que a assembleia vai '
                  'perguntar, respondido no papel</h2><p>Elevador, bombas, portaria e iluminação fazem da conta de luz uma das '
                  'maiores despesas fixas do condomínio. A proposta mostra, em reais, quanto o condomínio paga hoje e quanto '
                  'vai pagar: é o número que o síndico precisa para prestar contas.</p>'
                  + b.pendente_bloco('D17', 'Kit de assembleia (apresentação e modelo de ata): só anunciar quando existir.')
                  + '</div><div><h2>O que não muda no prédio</h2>'
                  + lista(['Nada é instalado no telhado nem na garagem.', 'A conta de cada apartamento continua igual.',
                           'A Equatorial continua cuidando da rede e da ligação.'])
                  + '</div></div>', '', 'sindico', 't-sindico')
        + b.secao(b.passos(d, CAMINHO), 'sec-clara', 'como-funciona', 't-passos')
        + b.secao(b.usina(d), 'sec-escura', 'usina', 't-usina')
        + b.secao(b.perguntas_bloco(d, itens, 'Dúvidas de síndico'), '', 'perguntas', 't-faq')
        + b.secao(b.contato(d, CAMINHO, SEGMENTO, 'Mande a conta do condomínio e receba o cálculo'), 'sec-escura', 'contato', 't-contato')
    )


def schema(d):
    itens = FAQ_CONDO + perguntas.escolhe(d, FAQ)
    return [b.servico(d, CAMINHO), b.faq_schema(itens), b.migalhas_schema(d, MIGALHAS)]
