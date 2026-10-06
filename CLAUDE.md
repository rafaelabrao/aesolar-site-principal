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

## Como trabalhar aqui

Explique o porquê de cada mudança em linguagem direta e mostre o resultado
(build local ou captura de tela) antes de publicar.
