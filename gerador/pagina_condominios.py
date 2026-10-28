"""/condominios/: para o síndico e o conselho. Busca: "energia solar para condomínio", "conta de luz condomínio".
Mesmo molde das outras páginas de segmento (capas.topo_seg); o texto é só desta página."""
import blocos as b
import capas
import perguntas

CAMINHO = '/condominios/'
TITULO = 'Energia solar por assinatura para condomínios | AESOLAR'
# A prévia no WhatsApp e no Facebook (gerador/prepara_assets.py compartilhar): título e linha de baixo.
COMPARTILHAR = ('Energia solar por assinatura para condomínios', 'Sem obra no prédio · Goiás')
DESCRICAO = ('Conta das áreas comuns do condomínio até 30% mais barata na parte da energia, sem obra no prédio. Simule em '
             'reais e receba a proposta para a assembleia.')
CABECALHO = 'completo'
SEGMENTO = 'condominio'
SIMULADOR = True
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
SPRITE_EXTRA = capas.sprite_extra
MIGALHAS = [('Início', '/'), ('Condomínios', None)]
EXEMPLO = 10000  # conta típica das áreas comuns de um prédio com elevador e bombas
FAQ_CONDO = [
    {'id': 'condo-assembleia', 'p': 'Precisa de aprovação em assembleia?',
     'r': '<p>Depende da convenção do condomínio. Em muitos casos a decisão passa pela assembleia ou pelo conselho, e a '
          'proposta em reais é feita para essa conversa: quanto o condomínio paga hoje, quanto vai pagar e o que fica de '
          'fora do desconto.</p>'},
    {'id': 'condo-moradores', 'p': 'Muda alguma coisa para os moradores?',
     'r': '<p>Não. A assinatura vale para a conta do condomínio (áreas comuns). As contas dos apartamentos e a instalação do '
          'prédio continuam iguais.</p>'},
    {'id': 'condo-sindico', 'p': 'E se o síndico mudar?',
     'r': '<p>O contrato é do condomínio, não do síndico. A troca de síndico não muda nada na assinatura.</p>'},
    {'id': 'condo-medidores', 'p': 'O condomínio tem mais de um medidor (torres, lazer, bombas). Entra tudo?',
     'r': '<p>Entra. Cada medidor da Equatorial em nome do condomínio recebe o seu cálculo, e a cobrança da AESOLAR chega '
          'numa fatura só, somando todos.</p>'},
]
FAQ = ['continuo-pagando', 'quando-comeca', 'contrato-prazo', 'e-legal']


def corpo(d):
    of = d.of
    itens = FAQ_CONDO + perguntas.escolhe(d, FAQ)
    return (
        capas.topo_seg(
            d, CAMINHO, 'Energia solar para condomínios · Goiás',
            'Quanto o seu condomínio <em>economiza</em> na conta de luz?',
            f'Elevador, bombas, portaria e iluminação pesam todo mês. Com a energia da nossa usina em Goiás, a conta das '
            f'áreas comuns fica até {b.pct(of["desconto_max_pct"])} mais barata na parte da energia, sem obra no prédio.',
            'ia-condominio', 'Prédio residencial ao anoitecer, com portaria, garagem e jardim iluminados',
            'A conta do condomínio, em reais', EXEMPLO, 'Conta das áreas comuns, por mês')
        + b.secao(f'<div class="revela">{capas.caso(d, ["condominio-goiania"])}</div>', '', 'caso', 't-caso')
        + b.secao('<div class="revela">' + capas.muda(
            'O número que a assembleia pede, em reais',
            '<p>A proposta mostra quanto o condomínio paga hoje e quanto vai pagar: a conta da Equatorial, a da AESOLAR e a '
            'soma das duas. É o que o síndico precisa para levar ao conselho e prestar contas. Não há investimento para '
            'aprovar nem obra para acompanhar.</p>',
            ['A conta das áreas comuns fica menor.',
             'Chega uma segunda conta, da AESOLAR, com o desconto sobre a energia que virou crédito.',
             'Todo mês, a gente confere se os créditos entraram certos na conta do condomínio.'],
            ['Nada é instalado no telhado, na garagem ou na casa de máquinas.',
             'A conta de cada apartamento continua igual.',
             'A Equatorial continua cuidando da rede e da ligação.',
             'O contrato é do condomínio: a troca de síndico não muda nada.'],
            'Para o síndico') + '</div>', 'sec-clara', 'sindico', 't-seg')
        + b.secao('<div class="revela">' + capas.cartoes('Por que a AESOLAR', 'Menos trabalho para o síndico, não mais', [
            ('escudo', 'Conferência todo mês',
             'A gente confere, na conta da Equatorial, se os créditos da usina entraram certos. Se vier errado, a gente pede '
             'a correção. O síndico não precisa virar especialista em fatura.'),
            ('recibo', 'Prestação de contas simples',
             'Todo mês, duas contas com valores claros: a da Equatorial, menor, e a da AESOLAR. A economia aparece no '
             'balancete.'),
            ('caneta', 'Contrato com prazo claro',
             f'{of["contrato_meses"]} meses. Para sair ao fim do prazo, sem custo, basta avisar com '
             f'{of["aviso_saida_dias"]} dias. Depois, o contrato segue sem prazo e sem multa de saída.'),
        ]) + '</div>', '', 'diferenciais', 't-dif')
        + b.secao(f'<div class="revela">{capas.passos_seg(d, CAMINHO, "Três passos. Nenhuma obra no prédio.")}</div>',
                  'sec-clara', 'como-funciona', 't-passos')
        + capas.usina_v2(d, 'conta do condomínio')
        + b.secao(b.perguntas_bloco(d, itens, 'Dúvidas de síndico'), '', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'vereda-ceu', 'Fileira de painéis do Complexo Vereda sob céu de nuvens, em Goiás',
                      'Mande a conta do condomínio. A gente devolve o número para a assembleia.',
                      f'Uma foto ou o PDF da última conta da Equatorial. Em até {of["proposta_horas"]} horas, quanto o '
                      f'condomínio paga hoje e quanto vai pagar com a AESOLAR, em reais.', SEGMENTO)
    )


def schema(d):
    itens = FAQ_CONDO + perguntas.escolhe(d, FAQ)
    return [b.servico(d, CAMINHO, 'condomínios'), b.faq_schema(itens), b.migalhas_schema(d, MIGALHAS)]
