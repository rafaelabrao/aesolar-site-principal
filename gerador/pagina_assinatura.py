"""/energia-solar-por-assinatura-goias/: o destino do anúncio de Pesquisa do Google (plano de anúncios de 16/10).
Cabeçalho enxuto: quem vem do anúncio não precisa de menu; os sitelinks levam às outras páginas."""
import blocos as b
import perguntas

CAMINHO = '/energia-solar-por-assinatura-goias/'
TITULO = 'Energia solar por assinatura em Goiás | AESOLAR'
DESCRICAO = ('Para empresas e condomínios de Goiás: até 30% de economia na parte da energia, com usina própria no estado. '
             'Cálculo em reais em até 24 horas.')
CABECALHO = 'enxuto'
SEGMENTO = 'geral'
SIMULADOR = True
MIGALHAS = [('Início', '/'), ('Energia solar por assinatura em Goiás', None)]
FAQ = ['precisa-instalar', 'continuo-pagando', 'quanto-economizo', 'quando-comeca', 'quem-pode', 'e-legal',
       'quanto-custa']


def o_que_e(d):
    return (
        '<div class="duas-col"><div><p class="olho">O que é</p>'
        '<h2 id="t-oque">Você assina a energia de uma usina solar, sem comprar nada</h2>'
        '<p>Sua empresa reserva uma parte da energia de uma usina solar em Goiás. A usina gera, a energia entra na rede da '
        'Equatorial e volta como crédito na sua conta de luz. Você paga essa energia à AESOLAR, com desconto, e paga à '
        'Equatorial só o que sobra.</p>'
        '<p>Sem comprar placa, sem obra e sem investimento. O nome técnico é <strong>geração compartilhada</strong>, e ela está '
        'prevista na Lei 14.300/2022.</p></div>'
        f'<div>{b.duas_contas(d)}</div></div>')


def corpo(d):
    return (
        b.topo(d, CAMINHO, 'Para empresas e condomínios de Goiás',
               'Energia solar por assinatura para empresas de Goiás',
               f'Até {b.pct(d.of["desconto_max_pct"])} de economia na parte da energia, com usina própria no estado. Mande '
               f'a fatura e receba o cálculo em reais em até {d.of["proposta_horas"]} horas.')
        + b.secao(o_que_e(d), '', 'o-que-e', 't-oque')
        + b.secao(b.passos(d, CAMINHO), 'sec-clara', 'como-funciona', 't-passos')
        + b.secao(b.usina(d), 'sec-escura', 'usina', 't-usina')
        + b.secao(b.letra_miuda(d), '', 'letra-miuda', 't-miuda')
        + b.secao(b.para_quem(d), 'sec-clara', 'para-quem', 't-quem')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ)), '', 'perguntas', 't-faq')
        + b.secao(b.contato(d, CAMINHO, SEGMENTO), 'sec-escura', 'contato', 't-contato')
    )


def schema(d):
    return [b.servico(d, CAMINHO), b.faq_schema(perguntas.escolhe(d, FAQ)), b.migalhas_schema(d, MIGALHAS)]
