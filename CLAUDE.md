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

Armadilhas já pagas no site novo:

- Ícone de `<symbol>` reaproveitado com `<use>` herda `fill` e `stroke` do `<svg>` que o usa, não do
  sprite: sem `fill: none; stroke: currentColor` em `.ic`, sai borrão preto.
- Regra de cor para parágrafo de seção escura (`.topo p`) vaza para o cartão branco do simulador dentro
  dela. Cor de texto em fundo escuro vai no contêiner, e o parágrafo herda.
- Captura de página inteira do Playwright desenha a barra fixa no meio da página: esconder a barra na
  captura e conferir a barra numa captura da tela.
- fontTools: recortar a Inter depois do `instancer` dá `KeyError`; salvar e recarregar a fonte entre os
  dois passos.

## Como trabalhar aqui

Explique o porquê de cada mudança em linguagem direta e mostre o resultado
(build local ou captura de tela) antes de publicar.
