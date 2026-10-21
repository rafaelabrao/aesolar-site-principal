"""A capa (/). Ordem da diretriz A1 §5.1, com "quem está por trás" e "resultados" num bloco só."""
import blocos as b
import perguntas

CAMINHO = '/'
TITULO = 'AESOLAR | Energia por assinatura com usina própria em Goiás'
DESCRICAO = ('Até 30% de economia na parte da energia da conta, com usina própria em Goiás e sem obra. Simule em reais '
             'ou mande a fatura e receba o cálculo em até 24 horas.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = True
FAQ = ['precisa-instalar', 'continuo-pagando', 'quanto-economizo', 'quando-comeca', 'quem-pode', 'contrato-prazo',
       'mercado-livre']


def corpo(d):
    return (
        b.topo(d, CAMINHO, 'Só para empresas e condomínios de Goiás',
               'Desconto todo mundo promete. A gente mostra em reais.',
               f'Energia solar por assinatura: até {b.pct(d.of["desconto_max_pct"])} de economia na parte da energia da '
               f'conta, com usina própria em Goiás e sem obra. Mande a fatura e receba o cálculo em até '
               f'{d.of["proposta_horas"]} horas.')
        + b.pendente_bloco('D1', 'Aprovar o título e o subtítulo do topo (posicionamento).')
        + b.secao(b.passos(d, CAMINHO), 'sec-clara', 'como-funciona', 't-passos')
        + b.secao(b.usina(d), 'sec-escura', 'usina', 't-usina')
        + b.secao(b.letra_miuda(d), '', 'letra-miuda', 't-miuda')
        + b.secao(b.para_quem(d), 'sec-clara', 'para-quem', 't-quem')
        + b.secao(b.quem_somos(d), '', 'quem-somos', 't-somos')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ)), 'sec-clara', 'perguntas', 't-faq')
        + b.secao(b.contato(d, CAMINHO, SEGMENTO), 'sec-escura', 'contato', 't-contato')
    )


def schema(d):
    return [
        {'@type': 'WebSite', '@id': f'{d.site}/#site', 'url': f'{d.site}/', 'name': 'AESOLAR', 'inLanguage': 'pt-BR',
         'publisher': {'@id': f'{d.site}/#organizacao'}},
        b.servico(d, CAMINHO),
        b.faq_schema(perguntas.escolhe(d, FAQ)),
    ]
