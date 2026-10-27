"""Perguntas frequentes. Cada página escolhe as suas pelo id; /perguntas-frequentes/ mostra todas, por grupo.
Números (mínimo, prazos) vêm de dados.json. Resposta com marca PENDENTE fica fora dos dados para o Google
(blocos.faq_schema) até a decisão sair."""
from blocos import pendente, pct, reais

GRUPOS = [('como', 'Como funciona'), ('conta', 'Sua conta e a economia'), ('quem', 'Quem pode contratar'),
          ('contrato', 'Contrato e segurança')]


def todas(d):
    of = d.of
    mn = reais(of['minimo_conta'])
    return [
        {'id': 'precisa-instalar', 'grupo': 'como', 'p': 'Preciso instalar placa ou fazer obra?',
         'r': '<p>Não. A energia é gerada nas usinas da Boreal Solar em Goiás e chega à sua empresa pela rede da Equatorial, '
              'que já existe. Nada muda na sua instalação.</p>'},
        {'id': 'continuo-pagando', 'grupo': 'conta', 'p': 'Continuo pagando a Equatorial?',
         'r': '<p>Sim. Você passa a receber duas contas: a da Equatorial, menor, e a da AESOLAR, com o desconto sobre a energia '
              'que a usina abateu. A soma das duas é que fica mais barata que a conta de hoje.</p>'},
        {'id': 'quanto-economizo', 'grupo': 'conta', 'p': 'Quanto vou economizar?',
         'r': f'<p>Até {pct(of["desconto_max_pct"])} na parte da energia que a usina abate. Iluminação pública, o custo mínimo '
              f'da Equatorial e parte dos tributos continuam, então a economia sobre a conta inteira é menor que isso. Por '
              f'isso a gente mostra o número em reais: use o <a href="/#simulador">simulador</a> ou mande a fatura e receba o '
              f'cálculo exato em até {of["proposta_horas"]} horas.</p>'},
        {'id': 'quando-comeca', 'grupo': 'como', 'p': 'Quanto tempo leva para começar?',
         'r': f'<p>Depois do contrato assinado, a Equatorial precisa cadastrar sua unidade na usina. Os créditos aparecem '
              f'em torno de {of["creditos_dias_normal"]} dias; o contrato prevê até {of["creditos_dias_contrato"]}. '
              f'Até lá, sua conta continua como está.</p>'},
        {'id': 'quem-pode', 'grupo': 'quem', 'p': 'Quem pode contratar?',
         'r': f'<p>Empresas e condomínios de Goiás atendidos pela Equatorial Goiás, inclusive no Entorno do DF (DDD 61), '
              f'com conta a partir de {mn} por mês. O Distrito Federal tem outra distribuidora e não é atendido.</p>'},
        {'id': 'varias-unidades', 'grupo': 'quem', 'p': 'Minha empresa tem várias unidades. Dá para incluir todas?',
         'r': '<p>Dá. A proposta pode reunir todas as unidades da Equatorial em Goiás em nome da mesma empresa, cada uma com o '
              'seu cálculo, e a cobrança da AESOLAR chega numa fatura só, somando todas as unidades.</p>'},
        {'id': 'alta-tensao', 'grupo': 'quem', 'p': 'Minha empresa é atendida em alta tensão. Serve?',
         'r': '<p>Hoje atendemos baixa tensão (Grupo B), que é o caso da maioria das empresas e condomínios. Alta tensão '
              '(Grupo A) ainda não faz parte da assinatura.</p>'},
        {'id': 'e-legal', 'grupo': 'contrato', 'p': 'Isso é permitido? É seguro?',
         'r': '<p>Sim. A geração compartilhada está prevista na Lei 14.300/2022 e nas regras da ANEEL. A energia da usina entra '
              'na rede da Equatorial e é a própria Equatorial que lança os créditos na sua conta.</p>'},
        {'id': 'por-que-associacao', 'grupo': 'contrato', 'p': 'Por que a AESOLAR é uma associação?',
         'r': '<p>Na geração compartilhada, a lei pede que quem recebe a energia esteja reunido em consórcio, cooperativa ou '
              'associação. A AESOLAR é essa associação, com CNPJ e sede em Goiânia, operada pela Boreal Solar, dona das '
              'usinas. Sua empresa entra como associada.</p>'},
        {'id': 'usina-gera-menos', 'grupo': 'conta', 'p': 'E se a usina gerar menos num mês?',
         'r': '<p>Você paga à AESOLAR pela energia que virou crédito na sua conta. Num mês de menos geração, a conta da '
              'Equatorial sobe um pouco e a da AESOLAR vem menor.</p>'},
        {'id': 'falta-luz', 'grupo': 'como', 'p': 'Se faltar luz, com quem eu falo?',
         'r': '<p>Com a Equatorial, como hoje. A rede, a ligação e a manutenção continuam com ela. A AESOLAR cuida da energia '
              'da usina e dos créditos na sua conta.</p>'},
        {'id': 'conferencia', 'grupo': 'conta', 'p': 'Quem confere se os créditos vieram certos?',
         'r': '<p>A AESOLAR. Todo mês a gente confere, na sua conta da Equatorial, se os créditos da usina entraram certos. '
              'Você só paga à AESOLAR pela energia que virou crédito; a conferência existe para que nenhum crédito fique '
              'para trás e você não pague à Equatorial, com a tarifa cheia, uma energia que a usina já gerou para você. Se '
              'algo vier errado, a gente pede a correção.</p>'},
        {'id': 'contrato-prazo', 'grupo': 'contrato', 'p': 'Quanto tempo dura o contrato? Como faço para sair?',
         'r': f'<p>O contrato é de {of["contrato_meses"]} meses: o tempo de a economia aparecer em várias contas seguidas. '
              f'Para sair ao fim desse prazo, sem custo, basta avisar com {of["aviso_saida_dias"]} dias de antecedência: '
              f'quem avisa no {of["contrato_meses"] - of["aviso_saida_dias"] // 30}º mês sai no {of["contrato_meses"]}º. '
              f'Se você ficar, o contrato continua sem prazo e você sai quando quiser, sem multa. Todas as condições estão '
              f'no contrato, que você lê antes de assinar.</p>'},
        {'id': 'mercado-livre', 'grupo': 'contrato', 'p': 'Vale esperar o mercado livre de energia?',
         'r': '<p>A lei prevê abrir o mercado livre para empresas em baixa tensão a partir do fim de 2027, com regras que '
              'ainda estão sendo definidas. Até lá, a assinatura já reduz sua conta. Quando o mercado abrir, a gente avalia '
              'com você o que vale mais a pena.</p>'},
        {'id': 'meus-dados', 'grupo': 'contrato', 'p': 'O que vocês fazem com a minha fatura e os meus dados?',
         'r': '<p>Usamos só para calcular e preparar a sua proposta. Não vendemos seus dados. Eles ficam com a AESOLAR e com '
              'os serviços que usamos para guardar e atender, como a hospedagem e o WhatsApp. O detalhe está na <a href="/politica-de-privacidade/">Política de privacidade</a>.</p>'},
        {'id': 'quanto-custa', 'grupo': 'conta', 'p': 'Tem custo para começar?',
         'r': '<p>A análise da fatura é gratuita e sem compromisso. Não há equipamento para comprar nem obra para pagar.</p>'},
    ]


def escolhe(d, ids):
    por_id = {x['id']: x for x in todas(d)}
    faltam = [i for i in ids if i not in por_id]
    if faltam:
        from blocos import Erro
        raise Erro(f'Pergunta que não existe em perguntas.py: {", ".join(faltam)}')
    return [por_id[i] for i in ids]
