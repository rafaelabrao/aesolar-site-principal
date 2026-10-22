/* AESOLAR — comportamento dos protótipos da capa (v2 e v3, sessão A3): o simulador com as duas contas, a barra fixa
   com o número simulado, os números que contam ao aparecer e as seções que surgem ao rolar.
   A conta é a de simulador.js (window.AesolarSimulador), a mesma de gerador/simulador.py: aqui só se desenha.
   O exemplo com que a página abre não conta como simulação: não vai para a medição nem para o formulário.
   Sem este arquivo, a página continua inteira: o exemplo já vem escrito e nada fica escondido. */
(function () {
  'use strict';
  var S = window.AesolarSimulador;
  var doc = document;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var calma = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var dl = window.dataLayer = window.dataLayer || [];
  var SAUDACAO = 'Olá! Vim pelo site.';

  // número que corre do valor atual até o novo (direto, para quem pediu menos movimento)
  function corre(el, para, formata, ms) {
    var de = Number(el.getAttribute('data-valor') || 0);
    el.setAttribute('data-valor', para);
    if (calma || de === para || !window.requestAnimationFrame) { el.textContent = formata(para); return; }
    var t0 = null;
    function passo(t) {
      if (t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / ms), suave = 1 - Math.pow(1 - k, 3);
      el.textContent = formata(Math.round(de + (para - de) * suave));
      if (k < 1) window.requestAnimationFrame(passo);
    }
    window.requestAnimationFrame(passo);
  }

  function faixa(conta) {
    return conta < 1500 ? 'ate-1500' : conta < 5000 ? '1500-5000' : conta < 15000 ? '5000-15000' : '15000-mais';
  }

  // ---------- a barra fixa do celular passa a levar o número simulado ----------
  function barraComNumero(r, msg) {
    var barra = doc.querySelector('[data-barra]');
    if (!barra) return;
    var est = barra.querySelector('.barra-est');
    if (!est) {
      est = doc.createElement('p');
      est.className = 'barra-est';
      barra.insertBefore(est, barra.firstChild);
    }
    est.innerHTML = 'Sua estimativa: <b></b> por mês';
    est.querySelector('b').textContent = S.reais(r.min) + ' a ' + S.reais(r.max);
    var bt = barra.querySelector('[data-wa]');
    if (bt) { bt.setAttribute('data-wa', msg); if (window.AesolarWa) window.AesolarWa(bt); }
  }

  // ---------- o simulador ----------
  var params = null;
  try { params = JSON.parse(doc.getElementById('sim-params').textContent); } catch (e) {}

  if (S && params) $$('[data-calc-caixa]').forEach(function (box) {
    var campo = box.querySelector('input[name="conta"]');
    var estado = box.querySelector('[data-calc-estado]');
    var abaixo = box.querySelector('[data-calc-abaixo]');
    var res = box.querySelector('[data-calc-res]');
    var cta = box.querySelector('[data-calc-cta]');
    var onde = box.getAttribute('data-calc-caixa');
    var exemplo = Number(box.getAttribute('data-exemplo'));
    var textoExemplo = estado.textContent;
    var msgPadrao = cta ? cta.getAttribute('data-wa') : '';
    var MAXIMO = 1000000;
    var contou = false, espera = null;
    // o simulador e os blocos que repetem as duas contas em outra parte da página (data-calc-espelho)
    var alvos = [box].concat($$('[data-calc-espelho]'));
    var rotulos = $$('[data-calc-espelho-rot]');
    var rotuloExemplo = rotulos.map(function (el) { return el.textContent; });
    function cada(sel, fn) { alvos.forEach(function (a) { $$(sel, a).forEach(fn); }); }
    // os números já vêm escritos pelo gerador (o exemplo): a animação parte deles
    cada('[data-calc]', function (el) { el.setAttribute('data-valor', S.leValor(el.textContent)); });

    function desenha(r, eExemplo) {
      var v = { min: r.min, max: r.max, ano_min: r.ano_min, ano_max: r.ano_max, conta: r.conta, total: r.conta - r.min,
                equatorial_depois: r.equatorial_depois, aesolar_min: r.aesolar_min };
      cada('[data-calc]', function (el) {
        var k = el.getAttribute('data-calc');
        if (k in v) corre(el, v[k], S.reais, 450);
      });
      // as barras, com o desconto mínimo, em % da conta de hoje
      var w = { hoje: r.conta, eq: r.equatorial_depois, ae: r.aesolar_min, eco: r.min };
      cada('[data-calc-w]', function (el) {
        el.style.setProperty('--w', (w[el.getAttribute('data-calc-w')] / r.conta * 100).toFixed(1) + '%');
      });
      rotulos.forEach(function (el, i) {
        el.textContent = eExemplo ? rotuloExemplo[i] : 'A sua conta: ' + S.reais(r.conta) + ' por mês.';
      });
    }

    function atualiza() {
      var conta = S.leValor(campo.value);
      clearTimeout(espera);
      if (!conta) {
        box.setAttribute('data-modo', 'exemplo');
        estado.textContent = textoExemplo;
        abaixo.hidden = true;
        res.hidden = false;
        desenha(S.estima(exemplo, params), true);
        if (cta) { cta.setAttribute('data-wa', msgPadrao); if (window.AesolarWa) window.AesolarWa(cta); }
        return;
      }
      var r = conta <= MAXIMO ? S.estima(conta, params) : null;
      box.setAttribute('data-modo', 'sua');
      abaixo.hidden = !(conta < params.minimo_conta);
      res.hidden = !r;
      if (!r) {
        estado.textContent = conta > MAXIMO ? 'Conta acima de ' + S.reais(MAXIMO) + ': mande a fatura, o cálculo é outro.' : '';
        return;
      }
      estado.textContent = 'Sua conta: ' + S.reais(r.conta) + ' por mês';
      desenha(r, false);
      var msg = SAUDACAO + ' Simulei uma conta de ' + S.reais(r.conta).replace(' ', ' ') + ' por mês e quero o cálculo exato.';
      if (cta) { cta.setAttribute('data-wa', msg); if (window.AesolarWa) window.AesolarWa(cta); }
      // depois que a pessoa para de digitar: guarda para o formulário, leva o número para a barra e mede (uma vez)
      espera = setTimeout(function () {
        try { sessionStorage.setItem('aes_simulacao', JSON.stringify({ conta: r.conta, economia_min: r.min, economia_max: r.max })); } catch (e) {}
        $$('form[data-form] input[name="valor"]').forEach(function (inp) {
          if (!inp.value) inp.value = r.conta.toLocaleString('pt-BR');
        });
        barraComNumero(r, msg);
        if (contou) return;
        contou = true;
        dl.push({ event: 'simulador_usado', local: onde, faixa: faixa(conta) });
      }, 900);
    }

    campo.addEventListener('input', atualiza);
    $$('[data-calc-exemplo]', box).forEach(function (bt) {
      bt.addEventListener('click', function () {
        campo.value = Number(bt.getAttribute('data-calc-exemplo')).toLocaleString('pt-BR');
        atualiza();
      });
    });
    atualiza();
  });

  // ---------- números que contam quando aparecem, e seções que surgem ao rolar ----------
  if (!('IntersectionObserver' in window)) return;

  var numeros = $$('[data-conta]');
  if (numeros.length && !calma) {
    var ion = new IntersectionObserver(function (itens) {
      itens.forEach(function (it) {
        if (!it.isIntersecting) return;
        ion.unobserve(it.target);
        it.target.setAttribute('data-valor', 0);
        corre(it.target, Number(it.target.getAttribute('data-conta')), function (n) { return n.toLocaleString('pt-BR'); }, 1200);
      });
    }, { threshold: 0.6 });
    numeros.forEach(function (el) { ion.observe(el); });
  }

  var revela = $$('.revela');
  if (revela.length && !calma) {
    doc.documentElement.classList.add('revela-pronto');
    var ior = new IntersectionObserver(function (itens) {
      itens.forEach(function (it) {
        if (it.isIntersecting) { it.target.classList.add('visto'); ior.unobserve(it.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revela.forEach(function (el) { ior.observe(el); });
  }
})();
