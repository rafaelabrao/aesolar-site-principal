"""/como-funciona/: o passo a passo completo e as duas contas, com o exemplo em reais."""
import blocos as b
import perguntas

CAMINHO = '/como-funciona/'
TITULO = 'Como funciona a energia solar por assinatura | AESOLAR'
DESCRICAO = ('Passo a passo da energia solar por assinatura da AESOLAR: da fatura ao crédito na conta da Equatorial, '
             'com as duas contas do mês e um exemplo em reais.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = False
MIGALHAS = [('Início', '/'), ('Como funciona', None)]
FAQ = ['continuo-pagando', 'falta-luz', 'usina-gera-menos', 'alta-tensao']


def corpo(d):
    of = d.of
    etapas = [
        ('fatura', 'Você manda a fatura',
         'Uma foto ou o PDF da última conta da Equatorial, pelo WhatsApp. É dela que sai o cálculo: consumo, tipo de ligação e '
         'tarifa da sua unidade. A análise é gratuita.'),
        ('calculadora', 'A gente calcula em reais',
         f'Em até {of["proposta_horas"]} horas você recebe a proposta: quanto paga hoje, quanto vai pagar à Equatorial e à '
         f'AESOLAR, e quanto sobra no seu bolso por mês e por ano. A proposta vale por {of["validade_proposta_dias"]} dias.'),
        ('caneta', 'Você assina pelo celular',
         'O contrato e a procuração que permite cadastrar sua unidade na usina junto à Equatorial são assinados de forma '
         'digital. Sem cartório e sem visita.'),
        ('raio', 'A Equatorial cadastra sua unidade',
         f'A usina passa a mandar energia para a sua unidade. Os créditos aparecem em torno de '
         f'{of["creditos_dias_normal"]} dias; o contrato prevê até {of["creditos_dias_contrato"]}. Até lá, sua conta continua '
         f'como está.'),
        ('recibo', 'Todo mês, duas contas',
         'A da Equatorial, menor, e a da AESOLAR, com o desconto sobre a energia que virou crédito. E a gente confere, '
         'todo mês, se os créditos entraram certos na sua conta.'),
    ]
    lis = ''.join(f'<li class="etapa">{b.icone(i, "ic ic-etapa")}<div><h3>{t}</h3><p>{x}</p></div></li>'
                  for i, t, x in etapas)
    nao_muda = [
        'A rede, a ligação e o medidor continuam da Equatorial.',
        'Se faltar luz, você liga para a Equatorial, como hoje.',
        'Nada é instalado na sua empresa.',
        'O número da sua unidade e o titular da conta não mudam.',
    ]
    quem = [
        'Empresas e condomínios de Goiás atendidos pela Equatorial Goiás.',
        'Entorno do DF (DDD 61) também. O Distrito Federal não é atendido.',
        f'Conta a partir de {b.reais(of["minimo_conta"])} por mês, ou várias unidades somando isso.',
        'Baixa tensão (Grupo B). Alta tensão: mande a fatura que a gente avalia.',
    ]
    lista = lambda xs: '<ul class="lista-check">' + ''.join(f'<li>{b.icone("check")}<span>{x}</span></li>' for x in xs) + '</ul>'
    return (
        b.cabeca_pagina('Passo a passo', 'Como funciona a energia solar por assinatura',
                        'Da sua fatura ao crédito na conta da Equatorial, sem obra e sem comprar nada. E o que muda (e o '
                        'que não muda) na sua conta.', MIGALHAS)
        + b.secao(f'<h2 id="t-etapas">Do primeiro contato ao primeiro crédito</h2><ol class="etapas">{lis}</ol>', '',
                  'etapas', 't-etapas')
        + b.secao('<div class="duas-col"><div><p class="olho">Como fica a conta</p><h2 id="t-conta">A soma das duas contas '
                  'é que fica mais barata</h2><p>A conta da Equatorial cai, porque a energia da usina vira crédito. Por essa '
                  'energia você paga à AESOLAR, com desconto. O que fica fora do desconto (custo mínimo da ligação, '
                  'iluminação pública e parte dos tributos) continua na conta da Equatorial.</p>'
                  f'<p class="mais"><a href="/#simulador">Simular com a sua conta {b.icone("seta")}</a></p></div>'
                  f'<div>{b.duas_contas(d)}</div></div>', 'sec-clara', 'conta', 't-conta')
        + b.secao(f'<div class="duas-col"><div><h2 id="t-naomuda">O que não muda</h2>{lista(nao_muda)}</div>'
                  f'<div><h2>Quem pode contratar</h2>{lista(quem)}</div></div>', '', 'nao-muda', 't-naomuda')
        + b.secao(b.perguntas_bloco(d, perguntas.escolhe(d, FAQ), 'Dúvidas sobre o funcionamento'), 'sec-clara',
                  'perguntas', 't-faq')
        + b.cta_final(d, CAMINHO)
    )


def schema(d):
    return [b.faq_schema(perguntas.escolhe(d, FAQ)), b.migalhas_schema(d, MIGALHAS)]
