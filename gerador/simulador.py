"""A conta do simulador, em Python, para os exemplos que saem escritos nas páginas.

O simulador da tela roda a mesma conta em site/assets/simulador.js. As duas têm de dar o mesmo número
(teste_gerador.py confere numa grade de valores): o exemplo escrito numa página nunca pode contradizer o
simulador da mesma página. Mudou a conta aqui, mude lá, na mesma ordem de operações.

A regra vem do cálculo de fatura do app (api/app/services/calculo_fatura.py, modo "Compartilhada"): a
AESOLAR cobra sobre a energia compensada e o desconto vale só sobre essa parte. Custo de disponibilidade,
iluminação pública e os tributos que a Equatorial continua cobrando ficam fora. Desconto sobre a conta
inteira é o erro do site antigo e nunca entra aqui.
"""
import math


def estima(conta, p):
    """conta: valor médio da conta em reais. p: o bloco "simulador" de dados.json.

    Devolve None abaixo do mínimo. Os valores saem arredondados PARA BAIXO (de R$ 10 em R$ 10 por mês,
    de R$ 100 em R$ 100 por ano): estimativa que erra, erra a favor de prometer menos."""
    if conta < p['minimo_conta']:
        return None
    kwh = conta * (1 - p['fora_do_desconto_pct'] / 100) / p['tarifa_kwh']
    kwh_abatido = max(0, kwh - p['disponibilidade_kwh'])
    abatido = kwh_abatido * p['tarifa_kwh'] * (1 - p['tributos_que_ficam_pct'] / 100)
    eco_min = abatido * p['desconto_min_pct'] / 100
    eco_max = abatido * p['desconto_max_pct'] / 100
    abatido_r = math.floor(abatido / 10) * 10
    return {
        'conta': conta,
        'abatido': abatido_r,
        'fora': conta - abatido_r,
        'min': math.floor(eco_min / 10) * 10,
        'max': math.floor(eco_max / 10) * 10,
        'ano_min': math.floor(eco_min * 12 / 100) * 100,
        'ano_max': math.floor(eco_max * 12 / 100) * 100,
        # as duas contas do mês, com o desconto mínimo (para o desenho de "como fica a conta")
        'equatorial_depois': conta - abatido_r,
        'aesolar_min': abatido_r - math.floor(eco_min / 10) * 10,
    }
