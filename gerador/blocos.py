"""Peças comuns das páginas do site da AESOLAR: cabeçalho, rodapé, simulador, blocos da capa, formulário,
dados para o Google e o esqueleto da página. O texto próprio de cada página fica em pagina_*.py; números e
contatos vêm de dados.json (objeto Dados, em gera_site.py)."""
import html
import json
import re
from urllib.parse import quote


class Erro(Exception):
    """Algo que impede gerar a página. A mensagem diz o que corrigir."""


def e(s):
    return html.escape(str(s), quote=True)


def reais(n):
    """5000 -> 'R$ 5.000' (com espaço que não quebra a linha)."""
    return 'R$ ' + f'{int(n):,}'.replace(',', '.')


def mes_ano(iso):
    meses = 'jan fev mar abr mai jun jul ago set out nov dez'.split()
    a, m = iso[:4], int(iso[5:7])
    return f'{meses[m - 1]}/{a}'


def pct(n):
    return f'{n:g}%'


def tarifa(n):
    return 'R$ ' + f'{n:.2f}'.replace('.', ',')


# ---------- marca de pendência: aparece em amarelo na prévia; o gerador não libera o site com uma delas ----------

def pendente(cod, texto):
    return (f'<span class="pend" data-pendente="{e(cod)}"><b>PENDENTE {e(cod)}</b> {texto}</span>')


def pendente_bloco(cod, texto):
    return (f'<p class="pend pend-bloco" data-pendente="{e(cod)}"><b>PENDENTE {e(cod)}</b> {texto}</p>')


# ---------- ícones (Lucide, a família da identidade visual; o do WhatsApp é a marca dele) ----------

_ICONES = {
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'seta': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'abre': '<path d="m6 9 6 6 6-6"/>',
    'menu': '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    'fecha': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    'relogio': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'fatura': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
              '<path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    'sol': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/>'
           '<path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/>'
           '<path d="m19.07 4.93-1.41 1.41"/>',
    'escudo': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 '
              '6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'predio': '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/>'
              '<path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/>'
              '<path d="M10 14h4"/><path d="M10 18h4"/>',
    'loja': '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/>'
            '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/>'
            '<path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12'
            'a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 '
            '0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>',
    'rede': '<rect x="16" y="16" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/>'
            '<rect x="9" y="2" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/>'
            '<path d="M12 12V8"/>',
    'local': '<path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0"/>'
             '<circle cx="12" cy="10" r="3"/>',
    'email': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    'recibo': '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/>'
              '<path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 17.5v-11"/>',
    'raio': '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 '
            '.78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    'calculadora': '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M8 6h8"/><path d="M16 14v4"/>'
                   '<path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/>'
                   '<path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
    'pessoas': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
               '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    'caneta': '<path d="M12 20h9"/><path d="M16.38 3.62a1 1 0 0 1 3 3L7.37 18.64a2 2 0 0 1-.86.5l-2.87.84a.5.5 0 0 1'
              '-.62-.62l.84-2.87a2 2 0 0 1 .5-.86z"/>',
    'tomada': '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    'igual': '<path d="M5 9h14"/><path d="M5 15h14"/>',
    'olho': '<path d="M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0"/>'
            '<circle cx="12" cy="12" r="3"/>',
    'instagram': '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
                 '<path d="M17.5 6.5h.01"/>',
}
_WHATSAPP = ('<path fill="currentColor" stroke="none" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3'
             '-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13'
             '-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.91-2.2-.24-.58-.49-.5-.67-.51'
             '-.17-.01-.37-.01-.57-.01-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 '
             '3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08'
             '-.13-.27-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1'
             '-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88'
             '-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3'
             '-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41Z"/>')


def sprite():
    simbolos = ''.join(f'<symbol id="i-{n}" viewBox="0 0 24 24">{p}</symbol>' for n, p in _ICONES.items())
    simbolos += f'<symbol id="i-whatsapp" viewBox="0 0 24 24">{_WHATSAPP}</symbol>'
    return (f'<svg class="sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{simbolos}</svg>')


def icone(nome, cls='ic'):
    if nome != 'whatsapp' and nome not in _ICONES:
        raise Erro(f'Ícone "{nome}" não existe em blocos.py.')
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{nome}"/></svg>'


# ---------- WhatsApp: todo botão sai com a saudação padrão; o site.js troca por "Vim pelo Google" quando é o caso ----------

SAUDACAO = 'Olá! Vim pelo site.'


def wa_href(d, msg):
    return f'https://wa.me/{d.emp["whatsapp"]}?text={quote(msg)}'


def wa(d, msg, onde, texto, cls='btn btn-pri', com_icone=True):
    if not msg.startswith(SAUDACAO):
        msg = f'{SAUDACAO} {msg}'
    ic = icone('whatsapp') if com_icone else ''
    return (f'<a class="{cls}" href="{e(wa_href(d, msg))}" data-wa="{e(msg)}" data-where="{e(onde)}" '
            f'target="_blank" rel="noopener">{ic}<span>{texto}</span></a>')


MSG_FATURA = f'{SAUDACAO} Quero mandar minha fatura para a análise gratuita.'


# ---------- fotos: AVIF e WebP, nos tamanhos que prepara_assets.py gerou ----------

FOTOS = {
    # nome: (largura, altura) do arquivo de 1600 (ou o maior), para a proporção
    'vereda-aerea': (1600, 870),
    'vereda-paineis': (1600, 1200),
    'vereda-inversores': (1600, 1200),
    'vereda-entardecer': (1600, 1200),
    'vereda-inversores-dentro': (1600, 1200),
}
LARGURAS = (640, 800, 1024, 1600)


SIZES_LARGA = '(min-width: 1120px) 1088px, calc(100vw - 32px)'


def preload_foto(nome, sizes=SIZES_LARGA):
    """Para a foto que é o maior bloco da tela (LCP): o navegador começa a baixar antes de ler o corpo da página."""
    w = FOTOS[nome][0]
    srcset = ', '.join(f'/assets/img/{nome}-{x}.avif {x}w' for x in LARGURAS if x <= w)
    return f'<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset}" imagesizes="{sizes}" fetchpriority="high">'


def foto(nome, alt, sizes=SIZES_LARGA, lazy=True, cls='foto'):
    if nome not in FOTOS:
        raise Erro(f'Foto "{nome}" não está em blocos.FOTOS (e em prepara_assets.py).')
    w, h = FOTOS[nome]
    srcset = lambda ext: ', '.join(f'/assets/img/{nome}-{x}.{ext} {x}w' for x in LARGURAS if x <= w)
    carga = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"'
    return (f'<picture class="{cls}"><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<img src="/assets/img/{nome}-1024.webp" srcset="{srcset("webp")}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {carga}></picture>')


# ---------- cabeçalho, rodapé, barra fixa, aviso de cookies ----------

MENU = [('/como-funciona/', 'Como funciona'), ('/usinas/', 'Usinas'), ('/perguntas-frequentes/', 'Perguntas')]


def cabecalho(d, caminho, tipo, sim_href='/#simulador'):
    logo = ('<a class="cab-logo" href="/" aria-label="AESOLAR, página inicial">'
            '<img src="/assets/img/logo-escuro.svg" width="134" height="40" alt="AESOLAR — Powered by Boreal Solar"></a>')
    if tipo == 'enxuto':
        return (f'<header class="cab cab-enxuto"><div class="wrap cab-in">{logo}'
                f'{wa(d, MSG_FATURA, caminho_curto(caminho) + ":cabecalho", "WhatsApp", "cab-wa")}</div></header>')
    atual = ' aria-current="page"'
    itens = ''.join(f'<li><a href="{u}"{atual if u == caminho else ""}>{t}</a></li>' for u, t in MENU)
    extra = ''.join(f'<li><a href="{s["pagina"]}">{s["nome"]}</a></li>'
                    for s in d.b['segmentos'] if d.link_ok(s['pagina']))
    return (f'<header class="cab"><div class="wrap cab-in">{logo}'
            f'<nav class="cab-nav" aria-label="Principal"><ul>{itens}</ul></nav>'
            f'<a class="btn btn-fantasma btn-p cab-sim" href="{sim_href}">{icone("calculadora")}<span>Simular</span></a>'
            f'<details class="cab-menu"><summary aria-label="Abrir o menu">{icone("menu", "ic ic-abre")}'
            f'{icone("fecha", "ic ic-fecha")}</summary>'
            f'<nav class="cab-gaveta" aria-label="Menu"><ul>{itens}{extra}'
            f'<li><a href="/representante/">Seja representante</a></li></ul>'
            f'{wa(d, MSG_FATURA, caminho_curto(caminho) + ":menu", "Mandar minha fatura", "btn btn-pri")}</nav>'
            f'</details></div></header>')


def caminho_curto(caminho):
    """'/como-funciona/' -> 'como-funciona'; '/' -> 'capa'; '/404.html' -> '404'. Vai no data-where da medição."""
    return caminho.strip('/').split('/')[-1].replace('.html', '') or 'capa'


def rodape(d, caminho):
    emp = d.emp
    links = [('/como-funciona/', 'Como funciona'), ('/usinas/', 'Nossas usinas'),
             ('/perguntas-frequentes/', 'Perguntas frequentes'),
             ('/energia-solar-por-assinatura-goias/', 'Energia solar por assinatura em Goiás')]
    links += [(s['pagina'], s['nome']) for s in d.b['segmentos'] if d.link_ok(s['pagina'])]
    links += [('/representante/', 'Seja representante'), ('/politica-de-privacidade/', 'Política de privacidade'),
              ('/termos-de-uso/', 'Termos de uso')]
    lis = ''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in links)
    return (
        f'<footer class="rod"><div class="wrap rod-in">'
        f'<div class="rod-marca"><img src="/assets/img/logo-escuro.svg" width="134" height="40" loading="lazy" '
        f'alt="AESOLAR — Powered by Boreal Solar"><p>Energia solar por assinatura para empresas e condomínios de Goiás, '
        f'com usinas próprias no estado.</p></div>'
        f'<nav class="rod-links" aria-label="Rodapé"><ul>{lis}</ul></nav>'
        f'<div class="rod-contato"><p class="rod-tit">Fale com a gente</p><ul>'
        f'<li>{wa(d, MSG_FATURA, caminho_curto(caminho) + ":rodape", emp["whatsapp_exibir"], "rod-wa", True)}</li>'
        f'<li><a href="mailto:{emp["email"]}">{icone("email")}<span>{emp["email"]}</span></a></li>'
        f'<li><a href="{emp["instagram"]}" target="_blank" rel="noopener">{icone("instagram")}<span>@aesolar.go</span></a></li>'
        f'<li class="rod-end">{icone("local")}<span>{emp["rua"]}, {emp["bairro"]}, {emp["cidade"]}-{emp["uf"]}</span></li>'
        f'</ul></div></div>'
        f'<div class="wrap rod-base"><p>Atendemos empresas e condomínios em Goiás, inclusive o Entorno do DF atendido pela '
        f'Equatorial Goiás. O Distrito Federal não é atendido.</p>'
        f'<p>{emp["razao_social"]} · CNPJ {emp["cnpj"]} · {emp["assinatura"]}</p></div></footer>')


def barra_wa(d, caminho):
    return (f'<div class="barra" data-barra>{wa(d, MSG_FATURA, caminho_curto(caminho) + ":barra", "Mandar minha fatura pelo WhatsApp", "btn btn-pri btn-larga")}</div>')


AVISO_COOKIES = (
    '<div class="ck" id="ck" role="region" aria-label="Aviso de cookies" hidden><div class="wrap ck-in">'
    '<p>Usamos cookies para medir de onde vêm as visitas e os anúncios. '
    '<a href="/politica-de-privacidade/#cookies">Saiba mais</a>.</p>'
    '<div class="ck-bt"><button type="button" class="btn btn-sec btn-p" data-ck="nao">Recusar</button>'
    '<button type="button" class="btn btn-escuro btn-p" data-ck="sim">Aceitar</button></div></div></div>')


# ---------- blocos de conteúdo ----------

def secao(conteudo, cls='', id_=None, rotulo=None):
    i = f' id="{id_}"' if id_ else ''
    r = f' aria-labelledby="{rotulo}"' if rotulo else ''
    return f'<section class="sec {cls}"{i}{r}><div class="wrap">{conteudo}</div></section>'


def provas():
    itens = [('sol', 'A usina é nossa, em Goiás'), ('relogio', 'Cálculo em reais em até 24 horas'),
             ('escudo', 'Sem obra e sem placa no telhado')]
    return '<ul class="provas">' + ''.join(f'<li>{icone(i)}<span>{t}</span></li>' for i, t in itens) + '</ul>'


def topo(d, caminho, olho, h1, sub, sim_titulo='Quanto sua empresa economiza, em reais'):
    """O topo escuro: texto à esquerda, simulador à direita (no celular, um embaixo do outro)."""
    return (
        f'<section class="topo"><div class="wrap topo-in"><div class="topo-txt">'
        f'<p class="olho olho-escuro">{icone("local")}<span>{olho}</span></p>'
        f'<h1>{h1}</h1><p class="topo-sub">{sub}</p>'
        f'<div class="topo-bt">{wa(d, MSG_FATURA, caminho_curto(caminho) + ":topo", "Mandar minha fatura pelo WhatsApp")}'
        f'<a class="btn btn-fantasma" href="#simulador">{icone("calculadora")}<span>Simular em reais</span></a></div>'
        f'{provas()}</div>{simulador(d, caminho, sim_titulo)}</div></section>')


def simulador(d, caminho, titulo):
    s = d.sim
    onde = caminho_curto(caminho) + ':simulador'
    chips = ''.join(f'<button type="button" class="chip" data-sim-exemplo="{v}">{reais(v)}</button>' for v in s['exemplos'])
    linha = lambda rot, k, cls='': (f'<div class="nota-linha {cls}"><dt>{rot}</dt><dd data-sim="{k}">—</dd></div>')
    provisorio = '' if s['validado_em'] else pendente(
        'D4', 'Simulador provisório: premissas a calibrar com 3 ou 4 faturas reais tarjadas.')
    return (
        f'<div class="sim" id="simulador" data-simulador="{onde}"><h2 class="sim-tit">{titulo}</h2>'
        f'<label class="sim-rot" for="conta-{caminho_curto(caminho)}">Valor médio da conta de luz, por mês</label>'
        f'<div class="sim-campo"><span aria-hidden="true">R$</span><input id="conta-{caminho_curto(caminho)}" name="conta" '
        f'type="text" inputmode="numeric" autocomplete="off" placeholder="0" aria-describedby="sim-ajuda-{caminho_curto(caminho)}"></div>'
        f'<div class="chips" role="group" aria-label="Exemplos de valor">{chips}</div>'
        f'<label class="caixa"><input type="checkbox" name="varias"><span>Somei a conta de mais de uma unidade</span></label>'
        f'<p class="sim-vazio" data-sim-vazio id="sim-ajuda-{caminho_curto(caminho)}">Digite o valor da conta ou toque num exemplo. '
        f'A economia aparece aqui, em reais, sem pedir seu contato.</p>'
        f'<p class="sim-abaixo" data-sim-abaixo hidden>A assinatura é para contas a partir de {reais(d.of["minimo_conta"])} '
        f'por mês. Se a empresa tem mais de uma unidade, some as contas.</p>'
        f'<div class="nota" data-sim-saida hidden aria-live="polite"><dl>'
        f'{linha("Sua conta hoje", "conta")}'
        f'{linha("Fica fora do desconto <small>custo mínimo, iluminação pública e tributos</small>", "fora")}'
        f'{linha("Parte da energia que a usina abate", "abatido")}</dl>'
        f'<div class="nota-total"><p class="nota-rot">Economia estimada por mês</p>'
        f'<p class="nota-valor"><span data-sim="min">—</span> <span class="nota-a">a</span> <span data-sim="max">—</span></p>'
        f'<p class="nota-ano">Em 12 meses: <span data-sim="ano_min">—</span> a <span data-sim="ano_max">—</span></p></div></div>'
        f'<a class="btn btn-pri btn-larga" data-sim-cta hidden href="{e(wa_href(d, SAUDACAO + " Quero o cálculo exato."))}" '
        f'data-wa="{e(SAUDACAO + " Quero o cálculo exato da minha conta.")}" data-where="{e(onde)}" target="_blank" rel="noopener">'
        f'{icone("whatsapp")}<span>Receber o cálculo exato pelo WhatsApp</span></a>'
        f'<p class="sim-prem">Premissas: tarifa de {tarifa(s["tarifa_kwh"])} por kWh ({s["tarifa_fonte"]}, '
        f'{mes_ano(s["tarifa_data"])}), desconto de {pct(s["desconto_min_pct"])} a {pct(s["desconto_max_pct"])} sobre a '
        f'energia abatida, bandeira verde, baixa tensão (Grupo B). <strong>O número real vem da sua fatura.</strong></p>'
        f'<details class="sim-como"><summary>Como a conta é feita {icone("abre")}</summary>'
        f'<p>A economia vale só sobre a energia que a usina abate da sua conta. Ficam fora o custo mínimo que a Equatorial '
        f'cobra de toda ligação ({s["disponibilidade_kwh"]} kWh numa ligação trifásica), a iluminação pública e parte dos '
        f'tributos. Por isso a gente mostra a economia em reais, e não em percentual da conta inteira.</p></details>'
        f'{provisorio}<noscript><p class="sim-vazio">Para simular, ative o JavaScript, ou mande a fatura pelo WhatsApp.</p></noscript></div>')


def passos(d, caminho, link=True):
    of = d.of
    itens = [
        ('fatura', 'Mande a fatura', 'Pelo WhatsApp, em foto ou PDF. A análise é gratuita e sem compromisso.'),
        ('calculadora', 'Receba o cálculo em reais',
         f'Em até {of["proposta_horas"]} horas: quanto você paga hoje e quanto vai pagar com a AESOLAR.'),
        ('caneta', 'Assine e comece a receber',
         f'O contrato é assinado pelo celular. Os créditos começam em torno de {of["creditos_dias_normal"]} dias '
         f'(o contrato prevê até {of["creditos_dias_contrato"]}).'),
    ]
    lis = ''.join(f'<li class="passo"><span class="passo-n" aria-hidden="true">{i}</span><div>'
                  f'<h3>{t}</h3><p>{txt}</p></div></li>' for i, (_, t, txt) in enumerate(itens, 1))
    mais = '<p class="mais"><a href="/como-funciona/">Ver o passo a passo completo ' + icone('seta') + '</a></p>' if link else ''
    return (f'<p class="olho">Como funciona</p><h2 id="t-passos">Três passos, sem obra</h2>'
            f'<ol class="passos">{lis}</ol>'
            f'<p class="aviso-eq">{icone("tomada")}<span><strong>Você continua pagando a Equatorial.</strong> A conta dela fica '
            f'menor e chega uma segunda conta, da AESOLAR, com o desconto. A soma das duas é que fica mais barata.</span></p>{mais}')


def duas_contas(d):
    """O desenho de "como fica a conta", com o exemplo calculado pela mesma conta do simulador."""
    from simulador import estima
    s = d.sim
    r = estima(s['exemplo_pagina'], d.sim_params)
    total = r['equatorial_depois'] + r['aesolar_min']
    w = lambda v: f'{v / r["conta"] * 100:.1f}%'
    return (
        f'<figure class="contas"><figcaption><strong>Exemplo: conta de {reais(r["conta"])} por mês</strong>, com o desconto '
        f'mínimo de {pct(s["desconto_min_pct"])} e as premissas do simulador.</figcaption>'
        f'<div class="contas-linha"><p class="contas-rot">Hoje</p><div class="contas-barra">'
        f'<span class="cb cb-eq" style="width:100%">Equatorial {reais(r["conta"])}</span></div></div>'
        f'<div class="contas-linha"><p class="contas-rot">Com a AESOLAR</p><div class="contas-barra">'
        f'<span class="cb cb-eq" style="width:{w(r["equatorial_depois"])}" title="Equatorial {reais(r["equatorial_depois"])}"></span>'
        f'<span class="cb cb-ae" style="width:{w(r["aesolar_min"])}">AESOLAR {reais(r["aesolar_min"])}</span>'
        f'<span class="cb cb-eco" style="width:{w(r["conta"] - total)}" aria-hidden="true"></span></div></div>'
        f'<dl class="contas-leg"><div><dt><i class="cb-eq"></i>Equatorial, depois</dt><dd>{reais(r["equatorial_depois"])}</dd></div>'
        f'<div><dt><i class="cb-ae"></i>AESOLAR</dt><dd>{reais(r["aesolar_min"])}</dd></div>'
        f'<div><dt><i class="cb-eco"></i>Fica com você</dt><dd>{reais(r["conta"] - total)} por mês</dd></div></dl>'
        f'{"" if s["validado_em"] else pendente("D4", "Exemplo calculado com as premissas provisórias do simulador.")}'
        f'</figure>')


def usina(d, titulo_tag='h2'):
    return (
        f'<div class="usina"><div class="usina-txt"><p class="olho olho-escuro">A usina é nossa</p>'
        f'<{titulo_tag} id="t-usina">Sua energia vem de uma usina que você pode ver</{titulo_tag}>'
        f'<p>A energia que chega à sua empresa é gerada em usinas da Boreal Solar em Goiás. A principal é o '
        f'<strong>Complexo Vereda</strong>, a cerca de 30 km de Goiânia, em operação desde 2023.</p>'
        f'<p>A usina gera, a energia entra na rede da Equatorial e vira crédito na conta da sua empresa. Nada de placa no seu '
        f'telhado, obra ou manutenção do seu lado.</p>'
        f'<p class="mais mais-escuro"><a href="/usinas/">Ver as fotos das usinas {icone("seta")}</a></p></div>'
        f'<figure class="usina-foto">{foto("vereda-aerea", "Vista aérea do Complexo Vereda, usina solar da Boreal Solar em Goiás", "(min-width: 900px) 560px, calc(100vw - 32px)")}'
        f'<figcaption>Complexo Vereda, visto de cima. Foto real, sem retoque.</figcaption></figure></div>')


def perguntas_bloco(d, itens, titulo='Perguntas frequentes', link=True, h='h2', id_titulo='t-faq'):
    corpo = ''.join(
        f'<details class="faq" id="{x["id"]}"><summary><span>{x["p"]}</span>{icone("abre")}</summary>'
        f'<div class="faq-r">{x["r"]}</div></details>' for x in itens)
    mais = (f'<p class="mais"><a href="/perguntas-frequentes/">Ver todas as perguntas {icone("seta")}</a></p>' if link else '')
    tit = f'<p class="olho">Dúvidas</p><{h} id="{id_titulo}">{titulo}</{h}>' if titulo else ''
    return f'{tit}<div class="faqs">{corpo}</div>{mais}'


def contato(d, caminho, segmento='geral', titulo='Mande a fatura e receba o cálculo em reais'):
    c = caminho_curto(caminho)
    return (
        f'<div class="contato"><div class="contato-txt"><p class="olho olho-escuro">Análise gratuita</p>'
        f'<h2 id="t-contato">{titulo}</h2>'
        f'<p>Mande uma foto ou o PDF da última conta da Equatorial. Em até {d.of["proposta_horas"]} horas você recebe quanto '
        f'paga hoje e quanto vai pagar com a AESOLAR, em reais.</p>'
        f'{wa(d, MSG_FATURA, c + ":contato", "Mandar minha fatura pelo WhatsApp", "btn btn-pri btn-larga")}</div>'
        f'<form class="form" data-form data-segmento="{e(segmento)}" novalidate>'
        f'<p class="form-tit">Prefere que a gente chame?</p>'
        f'{campo("nome", "Seu nome", "text", "name", c)}'
        f'{campo("whatsapp", "WhatsApp com DDD", "tel", "tel", c, inputmode="tel")}'
        f'{campo("cidade", "Cidade", "text", "address-level2", c)}'
        f'{campo("valor", "Valor médio da conta (R$ por mês)", "text", "off", c, inputmode="numeric")}'
        f'{campo("email", "E-mail (opcional)", "email", "email", c, obrigatorio=False)}'
        f'<label class="caixa"><input type="checkbox" name="varias"><span>Somei a conta de mais de uma unidade</span></label>'
        f'<div class="isca" aria-hidden="true"><label for="website-{c}">Não preencha</label>'
        f'<input id="website-{c}" name="website" type="text" tabindex="-1" autocomplete="off"></div>'
        f'<button class="btn btn-pri btn-larga" type="submit">{icone("whatsapp")}<span>Enviar e abrir o WhatsApp</span></button>'
        f'<p class="form-lgpd">Ao enviar, você concorda com a <a href="/politica-de-privacidade/">Política de privacidade</a>. '
        f'Seus dados servem só para preparar a proposta.</p>'
        f'<div class="form-msg" data-form-msg role="status" aria-live="polite" hidden></div></form></div>')


def campo(nome, rotulo, tipo, auto, sufixo, inputmode=None, obrigatorio=True):
    im = f' inputmode="{inputmode}"' if inputmode else ''
    req = ' required' if obrigatorio else ''
    return (f'<div class="campo"><label for="{nome}-{sufixo}">{rotulo}</label>'
            f'<input id="{nome}-{sufixo}" name="{nome}" type="{tipo}" autocomplete="{auto}"{im}{req}>'
            f'<p class="campo-erro" hidden></p></div>')


def migalhas(itens):
    lis = ''.join(f'<li><a href="{u}">{t}</a></li>' if u else f'<li aria-current="page">{t}</li>' for t, u in itens)
    return f'<nav class="mig" aria-label="Você está em"><ol>{lis}</ol></nav>'


def cabeca_pagina(olho, h1, intro, migs=None):
    return (f'<section class="pg-topo"><div class="wrap">{migalhas(migs) if migs else ""}'
            f'<p class="olho olho-escuro">{olho}</p><h1>{h1}</h1><p class="pg-intro">{intro}</p></div></section>')


def cta_final(d, caminho, titulo='Quanto a sua empresa economiza?', texto=None):
    texto = texto or (f'Mande a fatura pelo WhatsApp e receba o cálculo em reais em até {d.of["proposta_horas"]} horas. '
                      f'A análise é gratuita.')
    return secao(f'<div class="cta"><h2>{titulo}</h2><p>{texto}</p><div class="cta-bt">'
                 f'{wa(d, MSG_FATURA, caminho_curto(caminho) + ":final", "Mandar minha fatura pelo WhatsApp")}'
                 f'<a class="btn btn-fantasma" href="/#simulador">{icone("calculadora")}<span>Simular em reais</span></a>'
                 f'</div></div>', 'sec-escura')


# ---------- dados para o Google (JSON-LD) ----------

def organizacao(d):
    emp = d.emp
    return {
        '@type': 'Organization', '@id': f'{d.site}/#organizacao', 'name': 'AESOLAR', 'legalName': emp['razao_social'],
        'url': f'{d.site}/', 'logo': f'{d.site}/assets/img/logo-claro.webp', 'taxID': emp['cnpj'],
        'email': emp['email'], 'sameAs': [emp['instagram']],
        'address': {'@type': 'PostalAddress', 'streetAddress': emp['rua'], 'addressLocality': emp['cidade'],
                    'addressRegion': emp['uf'], 'addressCountry': 'BR'},
        'contactPoint': {'@type': 'ContactPoint', 'telephone': '+' + emp['whatsapp'], 'contactType': 'sales',
                         'areaServed': 'BR-GO', 'availableLanguage': 'pt-BR'},
        'parentOrganization': {'@type': 'Organization', 'name': 'Boreal Solar'},
    }


def servico(d, caminho, publico=None):
    """O serviço; nas páginas de segmento, com o público delas (publico: 'condomínios', 'comércio e serviços'...)."""
    no = {
        '@type': 'Service', '@id': f'{d.site}{caminho}#servico',
        'name': 'Energia solar por assinatura (geração compartilhada)' + (f' para {publico}' if publico else ''),
        'serviceType': f'Energia solar por assinatura para {publico or "empresas e condomínios"}',
        'provider': {'@id': f'{d.site}/#organizacao'},
        'areaServed': {'@type': 'State', 'name': 'Goiás', 'containedInPlace': {'@type': 'Country', 'name': 'Brasil'}},
        'description': (f'Créditos de energia de usina solar própria em Goiás, com economia de até '
                        f'{pct(d.of["desconto_max_pct"])} na parte da energia da conta da Equatorial.'),
    }
    if publico:
        no['audience'] = {'@type': 'BusinessAudience', 'name': publico[0].upper() + publico[1:]}
    return no


def texto_puro(h):
    h = re.sub(r'<span class="pend".*?</span>', '', h, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def faq_schema(itens):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': texto_puro(x['p']),
         'acceptedAnswer': {'@type': 'Answer', 'text': texto_puro(x['r'])}} for x in itens if not x.get('pendente')]}


def migalhas_schema(d, itens):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': t, 'item': f'{d.site}{u or itens[-1][1] or ""}'}
        for i, (t, u) in enumerate(itens, 1)]}


def json_ld(nos):
    txt = json.dumps({'@context': 'https://schema.org', '@graph': nos}, ensure_ascii=False, separators=(',', ':'))
    return '<script type="application/ld+json">' + txt.replace('</', '<\\/') + '</script>'
