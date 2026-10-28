# aesolar.com.br

Site da AESOLAR, energia solar por assinatura em Goiás.

O site é HTML pronto (pasta `site/`), gerado por `gerador/gera_site.py` a partir de um arquivo único de dados,
`gerador/dados.json`. Só Python padrão (3.9 ou mais novo); os testes precisam do Node.

```bash
python3 gerador/gera_site.py              # gera site/
python3 gerador/gera_site.py --producao   # a conferência que roda antes de publicar
python3 gerador/teste_gerador.py          # testes
python3 -m http.server 8090 --directory site   # ver em http://localhost:8090
```

Push na `main` publica em aesolar.com.br pelo GitHub Pages (`.github/workflows/pages.yml`).

O site antigo (Vite + React) está na etiqueta `site-antigo-vite`.
