# Site da Aesolar — aesolar.com.br

Site institucional e de captação de leads da Aesolar. Repositório **público**.

## Push na `main` publica o site

Todo push na branch `main` dispara `.github/workflows/pages.yml`, que **não gera nada**: roda
`gera_site.py --producao` (a pasta `site/` tem de bater com a fonte, prévia desligada, nenhuma marca PENDENTE)
e os testes do gerador, e publica a pasta `site/` em **aesolar.com.br** (GitHub Pages). Não há etapa de
aprovação: o que entra na `main` vai ao ar em poucos minutos. Se a conferência falhar, nada é publicado e o
site anterior continua no ar.

O domínio está nas configurações do Pages do repositório (`rafaelabrao/aesolar-site-principal`, modo
"workflow", HTTPS obrigatório, certificado para `aesolar.com.br` e `www`). O arquivo `CNAME` na raiz é só
registro: não é ele que liga o domínio. O DNS fica na Locaweb, junto com o e-mail: não mexer.

Por isso:

- Não faça push na `main` sem o Rafael pedir aquela publicação.
- Antes de qualquer push: gerar, `--producao` e os testes (abaixo). Conteúdo errado que passa nas travas
  publica.
- Trabalho em andamento fica em outra branch.

**Voltar atrás:** `git revert` do commit (ou do merge, com `-m 1`) e push: o site anterior volta em poucos
minutos. O site antigo inteiro (Vite + React, até 27/10/2026) está na etiqueta `site-antigo-vite`; a página
`/proposta_old/` tem cópia em `entregas-intensivo/backup-site-antigo/`.

## O repositório é público

Qualquer pessoa lê tudo o que está aqui, inclusive o histórico. Nada de senha, token, dado de cliente ou
número interno em arquivo, commit ou comentário.

O formulário manda o lead direto ao app (`integracao.endpoint` em `dados.json`, rota pública do app, que só
aceita a origem `https://aesolar.com.br`). Não há segredo no build. O segredo `VITE_N8N_WEBHOOK_URL` do
GitHub Actions era do site antigo e não é mais usado (não foi apagado: só com ordem do Rafael).

## Como é feito

HTML pronto por página (no modelo do site do Top Office), gerado de um arquivo único de dados. Proposta
original e decisões: `entregas-intensivo/A2-PROPOSTA-SITE-NOVO.md` (fora do git, só neste Mac). No ar desde a
sessão A6 (10/2026).

```bash
python3 gerador/gera_site.py              # gera site/ (só Python padrão, 3.9+)
python3 gerador/gera_site.py --producao   # o que precisa passar antes de publicar
python3 gerador/teste_gerador.py          # testes (precisa do node)
python3 -m http.server 8090 --directory site   # ver em http://localhost:8090
.venv/bin/python gerador/prepara_assets.py     # só se mudar foto, logo ou fonte (Pillow e fontTools no .venv)
.venv/bin/python gerador/prepara_assets.py compartilhar   # só as prévias de WhatsApp/Facebook de cada página
node entregas-intensivo/A5-ferramentas/revisao.cjs <pasta>     # capturas tela a tela (390 e 1440) + conferências
node entregas-intensivo/A5-ferramentas/funcional.cjs <pasta>   # simulador, menu, barra, cookies, formulário (envio interceptado)
```

- `gerador/dados.json` é a fonte única (WhatsApp, mínimo, prazos, parâmetros do simulador). Nunca editar
  o HTML de `site/` à mão.
- O gerador para se achar frase proibida pela marca, percentual sem "até", link quebrado, WhatsApp fora
  do padrão, cor fora dos tokens de `gerador/estilo.css` ou depoimento sem termo. Marcas `PENDENTE Dn`
  são decisões do Rafael (proposta §9); `--producao` não passa com nenhuma.
- A conta do simulador existe em `gerador/simulador.py` e em `site/assets/simulador.js`: mudou uma,
  mude a outra (o teste compara as duas).
- Fotos de usina: só do banco da Academia (`22_ACADEMIA_AESOLAR/03_INSUMOS/fotos_usinas`, sem GPS).
  Os originais de `Fotos/` têm a coordenada da usina. `src/assets/hero-background*.jpg` são banco de
  imagem: não usar.
- O DNS de `aesolar.com.br` está na Locaweb, junto com o e-mail. Por isso a recomendação é continuar no
  GitHub Pages (sem mexer em DNS).
- As duas capas (D19, 26/10/2026): `/` (pagina_capa.py, "a usina é nossa", para quem já conhece a AESOLAR) e
  `/energia-solar-por-assinatura-goias/` (pagina_assinatura.py, o simulador no topo, destino do anúncio do Google, com
  cabeçalho enxuto). Peças em `gerador/capas.py`, estilo em `gerador/estilo_capas.css`, comportamento em
  `site/assets/capas.js`. As peças antigas de `blocos.py` que sobraram servem às páginas internas.
- Foto de banco ou de IA aprovada fica em `imagens_banco` com `"provisoria": false`: sai sem etiqueta, mas continua
  proibido descrevê-la como usina, cliente ou equipe.
- Prévia de compartilhar: página com `COMPARTILHAR = (título, linha de baixo)` no módulo ganha imagem própria
  (`compartilhar-<página>.jpg`, gerada por `prepara_assets.py compartilhar`); sem ele, sai a geral. O texto vira o
  `og:image:alt` e passa pelas travas da marca; o gerador para se a imagem não existir.
- O olho (a linha acima do H1) da página do Google e das de segmento repete a busca do anúncio ("Energia solar por
  assinatura · Goiás", "Energia solar para condomínios · Goiás"): o Google Ads mede se a primeira tela fala da
  palavra-chave (D25 e D26, 27/10/2026).
- SEO, Google Ads e Tag Manager (estado e proposta): `entregas-intensivo/A5-SEO-ADS-MEDICAO.md`. Revisão tela a tela:
  `entregas-intensivo/A5-REVISAO-TELAS.md`.
- `?limpo` no endereço esconde as marcas PENDENTE e a faixa da prévia, só para julgar o visual.
- Economia gerada: `oferta.economia_gerada_piso` em `dados.json`, sempre o valor do app (Painel geral → Economia
  entregue) arredondado PARA BAIXO de 50 em 50 mil; nunca o número exato (o repositório é público). Cresce cerca de
  R$ 50 mil por mês; o gerador avisa depois de 45 dias sem atualizar. `oferta.economia_url` liga a atualização
  automática pelo app (prompt em `entregas-intensivo/A4-PROMPT-APP-ECONOMIA.md`).
- Caso real (`casos` em `dados.json`): sempre anônimo, sem nome (a cidade pode, se o cliente autorizou), com termo
  assinado e fatura tarjada. Números da exportação de faturas do app; a fatura tarjada e a foto de Goiânia à noite
  ficam em `entregas-intensivo/A4-caso/`.
- A multa de saída antecipada fica no contrato, não no site (decisão do Rafael, 27/10/2026).
- Decisões fechadas em 27/10/2026 (zero marca PENDENTE): a AESOLAR confere os créditos todo mês (D3, pode anunciar);
  cobrança única para várias unidades pode ser anunciada (D14); a tabela de comissão do representante não vai ao site
  (D8); fotos de `/usinas/` são do Complexo Vereda (D11); privacidade com `comercial@aesolar.com.br` e guarda de 2
  anos para quem não contratou (D6; termos e política aprovados pelo jurídico em 27/10/2026: mudou, volta para ele); a política cita o Pixel do Meta (D10); kit de
  assembleia de condomínio fica para depois (D17).
- Vídeo do Rafael na usina (D5): até ficar pronto, "Quem está por trás" mostra uma foto real da usina
  (`capas.quem`). Com o vídeo editado, ele entra no lugar da foto.
- Botão do WhatsApp: no celular, barra de lado a lado; no computador, botão redondo no canto (`.barra` em
  `estilo.css`). Os dois somem quando outro botão grande do WhatsApp está na tela (`data-sem-barra`).
- `.venv/bin/python gerador/prepara_assets.py capas` gera só as fotos dos protótipos (os originais de banco ficam em
  `entregas-intensivo/A3-imagens-banco/`); as do Gemini, em
  `entregas-intensivo/A4-imagens-gemini/`, com um LEIA-ME de qual foto vai onde).

Armadilhas já pagas no site novo:

- Ícone de `<symbol>` reaproveitado com `<use>` herda `fill` e `stroke` do `<svg>` que o usa, não do
  sprite: sem `fill: none; stroke: currentColor` em `.ic`, sai borrão preto.
- Regra de cor para parágrafo de seção escura (`.topo p`) vaza para o cartão branco do simulador dentro
  dela. Cor de texto em fundo escuro vai no contêiner, e o parágrafo herda.
- Captura de página inteira do Playwright desenha a barra fixa no meio da página: esconder a barra na
  captura e conferir a barra numa captura da tela.
- fontTools: recortar a Inter depois do `instancer` dá `KeyError`; salvar e recarregar a fonte entre os
  dois passos.
- Seção que "aparece ao rolar" (`.revela`) sai em branco na captura de página inteira se o script rolar rápido
  demais: rolar de 400 em 400 px, com 160 ms de pausa, antes de capturar.
- O gerador roda no Python 3.9 do Mac: f-string dentro de f-string com o mesmo tipo de aspas é erro de sintaxe.
- Regra de elemento dentro de classe (`.pv p`) ganha de classe sozinha (`.pv-num`): escrever `.pv .pv-num`.
- Unsplash: o endereço `/download` responde 401 para navegador; baixar pelo `images.unsplash.com/photo-...?w=2400`.
- potracer (vetorizar PNG): o `Bitmap` trata o valor baixo como tinta; passar a máscara invertida (`~mascara`), senão
  ele pinta o fundo e deixa a figura vazada. Logo em SVG e o script: `entregas-intensivo/A3-logo-svg/` (em revisão).
- Botão fixo que fica acima da borda (o redondo do WhatsApp no computador, `bottom: 1.5rem`): escondido com
  `translateY(110%)` deixa meio botão na tela. O deslocamento soma a folga da borda.
- Legenda branca sobre foto some no céu claro, e o Lighthouse não acusa (o fundo é imagem): legenda sobre foto leva
  fundo escuro próprio (`--veu-3`).
- Texto livre de `dados.json` com valor ("R$ 1.216,00 da Equatorial + R$ ...") quebra a linha entre "R$" e o número:
  o gerador troca o espaço por um que não quebra.
- O app só libera o CORS para `https://aesolar.com.br` (não `www`, não localhost): `capas.js` só busca a economia no
  domínio oficial. Medido fora dele, a busca vira erro de console e derruba "boas práticas".
- `package.json` tem `"type": "module"`: script Node com `require` precisa da extensão `.cjs`.
- Teste que abre outra página do site antes de chegar com `?gclid=` grava a página errada como "primeira da visita":
  ler o que precisar em outro contexto do navegador.
- Formulário em modo `app` manda lead de verdade: teste de tela intercepta o envio (`page.route`), nunca envia.
- Lighthouse neste Mac: `CHROME_PATH` apontando para o Chromium do Playwright
  (`~/Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/Google Chrome for Testing.app/...`). Medir o SEO
  numa cópia sem o "não indexar" e com o `robots.txt` aberto; senão dá 69.

## Como trabalhar aqui

Explique o porquê de cada mudança em linguagem direta e mostre o resultado
(build local ou captura de tela) antes de publicar.
