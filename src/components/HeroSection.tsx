import { LeadCaptureForm } from "@/components/LeadCaptureForm";
import { Check } from "lucide-react";
import heroBackground from "@/assets/hero-background.jpg";
import logo from "@/assets/logo-aesolar-horizontal.png";

const benefits = [
  "Economia de até 26% na conta de luz",
  "Sem instalação de equipamentos",
  "Sem investimento inicial",
  "Exclusivo para Goiás",
];

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center">
      {/* Background Image */}
      <div
     className="absolute inset-0 bg-cover bg-no-repeat bg-[center_80%] md:bg-center"
      style={{ backgroundImage: `url(${heroBackground})` }}
    />
      
      {/* Overlay */}
      <div className="absolute inset-0 hero-overlay" />
      
      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 py-16 md:py-24">
        {/* Header/Logo */}
        <div className="mb-8 md:mb-12">
          <img 
            src={logo} 
            alt="AESOLAR" 
            className="h-10 md:h-14 w-auto brightness-0 invert"
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
          {/* Left Content */}
          <div className="space-y-6 animate-fade-in">
            <div>
              <span className="inline-block px-4 py-1.5 rounded-full bg-primary/20 text-primary-foreground text-sm font-medium mb-4 backdrop-blur-sm border border-primary/30">
                Para Empresários em Goiás
              </span>
              
              <h1 className="text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-extrabold text-primary-foreground leading-tight text-balance">
                Economize até{" "}
                <span className="text-primary">26%</span> na conta de luz{" "}
                <span className="text-primary-foreground/80">sem investir nada</span>
              </h1>
            </div>

            <p className="text-lg md:text-xl text-primary-foreground/80 max-w-xl">
              Associe-se à <strong className="text-primary">AESOLAR</strong> e comece a economizar desde a primeira fatura. Energia solar por assinatura para seu comércio.
            </p>

            {/* Benefits List */}
            <ul className="space-y-3 pt-4">
              {benefits.map((benefit, index) => (
                <li 
                  key={index}
                  className="flex items-center gap-3 text-primary-foreground/90"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center">
                    <Check className="w-4 h-4 text-primary" />
                  </span>
                  <span className="text-base md:text-lg">{benefit}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Right Content - Form */}
          <div className="lg:justify-self-end w-full max-w-md mx-auto lg:mx-0">
            <LeadCaptureForm />
          </div>
        </div>
      </div>
    </section>
  );
}
