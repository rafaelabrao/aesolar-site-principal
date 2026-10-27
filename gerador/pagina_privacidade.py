"""/politica-de-privacidade/: texto aprovado pelo Rafael em 27/10/2026, sem revisão de advogado. Cita cada campo que o formulário coleta: se o
formulário mudar o que coleta, esta página muda junto."""
import blocos as b

CAMINHO = '/politica-de-privacidade/'
TITULO = 'Política de privacidade | AESOLAR'
DESCRICAO = ('Como a AESOLAR trata os dados de quem visita o site ou pede uma proposta: o que coleta, para quê, com quem '
             'compartilha e como pedir para apagar.')
CABECALHO = 'completo'
SEGMENTO = 'geral'
SIMULADOR = False
MIGALHAS = [('Início', '/'), ('Política de privacidade', None)]


def corpo(d):
    emp = d.emp
    return (
        b.cabeca_pagina('Seus dados', 'Política de privacidade',
                        f'Versão de {d.b["integracao"]["politica_versao"][8:10]}/{d.b["integracao"]["politica_versao"][5:7]}/'
                        f'{d.b["integracao"]["politica_versao"][:4]}. Em linguagem direta, como manda a Lei Geral de Proteção '
                        f'de Dados (Lei 13.709/2018).', MIGALHAS)
        + b.secao(
            '<div class="texto-legal">'
            f'<h2>Quem cuida dos seus dados</h2><p>{emp["razao_social"]}, CNPJ {emp["cnpj"]}, {emp["rua"]}, {emp["bairro"]}, '
            f'{emp["cidade"]}-{emp["uf"]} ("AESOLAR"). Contato para assuntos de privacidade (encarregado): '
            f'<a href="mailto:{emp["email_privacidade"]}">{emp["email_privacidade"]}</a>.</p>'
            '<h2>O que coletamos, e para quê</h2>'
            '<table class="tabela"><thead><tr><th scope="col">Dado</th><th scope="col">Onde</th><th scope="col">Para quê</th></tr></thead><tbody>'
            '<tr><td>Nome</td><td>formulário</td><td>saber com quem falar e preparar a proposta</td></tr>'
            '<tr><td>WhatsApp</td><td>formulário</td><td>responder e mandar a proposta</td></tr>'
            '<tr><td>Cidade</td><td>formulário</td><td>confirmar que atendemos a sua região</td></tr>'
            '<tr><td>Valor médio da conta de luz</td><td>formulário e simulador</td><td>calcular a economia</td></tr>'
            '<tr><td>E-mail (opcional)</td><td>formulário</td><td>mandar a proposta, se você preferir</td></tr>'
            '<tr><td>"Somei mais de uma unidade"</td><td>formulário e simulador</td><td>preparar a proposta certa</td></tr>'
            '<tr><td>Página de entrada e origem da visita (etiquetas de anúncio: utm, gclid, fbclid)</td><td>automático</td>'
            '<td>saber qual anúncio ou página trouxe o pedido</td></tr>'
            '<tr><td>Fatura de energia</td><td>WhatsApp, se você mandar</td><td>fazer o cálculo exato e, se você contratar, '
            'cadastrar sua unidade na usina</td></tr></tbody></table>'
            '<p>O simulador faz a conta no seu próprio navegador: o valor digitado nele não é enviado a ninguém, a não ser que '
            'você mande o formulário ou toque no botão do WhatsApp.</p>'
            '<h2>Por que podemos tratar esses dados</h2><p>Porque você pediu uma proposta: é tratamento para procedimentos '
            'anteriores a um contrato, a seu pedido (Lei 13.709/2018, art. 7º, V). Os cookies de medição dependem da sua '
            'escolha no aviso de cookies.</p>'
            '<h2>Com quem compartilhamos</h2><p>Não vendemos seus dados. Eles passam só pelos serviços que usamos para '
            'funcionar: a hospedagem do site e do nosso sistema, o WhatsApp (Meta) para a conversa e, se você aceitar os '
            'cookies, o Google (Tag Manager, Analytics e Google Ads) e a Meta (Pixel do Facebook e do Instagram) para '
            'medir as visitas e os anúncios.</p>'
            '<h2 id="cookies">Cookies</h2><p>Usamos cookies de medição para saber de onde vêm as visitas e quais anúncios '
            'funcionam. Você pode recusar no aviso que aparece no alto da página, e o site continua funcionando igual. Para '
            'mudar a escolha depois, apague os dados deste site no seu navegador.</p>'
            f'<h2>Por quanto tempo guardamos</h2><p>Se você pediu proposta e não contratou, guardamos seus dados por até '
            f'{d.b["integracao"]["guarda_anos"]} anos depois do último contato, e depois apagamos. Se contratou, guardamos '
            f'enquanto durar o contrato e, depois dele, pelo prazo que a lei exige para documentos fiscais e contratuais.</p>'
            '<h2>Seus direitos</h2><p>Você pode pedir, a qualquer momento, para ver, corrigir ou apagar seus dados, e saber '
            f'com quem foram compartilhados (art. 18 da lei). Basta escrever para <a href="mailto:{emp["email_privacidade"]}">{emp["email_privacidade"]}</a> '
            'ou pedir pelo WhatsApp.</p>'
            '<h2>Mudanças nesta política</h2><p>Se mudarmos o que coletamos, esta página muda junto e a data no alto é '
            'atualizada.</p></div>', '', None)
    )


def schema(d):
    return [b.migalhas_schema(d, MIGALHAS)]
