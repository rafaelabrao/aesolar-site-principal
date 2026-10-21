"""/termos-de-uso/: rascunho para a revisão jurídica (D6)."""
import blocos as b

CAMINHO = '/termos-de-uso/'
TITULO = 'Termos de uso do site | AESOLAR'
DESCRICAO = ('Regras de uso do site da AESOLAR: o simulador é uma estimativa, a proposta vale depois da análise da fatura e '
             'o contrato é o que define as condições.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = False
MIGALHAS = [('Início', '/'), ('Termos de uso', None)]


def corpo(d):
    emp, of = d.emp, d.of
    return (
        b.cabeca_pagina('Regras do site', 'Termos de uso', 'O que vale para quem usa este site.', MIGALHAS)
        + b.secao(
            '<div class="texto-legal">'
            + b.pendente_bloco('D6', 'Rascunho para a revisão jurídica.')
            + f'<h2>Quem somos</h2><p>Este site é da {emp["razao_social"]}, CNPJ {emp["cnpj"]}, com sede em {emp["cidade"]}-'
            f'{emp["uf"]}, operada pela Boreal Solar.</p>'
            '<h2>O simulador é uma estimativa</h2><p>O simulador usa premissas que aparecem logo abaixo do resultado (tarifa, '
            'faixa de desconto, bandeira verde, baixa tensão). Ele não é proposta nem promessa de economia. O valor que vale é '
            'o da proposta, feita a partir da sua fatura.</p>'
            f'<h2>A proposta</h2><p>A proposta é feita depois da análise da fatura, depende de haver energia disponível na '
            f'usina e vale por {of["validade_proposta_dias"]} dias corridos. As condições da assinatura são as do contrato '
            f'que você assina.</p>'
            '<h2>Quem pode contratar</h2><p>Empresas e condomínios atendidos pela Equatorial Goiás, inclusive no Entorno do DF. '
            f'O Distrito Federal não é atendido. Conta a partir de {b.reais(of["minimo_conta"])} por mês.</p>'
            '<h2>Conteúdo do site</h2><p>Textos, fotos e marcas são da AESOLAR e da Boreal Solar. As fotos das usinas são '
            'reais. Não use sem autorização.</p>'
            '<h2>Seus dados</h2><p>Estão na <a href="/politica-de-privacidade/">Política de privacidade</a>.</p>'
            f'<h2>Foro</h2><p>Fica eleito o foro de {emp["cidade"]}-{emp["uf"]}. '
            + b.pendente('D6', 'conferir com a advogada.') + '</p></div>', '', None)
    )


def schema(d):
    return [b.migalhas_schema(d, MIGALHAS)]
