import { Star, Quote } from "lucide-react";

const testimonials = [
  {
    name: "Carlos Alberto",
    role: "Dono de Açougue",
    location: "Goiânia, GO",
    content: "Minha conta de energia era um pesadelo. Com a AESOLAR, economizo mais de R$ 800 por mês. Melhor decisão que tomei pro meu negócio!",
    rating: 5,
  },
  {
    name: "Maria Helena",
    role: "Proprietária de Padaria",
    location: "Anápolis, GO",
    content: "Achei que era bom demais pra ser verdade, mas já são 8 meses economizando. Sem instalação, sem dor de cabeça. Recomendo muito!",
    rating: 5,
  },
  {
    name: "Roberto Santos",
    role: "Síndico de Condomínio",
    location: "Aparecida de Goiânia, GO",
    content: "Consegui reduzir em 25% o custo de energia do condomínio. Os moradores adoraram e a taxa condominial ficou mais acessível.",
    rating: 5,
  },
];

export function TestimonialsSection() {
  return (
    <section id="depoimentos" className="py-16 md:py-24 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-12 md:mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-secondary text-secondary-foreground text-sm font-medium mb-4">
            Depoimentos Reais
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Quem já <span className="text-primary">economiza</span> com a gente
          </h2>
          <p className="text-lg text-muted-foreground">
            Veja o que empresários de Goiás estão dizendo sobre a AESOLAR.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="relative p-6 md:p-8 rounded-2xl bg-card border border-border/50 hover:border-primary/30 transition-smooth hover:shadow-soft"
            >
              {/* Quote Icon */}
              <div className="absolute top-6 right-6 w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <Quote className="w-5 h-5 text-primary" />
              </div>

              {/* Rating */}
              <div className="flex gap-1 mb-4">
                {Array.from({ length: testimonial.rating }).map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-primary text-primary" />
                ))}
              </div>

              {/* Content */}
              <p className="text-foreground mb-6 leading-relaxed">
                "{testimonial.content}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full hero-gradient flex items-center justify-center text-primary-foreground font-bold text-lg">
                  {testimonial.name.charAt(0)}
                </div>
                <div>
                  <p className="font-semibold text-foreground">{testimonial.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {testimonial.role} • {testimonial.location}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <p className="text-center text-sm text-muted-foreground mt-8">
          * Depoimentos de clientes AESOLAR em Goiás.
        </p>
      </div>
    </section>
  );
}
