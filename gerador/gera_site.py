#!/usr/bin/env python3
"""Gera o site da AESOLAR (aesolar.com.br): todas as páginas, inclusive a capa, o sitemap.xml e o robots.txt.

    python3 gerador/gera_site.py              grava em site/
    python3 gerador/gera_site.py --confere    não grava: acusa se site/ difere do que sairia agora
    python3 gerador/gera_site.py --producao   como --confere, e também recusa prévia ligada, marca PENDENTE e
                                              simulador sem validação (é o que roda antes de publicar)

Rodar na raiz do repositório. Só Python padrão (3.9 ou mais novo): nada para instalar. Gerar não publica nada.

Números e contatos vêm de gerador/dados.json; o texto de cada página, de gerador/pagina_*.py; as peças comuns,
de gerador/blocos.py; o estilo, de gerador/estilo.css (embutido em cada página). O gerador para, com a
explicação, em vez de gravar página que quebra uma regra da marca ou do site (lista em PROIBIDO e em
confere_pagina).
"""
import hashlib
import html
import json
import os
import re
import sys
from datetime import date

sys.dont_write_bytecode = True  # sem pasta __pycache__ no repositório

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SITE = os.path.join(RAIZ, 'site')  # a pasta que vai ao ar
sys.path.insert(0, AQUI)

import blocos as b  # noqa: E402
import capas  # noqa: E402
from blocos import Erro  # noqa: E402
import pagina_capa, pagina_assinatura, pagina_como_funciona, pagina_usinas, pagina_perguntas  # noqa: E402,E401
import pagina_representante, pagina_privacidade, pagina_termos, pagina_condominios, pagina_404  # noqa: E402,E401
import pagina_comercio, pagina_varias_unidades  # noqa: E402,E401

PAGINAS = [pagina_capa, pagina_assinatura, pagina_como_funciona, pagina_usinas, pagina_perguntas, pagina_representante,
           pagina_privacidade, pagina_termos, pagina_condominios, pagina_comercio, pagina_varias_unidades, pagina_404]

# Regras da marca (fonte única comercial §4 e CLAUDE.md do aesolar-marketing). Se uma aparecer, a página não é gravada.
PROIBIDO = [
    (r'\b26\s*%', 'o desconto da marca é "até 30%"; "26%" é do site antigo'),
    (r'energia\s+(?:gr[áa]tis|gratuita|de\s+gra[çc]a)', 'nunca "energia grátis"'),
    (r'zer(?:e|ar|a)\s+(?:a\s+|sua\s+)?conta', 'nunca "zere sua conta"'),
    (r'pare\s+de\s+pagar', 'nunca "pare de pagar a Equatorial": o cliente continua pagando a distribuidora'),
    (r'economia\s+imediata', 'nunca "economia imediata": os créditos levam em torno de 60 dias'),
    (r'desde\s+a\s+primeira\s+fatura', 'nunca "desde a primeira fatura": os créditos levam em torno de 60 dias'),
    (r'serve\s+para\s+qualquer\s+empresa', 'nunca "serve para qualquer empresa"'),
    (r'(?:economia|desconto)s?\s+garantid', 'nunca economia ou desconto garantido'),
    (r'\bcentenas\s+de\b|\bmilhares\s+de\b', 'não citar quantidade de clientes'),
    (r'\b\d[\d.]*\s+(?:clientes|associados|empresas\s+atendidas|munic[íi]pios|cidades\s+atendidas)\b',
     'não citar quantidade de clientes nem de municípios'),
    (r'\b(?:kWp|MWp|megawatts?|MW\b|kW\b)', 'não citar potência nem capacidade de usina'),
    (r'\b\d+\s+usinas\b', 'não citar quantidade de usinas: "usinas em diversas regiões de Goiás"'),
    (r'lorem\s+ipsum', 'texto de enchimento'),
    (r'993420248', 'número antigo do WhatsApp'),
    (r'sem\s+fidelidade', 'só depois da decisão D2 sobre os termos do contrato'),
]

PALAVRAS_TITULO = (10, 60)    # caracteres do <title>
PALAVRAS_DESCRICAO = (70, 160)


class Dados:
    def __init__(self, bruto, hoje):
        self.b = bruto
        self.hoje = hoje
        self.site = bruto['site'].rstrip('/')
        self.emp = bruto['empresa']
        self.of = bruto['oferta']
        self.sim = bruto['simulador']
        self.previa = bruto['previa']
        self.previa_paginas = set(bruto.get('previa_paginas', []))
        self.avisos = []
        self.verificacao_google = bruto.get('verificacao_google', '')
        if self.verificacao_google and not re.fullmatch(r'google[0-9a-f]{16}\.html', self.verificacao_google):
            raise Erro('dados.json: "verificacao_google" tem de ser o nome do arquivo do Search Console (google + 16 letras e números + .html).')
        if not isinstance(self.previa, bool):
            raise Erro('dados.json: "previa" tem de ser true ou false.')
        if not re.fullmatch(r'55\d{10,11}', self.emp['whatsapp']):
            raise Erro('dados.json: o WhatsApp precisa de 55 + DDD + número, só dígitos.')
        s = self.sim
        if not (0 < s['desconto_min_pct'] <= s['desconto_max_pct'] <= self.of['desconto_max_pct']):
            raise Erro('dados.json: a faixa de desconto do simulador tem de ficar entre 0 e o desconto máximo da oferta.')
        if s['validado_em'] is None:
            self.avisos.append('Simulador PROVISÓRIO: "validado_em" vazio em dados.json (decisão D4).')
        # o que o simulador do navegador recebe: os parâmetros e o mínimo da oferta, de um lugar só
        self.sim_params = {k: v for k, v in s.items() if not k.startswith('_') and k not in ('exemplos', 'tarifa_fonte')}
        self.sim_params['minimo_conta'] = self.of['minimo_conta']
        for x in bruto['depoimentos'] + bruto.get('casos', []):
            if not (x.get('termo_assinado') is True and x.get('fatura_tarjada') is True):
                raise Erro(f'Depoimento sem termo assinado e fatura tarjada: "{x.get("quem", "?")}". Sem termo, sem depoimento.')
        for x in bruto.get('casos', []):
            if abs(x['sem_aesolar'] - x['com_aesolar'] - x['economia']) > 0.02:
                raise Erro(f'dados.json: no caso "{x["id"]}", sem_aesolar - com_aesolar não dá a economia.')
        # Economia gerada: piso de 50 em 50 mil, para o "mais de" ser verdade todo dia; o texto sai daqui, de um lugar só.
        piso = self.of['economia_gerada_piso']
        if not (isinstance(piso, int) and piso > 0 and piso % 50000 == 0):
            raise Erro('dados.json: "economia_gerada_piso" tem de ser múltiplo de 50 mil (arredondado para baixo).')
        if piso >= 1000000:
            raise Erro('dados.json: a economia gerada chegou a R$ 1 milhão. O formato "R$ N mil" não serve mais: ajustar '
                       'capas.numeros, os selos e capas.js para "milhão" antes de atualizar.')
        self.of['economia_gerada'] = f'mais de R$ {piso // 1000} mil'
        dias = (hoje - date.fromisoformat(self.of['economia_gerada_data'])).days
        if dias > 45:
            self.avisos.append(f'Economia gerada atualizada há {dias} dias: cresce cerca de R$ 50 mil por mês. Conferir no app '
                               f'(economia entregue) e atualizar "economia_gerada_piso".')
        for h in bruto['historia']:
            h['texto'] = h['texto'].replace('{economia_gerada}', self.of['economia_gerada'])
        self.caminhos = {m.CAMINHO for m in PAGINAS}
        for s_ in bruto['segmentos']:
            if s_['pagina'] and s_['pagina'] not in self.caminhos:
                raise Erro(f'dados.json: o segmento "{s_["nome"]}" aponta para {s_["pagina"]}, que não é uma página gerada.')

    def em_previa(self, caminho):
        return self.previa or caminho in self.previa_paginas or caminho == '/404.html'

    def link_ok(self, caminho):
        """Pode haver link para esta página? Página em prévia individual só recebe link enquanto o site todo é prévia."""
        if not caminho:
            return False
        return self.previa or caminho not in self.previa_paginas


def css_minimo(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{}:;,>])\s*', r'\1', css)
    return css.replace(';}', '}').strip()


def versao(arquivo):
    with open(os.path.join(SITE, arquivo.lstrip('/')), 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


_CSS_EXTRA = {}


def css_extra(nome):
    """Estilo que só algumas páginas usam (os protótipos da capa): conferido como o principal e embutido só nelas."""
    if nome not in _CSS_EXTRA:
        with open(os.path.join(AQUI, nome), encoding='utf-8') as f:
            bruto = f.read()
        confere_css(bruto, nome)
        _CSS_EXTRA[nome] = css_minimo(bruto)
    return _CSS_EXTRA[nome]


# Página aberta com ?limpo no endereço esconde as marcas PENDENTE e a faixa da prévia: só para julgar o visual.
CABECA_JS = ('<script>(function(h){h.classList.add("js");'
             'if(/[?&]limpo(&|=|$)/.test(location.search))h.classList.add("limpo")})(document.documentElement)</script>')


GTM = """<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
(function(){var c=null;try{c=localStorage.getItem('aes_cookies');}catch(e){}
var v=c==='nao'?'denied':'granted';
gtag('consent','default',{ad_storage:v,ad_user_data:v,ad_personalization:v,analytics_storage:v});
// Medição só no domínio oficial (os testes na prévia não entram nos relatórios) e depois que a página abriu.
if(!/(^|\\.)%(dominio)s$/.test(location.hostname))return;
addEventListener('load',function(){setTimeout(function(){
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','%(gtm)s');},1500);});})();
</script>"""


def imagem_de_compartilhar(m):
    """A prévia no WhatsApp e no Facebook: a da página (com o título dela), ou a geral, com a usina e o logo."""
    return f'compartilhar-{b.caminho_curto(m.CAMINHO)}.jpg' if getattr(m, 'COMPARTILHAR', None) else 'compartilhar.jpg'


def alt_compartilhar(m):
    if getattr(m, 'COMPARTILHAR', None):
        return ' — '.join(m.COMPARTILHAR).replace('\n', ' ')
    return 'Vista aérea do Complexo Vereda, usina solar da Boreal Solar em Goiás, com o logo da AESOLAR'


def monta(d, m, css, v):
    caminho = m.CAMINHO
    corpo = m.corpo(d)
    url = d.site + (caminho if caminho != '/404.html' else '/')
    noindex = d.em_previa(caminho) or getattr(m, 'SEMPRE_NOINDEX', False)
    nos = [b.organizacao(d)] + m.schema(d)
    sim = ''
    if m.SIMULADOR:
        sim = (f'<script type="application/json" id="sim-params">{json.dumps(d.sim_params, ensure_ascii=False)}</script>'
               f'<script src="/assets/simulador.js?v={v["simulador.js"]}" defer></script>')
    for js in getattr(m, 'JS_EXTRA', []):
        sim += f'<script src="/assets/{js}?v={v.get(js) or versao("/assets/" + js)}" defer></script>'
    if getattr(m, 'CSS_EXTRA', None):
        css = css + css_extra(m.CSS_EXTRA)
    classe = f' class="{m.CLASSE_BODY}"' if getattr(m, 'CLASSE_BODY', None) else ''
    sprite_extra = m.SPRITE_EXTRA() if getattr(m, 'SPRITE_EXTRA', None) else ''
    barra_msg = getattr(m, 'MSG', None)
    barra = (b.barra_wa(d, caminho) if not barra_msg else
             f'<div class="barra" data-barra>{b.wa(d, barra_msg, b.caminho_curto(caminho) + ":barra", "Quero ser representante", "btn btn-pri btn-larga")}</div>')
    pend = len(re.findall(r'data-pendente="', corpo))
    faixa = ''
    if d.previa:
        faixa = (f'<div class="faixa-previa" role="note">PRÉVIA, não indexada · '
                 f'{pend} pendência{"s" if pend != 1 else ""} nesta página</div>')
    medicao = '' if d.previa else GTM % {'dominio': re.escape(d.emp['dominio_medicao']), 'gtm': d.emp['gtm']}
    return (
        '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{b.e(m.TITULO)}</title>\n<meta name="description" content="{b.e(m.DESCRICAO)}">\n'
        + (f'<link rel="canonical" href="{url}">\n' if caminho != '/404.html' else '')
        + ('<meta name="robots" content="noindex, nofollow">\n' if noindex else '')
        + f'<meta property="og:type" content="website">\n<meta property="og:locale" content="pt_BR">\n'
        f'<meta property="og:site_name" content="AESOLAR">\n<meta property="og:title" content="{b.e(m.TITULO)}">\n'
        f'<meta property="og:description" content="{b.e(m.DESCRICAO)}">\n<meta property="og:url" content="{url}">\n'
        f'<meta property="og:image" content="{d.site}/assets/img/{imagem_de_compartilhar(m)}">\n'
        '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{b.e(alt_compartilhar(m))}">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="theme-color" content="#0F172A">\n'
        '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" href="/favicon-32.png" type="image/png">\n'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '<link rel="preload" href="/assets/fontes/inter-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
        + (b.preload_foto(m.FOTO_TOPO) + '\n' if getattr(m, 'FOTO_TOPO', None) else '')
        + (m.PRELOAD + '\n' if getattr(m, 'PRELOAD', None) else '')
        + f'<style>{css}</style>\n{b.json_ld(nos)}\n'
        f'{CABECA_JS}\n'
        f'<script src="/assets/site.js?v={v["site.js"]}" defer></script>\n{sim}\n{medicao}\n</head>\n'
        f'<body{classe} data-segmento="{m.SEGMENTO}" data-integracao="{d.b["integracao"]["modo"]}" '
        f'data-endpoint="{d.b["integracao"]["endpoint"]}" data-politica="{d.b["integracao"]["politica_versao"]}" '
        f'data-wa-numero="{d.emp["whatsapp"]}">\n'
        f'<a class="pular" href="#conteudo">Pular para o conteúdo</a>\n{faixa}{b.AVISO_COOKIES}\n'
        f'{b.cabecalho(d, caminho, m.CABECALHO, getattr(m, "SIM_HREF", "/#simulador"))}\n<main id="conteudo">\n{corpo}\n</main>\n'
        f'{b.rodape(d, caminho)}\n{barra}\n{b.sprite()}{sprite_extra}\n</body>\n</html>\n'
    )


def texto_visivel(pagina):
    t = re.sub(r'(?s)<(script|style|svg)\b.*?</\1>', ' ', pagina)
    t = re.sub(r'(?s)<!--.*?-->', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t).replace(' ', ' '))


def confere_pagina(d, m, pagina):
    c = m.CAMINHO
    visivel = texto_visivel(pagina)
    atributos = ' '.join(re.findall(r'(?:alt|title|content|data-wa|aria-label)="([^"]*)"', pagina))
    todo_texto = visivel + ' ' + html.unescape(atributos)
    for rx, porque in PROIBIDO:
        achou = re.search(rx, todo_texto, flags=re.I)
        if achou:
            raise Erro(f'{c}: "{achou.group(0)}" — {porque}.')

    # percentuais: só os da oferta e da faixa do simulador; o teto sempre com "até" (ou como fim da faixa "20% a 30%")
    s, teto = d.sim, d.of['desconto_max_pct']
    permitidos = {teto, s['desconto_min_pct'], s['desconto_max_pct']}
    for x in re.finditer(r'(\d+(?:,\d+)?)\s?%', todo_texto):
        n = float(x.group(1).replace(',', '.'))
        if n not in permitidos:
            raise Erro(f'{c}: percentual "{x.group(0)}" fora da oferta e da faixa do simulador (dados.json).')
        antes = todo_texto[max(0, x.start() - 12):x.start()].lower()
        if n == teto and not (antes.endswith('até ') or re.search(r'\d%\s+a\s+$', antes)):
            raise Erro(f'{c}: "{x.group(0)}" sem "até" antes ("...{antes}{x.group(0)}"). É sempre "até {teto:g}%".')

    if len(re.findall(r'<h1[ >]', pagina)) != 1:
        raise Erro(f'{c}: a página precisa de exatamente um título principal (h1).')
    if not (PALAVRAS_TITULO[0] <= len(m.TITULO) <= PALAVRAS_TITULO[1]):
        raise Erro(f'{c}: o <title> tem {len(m.TITULO)} caracteres; o Google corta depois de {PALAVRAS_TITULO[1]}.')
    if not (PALAVRAS_DESCRICAO[0] <= len(m.DESCRICAO) <= PALAVRAS_DESCRICAO[1]):
        raise Erro(f'{c}: a descrição tem {len(m.DESCRICAO)} caracteres; precisa de {PALAVRAS_DESCRICAO[0]} a {PALAVRAS_DESCRICAO[1]}.')
    if ('name="robots" content="noindex' in pagina) != (d.em_previa(c) or getattr(m, 'SEMPRE_NOINDEX', False)):
        raise Erro(f'{c}: o "não indexar" não bate com "previa" / "previa_paginas" em dados.json.')

    # WhatsApp: saudação padrão, lugar marcado, número só de dados.json
    for msg, onde in re.findall(r'data-wa="([^"]*)" data-where="([^"]*)"', pagina):
        if not html.unescape(msg).startswith(b.SAUDACAO) or len(msg) < 30:
            raise Erro(f'{c}: mensagem de WhatsApp fora do padrão: "{msg}"')
        if not re.fullmatch(r'[a-z0-9-]+:[a-z]+', onde):
            raise Erro(f'{c}: lugar do botão de WhatsApp fora do padrão "página:posição": "{onde}"')
    if pagina.count('data-wa="') != len(re.findall(r'data-wa="[^"]*" data-where="', pagina)):
        raise Erro(f'{c}: há botão de WhatsApp sem data-where.')
    for num in re.findall(r'wa\.me/(\d+)', pagina):
        if num != d.emp['whatsapp']:
            raise Erro(f'{c}: link de WhatsApp para {num}, que não é o número de dados.json.')

    # links internos e âncoras
    ids = set(re.findall(r'\bid="([^"]+)"', pagina))
    for ref in set(re.findall(r'href="([^"]+)"', pagina)):
        if re.match(r'(?:https?:|mailto:|tel:|//)', ref):
            continue
        if ref.startswith('#'):
            if ref[1:] not in ids:
                raise Erro(f'{c}: âncora {ref} sem o id correspondente na página.')
            continue
        alvo = ref.split('#')[0].split('?')[0]
        if alvo in d.caminhos:
            if not d.link_ok(alvo) and alvo != c:
                raise Erro(f'{c}: link para {alvo}, que está em prévia individual.')
            continue
        if not os.path.isfile(os.path.join(SITE, alvo.lstrip('/'))):
            raise Erro(f'{c}: link para {ref}, que não existe.')

    # imagens: arquivo existe, com largura, altura e texto alternativo (sem isso a tela pula ao carregar)
    for tag in re.findall(r'<img\b[^>]*>', pagina):
        for attr in ('src', 'width', 'height', 'alt'):
            if f' {attr}="' not in tag:
                raise Erro(f'{c}: imagem sem {attr}: {tag[:90]}')
    for ref in set(re.findall(r'(?:src|srcset)="([^"]+)"', pagina)):
        for parte in ref.split(','):
            arq = parte.strip().split(' ')[0].split('?')[0]
            if arq.startswith('/') and not os.path.isfile(os.path.join(SITE, arq.lstrip('/'))):
                raise Erro(f'{c}: arquivo que não existe: {arq}')

    # a prévia de compartilhar existe (é gerada por prepara_assets.py compartilhar, a partir de COMPARTILHAR)
    if not os.path.isfile(os.path.join(SITE, 'assets', 'img', imagem_de_compartilhar(m))):
        raise Erro(f'{c}: falta a imagem de compartilhar {imagem_de_compartilhar(m)}. Rode '
                   f'.venv/bin/python gerador/prepara_assets.py compartilhar')

    # uma fonte única de cor: nenhuma cor escrita no HTML (só a theme-color, que o navegador pede)
    sem_meta = re.sub(r'<meta name="theme-color"[^>]*>|<style>.*?</style>', '', pagina, flags=re.S)  # o CSS tem conferência própria
    cor = re.search(r'#[0-9a-fA-F]{3,8}\b(?=[;"\s)])|rgba?\(|hsla?\(', re.sub(r'href="[^"]*"', '', sem_meta))
    if cor:
        raise Erro(f'{c}: cor escrita direto no HTML ({cor.group(0)}). Cor só nos tokens de gerador/estilo.css.')
    if re.search(r'<form\b[^>]*method="get"', pagina, re.I):
        raise Erro(f'{c}: formulário com method="get" põe dado pessoal no endereço.')

    # dados para o Google: JSON válido, com a organização e os tipos que a página promete
    blocos_ld = re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', pagina)
    if len(blocos_ld) != 1:
        raise Erro(f'{c}: esperava um bloco de dados para o Google, achei {len(blocos_ld)}.')
    tipos = {x['@type'] for x in json.loads(blocos_ld[0].replace('<\\/', '</'))['@graph']}
    if 'Organization' not in tipos:
        raise Erro(f'{c}: dados para o Google sem a organização.')
    if hasattr(m, 'MIGALHAS') and 'BreadcrumbList' not in tipos:
        raise Erro(f'{c}: página com migalhas sem BreadcrumbList nos dados para o Google.')
    if 'class="faq"' in pagina and 'FAQPage' not in tipos:
        raise Erro(f'{c}: página com perguntas sem FAQPage nos dados para o Google.')
    confere_imagens_banco(d, c, pagina)
    return len(re.findall(r'data-pendente="', pagina))


def confere_css(css, nome='estilo.css'):
    """Cor só dentro de :root (os tokens). Fora dele, só var(--...)."""
    fora = re.sub(r'(?s):root\s*\{.*?\}', '', re.sub(r'(?s)/\*.*?\*/', '', css))
    achou = re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(', fora)
    if achou:
        linha = fora[:achou.start()].count('\n') + 1
        raise Erro(f'gerador/{nome}: cor solta fora de :root ("{achou.group(0)}", perto da linha {linha}). '
                   f'Crie um token em :root e use var(--nome).')


def provisorias(pagina):
    """As fotos de banco (ou de IA) que a página usa: as marcadas com data-provisoria."""
    return sorted(set(re.findall(r'data-provisoria="([^"]+)"', pagina)))


def confere_imagens_banco(d, c, pagina):
    """Foto de banco só entra marcada como provisória, e nunca como a usina da AESOLAR ou como cliente."""
    reg = d.b.get('imagens_banco', {})
    for nome in provisorias(pagina):
        if nome not in reg:
            raise Erro(f'{c}: foto "{nome}" marcada como provisória, mas fora de "imagens_banco" em dados.json.')
    for nome, alt in re.findall(r'(?s)<picture[^>]*data-provisoria="([^"]+)"[^>]*>.*?<img[^>]*\balt="([^"]*)"', pagina):
        if capas.NAO_PODE_DIZER.search(html.unescape(alt)):
            raise Erro(f'{c}: foto de banco "{nome}" descrita como usina ou cliente: "{alt}".')
    marcadas = set(provisorias(pagina))
    for nome in set(re.findall(r'/assets/img/([a-z0-9-]+?)-\d+\.(?:avif|webp)', pagina)):
        if nome in reg and reg[nome].get('provisoria', True) and nome not in marcadas:
            raise Erro(f'{c}: a foto de banco "{nome}" aparece sem a marca de provisória (use capas.foto).')


def mapa_do_site(d):
    urls = [m.CAMINHO for m in PAGINAS if not d.em_previa(m.CAMINHO) and not getattr(m, 'SEMPRE_NOINDEX', False)]
    linhas = '\n'.join(f'  <url><loc>{d.site}{u}</loc></url>' for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- Gerado por gerador/gera_site.py: não editar à mão. -->\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{linhas}\n</urlset>\n')


def robots(d):
    if d.previa:
        return '# Prévia: nada indexado. Gerado por gerador/gera_site.py.\nUser-agent: *\nDisallow: /\n'
    return f'# Gerado por gerador/gera_site.py.\nUser-agent: *\nAllow: /\n\nSitemap: {d.site}/sitemap.xml\n'


def arquivo_de(caminho):
    if caminho.endswith('.html'):
        return os.path.join(SITE, caminho.lstrip('/'))
    return os.path.join(SITE, caminho.strip('/'), 'index.html') if caminho != '/' else os.path.join(SITE, 'index.html')


def main(argv):
    so_confere = '--confere' in argv or '--producao' in argv
    producao = '--producao' in argv
    with open(os.path.join(AQUI, 'dados.json'), encoding='utf-8') as f:
        d = Dados(json.load(f), date.today())
    with open(os.path.join(AQUI, 'estilo.css'), encoding='utf-8') as f:
        bruto_css = f.read()
    confere_css(bruto_css)
    css = css_minimo(bruto_css)
    v = {'site.js': versao('/assets/site.js'), 'simulador.js': versao('/assets/simulador.js')}

    v['capas.js'] = versao('/assets/capas.js')

    saidas, pendencias, banco = [], {}, {}
    for m in PAGINAS:
        pagina = monta(d, m, css, v)
        n = confere_pagina(d, m, pagina)
        if n:
            pendencias[m.CAMINHO] = sorted(set(re.findall(r'data-pendente="([^"]+)"', pagina)), key=lambda x: (len(x), x))
        if provisorias(pagina):
            banco[m.CAMINHO] = provisorias(pagina)
        saidas.append((m.CAMINHO, arquivo_de(m.CAMINHO), pagina))
    saidas.append(('/sitemap.xml', os.path.join(SITE, 'sitemap.xml'), mapa_do_site(d)))
    saidas.append(('/robots.txt', os.path.join(SITE, 'robots.txt'), robots(d)))
    if d.verificacao_google:
        saidas.append(('/' + d.verificacao_google, os.path.join(SITE, d.verificacao_google),
                       f'google-site-verification: {d.verificacao_google}'))

    diferentes = 0
    for caminho, arquivo, conteudo in saidas:
        atual = None
        if os.path.isfile(arquivo):
            with open(arquivo, encoding='utf-8') as f:
                atual = f.read()
        mudou = atual != conteudo
        diferentes += mudou
        if not so_confere and mudou:
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
        estado = ('DIFERENTE do que está na pasta' if mudou else 'igual') if so_confere else ('gravada' if mudou else 'sem mudança')
        print(f'{caminho:<40} {len(conteudo.encode("utf-8")) / 1024:5.1f} KB  {estado}')

    print('\nPrévia (não indexar, robots fechado): ' + ('SIM, o site todo' if d.previa else 'não, liberado para o Google'))
    if d.previa_paginas:
        print('Em prévia, uma a uma: ' + ', '.join(sorted(d.previa_paginas)))
    total = sum(len(x) for x in pendencias.values())
    if pendencias:
        print(f'\nMarcas PENDENTE ({total}):')
        for cam, cods in pendencias.items():
            print(f'  {cam:<40} {", ".join(cods)}')
    if banco:
        print('\nImagens provisórias, de banco ou de IA (aprovar ou trocar antes de publicar):')
        for cam, nomes in banco.items():
            print(f'  {cam:<40} {", ".join(nomes)}')
    prototipos = [m.CAMINHO for m in PAGINAS if getattr(m, 'PROTOTIPO', False)]
    if prototipos:
        print('Protótipos (não indexados, fora do sitemap): ' + ', '.join(prototipos))
    for a in d.avisos:
        print('AVISO: ' + a)

    erros = []
    if so_confere and diferentes:
        erros.append('As páginas da pasta não batem com a fonte. Rode sem --confere.')
    if producao:
        if d.previa:
            erros.append('"previa" ainda é true em dados.json.')
        if pendencias:
            erros.append(f'Ainda há {total} marca(s) PENDENTE.')
        if banco:
            erros.append('Imagem provisória (banco ou IA) em ' + ', '.join(banco) + ' (dados.json, imagens_banco).')
        if prototipos:
            erros.append('Protótipo da capa ainda no site: ' + ', '.join(prototipos) + '. Escolhida a capa, tire os outros.')
        if d.sim['validado_em'] is None:
            erros.append('O simulador não foi validado com faturas reais ("validado_em").')
        if d.b['integracao']['modo'] != 'app':
            erros.append('O formulário ainda está em modo "simulado" (dados.json, integracao.modo).')
    for x in erros:
        print('NÃO PUBLICAR: ' + x)
    return 1 if erros else 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except Erro as x:
        print('NÃO GEROU: ' + str(x), file=sys.stderr)
        sys.exit(2)
