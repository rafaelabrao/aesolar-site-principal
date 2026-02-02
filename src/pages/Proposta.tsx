import { useMemo } from "react";
import { useLocation, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

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
  return value.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function Proposta() {
  const q = useQuery();

  const nome = (q.get("nome") || "").trim() || "Cliente";
  const empresa = (q.get("empresa") || "").trim();
  const cidade = (q.get("cidade") || "").trim() || "—";
  const tipoEstabelecimento = (q.get("tipo_estabelecimento") || "").trim() || "—";

  const valorConta = Number((q.get("valor_conta") || "").replace(",", ".")) || 0;

  // Consumo estimado (kWh) = valorConta / 1,15
  const consumoKwh = valorConta > 0 ? valorConta / TARIFA : 0;

  // Mantendo as mesmas regras do HTML antigo
  const fatorDesconto = DESCONTO_BASE / 100;
  const monthlyCostOld = valorConta; // equivalente a consumoKwh * TARIFA
  const monthlySavings = monthlyCostOld * fatorDesconto;
  const monthlyCostNew = monthlyCostOld - monthlySavings;
  const yearlySavings = monthlySavings * 12;
  const trees = Math.floor(yearlySavings / 200);

  // Manchete de economia máxima (bandeira V2), igual ao HTML antigo (arredonda p/ baixo, sem decimais)
  const maxEconomyPct = useMemo(() => {
    const valorBandeiraV2 = 0.101;
    const numeradorMax = (TARIFA * fatorDesconto) + valorBandeiraV2;
    const denominadorMax = TARIFA + valorBandeiraV2;
    return Math.floor((numeradorMax / denominadorMax) * 100);
  }, [fatorDesconto]);

  const whatsappHref = useMemo(() => {
    const telefone = "556236382770";
    const msg =
      `Olá! Vim pela proposta no site.\n\n` +
      `Nome: ${nome}\n` +
      (empresa ? `Empresa: ${empresa}\n` : "") +
      `Cidade: ${cidade}\n` +
      `Tipo: ${tipoEstabelecimento}\n` +
      `Conta de luz: R$ ${formatMoneyBR(valorConta)}\n` +
      `Consumo estimado: ${consumoKwh.toFixed(2)} kWh/mês\n\n` +
      `Quero garantir os 20% de economia.`;
    return `https://wa.me/${telefone}?text=${encodeURIComponent(msg)}`;
  }, [nome, empresa, cidade, tipoEstabelecimento, valorConta, consumoKwh]);

  return (
    <main className="min-h-screen bg-background">
      <section className="container mx-auto px-6 py-10">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Proposta personalizada</p>
            <h1 className="text-2xl md:text-3xl font-bold text-foreground">
              Reduza sua conta em até <span className="text-primary">{maxEconomyPct}%</span> sem instalar nada
            </h1>
            <p className="text-muted-foreground mt-2">
              Economia garantida com energia solar por assinatura em Goiás.
            </p>
          </div>

          <div className="hidden md:flex gap-3">
            <Button asChild variant="outline">
              <Link to="/">Voltar</Link>
            </Button>
            <Button asChild variant="hero">
              <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                Falar no WhatsApp
              </a>
            </Button>
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
                <span className="font-bold text-primary text-right">R$ {formatMoneyBR(valorConta)}</span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-muted-foreground">Consumo estimado</span>
                <span className="font-semibold text-right">{consumoKwh.toFixed(2)} kWh/mês</span>
              </div>
            </div>

            <div className="mt-6">
              <Button asChild variant="hero" size="xl" className="w-full">
                <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                  Quero garantir minha economia no WhatsApp
                </a>
              </Button>
              <p className="text-xs text-muted-foreground text-center mt-3">
                Atendimento rápido. Sem compromisso.
              </p>
            </div>
          </div>

          <div className="lg:col-span-8 space-y-6">
            <div className="rounded-2xl bg-card p-6 shadow-soft">
              <h2 className="text-lg font-bold text-foreground mb-4">Seu comparativo</h2>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="rounded-xl border border-border p-5">
                  <p className="text-sm text-muted-foreground">Custo Estimado Mensal (atual)</p>
                  <p className="text-3xl font-bold text-foreground">R$ {formatMoneyBR(monthlyCostOld)}</p>
                  <p className="text-xs text-muted-foreground mt-2">Sujeito a bandeiras tarifárias</p>
                </div>

                <div className="rounded-xl border border-border p-5">
                  <p className="text-sm text-muted-foreground">Novo Custo Estimado (AESOLAR)</p>
                  <p className="text-3xl font-bold text-primary">R$ {formatMoneyBR(monthlyCostNew)}</p>
                  <p className="text-xs text-muted-foreground mt-2">
                    {DESCONTO_BASE}% de economia garantida
                  </p>
                </div>
              </div>

              <div className="mt-5 rounded-xl bg-muted/30 p-5 flex items-center justify-between gap-6">
                <div>
                  <p className="text-sm text-muted-foreground">Impacto Financeiro em 12 Meses</p>
                  <p className="text-2xl font-bold text-foreground">R$ {formatMoneyBR(yearlySavings)}</p>
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
                  const numerador = (TARIFA * fatorDesconto) + b.valor;
                  const denominador = TARIFA + b.valor;
                  const economiaRealPct = (numerador / denominador) * 100;

                  return (
                    <div key={b.nome} className="flex items-center justify-between gap-4 rounded-xl border border-border p-4">
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
          </div>
        </div>

        <div className="mt-10 flex md:hidden gap-3">
          <Button asChild variant="outline" className="w-full">
            <Link to="/">Voltar</Link>
          </Button>
          <Button asChild variant="hero" className="w-full">
            <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
              WhatsApp
            </a>
          </Button>
        </div>
      </section>
    </main>
  );
}