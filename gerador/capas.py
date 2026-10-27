"""Peças das duas capas (decisão D19): a da página inicial ("a usina é nossa", nomes _v2) e a da página do Google
("a conta em reais", nomes _v3), mais as que as duas usam. O estilo próprio está em estilo_capas.css e o
comportamento em site/assets/capas.js; a conta continua uma só (simulador.py e simulador.js).
"""
import re

import blocos as b
import mapa_goias
from blocos import Erro, e, reais, pct, icone, wa, wa_href, caminho_curto, pendente, pendente_bloco, MSG_FATURA, SAUDACAO
from simulador import estima

# ---------- ícones que só as capas novas usam (Lucide), num sprite à parte ----------

_ICONES = {
    'play': '<polygon points="6 3 20 12 6 21 6 3"/>',
    'camera': '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>'
              '<circle cx="12" cy="13" r="3"/>',
    'desce': '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
}


def sprite_extra():
    simbolos = ''.join(f'<symbol id="i-{n}" viewBox="0 0 24 24">{p}</symbol>' for n, p in _ICONES.items())
    return f'<svg class="sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{simbolos}</svg>'


def ic(nome, cls='ic'):
    if nome in _ICONES:
        return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{nome}"/></svg>'
    return icone(nome, cls)


# ---------- fotos: as da capa nova têm tamanhos próprios (prepara_assets.py, FOTOS_CAPAS) ----------

FOTOS = {
    # nome: (largura, altura) do maior arquivo, e as larguras geradas
    'vereda-entardecer-retrato': (810, 1440, (480, 640, 810)),
    'vereda-entardecer-larga': (1920, 1200, (1024, 1440, 1920)),
    'vereda-ceu': (1920, 1080, (640, 1024, 1600, 1920)),
    'vereda-aerea-larga': (1600, 800, (640, 1024, 1600)),
    'goiania-noite': (1920, 1080, (640, 1024, 1600, 1920)),
    'ia-condominio': (800, 600, (480, 640, 800)),
    'ia-comercio': (800, 600, (480, 640, 800)),
    'ia-varias-unidades': (800, 600, (480, 640, 800)),
    'ia-fatura': (1600, 2000, (640, 1024, 1600)),
    'caso-fatura': (1200, 1107, (480, 800, 1200)),
}

# Foto de banco ou de IA nunca pode passar por foto da usina nem de cliente (regra da marca).
NAO_PODE_DIZER = re.compile(r'usina|vereda|cliente|associad|nossa\s+equipe', re.I)


def _srcset(nome, ext):
    return ', '.join(f'/assets/img/{nome}-{x}.{ext} {x}w' for x in FOTOS[nome][2])


def banco(d, nome):
    """O registro da foto em dados.json (imagens_banco), ou None se é foto real."""
    return d.b.get('imagens_banco', {}).get(nome)


def foto(d, nome, alt, sizes='100vw', lazy=True, cls='foto', retrato=None):
    """<picture> em AVIF e WebP. retrato=(nome, largura_max_px): outra foto, em pé, para telas estreitas.
    Foto de banco sai marcada (data-provisoria) e com a etiqueta visível de imagem provisória."""
    for n in (nome, retrato[0] if retrato else None):
        if n and n not in FOTOS:
            raise Erro(f'Foto "{n}" não está em capas.FOTOS (e em prepara_assets.py, FOTOS_CAPAS).')
    reg = banco(d, nome)
    if reg and NAO_PODE_DIZER.search(alt):
        raise Erro(f'Foto de banco "{nome}" com texto que a faz passar por usina ou cliente: "{alt}".')
    w, h, _ = FOTOS[nome]
    fontes = ''
    if retrato:
        rn, ate = retrato
        mq = f'(max-width: {ate}px)'
        fontes = (f'<source media="{mq}" type="image/avif" srcset="{_srcset(rn, "avif")}" sizes="{sizes}">'
                  f'<source media="{mq}" type="image/webp" srcset="{_srcset(rn, "webp")}" sizes="{sizes}">')
    carga = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    menor = FOTOS[nome][2][1] if len(FOTOS[nome][2]) > 1 else FOTOS[nome][2][0]
    prov = reg and reg.get('provisoria', True)
    marca = f' data-provisoria="{e(nome)}"' if prov else ''
    etiqueta = (f'<span class="prov" aria-hidden="true">Imagem provisória · {e(reg["origem"])}</span>' if prov else '')
    return (f'<picture class="{cls}"{marca}>{fontes}<source type="image/avif" srcset="{_srcset(nome, "avif")}" sizes="{sizes}">'
            f'<img src="/assets/img/{nome}-{menor}.webp" srcset="{_srcset(nome, "webp")}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {carga}></picture>{etiqueta}')


def preload(nome, retrato=None):
    """Começa a baixar a foto do topo antes de ler o corpo da página: é o maior bloco da primeira tela."""
    if not retrato:
        return (f'<link rel="preload" as="image" type="image/avif" imagesrcset="{_srcset(nome, "avif")}" '
                f'imagesizes="100vw" fetchpriority="high">')
    rn, ate = retrato
    return (f'<link rel="preload" as="image" type="image/avif" media="(max-width: {ate}px)" '
            f'imagesrcset="{_srcset(rn, "avif")}" imagesizes="100vw" fetchpriority="high">\n'
            f'<link rel="preload" as="image" type="image/avif" media="(min-width: {ate + 1}px)" '
            f'imagesrcset="{_srcset(nome, "avif")}" imagesizes="100vw" fetchpriority="high">')


# ---------- o simulador das capas: a economia em reais e as duas contas, lado a lado ----------

def barras(r):
    """As duas contas do mês, com o desconto mínimo. A barra "com a AESOLAR" é mais curta e o que você deixa de pagar
    fica pontilhado, para a economia aparecer no desenho. Larguras em % da conta de hoje; capas.js muda tudo quando a
    pessoa digita a conta dela (dentro do simulador e em qualquer bloco data-calc-espelho)."""
    w = lambda v: f'{v / r["conta"] * 100:.1f}%'
    eco = r['min']
    return (
        f'<div class="barras" aria-hidden="true">'
        f'<div class="barra-l"><span class="barra-rot">Hoje</span><div class="trilho">'
        f'<i class="b-eq" data-calc-w="hoje" style="--w:100%"></i></div>'
        f'<span class="barra-v" data-calc="conta">{reais(r["conta"])}</span></div>'
        f'<div class="barra-l"><span class="barra-rot">Com a AESOLAR</span><div class="trilho">'
        f'<i class="b-eq" data-calc-w="eq" style="--w:{w(r["equatorial_depois"])}"></i>'
        f'<i class="b-ae" data-calc-w="ae" style="--w:{w(r["aesolar_min"])}"></i>'
        f'<i class="b-eco" data-calc-w="eco" style="--w:{w(eco)}"></i></div>'
        f'<span class="barra-v" data-calc="total">{reais(r["conta"] - eco)}</span></div></div>'
        f'<ul class="leg">'
        f'<li><i class="b-eq"></i>Equatorial <b data-calc="equatorial_depois">{reais(r["equatorial_depois"])}</b></li>'
        f'<li><i class="b-ae"></i>AESOLAR <b data-calc="aesolar_min">{reais(r["aesolar_min"])}</b></li>'
        f'<li><i class="b-eco"></i>Você deixa de pagar <b data-calc="min">{reais(eco)}</b></li></ul>')


def _chip(v):
    return f'R$ {v // 1000} mil' if v % 1000 == 0 else reais(v)


def calc(d, caminho, titulo, variante='cartao', exemplo=None, rotulo='Valor médio da conta de luz, por mês'):
    """Um campo só (o valor da conta). Já abre com o exemplo calculado; a pessoa digita a dela e a conta muda na hora.
    O exemplo não conta como simulação: nem medição, nem vai para o formulário (capas.js).
    variante 'cartao' (v2, ao lado da foto): enxuto, sem as barras. 'larga' (v3, o topo): com as duas contas.
    exemplo: a conta com que abre (as páginas de segmento usam uma conta típica do segmento)."""
    s = d.sim
    c = caminho_curto(caminho)
    onde = f'{c}:simulador'
    ex = exemplo or s['exemplo_pagina']
    r = estima(ex, d.sim_params)
    chips = ''.join(f'<button type="button" class="chip" data-calc-exemplo="{v}">{_chip(v)}</button>' for v in s['exemplos'])
    provisorio = '' if s['validado_em'] else pendente(
        'D4', 'Simulador provisório: premissas a calibrar com 3 ou 4 faturas reais tarjadas.')
    msg = f'{SAUDACAO} Quero o cálculo exato da minha conta.'
    larga = variante == 'larga'
    tit = f'<h2 class="calc-tit{" vh" if larga else ""}">{titulo}</h2>'
    nota_eq = (f'<p class="calc-eq">{icone("tomada")}<span>Você continua pagando a Equatorial: a conta dela fica menor e chega '
               f'uma segunda, da AESOLAR. A soma das duas é que fica mais barata.</span></p>')
    letra = (f'<p class="calc-prem">{"Barras com o desconto mínimo. " if larga else ""}Premissas: tarifa de '
             f'{b.tarifa(s["tarifa_kwh"])} por kWh ({b.mes_ano(s["tarifa_data"])}), desconto de {pct(s["desconto_min_pct"])} '
             f'a {pct(s["desconto_max_pct"])} sobre a energia abatida, bandeira verde, baixa tensão. '
             f'<strong>O número real vem da sua fatura.</strong></p>'
             f'<details class="sim-como"><summary>Como a conta é feita {icone("abre")}</summary>'
             f'<p>O desconto vale só sobre a energia que a usina abate da sua conta. Ficam fora o custo mínimo que a '
             f'Equatorial cobra de toda ligação ({s["disponibilidade_kwh"]} kWh numa ligação trifásica), a iluminação pública '
             f'e parte dos tributos. Por isso a gente mostra a economia em reais, e não em percentual da conta inteira.</p>'
             f'</details>{provisorio}')
    entra = (
        f'<div class="calc-entra">{tit}'
        f'<label class="calc-rot-campo" for="conta-{c}">{rotulo}</label>'
        f'<div class="calc-campo"><span aria-hidden="true">R$</span><input id="conta-{c}" name="conta" type="text" '
        f'inputmode="numeric" autocomplete="off" placeholder="{reais(ex)[3:]}" aria-describedby="calc-estado-{c}"></div>'
        f'<div class="chips" role="group" aria-label="Exemplos de valor">{chips}</div>'
        f'<p class="calc-abaixo" data-calc-abaixo hidden>A assinatura é para contas a partir de '
        f'{reais(d.of["minimo_conta"])} por mês. Se a empresa tem mais de uma unidade, some as contas.</p>'
        + '</div>')
    sai = (
        f'<div class="calc-sai" data-calc-res>'
        f'<p class="calc-estado" id="calc-estado-{c}" data-calc-estado aria-live="polite">Exemplo: conta de {reais(ex)}</p>'
        f'<p class="calc-rot">Fica com você, por mês</p>'
        f'<p class="calc-valor"><span data-calc="min">{reais(r["min"])}</span> <span class="calc-a">a</span> '
        f'<span data-calc="max">{reais(r["max"])}</span></p>'
        f'<p class="calc-ano">Em 12 meses: <b data-calc="ano_min">{reais(r["ano_min"])}</b> a '
        f'<b data-calc="ano_max">{reais(r["ano_max"])}</b></p>'
        + (barras(r) if larga else '')
        + f'<a class="btn btn-pri btn-larga" data-calc-cta href="{e(wa_href(d, msg))}" data-wa="{e(msg)}" '
        f'data-where="{e(onde)}" target="_blank" rel="noopener">{icone("whatsapp")}<span>Receber o cálculo exato pelo WhatsApp</span></a>'
        + ('' if larga else letra) + '</div>')
    mais = f'<div class="calc-mais">{nota_eq}{letra}</div>' if larga else ''
    return (
        f'<div class="calc calc-{variante}" id="simulador" data-calc-caixa="{e(onde)}" data-exemplo="{ex}" data-modo="exemplo">'
        f'{entra}{sai}{mais}<noscript><p class="calc-estado">Para simular outro valor, ative o JavaScript, ou mande a fatura pelo '
        f'WhatsApp.</p></noscript></div>')


def contas_espelho(d):
    """As duas contas fora do simulador (v2, em "como funciona"). Abrem com o exemplo e acompanham o que a pessoa
    digitar no simulador do topo."""
    r = estima(d.sim['exemplo_pagina'], d.sim_params)
    return (f'<figure class="espelho" data-calc-espelho><figcaption><strong data-calc-espelho-rot>Exemplo: conta de '
            f'{reais(r["conta"])} por mês.</strong> Com o desconto mínimo de {pct(d.sim["desconto_min_pct"])}.</figcaption>'
            f'<p class="eco-grande" data-calc="min">{reais(r["min"])}</p><p class="eco-sub">a menos por mês</p>'
            f'<p class="eco-ano">Em 12 meses: <b data-calc="ano_min">{reais(r["ano_min"])}</b></p>'
            f'{barras(r)}'
            f'{"" if d.sim["validado_em"] else pendente("D4", "Exemplo calculado com as premissas provisórias do simulador.")}'
            f'</figure>')


# ---------- peças comuns às duas capas ----------

def micro_confianca(d):
    return (f'<p class="micro">{icone("check")}<span>Análise gratuita · cálculo em reais em até '
            f'{d.of["proposta_horas"]} horas · sem compromisso</span></p>')


def numeros(d):
    """Os números da marca, grandes (o que pode ser dito, sem quantidade de cliente nem potência)."""
    prefixo, valor = _economia_gerada(d)
    mil = re.search(r'(\d+)\s*mil', valor)
    if not mil:
        raise Erro(f'dados.json: "economia_gerada" fora do formato "mais de R$ N mil": {d.of["economia_gerada"]}')
    itens = [
        (f'<small>{prefixo}</small> R$ <span data-conta="{mil.group(1)}" data-economia-mil>{mil.group(1)}</span> mil',
         f'de economia já gerada para os clientes, desde {d.b["historia"][0]["ano"]}'),
        (f'<small>até</small> <span data-conta="{d.of["desconto_max_pct"]}">{d.of["desconto_max_pct"]}</span>%',
         'de economia na parte da energia'),
        (f'<small>até</small> <span data-conta="{d.of["proposta_horas"]}">{d.of["proposta_horas"]}</span> h',
         'para o cálculo em reais'),
        ('0', 'obra, placa ou equipamento na sua empresa'),
    ]
    lis = ''.join(f'<li><p class="num">{n}</p><p class="num-rot">{t}</p></li>' for n, t in itens)
    return f'<h2 class="vh" id="t-numeros">A AESOLAR em números</h2><ul class="numeros">{lis}</ul>'


def passos(d, titulo='Três passos. Nenhuma obra.'):
    of = d.of
    itens = [
        ('Mande a fatura', 'Uma foto ou o PDF da última conta da Equatorial, pelo WhatsApp. A análise é gratuita.'),
        ('Receba o cálculo em reais',
         f'Em até {of["proposta_horas"]} horas: quanto você paga hoje e quanto vai pagar com a AESOLAR.'),
        ('Assine pelo celular', f'Os créditos começam a aparecer na conta em torno de {of["creditos_dias_normal"]} dias '
                                f'(o contrato prevê até {of["creditos_dias_contrato"]}).'),
    ]
    lis = ''.join(f'<li><span class="p-n" aria-hidden="true">0{i}</span><h3>{t}</h3><p>{x}</p></li>'
                  for i, (t, x) in enumerate(itens, 1))
    return f'<p class="olho">Como funciona</p><h2 id="t-passos">{titulo}</h2><ol class="p-lista">{lis}</ol>'


def vantagens(d):
    """Assinatura x placa no telhado: o que vende (sem obra, sem investimento, sem trocar de distribuidora).
    Só fatos qualitativos: nenhum preço de placa nem prazo de retorno sem fonte."""
    linhas = [
        ('Investimento', 'Você compra o sistema, à vista ou financiado.', 'Nenhum.'),
        ('Obra', 'Instalação no telhado, que precisa de espaço e estrutura.',
         'Nenhuma. A energia vem da usina pela rede da Equatorial.'),
        ('Manutenção e limpeza', 'Por sua conta.', 'Por conta da Boreal Solar, que opera a usina.'),
        ('Quando o dinheiro volta', 'Depois de alguns anos, quando o investimento se paga.',
         'Não há investimento para recuperar.'),
    ]
    lis = ''.join(f'<li><h3>{t}</h3><p class="cmp-placa"><small>Placa no telhado</small>{p}</p>'
                  f'<p class="cmp-ae"><small>Assinatura AESOLAR</small>{a}</p></li>' for t, p, a in linhas)
    return (
        f'<p class="olho">Por que assinar</p><h2 id="t-vant">Sem obra. Sem investimento. Sem trocar de distribuidora.</h2>'
        f'<ul class="cmp"><li class="cmp-cab" aria-hidden="true"><span></span><span>Placa no telhado</span>'
        f'<span>Assinatura AESOLAR</span></li>{lis}</ul>'
        f'<p class="cmp-eq">{icone("tomada")}<span><strong>Você continua cliente da Equatorial.</strong> Nada muda na '
        f'ligação: a conta dela fica menor e chega uma segunda, da AESOLAR, com o desconto.</span></p>')


def _centavos(n):
    """9804.68 -> 'R$ 9.804,68', com o mesmo espaço que não quebra de reais()."""
    inteiro, cent = f'{n:.2f}'.split('.')
    return reais(int(inteiro)) + ',' + cent


MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
         'novembro', 'dezembro']


def _caso_barras(x):
    """Para o caso sem a fatura tarjada em imagem: as duas contas do mês, sem e com a AESOLAR, em barras."""
    w = f'{x["com_aesolar"] / x["sem_aesolar"] * 100:.1f}%'
    eco = f'{x["economia"] / x["sem_aesolar"] * 100:.1f}%'
    return (
        f'<figure class="caso-fig caso-fig-barras"><figcaption>{x["quem"]}, {MESES[int(x["mes"][5:7]) - 1]} de '
        f'{x["mes"][:4]}</figcaption><div class="barras" aria-hidden="true">'
        f'<div class="barra-l"><span class="barra-rot">Sem a AESOLAR</span><div class="trilho"><i class="b-eq" style="--w:100%"></i>'
        f'</div><span class="barra-v">{reais(x["sem_aesolar"])}</span></div>'
        f'<div class="barra-l"><span class="barra-rot">Com a AESOLAR</span><div class="trilho"><i class="b-ae" style="--w:{w}"></i>'
        f'<i class="b-eco" style="--w:{eco}"></i></div><span class="barra-v">{reais(x["com_aesolar"])}</span></div></div>'
        f'<ul class="leg"><li><i class="b-ae"></i>Equatorial + AESOLAR</li>'
        f'<li><i class="b-eco"></i>Ficou com o cliente <b>{_centavos(x["economia"])}</b></li></ul></figure>')


def caso(d, ids=None):
    """A prova: faturas reais de clientes, anônimos, com termo assinado (dados.json, casos). Mesmo mês, sem e com.
    O primeiro caso vem em destaque, com a fatura tarjada (ou as duas contas em barras, se não há imagem) e a economia
    desde o início do contrato (número real, não projeção); os outros, numa linha cada.
    ids: quais casos e em que ordem (as páginas de segmento põem na frente o caso do segmento)."""
    por_id = {c['id']: c for c in d.b['casos']}
    escolhidos = [por_id[i] for i in ids] if ids else d.b['casos']
    x, outros = escolhidos[0], escolhidos[1:]
    mes, ano = MESES[int(x['mes'][5:7]) - 1], x['mes'][:4]
    alt = f'Fatura da AESOLAR de {mes} de {ano} de um cliente, com os dados do cliente tarjados'
    desde = (f'<div class="caso-n-desde"><dt>Desde o início do contrato</dt><dd>{_centavos(x["desde_inicio"])}</dd></div>'
             if x.get('desde_inicio') else '')
    det = f'<small>{x["detalhe"]}</small>' if x.get('detalhe') else ''
    mais = ''.join(
        f'<li><strong>{o["quem"]}:</strong> {_centavos(o["economia"])} a menos em {MESES[int(o["mes"][5:7]) - 1]} '
        f'<span>({_centavos(o["sem_aesolar"])} sem a AESOLAR, {_centavos(o["com_aesolar"])} com)</span></li>' for o in outros)
    return (
        f'<div class="caso"><div class="caso-txt"><p class="olho">Contas de verdade</p>'
        f'<h2 id="t-caso">{x["quem"]}: <span class="caso-eco">{_centavos(x["economia"])}</span> a menos em {mes}.</h2>'
        f'<dl class="caso-n"><div><dt>Sem a AESOLAR</dt><dd><s>{_centavos(x["sem_aesolar"])}</s></dd></div>'
        f'<div><dt>Com a AESOLAR</dt><dd>{_centavos(x["com_aesolar"])}{det}</dd></div>'
        f'<div class="caso-n-eco"><dt>Economia no mês</dt><dd>{_centavos(x["economia"])}</dd></div>{desde}</dl>'
        + (f'<ul class="caso-mais">{mais}</ul>' if mais else '')
        + f'<p class="caso-nota">Faturas reais de {mes} de {ano}, comparadas no mesmo mês, com os dados dos clientes '
        f'tarjados. A economia de cada empresa depende da conta dela: o simulador e a análise da sua fatura mostram a '
        f'sua.</p></div>'
        + (f'<figure class="caso-fig">{foto(d, x["imagem"], alt, "(min-width: 900px) 520px, calc(100vw - 32px)")}</figure>'
           if x.get('imagem') else _caso_barras(x)) + '</div>')


def quem(d, video=True):
    emp = d.emp
    linha = ''.join(f'<li><span class="hist-ano">{h["ano"]}</span><p>{h["texto"]}</p></li>' for h in d.b['historia'])
    vid = ''
    if video:
        # foto real da usina até o vídeo do Rafael na usina ficar pronto (D5); aí o vídeo entra no lugar dela
        vid = (f'<figure class="video">{foto(d, "vereda-entardecer-larga", "Painéis do Complexo Vereda ao entardecer", "(min-width: 900px) 560px, calc(100vw - 32px)")}'
               f'<figcaption><span><strong>Complexo Vereda, a cerca de 30 km de Goiânia.</strong> '
               f'Foto real da usina da Boreal Solar.</span></figcaption></figure>')
    return (
        f'<div class="quem2"><div class="quem2-a">{vid}</div><div class="quem2-b"><p class="olho olho-escuro">Quem está por trás</p>'
        f'<h2 id="t-somos">Gente de Goiás, com escritório em Goiânia</h2>'
        f'<p>A AESOLAR é a associação de geração compartilhada operada pela <strong>Boreal Solar</strong>, empresa de Goiás '
        f'que constrói e opera usinas solares no estado. Quando a conta vier errada, você sabe com quem falar.</p>'
        f'<ol class="hist hist-escuro">{linha}</ol>'
        f'<div class="ficha2">{icone("local")}<p><strong>Onde estamos</strong><br>'
        f'{emp["rua"]}, {emp["bairro"]}, {emp["cidade"]}-{emp["uf"]}</p></div></div></div>')


def contato_curto(d, caminho, segmento='geral'):
    """Formulário de três campos: nome, WhatsApp e o valor da conta (que já vem do simulador, se a pessoa simulou).
    O app só exige esses três (proposta A2, §4.3)."""
    c = caminho_curto(caminho)
    return (
        f'<form class="form form-curto" data-form data-segmento="{e(segmento)}" novalidate>'
        f'<p class="form-tit">Prefere que a gente chame?</p>'
        f'{b.campo("nome", "Seu nome", "text", "name", c)}'
        f'{b.campo("whatsapp", "WhatsApp com DDD", "tel", "tel", c, inputmode="tel")}'
        f'{b.campo("valor", "Valor médio da conta (R$ por mês)", "text", "off", c, inputmode="numeric")}'
        f'<div class="isca" aria-hidden="true"><label for="website-{c}">Não preencha</label>'
        f'<input id="website-{c}" name="website" type="text" tabindex="-1" autocomplete="off"></div>'
        f'<button class="btn btn-pri btn-larga" type="submit">{icone("whatsapp")}<span>Enviar e abrir o WhatsApp</span></button>'
        f'<p class="form-lgpd">Ao enviar, você concorda com a <a href="/politica-de-privacidade/">Política de privacidade</a>. '
        f'Seus dados servem só para preparar a proposta.</p>'
        f'<div class="form-msg" data-form-msg role="status" aria-live="polite" hidden></div></form>')


def final(d, caminho, nome_foto, alt, titulo, texto, segmento='geral'):
    """O fim da página, sobre uma foto: o WhatsApp em destaque e o formulário curto ao lado."""
    c = caminho_curto(caminho)
    return (
        f'<section class="fim" id="contato" aria-labelledby="t-contato">'
        f'{foto(d, nome_foto, alt, "100vw", cls="fim-foto")}'
        f'<div class="wrap fim-in"><div class="fim-txt"><p class="olho olho-escuro">Análise gratuita</p>'
        f'<h2 id="t-contato">{titulo}</h2><p>{texto}</p>'
        f'{wa(d, MSG_FATURA, c + ":contato", "Mandar minha fatura pelo WhatsApp", "btn btn-pri btn-larga")}'
        f'{micro_confianca(d)}{escassez(d)}</div>{contato_curto(d, caminho, segmento)}</div>{economia_fonte(d)}</section>')


def escassez(d):
    """Verdade (Rafael, 27/10/2026): a energia das usinas é limitada e o desconto para quem entra pode diminuir.
    Sem contagem regressiva nem "últimas vagas": só o fato e a validade da proposta, que já existe."""
    return (f'<p class="micro micro-esc">{icone("relogio")}<span>A energia das usinas é limitada e o desconto para novos '
            f'clientes pode mudar. A proposta vale por {d.of["validade_proposta_dias"]} dias.</span></p>')


def economia_fonte(d):
    """Endereço do app que devolve a economia gerada (piso de 50 mil). Vazio: nada a buscar, vale o número da página.
    Só busca no domínio oficial: o app só libera esse endereço para ele, e fora dele a busca vira erro no console."""
    url = d.of.get('economia_url')
    dom = d.emp['dominio_medicao']
    return f'<span hidden data-economia-url="{e(url)}" data-economia-dominio="{e(dom)}"></span>' if url else ''


# ---------- v2: a usina em tela cheia ----------

def topo_v2(d, caminho):
    c = caminho_curto(caminho)
    r = estima(d.sim['exemplo_pagina'], d.sim_params)
    return (
        f'<section class="h2t" data-sem-barra aria-labelledby="t-topo">'
        f'{foto(d, "vereda-entardecer-larga", "Fileiras de painéis solares do Complexo Vereda, em Goiás, ao entardecer", lazy=False, cls="h2t-foto", retrato=("vereda-entardecer-retrato", 699))}'
        f'<div class="wrap h2t-in"><div class="h2t-txt">'
        f'<p class="olho olho-escuro h2t-olho">Energia solar por assinatura · Goiás</p>'
        f'<h1 id="t-topo">A usina é nossa.<br>A economia é sua.</h1>'
        f'<p class="h2t-sub">A energia da nossa usina em Goiás vira crédito na conta da sua empresa: até '
        f'{pct(d.of["desconto_max_pct"])} de economia na parte da energia, sem obra.</p>'
        f'<a class="h2t-num" href="#simulador"><span>Numa conta de {reais(r["conta"])} por mês</span>'
        f'<strong>{reais(r["min"])} a {reais(r["max"])}</strong><span>de economia estimada. Simule a sua {ic("desce")}</span></a>'
        f'<div class="h2t-bt">{wa(d, MSG_FATURA, c + ":topo", "Mandar minha fatura pelo WhatsApp")}</div>'
        f'{micro_confianca(d)}</div>'
        f'<div class="h2t-calc">{calc(d, caminho, "Quanto a sua empresa economiza")}</div></div>'
        f'<p class="h2t-leg">Complexo Vereda, a cerca de 30 km de Goiânia. Foto real.</p></section>')


def usina_v2(d):
    return (
        f'<section class="faixa-foto" aria-labelledby="t-usina">'
        f'{foto(d, "vereda-aerea-larga", "Vista aérea do Complexo Vereda, usina solar da Boreal Solar em Goiás", "100vw", cls="ff-foto")}'
        f'<div class="wrap ff-in revela"><p class="olho olho-escuro">A usina é nossa</p>'
        f'<h2 id="t-usina">A energia vem daqui.</h2>'
        f'<p>Complexo Vereda, a cerca de 30 km de Goiânia, em operação desde 2023. Construído e operado pela Boreal Solar, '
        f'empresa goiana. A usina gera, a energia entra na rede da Equatorial e vira crédito na conta da sua empresa.</p>'
        f'<p class="mais mais-escuro"><a href="/usinas/">Ver as fotos das usinas {icone("seta")}</a></p></div>'
        f'<p class="ff-leg">Vista aérea do Complexo Vereda. Foto real, sem retoque.</p></section>')


def para_quem_v2(d):
    lis = ''
    for s in d.b['segmentos']:
        corpo = f'<h3>{s["nome"]}</h3><p>{s["texto"]}</p>'
        if d.link_ok(s['pagina']):
            lis += (f'<li><a class="seg" href="{s["pagina"]}">{corpo}<span class="seg-link">Ver como funciona '
                    f'{icone("seta")}</span></a></li>')
        else:
            lis += f'<li class="seg">{corpo}</li>'
    return (f'<p class="olho">Para quem é</p><h2 id="t-quem">Feito para empresa de conta alta</h2>'
            f'<p class="intro">Para empresas e condomínios de Goiás com conta a partir de {reais(d.of["minimo_conta"])} por '
            f'mês, inclusive no Entorno do DF. Quanto maior a conta, maior a economia em reais.</p><ul class="segs">{lis}</ul>')


# ---------- v3: a conta em reais ----------

def topo_v3(d, caminho):
    # O olho repete a busca do anúncio ("energia solar por assinatura"): o Google Ads mede se a primeira tela fala dela
    # (D25, 27/10/2026). Nas páginas de segmento, o olho faz o mesmo papel (D26).
    return (
        f'<section class="h3t" data-sem-barra aria-labelledby="t-topo">'
        f'<div class="wrap h3t-in"><div class="h3t-txt">'
        f'<p class="olho">{icone("local")}<span>Energia solar por assinatura · Goiás</span></p>'
        f'<h1 id="t-topo">Quanto a sua empresa <em>economiza</em> na conta de luz?</h1>'
        f'<p class="h3t-sub">Digite a conta. A economia aparece na hora, em reais, sem deixar contato, com a conta de '
        f'hoje e a com a AESOLAR lado a lado.</p></div>'
        f'<ul class="selos"><li>{icone("sol")}<span>A usina é nossa, em Goiás</span></li>'
        f'<li>{icone("local")}<span>Empresa goiana, escritório em Goiânia</span></li>'
        f'<li>{icone("recibo")}<span>Mais de R$ <span data-economia-mil>{d.of["economia_gerada_piso"] // 1000}</span> mil de '
        f'economia gerada</span></li></ul>'
        f'{calc(d, caminho, "Sua conta, em reais", "larga")}</div>'
        f'<div class="h3t-foto">{foto(d, "goiania-noite", "Goiânia à noite, vista do alto, com os prédios iluminados", "100vw", cls="h3t-img")}</div>'
        f'</section>')


def conversa_v3(d, caminho):
    """O passo seguinte ao simulador, desenhado: uma conversa de exemplo no WhatsApp."""
    c = caminho_curto(caminho)
    r = estima(d.sim['exemplo_pagina'], d.sim_params)
    return (
        f'<div class="conversa"><div class="fone" aria-hidden="true"><div class="fone-cab"><span class="fone-av">A</span>'
        f'<span><b>AESOLAR</b><small>Exemplo de conversa</small></span></div>'
        f'<div class="fone-msgs"><p class="msg msg-eu">Olá! Vim pelo site. Simulei uma conta de {reais(r["conta"])} e quero o '
        f'cálculo exato.</p><p class="msg msg-eu msg-arq">{icone("fatura")}<span>fatura-equatorial.pdf</span></p>'
        f'<p class="msg msg-ae">Recebido! Em até {d.of["proposta_horas"]} horas você recebe quanto paga hoje e quanto vai '
        f'pagar com a AESOLAR, em reais.</p></div></div>'
        f'<div class="conversa-txt"><p class="olho">Próximo passo</p><h2 id="t-passos">Mande a foto da fatura. '
        f'A gente devolve o número exato.</h2>'
        f'<ol class="p-curta"><li>{ic("camera")}<span>Tire uma foto da última conta da Equatorial, ou mande o PDF.</span></li>'
        f'<li>{icone("relogio")}<span>Em até {d.of["proposta_horas"]} horas, o cálculo com a sua conta de verdade.</span></li>'
        f'<li>{icone("caneta")}<span>Gostou, assina pelo celular. Os créditos começam em torno de '
        f'{d.of["creditos_dias_normal"]} dias.</span></li></ol>'
        f'{wa(d, MSG_FATURA, c + ":passos", "Mandar minha fatura pelo WhatsApp", "btn btn-pri")}</div></div>')


def _economia_gerada(d):
    """'mais de R$ 700 mil' -> ('mais de', 'R$ 700 mil'), para o número sair grande e o 'mais de' pequeno."""
    prefixo, _, valor = d.of['economia_gerada'].partition('R$')
    return prefixo.strip(), 'R$' + valor


def provas_v3(d):
    pre, _ = _economia_gerada(d)
    return (
        f'<p class="olho">Por que dá para confiar</p><h2 id="t-provas">Desconto todo mundo promete. A gente mostra.</h2>'
        f'<ul class="provas3">'
        f'<li class="pv pv-foto">{foto(d, "vereda-aerea-larga", "Vista aérea do Complexo Vereda, usina solar da Boreal Solar em Goiás", "(min-width: 900px) 360px, calc(100vw - 32px)")}'
        f'<h3>A usina é nossa</h3><p>Complexo Vereda, a cerca de 30 km de Goiânia, em operação desde 2023. Foto real.</p>'
        f'<a href="/usinas/">Ver as usinas {icone("seta")}</a></li>'
        f'<li class="pv"><p class="pv-num"><small>{pre}</small> R$ <span data-economia-mil>{d.of["economia_gerada_piso"] // 1000}'
        f'</span> mil</p><h3>De economia já gerada</h3>'
        f'<p>Para os clientes da AESOLAR em Goiás, desde {d.b["historia"][0]["ano"]}.</p></li>'
        f'<li class="pv">{icone("local", "ic pv-ic")}<h3>Quem opera</h3><p>A Boreal Solar, empresa goiana que constrói e '
        f'opera usinas no estado. Escritório no {d.emp["bairro"]}, em {d.emp["cidade"]}.</p></li></ul>')


def mapa(d):
    # Dentro do <g>, o ponto é (longitude, latitude) × 10 000, como no caminho do IBGE; fora dele, o texto usa as
    # unidades do viewBox: x = longitude, y = -latitude.
    lon, lat = -49.2648, -16.6869  # Goiânia
    svg = (f'<svg class="mapa-svg" viewBox="{mapa_goias.GOIAS_VIEWBOX}" role="img" aria-labelledby="t-mapa-svg">'
           f'<title id="t-mapa-svg">Mapa de Goiás: todo o estado é atendido; o Distrito Federal não é.</title>'
           f'<g transform="scale(0.0001,-0.0001)"><path class="m-go" d="{mapa_goias.GOIAS}"/>'
           f'<path class="m-df" d="{mapa_goias.DF}"/>'
           f'<circle class="m-pt" cx="{lon * 10000:.0f}" cy="{lat * 10000:.0f}" r="900"/></g>'
           f'<text class="m-tx m-tx-fim" x="{lon - 0.14:.2f}" y="{-lat + 0.1:.2f}">Goiânia</text>'
           f'<text class="m-tx m-tx-meio" x="-47.79" y="15.86">DF</text></svg>')
    return (
        f'<div class="mapa"><div class="mapa-txt"><p class="olho">Onde atendemos</p><h2 id="t-mapa">Goiás inteiro. '
        f'O DF, não.</h2><p>Atendemos todo o estado: Goiânia e diversas cidades do interior, inclusive o Entorno do DF '
        f'atendido pela Equatorial Goiás. O Distrito Federal tem outra distribuidora e não é atendido.</p>'
        f'<ul class="mapa-leg"><li><i class="m-go"></i>Atendido</li><li><i class="m-df"></i>Distrito Federal, não atendido</li></ul>'
        f'</div>{svg}</div>')


def para_quem_v3(d):
    fotos = {'condominio': ('ia-condominio', 'Prédio residencial ao anoitecer, com portaria, garagem e jardim iluminados'),
             'comercio': ('ia-comercio', 'Padaria e mercearia de bairro com as luzes acesas'),
             'varias_unidades': ('ia-varias-unidades', 'Três lojas da mesma rede, lado a lado, ao anoitecer')}
    lis = ''
    for s in d.b['segmentos']:
        nome, alt = fotos[s['id']]
        fig = f'<div class="sf-foto">{foto(d, nome, alt, "(min-width: 900px) 340px, calc(100vw - 32px)")}</div>'
        corpo = f'{fig}<div class="sf-txt"><h3>{s["nome"]}</h3><p>{s["texto"]}</p>'
        if d.link_ok(s['pagina']):
            lis += f'<li><a class="sf" href="{s["pagina"]}">{corpo}<span class="seg-link">Ver como funciona {icone("seta")}</span></div></a></li>'
        else:
            lis += f'<li class="sf">{corpo}</div></li>'
    return (f'<p class="olho">Para quem é</p><h2 id="t-quem">Para quem tem conta alta todo mês</h2>'
            f'<p class="intro">Para empresas e condomínios de Goiás com conta a partir de {reais(d.of["minimo_conta"])} por '
            f'mês, inclusive no Entorno do DF.</p><ul class="sfs">{lis}</ul>')


# ---------- páginas de segmento (condomínios, comércio e serviços, várias unidades) ----------
# O molde é o da página do Google (v3): o simulador no topo, a prova logo depois. O texto de cada página fica no
# pagina_*.py dela, e precisa ser próprio: página repetida o Google rebaixa.

def topo_seg(d, caminho, olho, h1, sub, foto_seg, alt, titulo_calc, exemplo, rotulo=None):
    """O topo claro com o simulador, como o da página do Google, e a foto do segmento embaixo (foto de IA aprovada:
    ilustra o tipo de cliente, nunca é apresentada como cliente)."""
    pre, _ = _economia_gerada(d)
    kw = {'rotulo': rotulo} if rotulo else {}
    return (
        f'<section class="h3t h3t-seg" data-sem-barra aria-labelledby="t-topo">'
        f'<div class="wrap h3t-in"><div class="h3t-txt">'
        f'<p class="olho">{icone("local")}<span>{olho}</span></p>'
        f'<h1 id="t-topo">{h1}</h1><p class="h3t-sub">{sub}</p></div>'
        f'<ul class="selos"><li>{icone("sol")}<span>A usina é nossa, em Goiás</span></li>'
        f'<li>{icone("escudo")}<span>Créditos conferidos todo mês</span></li>'
        f'<li>{icone("recibo")}<span>{pre.capitalize()} R$ <span data-economia-mil>{d.of["economia_gerada_piso"] // 1000}</span> mil '
        f'de economia gerada</span></li></ul>'
        f'{calc(d, caminho, titulo_calc, "larga", exemplo, **kw)}</div>'
        f'<div class="h3t-foto">{foto(d, foto_seg, alt, "100vw", cls="h3t-img")}</div></section>')


def muda(titulo, intro, sim, nao, olho_txt):
    """O texto do segmento, e as duas listas: o que muda e o que não muda."""
    li = lambda xs, ic_: ''.join(f'<li>{icone(ic_)}<span>{x}</span></li>' for x in xs)
    return (f'<div class="estreito"><p class="olho">{olho_txt}</p><h2 id="t-seg">{titulo}</h2>{intro}</div>'
            f'<div class="muda"><div><h3>O que muda</h3><ul class="m-lista m-sim">{li(sim, "check")}</ul></div>'
            f'<div><h3>O que não muda</h3><ul class="m-lista m-nao">{li(nao, "igual")}</ul></div></div>')


def cartoes(olho_txt, titulo, itens):
    """Os diferenciais do segmento, em cartões: (ícone, título, texto)."""
    lis = ''.join(f'<li class="pv">{icone(i, "ic pv-ic")}<h3>{t}</h3><p>{x}</p></li>' for i, t, x in itens)
    return f'<p class="olho">{olho_txt}</p><h2 id="t-dif">{titulo}</h2><ul class="provas3">{lis}</ul>'


def passos_seg(d, caminho, titulo):
    """Os três passos, com o lembrete de que a Equatorial continua e o botão do WhatsApp logo embaixo."""
    c = caminho_curto(caminho)
    return (f'{passos(d, titulo)}<p class="cmp-eq">{icone("tomada")}<span><strong>Você continua pagando a Equatorial.'
            f'</strong> A conta dela fica menor e chega uma segunda, da AESOLAR, com o desconto. A soma das duas é que '
            f'fica mais barata.</span></p>'
            f'<p class="passos-bt">{wa(d, MSG_FATURA, c + ":passos", "Mandar minha fatura pelo WhatsApp")}</p>')
