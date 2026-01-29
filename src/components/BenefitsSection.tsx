import { Zap, Wallet, Wrench, ShieldCheck, Clock, Leaf } from "lucide-react";

const benefits = [
  {
    icon: Wallet,
    title: "Economia de até 26%",
    description: "Reduza significativamente seus custos com energia elétrica todo mês, direto na sua fatura.",
  },
  {
    icon: Wrench,
    title: "Sem Instalação",
    description: "Você não precisa instalar nenhum equipamento. Nós cuidamos de toda a infraestrutura.",
  },
  {
    icon: ShieldCheck,
    title: "Sem Investimento",
    description: "Zero custo inicial. Comece a economizar sem precisar desembolsar nada.",
  },
  {
    icon: Clock,
    title: "Ativação Rápida",
    description: "Processo simples e descomplicado. Sua economia começa em poucos dias.",
  },
  {
    icon: Zap,
    title: "Energia Limpa",
    description: "100% energia solar. Contribua para um futuro mais sustentável para Goiás.",
  },
  {
    icon: Leaf,
    title: "Sustentabilidade",
    description: "Sua empresa mais verde. Valorize sua marca com energia renovável.",
  },
];

export function BenefitsSection() {
  return (
    <section id="beneficios" className="py-16 md:py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-12 md:mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-secondary text-secondary-foreground text-sm font-medium mb-4">
            Vantagens Exclusivas
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Por que escolher a{" "}
            <span className="text-primary">AESOLAR</span>?
          </h2>
          <p className="text-lg text-muted-foreground">
            Oferecemos a melhor solução em energia solar por assinatura para empresários em Goiás.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {benefits.map((benefit, index) => {
            const Icon = benefit.icon;
            return (
              <div
                key={index}
                className="group p-6 md:p-8 rounded-2xl bg-card border border-border/50 hover:border-primary/30 transition-smooth hover:shadow-soft"
              >
                <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-5 group-hover:bg-primary/20 transition-smooth">
                  <Icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">
                  {benefit.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {benefit.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
