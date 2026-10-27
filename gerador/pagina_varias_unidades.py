"""/empresas-com-varias-unidades/: redes, franquias e empresas com filiais em Goiás (7 de 24 titulares da carteira em
ago/2026 têm mais de uma unidade). Busca: "energia para empresa com filiais", "energia solar para rede de lojas".
O que vende aqui é a cobrança única (D14) e a conferência de cada unidade (D3). Mesmo molde das outras páginas de
segmento; o texto é só desta página."""
import blocos as b
import capas
import perguntas

CAMINHO = '/empresas-com-varias-unidades/'
TITULO = 'Energia solar para empresas com filiais em Goiás | AESOLAR'
# A prévia no WhatsApp e no Facebook (gerador/prepara_assets.py compartilhar): título e linha de baixo.
COMPARTILHAR = ('Todas as unidades.\nUma cobrança só.', 'Energia solar por assinatura para redes e filiais em Goiás')
DESCRICAO = ('Todas as unidades da sua empresa em Goiás numa proposta só e numa cobrança única da AESOLAR, com os créditos '
             'de cada unidade conferidos todo mês.')
CABECALHO = 'completo'
SEGMENTO = 'varias_unidades'
SIMULADOR = True
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
SPRITE_EXTRA = capas.sprite_extra
MIGALHAS = [('Início', '/'), ('Empresas com várias unidades', None)]
EXEMPLO = 20000  # a soma das contas de algumas unidades


def faq_vu(d):
    mn = b.reais(d.of['minimo_conta'])
    return [
        {'id': 'vu-minimo', 'p': f'O mínimo de {mn} vale para cada unidade?',
         'r': f'<p>Não. Vale a soma: unidades com conta pequena entram junto com as outras, desde que todas somem a partir de '
              f'{mn} por mês.</p>'},
        {'id': 'vu-cidades', 'p': 'As unidades ficam em cidades diferentes de Goiás. Pode?',
         'r': '<p>Pode, desde que todas sejam atendidas pela Equatorial Goiás, inclusive no Entorno do DF. Unidade no Distrito '
              'Federal fica de fora: lá a distribuidora é outra.</p>'},
    ]


FAQ = ['varias-unidades', 'conferencia', 'continuo-pagando', 'quando-comeca', 'alta-tensao', 'contrato-prazo']


def corpo(d):
    of = d.of
    itens = faq_vu(d) + perguntas.escolhe(d, FAQ)
    return (
        capas.topo_seg(
            d, CAMINHO, 'Redes e filiais · Goiás',
            'Todas as unidades.<br><em>Uma cobrança só.</em>',
            f'Energia solar por assinatura para rede, franquia ou empresa com filiais em Goiás: a energia da nossa usina vira crédito na conta de cada unidade '
            f'na Equatorial, e a AESOLAR cobra tudo numa fatura só. Até {b.pct(of["desconto_max_pct"])} de economia na '
            f'parte da energia, sem obra em nenhuma unidade.',
            'ia-varias-unidades', 'Três lojas da mesma rede, lado a lado, ao anoitecer',
            'A conta das suas unidades, em reais', EXEMPLO, 'Soma das contas de todas as unidades, por mês')
        + b.secao(f'<div class="revela">{capas.caso(d, ["bar-goiania"])}</div>', '', 'caso', 't-caso')
        + b.secao('<div class="revela">' + capas.muda(
            'Cada unidade com a sua conta. A da AESOLAR, uma só.',
            '<p>Quem tem várias unidades já gasta tempo conferindo uma conta de luz por endereço. Com a assinatura, cada '
            'unidade continua recebendo a conta dela da Equatorial, menor, e a AESOLAR soma todas numa cobrança única. A '
            'proposta mostra o cálculo de cada unidade e o total.</p>',
            ['Uma proposta para todas as unidades, cada uma com o seu cálculo.',
             'Uma cobrança só da AESOLAR, somando todas.',
             'Todo mês, a gente confere os créditos de cada unidade.'],
            ['Cada unidade continua com a conta dela da Equatorial.',
             'Nada é instalado em nenhuma unidade.',
             'Unidade no interior ou no Entorno do DF também entra. No Distrito Federal, não.'],
            'Para quem tem várias unidades') + '</div>', 'sec-clara', 'unidades', 't-seg')
        + b.secao('<div class="revela">' + capas.cartoes('Por que a AESOLAR', 'Mais unidades, menos conta para conferir', [
            ('recibo', 'Uma cobrança só',
             'Em vez de um boleto por unidade, uma fatura da AESOLAR com todas somadas. O financeiro paga uma conta e '
             'pronto.'),
            ('escudo', 'Conferência unidade por unidade',
             'Com várias contas, um crédito que não entrou passa despercebido. Todo mês a gente confere cada unidade na '
             'Equatorial e pede a correção quando algo vem errado.'),
            ('caneta', 'Contrato com prazo claro',
             f'{of["contrato_meses"]} meses. Para sair ao fim do prazo, sem custo, basta avisar com '
             f'{of["aviso_saida_dias"]} dias. Depois, o contrato segue sem prazo e sem multa de saída.'),
        ]) + '</div>', '', 'diferenciais', 't-dif')
        + b.secao(f'<div class="revela">{capas.passos_seg(d, CAMINHO, "Três passos. Todas as unidades de uma vez.")}</div>',
                  'sec-clara', 'como-funciona', 't-passos')
        + capas.usina_v2(d)
        + b.secao(b.perguntas_bloco(d, itens, 'Dúvidas de quem tem várias unidades'), '', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'vereda-ceu', 'Fileira de painéis do Complexo Vereda sob céu de nuvens, em Goiás',
                      'Mande as faturas. A gente soma e devolve em reais.',
                      f'Uma foto ou o PDF da última conta de cada unidade, pelo WhatsApp. Em até {of["proposta_horas"]} horas, '
                      f'o cálculo de cada uma e o total, sem compromisso.', SEGMENTO)
    )


def schema(d):
    itens = faq_vu(d) + perguntas.escolhe(d, FAQ)
    return [b.servico(d, CAMINHO, 'empresas com várias unidades'), b.faq_schema(itens), b.migalhas_schema(d, MIGALHAS)]
