"""/energia-solar-por-assinatura-goias/: o destino do anúncio de Pesquisa do Google, para quem busca economia
(decisão D19, 26/10/2026). O simulador é o topo: a pessoa digita a conta e vê a economia em reais antes de qualquer
outra coisa. Cabeçalho enxuto: quem vem do anúncio não precisa de menu; os sitelinks levam às outras páginas."""
import blocos as b
import capas
import perguntas

CAMINHO = '/energia-solar-por-assinatura-goias/'
TITULO = 'Energia solar por assinatura em Goiás | AESOLAR'
DESCRICAO = ('Para empresas e condomínios de Goiás: simule em reais quanto a sua conta de luz cai com a energia da nossa '
             'usina, sem obra. Cálculo exato em até 24 horas.')
CABECALHO = 'enxuto'
SEGMENTO = 'geral'
SIMULADOR = True
CLASSE_BODY = 'capa-v3'
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
SPRITE_EXTRA = capas.sprite_extra
MIGALHAS = [('Início', '/'), ('Energia solar por assinatura em Goiás', None)]
FAQ = ['precisa-instalar', 'continuo-pagando', 'quanto-economizo', 'quando-comeca', 'quem-pode', 'contrato-prazo',
       'mercado-livre']


def corpo(d):
    return (
        capas.topo_v3(d, CAMINHO)
        + b.secao(f'<div class="revela">{capas.caso(d)}</div>', '', 'caso', 't-caso')
        + b.secao(f'<div class="revela">{capas.conversa_v3(d, CAMINHO)}</div>', 'sec-clara', 'como-funciona', 't-passos')
        + b.secao(f'<div class="revela">{capas.provas_v3(d)}</div>', '', 'provas', 't-provas')
        + b.secao(f'<div class="revela">{capas.mapa(d)}</div>', 'sec-escura sec-mapa', 'onde', 't-mapa')
        + b.secao(f'<div class="revela">{capas.para_quem_v3(d)}</div>', 'sec-clara', 'para-quem', 't-quem')
        + b.secao(f'<div class="revela">{capas.vantagens(d)}</div>', '', 'vantagens', 't-vant')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ)), 'sec-clara', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'ia-fatura', 'Mãos fotografando uma conta de luz com o celular, no balcão de um comércio',
                      'Sua economia em reais, com a sua conta de verdade.',
                      f'Mande a foto da fatura pelo WhatsApp. Em até {d.of["proposta_horas"]} horas, o cálculo completo, '
                      f'sem compromisso.')
    )


def schema(d):
    return [b.servico(d, CAMINHO), b.faq_schema(perguntas.escolhe(d, FAQ)), b.migalhas_schema(d, MIGALHAS)]
