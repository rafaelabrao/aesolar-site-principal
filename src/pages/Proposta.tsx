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
  { nome: "Bandeira Verde", valor: 0.0, explicacao: "Condições normais" },
  { nome: "Bandeira Amarela", valor: 0.025, explicacao: "Custos maiores de geração" },
  { nome: "Bandeira Vermelha 1", valor: 0.057, explicacao: "Custo ainda maior" },
  { nome: "Bandeira Vermelha 2", valor: 0.101, explicacao: "Maior custo (pior cenário)" },
];

function formatMoneyBR(value: number) {
  const v = Number.isFinite(value) ? value : 0;
  return v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatKwhBR(value: number) {
  const v = Number.isFinite(value) ? value : 0;
  return Math.round(v).toLocaleString("pt-BR", { maximumFractionDigits: 0 });
}

function parseBRNumber(input: string | null) {
  if (!input) return 0;
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
    coworking: "Coworking",
  };

  const tipoEstabelecimento =
    tipoLabels[tipoEstabelecimentoRaw.toLowerCase()] ||
    (tipoEstabelecimentoRaw ? tipoEstabelecimentoRaw : "—");

  const valorConta = parseBRNumber(q.get("valor_conta"));
  const hasValorConta = Number.isFinite(valorConta) && valorConta > 0;

  const fatorDesconto = DESCONTO_BASE / 100;

  const consumoKwh = hasValorConta ? valorConta / TARIFA : 0;

  const monthlyCostOld = hasValorConta ? valorConta : 0;
  const monthlySavings = monthlyCostOld * fatorDesconto;
  const monthlyCostNew = monthlyCostOld - monthlySavings;
  const yearlySavings = monthlySavings * 12;
  const trees = Math.floor(yearlySavings / 200);

  const maxEconomyPct = useMemo(() => {
    const valorBandeiraV2 = 0.101;
    const numeradorMax = TARIFA * fatorDesconto + valorBandeiraV2;
    const denominadorMax = TARIFA + valorBandeiraV2;
    return Math.floor((numeradorMax / denominadorMax) * 100);
  }, [fatorDesconto]);

  const ctaText = hasValorConta
    ? `Quero economizar R$ ${formatMoneyBR(monthlySavings)}/mês no WhatsApp`
    : "Quero receber minha proposta no WhatsApp";

  // ⚠️ Observação de compliance/credibilidade:
  // Depoimentos com números/tempo devem ser reais/confirmados antes de produção.
  const testimonials = [
    {
      segment: "Coworking",
      name: "Cliente (Coworking)",
      location: "Goiânia/GO",
      quote:
        "Reduzimos custos sem precisar instalar nada no prédio. O atendimento foi rápido e a economia começou a aparecer mês a mês. Processo simples e bem explicado.",
    },
    {
      segment: "Condomínio",
      name: "Síndica (Condomínio)",
      location: "Goiânia/GO",
      quote:
        "O que mais me ajudou foi a previsibilidade e a transparência para prestação de contas. O suporte foi ágil e a solução fez sentido para o condomínio.",
    },
    {
      segment: "Restaurante",
      name: "Cliente (Restaurante)",
      location: "Goiânia/GO",
      quote:
        "Conta de energia pesa muito no restaurante. Gostei porque não precisei de obra e consegui reduzir custo fixo. Atendimento humano e objetivo.",
    },
  ];

  const whatsappHref = useMemo(() => {
    const telefone = "556236382770";
    const msg =
      `Olá! Vim pela proposta no site.\n\n` +
      `Nome: ${nome}\n` +
      (empresa ? `Empresa: ${empresa}\n` : "") +
      `Cidade: ${cidade}\n` +
      `Tipo: ${tipoEstabelecimento}\n` +
      (hasValorConta ? `Conta de luz: R$ ${formatMoneyBR(valorConta)}\n` : "") +
      (hasValorConta ? `Consumo estimado: ${formatKwhBR(consumoKwh)} kWh/mês\n` : "") +
      (hasValorConta
        ? `Economia estimada: R$ ${formatMoneyBR(monthlySavings)}/mês (R$ ${formatMoneyBR(yearlySavings)}/12 meses)\n\n`
        : "\n") +
      `Quero entender como funciona e avançar.`;

    return `https://wa.me/${telefone}?text=${encodeURIComponent(msg)}`;
  }, [nome, empresa, cidade, tipoEstabelecimento, hasValorConta, valorConta, consumoKwh, monthlySavings, yearlySavings]);

  return (
    <main className="min-h-screen bg-muted/30">
      <section className="container mx-auto px-6 py-10">
        {/* HERO */}
        <div className="relative overflow-hidden rounded-3xl border border-border bg-card shadow-soft">
          <img
            src={heroUfv}
            alt="Usina solar"
            className="absolute inset-0 h-full w-full object-cover opacity-45"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background/70 to-background/95" />

          <div className="relative p-6 md:p-10">
            {/* Top bar com logo */}
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <img
                  src="/logo-aesolar.png"
                  alt="AESOLAR"
                  className="h-8 w-auto"
                  onError={(e) => {
                    e.currentTarget.style.display = "none";
                  }}
                />
                <div className="leading-tight">
                  <p className="text-sm font-bold text-foreground">AESOLAR</p>
                  <p className="text-xs text-muted-foreground">Energia solar por assinatura</p>
                </div>
              </div>

              <div className="hidden md:flex gap-3">
                <Button asChild variant="outline">
                  <Link to="/">Voltar</Link>
                </Button>
                <Button asChild variant="hero" className="h-auto py-3 px-5 whitespace-normal leading-tight">
                  <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                    {ctaText}
                  </a>
                </Button>
              </div>
            </div>

            <p className="mt-6 text-sm text-muted-foreground">Proposta personalizada</p>

            <h1 className="mt-2 text-2xl md:text-4xl font-bold text-foreground max-w-3xl">
              Reduza sua conta em até <span className="text-primary">{maxEconomyPct}%</span> sem instalar nada
            </h1>

            <p className="text-muted-foreground mt-3 max-w-2xl">
              Economia com energia solar por assinatura em Goiás. Sem obra, sem investimento em placas no seu imóvel.
            </p>

            <div className="mt-5 flex flex-wrap gap-2">
              <span className="rounded-full border border-border bg-background/70 px-3 py-1 text-xs text-foreground">
                Sem instalação
              </span>
              <span className="rounded-full border border-border bg-background/70 px-3 py-1 text-xs text-foreground">
                Sem investimento inicial
              </span>
              <span className="rounded-full border border-border bg-background/70 px-3 py-1 text-xs text-foreground">
                Atendimento humano no WhatsApp
              </span>
            </div>

            <div className="mt-6 md:hidden">
              <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
                <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                  {ctaText}
                </a>
              </Button>
              <p className="text-xs text-muted-foreground mt-2 text-center">Sem compromisso. Resposta rápida.</p>
            </div>
          </div>
        </div>

        {/* GRID PRINCIPAL */}
        <div className="mt-8 grid lg:grid-cols-12 gap-6">
          {/* ESQUERDA */}
          <div className="lg:col-span-4 rounded-2xl bg-card p-6 shadow-soft">
            <h2 className="text-lg font-bold text-foreground mb-4">Seus dados</h2>

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
                <span className="text-muted-foreground">Tipo</span>
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
                Próximo passo: clique e eu te explico em 2 minutos.
              </p>
            </div>

            <div className="mt-6 rounded-xl border border-border p-4">
              <p className="text-sm font-semibold text-foreground">Como funciona (3 passos)</p>
              <ul className="mt-2 text-sm text-muted-foreground space-y-1 list-disc pl-5">
                <li>Você confirma seus dados no WhatsApp</li>
                <li>Validamos elegibilidade e disponibilidade</li>
                <li>Você começa a economizar na conta</li>
              </ul>
            </div>
          </div>

          {/* DIREITA */}
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
              &lt;>
                {/* RESUMO */}
                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground">Resumo da sua economia</h2>

                  <div className="mt-4 grid md:grid-cols-3 gap-4">
                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Economia estimada (mês)</p>
                      <p className="text-2xl font-bold text-primary">R$ {formatMoneyBR(monthlySavings)}</p>
                      <p className="text-xs text-muted-foreground mt-1">Base: {DESCONTO_BASE}%</p>
                    </div>

                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Em 12 meses</p>
                      <p className="text-2xl font-bold text-foreground">R$ {formatMoneyBR(yearlySavings)}</p>
                      <p className="text-xs text-muted-foreground mt-1">Economia recorrente</p>
                    </div>

                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Equivalente a</p>
                      <p className="text-2xl font-bold text-foreground">{trees}</p>
                      <p className="text-xs text-muted-foreground mt-1">árvores preservadas</p>
                    </div>
                  </div>

                  {/* CTA dentro do resumo (desktop também) */}
                  <div className="mt-5">
                    <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
                      <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                        {ctaText}
                      </a>
                    </Button>
                    <p className="text-xs text-muted-foreground mt-3">Atendimento humano. Sem compromisso.</p>
                  </div>
                </div>

                {/* COMPARATIVO */}
                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground mb-4">Seu comparativo</h2>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Custo Estimado Mensal (atual)</p>
                      <p className="text-3xl font-bold text-foreground">R$ {formatMoneyBR(monthlyCostOld)}</p>
                      <p className="text-xs text-muted-foreground mt-2">Sujeito a bandeiras tarifárias</p>
                    </div>

                    <div className="rounded-xl border border-border p-5">
                      <p className="text-sm text-muted-foreground">Novo Custo Estimado (com economia)</p>
                      <p className="text-3xl font-bold text-primary">R$ {formatMoneyBR(monthlyCostNew)}</p>
                      <p className="text-xs text-muted-foreground mt-2">{DESCONTO_BASE}% de economia estimada</p>
                    </div>
                  </div>
                </div>

                {/* BANDEIRAS */}
                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground mb-2">Economia adicional com bandeiras</h2>
                  <p className="text-sm text-muted-foreground mb-4">
                    Quando a bandeira sobe, a conta tende a ficar mais cara — e a economia costuma ficar ainda mais interessante.
                  </p>

                  <div className="space-y-3">
                    {bandeiras.map((b) => {
                      const numerador = TARIFA * fatorDesconto + b.valor;
                      const denominador = TARIFA + b.valor;
                      const economiaRealPct = (numerador / denominador) * 100;

                      return (
                        <div key={b.nome} className="rounded-xl border border-border p-4">
                          <div className="flex items-center justify-between gap-4">
                            <div className="font-semibold text-foreground">{b.nome}</div>
                            <div className="text-sm font-bold text-primary">{economiaRealPct.toFixed(2)}%</div>
                          </div>
                          <div className="mt-1 flex items-center justify-between gap-4">
                            <div className="text-xs text-muted-foreground">{b.explicacao}</div>
                            <div className="text-xs text-muted-foreground">Adicional: R$ {b.valor.toFixed(3)}</div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <p className="text-xs text-muted-foreground mt-4">
                    * Percentuais são estimativas com base no valor informado e nas bandeiras.
                  </p>
                </div>

                {/* PROVA SOCIAL */}
                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground mb-4">Relatos de clientes</h2>

                  <div className="grid md:grid-cols-3 gap-4">
                    {testimonials.map((t) => (
                      <div key={t.segment} className="rounded-xl border border-border p-4">
                        <p className="text-xs text-muted-foreground">{t.segment}</p>
                        <p className="text-sm font-semibold text-foreground mt-1">{t.name}</p>
                        <p className="text-xs text-muted-foreground">{t.location}</p>
                        <p className="text-sm text-muted-foreground mt-3">“{t.quote}”</p>
                      </div>
                    ))}
                  </div>

                  {/* CTA logo após prova social (muito bom para CRO) */}
                  <div className="mt-6">
                    <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
                      <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                        {ctaText}
                      </a>
                    </Button>
                    <p className="text-xs text-muted-foreground mt-2 text-center">
                      Tire dúvidas e confirme disponibilidade para sua cidade.
                    </p>
                  </div>
                </div>

                {/* FAQ + CTA no final do FAQ */}
                <div className="rounded-2xl bg-card p-6 shadow-soft">
                  <h2 className="text-lg font-bold text-foreground mb-4">Perguntas frequentes</h2>

                  <div className="space-y-3">
                    <details className="rounded-xl border border-border p-4">
                      <summary className="font-semibold text-foreground cursor-pointer">Preciso instalar placas?</summary>
                      <p className="text-sm text-muted-foreground mt-2">
                        Não. É energia solar por assinatura. Você não instala placas no seu imóvel.
                      </p>
                    </details>

                    <details className="rounded-xl border border-border p-4">
                      <summary className="font-semibold text-foreground cursor-pointer">Como avanço agora?</summary>
                      <p className="text-sm text-muted-foreground mt-2">
                        Clique no WhatsApp. Eu confirmo seus dados e explico como funciona para você avançar com segurança.
                      </p>
                    </details>

                    <details className="rounded-xl border border-border p-4">
                      <summary className="font-semibold text-foreground cursor-pointer">Essa economia é garantida?</summary>
                      <p className="text-sm text-muted-foreground mt-2">
                        Aqui é uma estimativa com base no que você informou. No WhatsApp a gente confirma os detalhes e fecha a proposta final.
                      </p>
                    </details>

                    <details className="rounded-xl border border-border p-4">
                      <summary className="font-semibold text-foreground cursor-pointer">Atende minha cidade?</summary>
                      <p className="text-sm text-muted-foreground mt-2">
                        Atendemos Goiás. No WhatsApp eu valido disponibilidade para sua região e perfil.
                      </p>
                    </details>
                  </div>

                  {/* CTA FINAL DO FAQ (resolve seu problema do desktop) */}
                  <div className="mt-6">
                    <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
                      <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                        {ctaText}
                      </a>
                    </Button>
                    <p className="text-xs text-muted-foreground mt-2 text-center">
                      Atendimento humano. Sem compromisso.
                    </p>
                  </div>
                </div>

                {/* CTA FINAL DA PÁGINA (desktop) */}
                <div className="hidden md:block rounded-3xl border border-border bg-card shadow-soft p-8">
                  <div className="flex items-center justify-between gap-6 flex-wrap">
                    <div>
                      <p className="text-sm text-muted-foreground">Pronto para avançar?</p>
                      <p className="text-2xl font-bold text-foreground mt-1">
                        Clique e finalize sua proposta no WhatsApp
                      </p>
                      <p className="text-muted-foreground mt-2">
                        Você confirma alguns dados e eu te explico o passo a passo.
                      </p>
                    </div>

                    <Button asChild variant="hero" className="h-auto py-4 px-6 whitespace-normal leading-tight">
                      <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                        {ctaText}
                      </a>
                    </Button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Espaço para o sticky CTA no mobile */}
        <div className="h-24 md:hidden" />

        {/* CTA FIXO MOBILE */}
        <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-background/90 backdrop-blur md:hidden">
          <div className="container mx-auto px-6 py-3">
            <Button asChild variant="hero" className="w-full h-auto py-4 whitespace-normal leading-tight">
              <a href={whatsappHref} target="_blank" rel="noopener noreferrer">
                {ctaText}
              </a>
            </Button>
            <p className="text-xs text-muted-foreground mt-2 text-center">Atendimento humano. Sem compromisso.</p>
          </div>
        </div>
      </section>
    </main>
  );
}