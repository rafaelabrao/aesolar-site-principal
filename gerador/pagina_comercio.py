"""/comercio-e-servicos/: lojas, clínicas, escritórios, escolas e restaurantes (32 das 48 unidades da carteira em
ago/2026 são de comércio e serviços). Busca: "energia solar para comércio", "conta de luz alta comércio",
"desconto na conta de luz empresa". Mesmo molde das outras páginas de segmento; o texto é só desta página."""
import blocos as b
import capas
import perguntas

CAMINHO = '/comercio-e-servicos/'
TITULO = 'Energia solar para comércio e serviços em Goiás | AESOLAR'
DESCRICAO = ('Loja, clínica, escritório ou restaurante em Goiás: até 30% de economia na parte da energia da conta de luz, '
             'sem obra e sem fechar um dia. Simule em reais.')
CABECALHO = 'completo'
SEGMENTO = 'comercio'
SIMULADOR = True
SIM_HREF = '#simulador'
CSS_EXTRA = 'estilo_capas.css'
JS_EXTRA = ['capas.js']
SPRITE_EXTRA = capas.sprite_extra
MIGALHAS = [('Início', '/'), ('Comércio e serviços', None)]
EXEMPLO = 5000
FAQ_COM = [
    {'id': 'com-aluguel', 'p': 'Meu ponto é alugado. Posso contratar?',
     'r': '<p>Pode. Nada é instalado no imóvel, então não há obra para pedir ao proprietário. O que conta é a conta da '
          'Equatorial estar em nome da sua empresa.</p>'},
    {'id': 'com-mudar', 'p': 'E se eu mudar de endereço?',
     'r': '<p>Avise a gente. A energia da usina pode passar para a conta da Equatorial do endereço novo, desde que ele '
          'continue em Goiás e na área da Equatorial Goiás.</p>'},
]
FAQ = ['quanto-economizo', 'continuo-pagando', 'quando-comeca', 'quem-pode', 'usina-gera-menos', 'falta-luz',
       'contrato-prazo']


def corpo(d):
    of = d.of
    itens = FAQ_COM + perguntas.escolhe(d, FAQ)
    return (
        capas.topo_seg(
            d, CAMINHO, 'Comércio e serviços · Goiás',
            'Quanto o seu negócio <em>economiza</em> na conta de luz?',
            f'Loja, clínica, escritório, escola ou restaurante: a energia da nossa usina em Goiás vira crédito na sua conta '
            f'da Equatorial. Até {b.pct(of["desconto_max_pct"])} de economia na parte da energia, sem placa no telhado e '
            f'sem fechar um dia.',
            'ia-comercio', 'Padaria e mercearia de bairro com as luzes acesas',
            'A conta do seu negócio, em reais', EXEMPLO)
        + b.secao(f'<div class="revela">{capas.caso(d, ["bar-goiania"])}</div>', '', 'caso', 't-caso')
        + b.secao('<div class="revela">' + capas.muda(
            'Ar-condicionado, geladeira e luz acesa o dia inteiro. A conta vem alta todo mês.',
            '<p>No comércio, a energia é custo fixo: não dá para desligar a vitrine nem o ar da clínica. A assinatura reduz a '
            'parte da energia dessa conta sem você comprar equipamento, mexer na instalação ou parar o atendimento. O que '
            'sobra fica no caixa, todo mês.</p>',
            ['A conta da Equatorial fica menor.',
             'Chega a conta da AESOLAR, com o desconto sobre a energia que virou crédito.',
             'A soma das duas fica menor que a conta de hoje.'],
            ['Nada é instalado: o negócio não fecha nem um dia.',
             'O medidor, a ligação e o titular da conta continuam os mesmos.',
             'Ponto alugado também serve: não há obra no imóvel.',
             'Se faltar luz, você chama a Equatorial, como hoje.'],
            'Para quem tem comércio') + '</div>', 'sec-clara', 'comercio', 't-seg')
        + b.secao('<div class="revela">' + capas.cartoes('Por que a AESOLAR', 'Economia sem investimento e sem dor de cabeça', [
            ('recibo', 'Nada para comprar',
             f'Não há sistema para pagar nem financiamento para assumir. Os créditos começam em torno de '
             f'{of["creditos_dias_normal"]} dias depois do contrato, e a economia vem junto.'),
            ('escudo', 'A conta conferida por quem entende',
             'Todo mês, a gente confere na sua conta da Equatorial se os créditos da usina entraram certos, e pede a '
             'correção quando não entram. Você cuida do negócio.'),
            ('caneta', 'Contrato com prazo claro',
             f'{of["contrato_meses"]} meses. Para sair ao fim do prazo, sem custo, basta avisar com '
             f'{of["aviso_saida_dias"]} dias. Depois, o contrato segue sem prazo e sem multa de saída.'),
        ]) + '</div>', '', 'diferenciais', 't-dif')
        + b.secao(f'<div class="revela">{capas.passos_seg(d, CAMINHO, "Três passos. O negócio não para.")}</div>',
                  'sec-clara', 'como-funciona', 't-passos')
        + capas.usina_v2(d)
        + b.secao(b.perguntas_bloco(d, itens, 'Dúvidas de quem tem comércio'), '', 'perguntas', 't-faq')
        + capas.final(d, CAMINHO, 'vereda-entardecer-larga', 'Painéis do Complexo Vereda ao entardecer, em Goiás',
                      'Quanto sobra no seu caixa? Mande a fatura e veja.',
                      f'Uma foto ou o PDF da última conta da Equatorial, pelo WhatsApp. Em até {of["proposta_horas"]} horas, '
                      f'o cálculo em reais, sem compromisso.', SEGMENTO)
    )


def schema(d):
    itens = FAQ_COM + perguntas.escolhe(d, FAQ)
    return [b.servico(d, CAMINHO), b.faq_schema(itens), b.migalhas_schema(d, MIGALHAS)]
