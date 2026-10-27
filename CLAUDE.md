# Site da Aesolar — aesolar.com.br

Site institucional e de captação de leads da Aesolar. Repositório **público**.

## Push na `main` publica o site

Todo push na branch `main` dispara `.github/workflows/pages.yml`, que compila
e publica em **aesolar.com.br** (GitHub Pages; o domínio vem do arquivo
`CNAME`). Não há etapa de aprovação: o que entra na `main` vai ao ar em poucos
minutos.

Por isso:

- Não faça push na `main` sem o dono do repositório pedir aquela publicação.
- Antes de qualquer push, rode `npm run build` e `npm test`. Build quebrado
  não publica, mas build que passa com conteúdo errado publica.
- Trabalho em andamento fica em outra branch.

## O repositório é público

Qualquer pessoa lê tudo o que está aqui, inclusive o histórico. Nada de
senha, token, dado de cliente ou número interno em arquivo, commit ou
comentário.

A URL do webhook que recebe os leads não está no código: ela entra no build
pelo segredo `VITE_N8N_WEBHOOK_URL` do GitHub Actions. Sem essa variável (por
exemplo, rodando local), o site abre normalmente e só o envio do formulário
avisa que falta configuração.

## Como é feito

- Vite + React + TypeScript + Tailwind, com componentes shadcn/ui. Nasceu no
  Lovable; o `README.md` ainda é o modelo de lá.
- Páginas em `src/pages/`: `Index.tsx` (a home) e `Proposta.tsx`.
- Formulário de lead em `src/components/LeadCaptureForm.tsx`; botão do
  WhatsApp em `src/components/WhatsAppButton.tsx`.
- `public/proposta_old/` é uma página antiga em HTML puro, servida como está.
- `vercel.json` e a menção ao Vercel no formulário são sobra de uma
  hospedagem anterior; a publicação hoje é pelo GitHub Pages.

## Comandos

```bash
npm ci           # instalar dependências
npm run dev      # abrir local, com recarga automática
npm run build    # compilar para dist/
npm test         # testes (vitest)
```

## Site novo (em construção, branch `site-novo`)

Desde 21/10/2026 o site novo está sendo feito na branch local `site-novo`, no modelo do site do Top
Office: HTML pronto por página, gerado de um arquivo único de dados. Proposta e decisões pendentes:
`entregas-intensivo/A2-PROPOSTA-SITE-NOVO.md` (fora do git, só neste Mac). Enquanto não for aprovado,
o site no ar continua sendo o Vite da `main`.

```bash
python3 gerador/gera_site.py              # gera site/ (só Python padrão, 3.9+)
python3 gerador/gera_site.py --producao   # o que precisa passar antes de publicar
python3 gerador/teste_gerador.py          # testes (precisa do node)
python3 -m http.server 8090 --directory site   # ver em http://localhost:8090
.venv/bin/python gerador/prepara_assets.py     # só se mudar foto, logo ou fonte (Pillow e fontTools no .venv)
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
- Lighthouse neste Mac: `CHROME_PATH` apontando para o Chromium do Playwright
  (`~/Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/Google Chrome for Testing.app/...`). Medir o SEO
  numa cópia sem o "não indexar" e com o `robots.txt` aberto; senão dá 69.

## Como trabalhar aqui

Explique o porquê de cada mudança em linguagem direta e mostre o resultado
(build local ou captura de tela) antes de publicar.
