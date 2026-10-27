#!/usr/bin/env python3
"""Prepara os arquivos de imagem e fonte do site a partir dos originais no OneDrive.

    .venv/bin/python gerador/prepara_assets.py

Precisa do Pillow, do fontTools e do brotli (estão no .venv do projeto). Só reduz, recorta e converte:
nunca retoca foto. Grava em site/assets/ e em site/ (ícones). Rodar de novo só quando um original mudar.

As fotos das usinas vêm do banco que a Academia já tratou (22_ACADEMIA_AESOLAR/03_INSUMOS/fotos_usinas),
porque lá elas estão SEM os dados de GPS: quatro dos originais de 15 - .../Fotos/ têm a coordenada exata da
usina e nunca podem ir para o site. Por garantia, o Pillow regrava cada foto sem nenhum metadado.
"""
import glob
import io
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(AQUI), 'site')
IMG = os.path.join(SITE, 'assets', 'img')
FONTES = os.path.join(SITE, 'assets', 'fontes')


def onedrive():
    # O nome da pasta muda com o idioma do macOS (OneDrive-Pessoal / OneDrive-Personal): procurar, nunca fixar.
    achados = glob.glob(os.path.expanduser('~/Library/CloudStorage/OneDrive*'))
    if not achados:
        sys.exit('Não achei a pasta do OneDrive em ~/Library/CloudStorage/.')
    return achados[0]


OD = onedrive()
MKT = os.path.join(OD, 'Boreal Solar - Usinas 1', '09-Associação', '15 - AESOLAR_MARKETING_IA')
LOGOS = os.path.join(MKT, 'AESOLAR - Identidade Visual', 'logos')
FOTOS = os.path.join(MKT, '22_ACADEMIA_AESOLAR', '03_INSUMOS', 'fotos_usinas')
INTER = os.path.expanduser('~/Projetos/aesolar/app/public/fonts/Inter-VariableFont_opsz_wght.ttf')

# nome no site: (arquivo de origem, recorte (proporção largura/altura) ou None)
FOTOS_SITE = {
    'vereda-aerea': ('complexo_vereda_01.jpg', None),                     # vista aérea do complexo pronto
    'vereda-paineis': ('complexo_vereda_02.jpg', None),                   # painéis em operação
    'vereda-inversores': ('complexo_vereda_03.jpg', None),                # casa de inversores e conexão à rede
    'vereda-entardecer': ('banco_complexo_vereda/vereda_14_20231208.jpg', 4 / 3),
    'vereda-inversores-dentro': ('banco_complexo_vereda/vereda_16_20231212.jpg', 4 / 3),
}
LARGURAS = (640, 800, 1024, 1600)

# Fotos dos protótipos da capa (sessão A3). Cada uma: (pasta, arquivo, proporção, foco, larguras).
# O foco (x, y, de 0 a 1) é o ponto da foto que fica no centro do recorte.
# As de banco (Unsplash, Pexels) são PROVISÓRIAS: estão marcadas em dados.json ("imagens_banco") e o
# gerador não publica com elas. Os originais ficam em entregas-intensivo/A3-imagens-banco/, só neste Mac.
BANCO = os.path.join(os.path.dirname(AQUI), 'entregas-intensivo', 'A3-imagens-banco')
# As geradas por IA (Gemini, 22/10/2026, prompts da A3 §5.2) também são provisórias e ficam fora do git.
GEMINI = os.path.join(os.path.dirname(AQUI), 'entregas-intensivo', 'A4-imagens-gemini')
# A fatura real do caso (cliente anônimo, com termo assinado), tarjada; e a foto de Goiânia à noite, do Rafael.
CASO = os.path.join(os.path.dirname(AQUI), 'entregas-intensivo', 'A4-caso')
VEREDA = os.path.join(FOTOS, 'banco_complexo_vereda')
FOTOS_CAPAS = {
    # a usina ao entardecer: em pé no celular (9:16), deitada no computador (16:10)
    'vereda-entardecer-retrato': (VEREDA, 'vereda_14_20231208.jpg', 9 / 16, (0.47, 0.5), (480, 640, 810)),
    'vereda-entardecer-larga': (VEREDA, 'vereda_14_20231208.jpg', 16 / 10, (0.5, 0.45), (1024, 1440, 1920)),
    'vereda-ceu': (VEREDA, 'vereda_09_20230209.jpg', 16 / 9, (0.5, 0.5), (640, 1024, 1600, 1920)),
    'vereda-aerea-larga': (FOTOS, 'complexo_vereda_01.jpg', 16 / 8, (0.5, 0.55), (640, 1024, 1600)),
    # banco (provisórias)
    # foto do Rafael (real; a localização do celular sai ao regravar)
    'goiania-noite': (CASO, 'goiania-noite-rafael.jpeg', 16 / 9, (0.5, 0.66), (640, 1024, 1600, 1920)),
    # IA (provisórias): cenas sem rosto, nunca como usina nem como cliente
    'ia-condominio': (GEMINI, 'condominio-2.jpeg', 4 / 3, (0.5, 0.5), (480, 640, 800)),
    'ia-comercio': (GEMINI, 'comercio.jpeg', 4 / 3, (0.5, 0.5), (480, 640, 800)),
    'ia-varias-unidades': (GEMINI, 'varias-unidades-1.jpeg', 4 / 3, (0.5, 0.5), (480, 640, 800)),
    # em pé, para caber no fim alto do celular; no computador o recorte mostra o celular e a conta
    'ia-fatura': (GEMINI, 'fatura-1.jpeg', 4 / 5, (0.5, 0.5), (640, 1024, 1600)),
    # foto real (não é banco): a fatura inteira, sem recorte
    'caso-fatura': (CASO, 'fatura-flamboyant-set2026-tarjada.png', 1306 / 1205, (0.5, 0.5), (480, 800, 1200)),
}


def recorta_foco(im, proporcao, foco):
    """Como recorta(), mas com o centro do recorte no ponto de foco, sem sair da foto."""
    w, h = im.size
    fx, fy = foco
    if w / h > proporcao:
        nw = round(h * proporcao)
        x = min(max(0, round(w * fx - nw / 2)), w - nw)
        return im.crop((x, 0, x + nw, h))
    nh = round(w / proporcao)
    y = min(max(0, round(h * fy - nh / 2)), h - nh)
    return im.crop((0, y, w, y + nh))


def fotos_capas():
    for nome, (pasta, arq, proporcao, foco, larguras) in FOTOS_CAPAS.items():
        src = os.path.join(pasta, arq)
        if not os.path.isfile(src):
            sys.exit(f'Não achei {src}')
        im = recorta_foco(Image.open(src).convert('RGB'), proporcao, foco)
        for w in larguras:
            if w > im.width:
                sys.exit(f'{nome}: a foto recortada tem {im.width} px, menos que os {w} pedidos.')
            r = im.resize((w, round(w / proporcao)), Image.LANCZOS)
            a = grava(r, os.path.join(IMG, f'{nome}-{w}.avif'), quality=52, speed=4)
            b = grava(r, os.path.join(IMG, f'{nome}-{w}.webp'), quality=72, method=6)
            print(f'{nome}-{w}: {r.width}x{r.height}  avif {a // 1024} KB  webp {b // 1024} KB')


def recorta(im, proporcao):
    if not proporcao:
        return im
    w, h = im.size
    if w / h > proporcao:
        nw = round(h * proporcao)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = round(w / proporcao)
    return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def sem_borda(im):
    """Corta a margem transparente do PNG do logo."""
    caixa = im.getchannel('A').getbbox()
    return im.crop(caixa) if caixa else im


def grava(im, caminho, **op):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    im.save(caminho, **op)
    return os.path.getsize(caminho)


def fotos():
    for nome, (origem, proporcao) in FOTOS_SITE.items():
        src = os.path.join(FOTOS, origem)
        im = recorta(Image.open(src).convert('RGB'), proporcao)
        for w in LARGURAS:
            if w > im.width:
                continue
            r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            a = grava(r, os.path.join(IMG, f'{nome}-{w}.avif'), quality=55, speed=4)
            b = grava(r, os.path.join(IMG, f'{nome}-{w}.webp'), quality=74, method=6)
            print(f'{nome}-{w}: {r.width}x{r.height}  avif {a // 1024} KB  webp {b // 1024} KB')


def logos():
    for nome, arq in (('logo-claro', 'aesolar-logo-fundo-claro.png'), ('logo-escuro', 'aesolar-logo-fundo-escuro.png'),
                      ('logo-branco', 'aesolar-logo-branco.png')):
        im = sem_borda(Image.open(os.path.join(LOGOS, arq)).convert('RGBA'))
        h = 80  # 2x da altura de exibição (40 px), nítido em tela de celular
        r = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
        n = grava(r, os.path.join(IMG, f'{nome}.webp'), quality=90, method=6)
        print(f'{nome}.webp: {r.width}x{r.height}  {n // 1024} KB')

    marca = sem_borda(Image.open(os.path.join(LOGOS, 'aesolar-mark-simbolo.png')).convert('RGBA'))

    def quadrado(lado, fundo=None):
        m = marca.copy()
        m.thumbnail((round(lado * 0.86), round(lado * 0.86)), Image.LANCZOS)
        q = Image.new('RGBA', (lado, lado), fundo or (0, 0, 0, 0))
        q.paste(m, ((lado - m.width) // 2, (lado - m.height) // 2), m)
        return q

    quadrado(48).save(os.path.join(SITE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    grava(quadrado(32), os.path.join(SITE, 'favicon-32.png'), optimize=True)
    # ícone da tela inicial do iPhone: fundo branco, porque o iOS põe preto onde é transparente
    grava(quadrado(180, (255, 255, 255, 255)).convert('RGB'), os.path.join(SITE, 'apple-touch-icon.png'), optimize=True)
    print('favicon.ico, favicon-32.png, apple-touch-icon.png')


def imagem_de_compartilhar():
    """1200x630, a prévia que o WhatsApp e o Facebook mostram: a usina real, com o logo numa faixa escura."""
    im = Image.open(os.path.join(FOTOS, 'complexo_vereda_01.jpg')).convert('RGB')
    im = recorta(im, 1200 / 630).resize((1200, 630), Image.LANCZOS)
    faixa = Image.new('RGBA', (1200, 150), (15, 23, 42, 235))       # --slate-900 da identidade visual
    im.paste(faixa, (0, 480), faixa)
    logo = sem_borda(Image.open(os.path.join(LOGOS, 'aesolar-logo-fundo-escuro.png')).convert('RGBA'))
    logo = logo.resize((round(logo.width * 96 / logo.height), 96), Image.LANCZOS)
    im.paste(logo, (56, 507), logo)
    n = grava(im, os.path.join(IMG, 'compartilhar.jpg'), quality=82, optimize=True, progressive=True)
    print(f'compartilhar.jpg: 1200x630  {n // 1024} KB')


def fonte():
    """Inter (a fonte da marca), só com os caracteres do português e o eixo de peso de 400 a 800.
    O original variável tem 850 KB; o recorte fica perto de 50 KB."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    from fontTools import subset

    f = instancer.instantiateVariableFont(TTFont(INTER), {'opsz': 14, 'wght': (400, 800)})
    tmp = io.BytesIO()
    f.save(tmp)
    tmp.seek(0)
    f = TTFont(tmp)  # recarregar: o subsetter falha com a fonte que o instancer deixa carregada pela metade
    op = subset.Options()
    op.flavor = 'woff2'
    op.layout_features = ['kern', 'liga', 'calt', 'tnum', 'case']
    op.name_IDs = ['*']
    op.notdef_outline = True
    sub = subset.Subsetter(op)
    faixas = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [
        0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2192, 0x2212, 0x20AC, 0x00B7, 0x2009, 0x202F]
    sub.populate(unicodes=faixas)
    sub.subset(f)
    os.makedirs(FONTES, exist_ok=True)
    destino = os.path.join(FONTES, 'inter-latin.woff2')
    buf = io.BytesIO()
    subset.save_font(f, buf, op)
    with open(destino, 'wb') as out:
        out.write(buf.getvalue())
    print(f'inter-latin.woff2: {len(buf.getvalue()) // 1024} KB')


if __name__ == '__main__':
    for pasta, nome in ((LOGOS, 'logos'), (FOTOS, 'fotos das usinas')):
        if not os.path.isdir(pasta):
            sys.exit(f'Não achei a pasta de {nome}: {pasta}')
    if sys.argv[1:] == ['capas']:
        # só as fotos dos protótipos da capa: não regrava as da v1
        fotos_capas()
        sys.exit(0)
    if not os.path.isfile(INTER):
        sys.exit(f'Não achei a fonte Inter em {INTER}')
    fotos()
    logos()
    imagem_de_compartilhar()
    fonte()
