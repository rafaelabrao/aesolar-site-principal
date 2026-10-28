#!/usr/bin/env python3
"""Testes do gerador e do simulador. Rodar na raiz do repositório:

    python3 gerador/teste_gerador.py

Precisa do node (para rodar o simulador.js de verdade). Não grava nada em site/.
"""
import copy
import json
import os
import subprocess
import sys
import unittest
from datetime import date

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import blocos as b  # noqa: E402
import capas  # noqa: E402
import gera_site as g  # noqa: E402
import pagina_capa  # noqa: E402
import pagina_capa as pagina_capa_v2, pagina_assinatura as pagina_capa_v3  # noqa: E402,E401  as duas capas
from blocos import Erro  # noqa: E402
from simulador import estima  # noqa: E402

with open(os.path.join(AQUI, 'dados.json'), encoding='utf-8') as f:
    BRUTO = json.load(f)


def dados(**troca):
    b = copy.deepcopy(BRUTO)
    for k, v in troca.items():
        b[k] = v
    return g.Dados(b, date(2026, 10, 21))


def capa(d):
    with open(os.path.join(AQUI, 'estilo.css'), encoding='utf-8') as f:
        css = g.css_minimo(f.read())
    return g.monta(d, pagina_capa, css, {'site.js': 'x', 'simulador.js': 'x'})


class Simulador(unittest.TestCase):
    def setUp(self):
        self.d = dados()
        self.p = self.d.sim_params

    def test_javascript_e_python_dao_o_mesmo_numero(self):
        contas = list(range(0, 1000, 50)) + list(range(800, 60001, 137)) + [799, 800, 801, 1500, 5000, 11000, 250000]
        js = os.path.join(os.path.dirname(AQUI), 'site', 'assets', 'simulador.js')
        prog = (f'require({json.dumps(js)}); const S = globalThis.AesolarSimulador;'
                f'const p = {json.dumps(self.p)};'
                f'console.log(JSON.stringify({json.dumps(contas)}.map(c => S.estima(c, p))));')
        saida = subprocess.run(['node', '-e', prog], capture_output=True, text=True, check=True).stdout
        do_js = json.loads(saida)
        for conta, r_js in zip(contas, do_js):
            self.assertEqual(estima(conta, self.p), r_js, f'conta de R$ {conta}')

    def test_exemplo_da_proposta(self):
        # tarifa de R$ 1,22 (reajuste da Equatorial, 27/10/2026); com R$ 1,15 era (600, 4400, 880, 1320, ...)
        r = estima(5000, self.p)
        self.assertEqual((r['fora'], r['abatido'], r['min'], r['max'], r['ano_min'], r['ano_max']),
                         (610, 4390, 870, 1310, 10440, 15720))

    def test_abaixo_do_minimo_nao_calcula(self):
        self.assertIsNone(estima(self.d.of['minimo_conta'] - 1, self.p))
        self.assertIsNotNone(estima(self.d.of['minimo_conta'], self.p))

    def test_nunca_desconto_sobre_a_conta_inteira(self):
        # a economia máxima fica sempre abaixo do teto aplicado à conta toda: custo mínimo, iluminação e tributos ficam fora
        for conta in range(800, 100001, 997):
            r = estima(conta, self.p)
            self.assertLess(r['max'], conta * self.p['desconto_max_pct'] / 100)
            self.assertLessEqual(r['min'], r['max'])
            self.assertEqual(r['fora'] + r['abatido'], conta)

    def test_leitura_do_valor_digitado(self):
        js = os.path.join(os.path.dirname(AQUI), 'site', 'assets', 'simulador.js')
        casos = {'R$ 5.000': 5000, '5000': 5000, '5.000,90': 5000, '5000.90': 5000, '12.345': 12345, '': 0, 'abc': 0}
        prog = (f'require({json.dumps(js)}); const S = globalThis.AesolarSimulador;'
                f'console.log(JSON.stringify({json.dumps(list(casos))}.map(S.leValor)));')
        saida = json.loads(subprocess.run(['node', '-e', prog], capture_output=True, text=True, check=True).stdout)
        self.assertEqual(saida, list(casos.values()))


class TravasDaMarca(unittest.TestCase):
    def setUp(self):
        self.d = dados()
        self.pagina = capa(self.d)

    def confere(self, html):
        return g.confere_pagina(self.d, pagina_capa, html)

    def test_capa_atual_passa(self):
        self.assertEqual(self.confere(self.pagina), 0)  # passa, e sem marca PENDENTE (decisões fechadas em 27/10/2026)

    def test_marca_pendente_e_contada(self):
        self.assertEqual(self.confere(self.pagina.replace('</main>', b.pendente('D99', 'teste') + '</main>')), 1)

    def test_frases_proibidas_param(self):
        for frase in ['Economize até 26% na conta', 'Energia grátis para sua empresa', 'Zere sua conta de luz',
                      'Pare de pagar a Equatorial', 'Economia imediata', 'Comece a economizar desde a primeira fatura',
                      'Serve para qualquer empresa', 'Economia garantida', 'Junte-se a centenas de empresários',
                      'Já são 150 clientes', 'Usina de 2 MWp', 'São 6 usinas', 'Lorem ipsum dolor',
                      'Ligue 5562993420248', 'Contrato sem fidelidade']:
            with self.subTest(frase=frase), self.assertRaises(Erro):
                self.confere(self.pagina.replace('</main>', f'<p>{frase}</p></main>'))

    def test_percentual_sem_ate_para(self):
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('</main>', '<p>Economia de 30% na conta.</p></main>'))
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('</main>', '<p>Desconto de 25%.</p></main>'))

    def test_whatsapp_de_outro_numero_para(self):
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('wa.me/' + self.d.emp['whatsapp'], 'wa.me/5562900000000', 1))

    def test_whatsapp_sem_saudacao_para(self):
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('data-wa="Olá! Vim pelo site.', 'data-wa="Oi', 1))

    def test_link_quebrado_para(self):
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('</main>', '<a href="/pagina-que-nao-existe/">x</a></main>'))

    def test_imagem_sem_alt_para(self):
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('</main>', '<img src="/favicon-32.png" width="32" height="32"></main>'))

    def test_cor_solta_no_html_para(self):
        with self.assertRaises(Erro):
            self.confere(self.pagina.replace('<main id="conteudo">', '<main id="conteudo"><p style="color:#ff0000">x</p>'))

    def test_cor_solta_no_css_para(self):
        with self.assertRaises(Erro):
            g.confere_css(':root { --a: #fff; }\n.x { color: #123456; }')
        g.confere_css(':root { --a: #fff; }\n.x { color: var(--a); }')

    def test_depoimento_sem_termo_para(self):
        with self.assertRaises(Erro):
            dados(depoimentos=[{'texto': 'Ótimo', 'quem': 'Cliente', 'termo_assinado': True}])

    def test_noindex_acompanha_a_previa(self):
        self.assertIn('content="noindex', capa(dados(previa=True)))
        liberado = dados(previa=False)
        self.assertNotIn('content="noindex', capa(liberado))


def pagina(d, modulo):
    with open(os.path.join(AQUI, 'estilo.css'), encoding='utf-8') as f:
        css = g.css_minimo(f.read())
    return g.monta(d, modulo, css, {'site.js': 'x', 'simulador.js': 'x', 'capas.js': 'x'})


class CapasNovas(unittest.TestCase):
    """Protótipos v2 e v3 da capa (sessão A3): passam nas travas, e foto de banco só entra marcada e sem fingir."""

    def setUp(self):
        # as fotos de IA já foram aprovadas; aqui voltam a provisórias para testar a trava
        reg = {k: dict(v, provisoria=True) for k, v in BRUTO['imagens_banco'].items()}
        self.d = dados(imagens_banco=reg)
        self.v2 = pagina(self.d, pagina_capa_v2)
        self.v3 = pagina(self.d, pagina_capa_v3)

    def test_as_duas_passam_nas_travas(self):
        self.assertEqual(g.confere_pagina(self.d, pagina_capa_v2, self.v2), 0)
        self.assertEqual(g.confere_pagina(self.d, pagina_capa_v3, self.v3), 0)

    def test_v2_so_tem_foto_real_e_v3_marca_as_de_banco(self):
        self.assertEqual(g.provisorias(self.v2), [])
        self.assertEqual(set(g.provisorias(self.v3)), set(self.d.b['imagens_banco']))
        self.assertIn('Imagem provisória', self.v3)

    def test_exemplo_escrito_bate_com_o_simulador(self):
        r = estima(self.d.sim['exemplo_pagina'], self.d.sim_params)
        for html_ in (self.v2, self.v3):
            self.assertIn(f'data-calc="min">{b.reais(r["min"])}<', html_)
            self.assertIn(f'data-calc="max">{b.reais(r["max"])}<', html_)

    def test_foto_de_banco_como_usina_ou_cliente_para(self):
        for alt in ('Nossa usina em Goiás', 'Cliente satisfeita da AESOLAR', 'Complexo Vereda'):
            with self.subTest(alt=alt), self.assertRaises(Erro):
                g.confere_pagina(self.d, pagina_capa_v3, self.v3.replace('alt="Padaria e mercearia de bairro com as luzes acesas"', f'alt="{alt}"'))
        with self.assertRaises(Erro):
            capas.foto(self.d, 'ia-comercio', 'Cliente no balcão')

    def test_foto_de_banco_sem_marca_para(self):
        img = '<img src="/assets/img/ia-condominio-480.webp" width="480" height="600" alt="Prédios">'
        with self.assertRaises(Erro):
            g.confere_pagina(self.d, pagina_capa_v2, self.v2.replace('</main>', img + '</main>'))

    def test_marca_de_provisoria_fora_do_registro_para(self):
        with self.assertRaises(Erro):
            g.confere_pagina(self.d, pagina_capa_v3, self.v3.replace('data-provisoria="ia-condominio"', 'data-provisoria="foto-qualquer"', 1))

    def test_foto_aprovada_sai_sem_marca_mas_com_a_regra_do_texto(self):
        d = dados()
        v3 = pagina(d, pagina_capa_v3)
        self.assertEqual(g.provisorias(v3), [])
        self.assertNotIn('Imagem provisória', v3)
        self.assertEqual(g.confere_pagina(d, pagina_capa_v3, v3), 0)
        with self.assertRaises(Erro):
            capas.foto(d, 'ia-comercio', 'Cliente no balcão')

    def test_capas_no_sitemap_e_sem_prototipo(self):
        mapa = g.mapa_do_site(dados(previa=False))
        self.assertIn('energia-solar-por-assinatura-goias', mapa)
        self.assertNotIn('/prototipos/', mapa)
        self.assertIn('<loc>https://aesolar.com.br/</loc>', mapa)


class Producao(unittest.TestCase):
    def test_producao_passa_com_o_site_no_ar(self):
        # Desde a publicação (A6) a prévia está desligada e não há pendência: --producao tem de passar, porque é
        # ele que o pages.yml roda antes de publicar.
        r = subprocess.run([sys.executable, os.path.join(AQUI, 'gera_site.py'), '--producao'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn('NÃO PUBLICAR', r.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=1)
