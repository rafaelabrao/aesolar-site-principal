"""/404.html: o GitHub Pages mostra esta página para endereço que não existe. Fora do sitemap e com "não indexar"."""
import blocos as b

CAMINHO = '/404.html'
TITULO = 'Página não encontrada | AESOLAR'
DESCRICAO = ('Esta página não existe ou mudou de endereço. Volte para o início, simule a economia em reais ou fale com a '
             'AESOLAR pelo WhatsApp.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = False
SEMPRE_NOINDEX = True


def corpo(d):
    return (b.cabeca_pagina('Erro 404', 'Esta página não existe', 'O endereço pode ter mudado. Estes caminhos levam ao que '
                            'você procura:')
            + b.secao('<ul class="lista-check">'
                      f'<li>{b.icone("seta")}<a href="/">Página inicial</a></li>'
                      f'<li>{b.icone("seta")}<a href="/#simulador">Simular a economia em reais</a></li>'
                      f'<li>{b.icone("seta")}<a href="/como-funciona/">Como funciona</a></li>'
                      f'<li>{b.icone("seta")}<a href="/perguntas-frequentes/">Perguntas frequentes</a></li></ul>', ''))


def schema(d):
    return []
