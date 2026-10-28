/* AESOLAR — comportamento do site. Tudo funciona sem ele (links de WhatsApp, menu, perguntas); aqui entram a
   mensagem por origem, a medição, a barra fixa, o aviso de cookies e o envio do formulário.
   O número do WhatsApp, o endereço do app e o modo do formulário vêm da página (atributos do <body>),
   que o gerador tira de dados.json: nada disso é escrito aqui. */
(function () {
  'use strict';
  var doc = document, body = doc.body;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var dl = window.dataLayer = window.dataLayer || [];
  var NUMERO = body.getAttribute('data-wa-numero');
  var SAUDACAO = 'Olá! Vim pelo site.';

  // ---------- links antigos do site anterior (aesolar.com.br/#/proposta?nome=...): o pedaço depois do # tem nome e
  // valor da conta. Apaga do endereço (não vai para a medição) e avisa que o link saiu do ar. ----------
  if (/^#\/?proposta/.test(location.hash)) {
    try { history.replaceState(null, '', location.pathname); } catch (e) { location.hash = ''; }
    var aviso = doc.createElement('div');
    aviso.className = 'pend pend-bloco';
    aviso.setAttribute('role', 'status');
    aviso.innerHTML = 'Este link de proposta é do site antigo e saiu do ar. <a href="#contato">Fale com a gente</a> e receba a proposta atualizada.';
    var main = doc.getElementById('conteudo');
    if (main) main.insertBefore(aviso, main.firstChild);
  }

  // ---------- origem da visita: etiquetas do link de chegada, guardadas só na primeira página da visita ----------
  var ETIQUETAS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'];
  var origem = null;
  try { origem = JSON.parse(sessionStorage.getItem('aes_origem') || 'null'); } catch (e) {}
  if (!origem) {
    origem = { pagina_entrada: location.pathname };
    var qs = new URLSearchParams(location.search);
    ETIQUETAS.forEach(function (k) { var x = qs.get(k); if (x) origem[k] = x.slice(0, 200); });
    try { sessionStorage.setItem('aes_origem', JSON.stringify(origem)); } catch (e) {}
  }
  // Quem veio de anúncio diz isso na mensagem, para o comercial registrar o canal certo.
  var fonte = (origem.utm_source || '').toLowerCase();
  var pago = /cpc|paid|ads|an[uú]ncio/i.test(origem.utm_medium || '');
  var SAUDA = (origem.gclid || /google/.test(fonte)) ? 'Olá! Vim pelo Google.'
    : (pago && /facebook|^fb$|meta|^ig$|instagram/.test(fonte)) ? 'Olá! Vi o anúncio no Instagram.' : SAUDACAO;

  function waUrl(msg) { return 'https://wa.me/' + NUMERO + '?text=' + encodeURIComponent(msg); }
  function preparaWa(a) {
    a.href = waUrl((a.getAttribute('data-wa') || SAUDACAO).replace(SAUDACAO, SAUDA));
  }
  window.AesolarWa = preparaWa; // o simulador troca a mensagem do botão dele e chama de novo

  $$('[data-wa]').forEach(function (a) {
    preparaWa(a);
    a.addEventListener('click', function () { dl.push({ event: 'whatsapp_click', local: a.getAttribute('data-where') || '' }); });
  });

  // ---------- o cabeçalho acompanha a página: no computador fica sempre; no celular some ao descer (a barra do
  // WhatsApp já fica fixa embaixo) e volta ao subir. "rolou" deixa o fundo sólido quando ele estava sobre a foto. ----------
  var cab = doc.querySelector('.cab');
  if (cab) {
    var ultimoY = window.scrollY;
    var acompanha = function () {
      var y = window.scrollY;
      cab.classList.toggle('rolou', y > 24);
      if (!cab.querySelector('.cab-menu[open]')) cab.classList.toggle('esconde', y > ultimoY && y > 320);
      ultimoY = y;
    };
    window.addEventListener('scroll', acompanha, { passive: true });
    acompanha();
  }

  // ---------- barra fixa do WhatsApp (no computador, botão no canto): só aparece quando nenhum outro botão de WhatsApp grande está na
  // tela (topo com o simulador, contato, rodapé). Assim ela nunca tapa o botão do simulador, que leva o valor. ----------
  var barra = doc.querySelector('[data-barra]');
  var vigiados = $$('.topo, .pg-topo, #contato, .rod, [data-sem-barra]');
  if (barra && 'IntersectionObserver' in window) {
    var naTela = new Set();
    var io = new IntersectionObserver(function (itens) {
      itens.forEach(function (it) { if (it.isIntersecting) naTela.add(it.target); else naTela.delete(it.target); });
      barra.classList.toggle('mostra', naTela.size === 0);
    });
    vigiados.forEach(function (el) { io.observe(el); });
  } else if (barra) {
    barra.classList.add('mostra');
  }

  // ---------- aviso de cookies: no pé da tela, para não tapar o logo e o menu (Rafael, 28/10/2026). Enquanto está
  // aberto, a barra do WhatsApp sobe a altura dele (--ck-h) e o fim da página ganha a mesma folga ----------
  var ck = doc.getElementById('ck'), escolha = null;
  try { escolha = localStorage.getItem('aes_cookies'); } catch (e) {}
  function alturaCk() { doc.documentElement.style.setProperty('--ck-h', ck.hidden ? '0px' : ck.offsetHeight + 'px'); }
  if (ck && !escolha) {
    ck.hidden = false;
    alturaCk();
    window.addEventListener('resize', alturaCk);
    $$('[data-ck]', ck).forEach(function (bt) {
      bt.addEventListener('click', function () {
        var v = bt.getAttribute('data-ck'), g = v === 'nao' ? 'denied' : 'granted';
        try { localStorage.setItem('aes_cookies', v); } catch (e) {}
        if (window.gtag) window.gtag('consent', 'update', { ad_storage: g, ad_user_data: g, ad_personalization: g, analytics_storage: g });
        dl.push({ event: 'cookie_choice', escolha: v });
        ck.hidden = true;
        alturaCk();
      });
    });
  }

  // ---------- formulário: valida, manda ao app (ou só mostra, no modo "simulado") e abre o WhatsApp ----------
  var MODO = body.getAttribute('data-integracao');
  var ENDPOINT = body.getAttribute('data-endpoint');
  var POLITICA = body.getAttribute('data-politica');

  function digitos(s) { return String(s || '').replace(/\D/g, ''); }
  function valorConta(s) {
    var t = String(s || '').replace(/\s/g, '').replace(/^R\$/i, '').replace(/[.,]\d{1,2}$/, '');
    return parseInt(t.replace(/\D/g, ''), 10) || 0;
  }
  function faixa(v) { return v < 800 ? 'abaixo-800' : v < 1500 ? '800-1500' : v < 5000 ? '1500-5000' : v < 15000 ? '5000-15000' : '15000-mais'; }

  $$('[data-form]').forEach(function (form) {
    var msgBox = form.querySelector('[data-form-msg]');
    function erro(nome, texto) {
      var campo = form.elements[nome].closest('.campo'), p = campo.querySelector('.campo-erro');
      campo.classList.toggle('erro', !!texto);
      p.hidden = !texto; p.textContent = texto || '';
      form.elements[nome].setAttribute('aria-invalid', texto ? 'true' : 'false');
      return !texto;
    }
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements;
      // o formulário curto (capas novas) não tem cidade, e-mail nem "várias unidades": o app só exige nome,
      // WhatsApp e valor da conta (proposta A2, §4.3)
      var nome = f.nome.value.trim(), zap = digitos(f.whatsapp.value), cidade = f.cidade ? f.cidade.value.trim() : '';
      var valor = valorConta(f.valor.value), email = f.email ? f.email.value.trim() : '';
      var ok = [
        erro('nome', nome.length < 2 ? 'Diga seu nome.' : ''),
        erro('whatsapp', (zap.length < 10 || zap.length > 13) ? 'WhatsApp com DDD, só números.' : ''),
        f.cidade ? erro('cidade', cidade.length < 2 ? 'Diga a cidade.' : '') : true,
        erro('valor', valor <= 0 ? 'Diga o valor médio da conta.' : ''),
        f.email ? erro('email', email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? 'Confira o e-mail.' : '') : true
      ].every(Boolean);
      if (!ok) { var primeiro = form.querySelector('[aria-invalid="true"]'); if (primeiro) primeiro.focus(); return; }

      var varias = f.varias ? f.varias.checked : false, simulacao = null;
      try { simulacao = JSON.parse(sessionStorage.getItem('aes_simulacao') || 'null'); } catch (e) {}
      var dados = {
        nome: nome, whatsapp: zap, cidade: cidade || null, valor_conta: valor, email: email || null, website: f.website.value,
        campanha: origem.utm_campaign || null, origem: 'site', segmento: form.getAttribute('data-segmento'),
        varias_unidades: varias, pagina_entrada: origem.pagina_entrada || null, pagina_envio: location.pathname,
        simulacao: simulacao, politica_versao: POLITICA
      };
      ETIQUETAS.forEach(function (k) { dados[k] = origem[k] || null; });
      var reais = 'R$ ' + valor.toLocaleString('pt-BR');
      var texto = SAUDA + ' Sou ' + nome + (cidade ? ', de ' + cidade : '') + '. Minha conta de luz é de uns ' + reais + ' por mês' +
        (varias ? ', somando mais de uma unidade' : '') + '. Quero o cálculo exato.';
      dl.push({ event: 'form_submit', segmento: dados.segmento, faixa: faixa(valor) });

      if (MODO !== 'app') {
        // Prévia: nada sai do navegador. Mostra o que seria enviado ao app e a mensagem do WhatsApp.
        msgBox.hidden = false;
        msgBox.innerHTML = '<p><strong>Prévia: nada foi enviado.</strong> No ar, isto iria para o app e o WhatsApp abriria com a mensagem abaixo.</p><pre></pre>';
        var copia = JSON.parse(JSON.stringify(dados)); delete copia.website;
        msgBox.querySelector('pre').textContent = JSON.stringify(copia, null, 2) + '\n\nWhatsApp: ' + texto;
        return;
      }
      // No ar: o lead vai ao app sem esperar a resposta. Se falhar, a pessoa não vê erro (o WhatsApp abre do mesmo
      // jeito) e a falha fica na medição (form_crm_erro) para alguém notar.
      try {
        fetch(ENDPOINT, { method: 'POST', mode: 'cors', keepalive: true, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) })
          .then(function (r) { if (!r.ok) dl.push({ event: 'form_crm_erro', status: r.status }); })
          .catch(function () { dl.push({ event: 'form_crm_erro', status: 0 }); });
      } catch (e) { dl.push({ event: 'form_crm_erro', status: 0 }); }
      msgBox.hidden = false;
      msgBox.innerHTML = '<p><strong>Recebemos seu contato.</strong> O WhatsApp vai abrir com a mensagem pronta: é só enviar e, se puder, mandar a foto da conta.</p>';
      window.open(waUrl(texto), '_blank', 'noopener');
    });
  });
})();
