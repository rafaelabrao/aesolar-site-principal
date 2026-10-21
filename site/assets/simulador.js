/* AESOLAR — simulador de economia em reais.
   A conta é a mesma de gerador/simulador.py (mesma ordem de operações): o exemplo escrito na página e o
   simulador nunca podem dar números diferentes. Os parâmetros vêm de dados.json, embutidos na página em
   <script type="application/json" id="sim-params">. Nada aqui é enviado a lugar nenhum. */
(function (raiz) {
  'use strict';

  function estima(conta, p) {
    if (conta < p.minimo_conta) return null;
    var kwh = conta * (1 - p.fora_do_desconto_pct / 100) / p.tarifa_kwh;
    var kwhAbatido = Math.max(0, kwh - p.disponibilidade_kwh);
    var abatido = kwhAbatido * p.tarifa_kwh * (1 - p.tributos_que_ficam_pct / 100);
    var ecoMin = abatido * p.desconto_min_pct / 100;
    var ecoMax = abatido * p.desconto_max_pct / 100;
    var abatidoR = Math.floor(abatido / 10) * 10;
    return {
      conta: conta,
      abatido: abatidoR,
      fora: conta - abatidoR,
      min: Math.floor(ecoMin / 10) * 10,
      max: Math.floor(ecoMax / 10) * 10,
      ano_min: Math.floor(ecoMin * 12 / 100) * 100,
      ano_max: Math.floor(ecoMax * 12 / 100) * 100,
      equatorial_depois: conta - abatidoR,
      aesolar_min: abatidoR - Math.floor(ecoMin / 10) * 10
    };
  }

  // "R$ 5.000", "5000", "5.000,90", "5000.90" -> 5000 (só reais inteiros; centavo não muda a estimativa)
  function leValor(texto) {
    var s = String(texto || '').replace(/\s/g, '').replace(/^R\$/i, '');
    s = s.replace(/[.,]\d{1,2}$/, '');
    s = s.replace(/\D/g, '');
    return s ? parseInt(s, 10) : 0;
  }

  function reais(n) { return 'R$ ' + Math.round(n).toLocaleString('pt-BR'); }

  raiz.AesolarSimulador = { estima: estima, leValor: leValor, reais: reais };

  if (typeof document === 'undefined') return; // carregado pelo teste (node), sem página

  var params;
  try { params = JSON.parse(document.getElementById('sim-params').textContent); } catch (e) { return; }
  var dl = window.dataLayer = window.dataLayer || [];

  Array.prototype.forEach.call(document.querySelectorAll('[data-simulador]'), function (box) {
    var campo = box.querySelector('input[name="conta"]');
    var varias = box.querySelector('input[name="varias"]');
    var saida = box.querySelector('[data-sim-saida]');
    var abaixo = box.querySelector('[data-sim-abaixo]');
    var vazio = box.querySelector('[data-sim-vazio]');
    var cta = box.querySelector('[data-sim-cta]');
    var onde = box.getAttribute('data-simulador');
    var contou = false, espera = null;
    var MAXIMO = 1000000;

    function poe(nome, valor) {
      var el = box.querySelector('[data-sim="' + nome + '"]');
      if (el) el.textContent = valor;
    }

    function faixa(conta) {
      return conta < 1500 ? 'ate-1500' : conta < 5000 ? '1500-5000' : conta < 15000 ? '5000-15000' : '15000-mais';
    }

    function atualiza() {
      var conta = leValor(campo.value);
      var r = conta > 0 && conta <= MAXIMO ? estima(conta, params) : null;
      vazio.hidden = conta > 0;
      abaixo.hidden = !(conta > 0 && conta < params.minimo_conta);
      saida.hidden = !r;
      if (cta) cta.hidden = !r;
      if (!r) return;
      poe('conta', reais(r.conta));
      poe('fora', reais(r.fora));
      poe('abatido', reais(r.abatido));
      poe('min', reais(r.min));
      poe('max', reais(r.max));
      poe('ano_min', reais(r.ano_min));
      poe('ano_max', reais(r.ano_max));
      if (cta) {
        var msg = 'Olá! Vim pelo site. Simulei uma conta de ' + reais(r.conta).replace(' ', ' ') + ' por mês' +
          (varias && varias.checked ? ', somando mais de uma unidade' : '') + ' e quero o cálculo exato.';
        cta.setAttribute('data-wa', msg);
        if (window.AesolarWa) window.AesolarWa(cta);
      }
      // mede uma vez por visita à página, depois que a pessoa para de digitar
      clearTimeout(espera);
      espera = setTimeout(function () {
        if (contou) return;
        contou = true;
        dl.push({ event: 'simulador_usado', local: onde, faixa: faixa(conta) });
        try { sessionStorage.setItem('aes_simulacao', JSON.stringify({ conta: r.conta, economia_min: r.min, economia_max: r.max })); } catch (e) {}
      }, 1200);
    }

    campo.addEventListener('input', atualiza);
    if (varias) varias.addEventListener('change', atualiza);
    Array.prototype.forEach.call(box.querySelectorAll('[data-sim-exemplo]'), function (b) {
      b.addEventListener('click', function () {
        campo.value = Number(b.getAttribute('data-sim-exemplo')).toLocaleString('pt-BR');
        atualiza();
      });
    });
    atualiza();
  });
})(typeof window !== 'undefined' ? window : globalThis);
