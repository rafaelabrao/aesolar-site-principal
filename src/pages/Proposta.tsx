import { useMemo } from "react";
import { useLocation, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import heroUfv from "@/assets/hero-ufv_vereda.jpg";

function useQuery() {
  const { search } = useLocation();
  return useMemo(() => new URLSearchParams(search), [search]);
}

const TARIFA = 1.15;
const DESCONTO_BASE = 20;

const bandeiras = [
  { nome: "Bandeira Verde", valor: 0.0 },
  { nome: "Bandeira Amarela", valor: 0.025 },
  { nome: "Bandeira Vermelha 1", valor: 0.057 },
  { nome: "Bandeira Vermelha 2", valor: 0.101 },
];

function formatMoneyBR(value: number) {
  const v = Number.isFinite(value) ? value : 0;
  return v.toLocaleString("pt-BR", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatKwhBR(value: number) {
  const v = Number.isFinite(value) ? value : 0;
  return Math.round(v).toLocaleString("pt-BR", { maximumFractionDigits: 0 });
}

function parseBRNumber(input: string | null) {
  if (!input) return 0;

  // aceita "9000", "9.000", "9.000,50", "9000,50"
  const normalized = input.trim().replace(/\./g, "").replace(",", ".");
  const n = Number(normalized);
  return Number.isFinite(n) ? n : 0;
}

export default function Proposta() {
  const q = useQuery();

  const nome = (q.get("nome") || "").trim() || "Cliente";
  const empresa = (q.get("empresa") || "").trim();
  const cidade = (q.get("cidade") || "").trim() || "—";

  const tipoEstabelecimentoRaw = (q.get("tipo_estabelecimento") || "").trim();

  const tipoLabels: Record<string, string> = {
    residencia: "Residência",
    farmacia: "Farmácia",
    restaurante: "Restaurante",
    mercado: "Mercado",
    padaria: "Padaria",
    acougue: "Açougue",
    condominio: "Condomínio",
  };

  const tipoEstabelecimento =
    tipoLabels[tipoEstabelecimentoRaw.toLowerCase()] ||
    (tipoEstabelecimentoRaw ? tipoEstabelecimentoRaw : "—");

  const valorConta = parseBRNumber(q.get("valor_conta"));
  const hasValorConta = Number.isFinite(valorConta) && valorConta > 0;

  // Consumo estimado (kWh) = valorConta / 1,15
  const consumoKwh = hasValorConta ? valorConta / TARIFA : 0;

  // Mantendo as mesmas regras do HTML antigo
  const fatorDesconto = DESCONTO_BASE / 100;
  const monthlyCostOld = valorConta;
  const monthlySavings = monthlyCostOld * fatorDesconto;
  const monthlyCostNew = monthlyCostOld - monthlySavings;
  const yearlySavings = monthlySavings * 12;
  const trees = Math.floor(yearlySavings / 200);

  // Manchete de economia máxima (bandeira V2), arredonda p/ baixo (sem decimais)
  const maxEconomyPct = useMemo(() => {
    const valorBandeiraV2 = 0.101;
    const numeradorMax = TARIFA * fatorDesconto + valorBandeiraV2;
    const denominadorMax = TARIFA + valorBandeiraV2;
    return Math.floor((numeradorMax / denominadorMax) * 100);
  }, [fatorDesconto]);

  const ctaText = hasValorConta
    ? `Quero economizar R$ ${formatMoneyBR(monthlySavings)}/mês no WhatsApp`
    : "Quero receber minha proposta no WhatsApp";

  const whatsappHref = useMemo(() => {
    const telefone = "556236382770";
    const msg =
      `Olá! Vim pela proposta no site.\n\n` +
      `Nome: ${nome}\n` +
      (empresa ? `Empresa: ${empresa}\n` : "") +
      `Cidade: ${cidade}\n` +
      `Tipo: ${tipoEstabelecimento}\n` +
      (hasValorConta ? `Conta de luz: R$ ${formatMoneyBR(valorConta)}\n` : "") +
      (hasValorConta ? `Consumo estimado: ${formatKwhBR(consumoKwh)} kWh/mês\n\n` : "\n") +
      `Quero garantir os 20% de economia.`;

    return `https://wa.me/${telefone}?text=${encodeURIComponent(msg)}`;
  }, [nome, empresa, cidade, tipoEstabelecimento, hasValorConta, valorConta, consumoKwh]);

  return (
    <main className="min-h-screen bg-background">
      <section className="container mx-auto px-6 py-10">
        <div className="relative overflow-hidden rounded-3xl border border-border bg-card shadow-soft">
          <img
            src={heroUfv}
            alt="Usina solar"
            className="absolute inset-0 h-full w-full object-cover opacity-25"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background via-background/90 to-background/40" />

          <div className="relative p-6 md:p-10">
            <p className="text-sm text-muted-foreground">Proposta personalizada</p>

            <h1 className="mt-2 text-2xl md:text-4xl font-bold text-foreground">
              Reduza sua conta em até{" "}
              <span className="text-primary">{maxEconomyPct}%</span> sem instalar nada
            </h1>

            <p className="text-muted-foreground mt-3 max-w-2xl">
              Economia garantida com energia solar por assinatura em Goiás. Sem obra, sem investimento inicial e com
              atendimento rápido.
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              <span className="rounded-full border border-border bg-background/60 px-3 py-1 text-xs text-foreground">
                Sem instalação
              </span>
              <span className="rounded-full border border-border bg-background/60 px-3 py-1 text-xs text-foreground">
                Sem investimento inicial
              </span>
              <span className="rounded-full border border-border bg-background/60 px-3 py-1 text-xs text-foreground">
                Economia garantida
              </span>
            </div>

            <div className="mt-6 hidden md:flex gap-3">
              <Button asChild variant="outline">
                <Link to="/">Voltar</Link>
              </Button>

              <Button asChild variant="hero" className="h-auto py-4 px-6 whitespace-normal leading-tight">
                <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                  {ctaText}
                </a>
              </Button>
            </div>
          </div>
        </div>

        <div className="mt-8 grid lg:grid-cols-12 gap-6">
          <div className="lg:col-span-4 rounded-2xl bg-card p-6 shadow-soft">
            <h2 className="text-lg font-bold text-foreground mb-4">Dados informados</h2>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between gap-4">
                <span className="text-muted-foreground">Nome</span>
                <span className="font-semibold text-right">{nome}</span>
              </div>

              {empresa ? (
                <div className="flex justify-between gap-4">
                  <span className="text-muted-foreground">Empresa</span>
                  <span className="font-semibold text-right">{empresa}</span>
                </div>
              ) : null}

              <div className="flex justify-between gap-4">
                <span className="text-muted-foreground">Cidade</span>
                <span className="font-semibold text-right">{cidade}</span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-muted-foreground">Tipo de Estabelecimento</span>
                <span className="font-semibold text-right">{tipoEstabelecimento}</span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-muted-foreground">Valor da conta</span>
                <span className="font-bold text-primary text-right">
                  {hasValorConta ? `R$ ${formatMoneyBR(valorConta)}` : "—"}
                </span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-muted-foreground">Consumo estimado</span>
                <span className="font-semibold text-right">
                  {hasValorConta ? `${formatKwhBR(consumoKwh)} kWh/mês` : "—"}
                </span>
              </div>
            </div>

            <div className="mt-6">
              <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
                <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                  {ctaText}
                </a>
              </Button>
              <p className="text-xs text-muted-foreground text-center mt-3">
                Atendimento rápido. Sem compromisso.
              </p>
            </div>
          </div>

          <div className="lg:col-span-8 space-y-6">
            {!hasValorConta ? (
              <div className="rounded-2xl bg-card p-6 shadow-soft">
                <h2 className="text-lg font-bold text-foreground">Faltou o valor da conta</h2>
                <p className="text-muted-foreground mt-2">
                  Para calcular sua economia e montar a proposta completa, preciso do valor da conta de luz.
                </p>
                <div className="mt-4">
                  <Button asChild variant="hero">
                    <Link to="/">Voltar ao formulário</Link>
                  </Button>
                </div>
              </div>
            ) : (
              <>
                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground mb-4">Seu comparativo</h2>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Custo Estimado Mensal (atual)</p>
                      <p className="text-3xl font-bold text-foreground">
                        R$ {formatMoneyBR(monthlyCostOld)}
                      </p>
                      <p className="text-xs text-muted-foreground mt-2">Sujeito a bandeiras tarifárias</p>
                    </div>

                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Novo Custo Estimado (AESOLAR)</p>
                      <p className="text-3xl font-bold text-primary">
                        R$ {formatMoneyBR(monthlyCostNew)}
                      </p>
                      <p className="text-xs text-muted-foreground mt-2">
                        {DESCONTO_BASE}% de economia garantida
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 rounded-xl bg-muted/30 p-5 flex items-center justify-between gap-6">
                    <div>
                      <p className="text-sm text-muted-foreground">Impacto Financeiro em 12 Meses</p>
                      <p className="text-2xl font-bold text-foreground">
                        R$ {formatMoneyBR(yearlySavings)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-muted-foreground">Equivalente a</p>
                      <p className="text-sm font-semibold text-foreground">{trees} árvores preservadas</p>
                    </div>
                  </div>
                </div>

                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground mb-4">Economia adicional com bandeiras</h2>

                  <div className="space-y-3">
                    {bandeiras.map((b) => {
                      const numerador = TARIFA * fatorDesconto + b.valor;
                      const denominador = TARIFA + b.valor;
                      const economiaRealPct = (numerador / denominador) * 100;

                      return (
                        <div
                          key={b.nome}
                          className="flex items-center justify-between gap-4 rounded-xl border border-border p-4"
                        >
                          <div className="font-semibold text-foreground">{b.nome}</div>
                          <div className="text-sm text-muted-foreground">Adicional: R$ {b.valor.toFixed(3)}</div>
                          <div className="text-sm font-bold text-primary">{economiaRealPct.toFixed(2)}%</div>
                        </div>
                      );
                    })}
                  </div>

                  <p className="text-xs text-muted-foreground mt-4">
                    * O percentual de desconto é aplicado sobre a Energia e a Tarifa Compensada.
                  </p>
                </div>
              </>
            )}
          </div>
        </div>

        <div className="h-24 md:hidden" />

        <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-background/90 backdrop-blur md:hidden">
          <div className="container mx-auto px-6 py-3">
            <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
              <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                {ctaText}
              </a>
            </Button>
          </div>
        </div>
      </section>
    </main>
  );
}