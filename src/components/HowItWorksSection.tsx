import { FileText, UserCheck, Zap } from "lucide-react";

const steps = [
  {
    number: "01",
    icon: FileText,
    title: "Solicite sua Proposta",
    description: "Preencha o formulário com seus dados e informações sobre seu consumo de energia.",
  },
  {
    number: "02",
    icon: UserCheck,
    title: "Análise Personalizada",
    description: "Nossa equipe analisa seu perfil e elabora uma proposta exclusiva de economia.",
  },
  {
    number: "03",
    icon: Zap,
    title: "Comece a Economizar",
    description: "Após a associação, sua economia começa a aparecer direto na conta de luz.",
  },
];

export function HowItWorksSection() {
  return (
    <section id="como-funciona" className="py-16 md:py-24 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-12 md:mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-secondary text-secondary-foreground text-sm font-medium mb-4">
            Processo Simples
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Como <span className="text-primary">funciona</span>?
          </h2>
          <p className="text-lg text-muted-foreground">
            Em apenas 3 passos simples você começa a economizar na sua conta de energia.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 md:gap-6 lg:gap-12">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="relative text-center group">
                {/* Connector Line */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-16 left-1/2 w-full h-0.5 bg-gradient-to-r from-primary/40 to-primary/10" />
                )}
                
                <div className="relative z-10 flex flex-col items-center">
                  {/* Step Number Badge */}
                  <div className="relative mb-6">
                    <div className="w-32 h-32 rounded-full bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center group-hover:from-primary/20 group-hover:to-primary/10 transition-smooth">
                      <Icon className="w-12 h-12 text-primary" />
                    </div>
                    <span className="absolute -top-2 -right-2 w-10 h-10 rounded-full hero-gradient flex items-center justify-center text-primary-foreground font-bold text-lg shadow-glow">
                      {step.number}
                    </span>
                  </div>

                  <h3 className="text-xl md:text-2xl font-bold text-foreground mb-3">
                    {step.title}
                  </h3>
                  <p className="text-muted-foreground max-w-xs leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
