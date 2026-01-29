import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "Como funciona a energia solar por assinatura?",
    answer: "A AESOLAR possui usinas de energia solar que geram eletricidade limpa. Ao se associar, você recebe créditos dessa energia diretamente na sua conta de luz da distribuidora local, garantindo economia sem precisar instalar nada no seu estabelecimento.",
  },
  {
    question: "Preciso instalar painéis solares no meu negócio?",
    answer: "Não! Essa é uma das grandes vantagens. Você não precisa instalar nenhum equipamento. Toda a geração acontece nas nossas usinas solares e os créditos são transferidos para sua conta de energia.",
  },
  {
    question: "Qual é o investimento inicial?",
    answer: "Zero! Não há nenhum custo inicial para aderir à AESOLAR. Você começa a economizar desde a primeira fatura sem precisar investir nada.",
  },
  {
    question: "A economia de até 26% é garantida?",
    answer: "Sim! O percentual de economia pode variar de acordo com o seu perfil de consumo, mas garantimos uma economia real e consistente na sua conta de luz todo mês.",
  },
  {
    question: "Esse serviço está disponível em todo o Brasil?",
    answer: "Atualmente, operamos exclusivamente no estado de Goiás, oferecendo um serviço personalizado e de qualidade para empresários da região.",
  },
  {
    question: "Como posso acompanhar minha economia?",
    answer: "Você receberá relatórios mensais detalhados mostrando sua economia e os créditos de energia aplicados à sua conta. Além disso, nossa equipe está sempre disponível para esclarecer dúvidas.",
  },
];

export function FAQSection() {
  return (
    <section id="faq" className="py-16 md:py-24 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-3xl mx-auto mb-12 md:mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-secondary text-secondary-foreground text-sm font-medium mb-4">
            Tire suas Dúvidas
          </span>
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4">
            Perguntas <span className="text-primary">Frequentes</span>
          </h2>
          <p className="text-lg text-muted-foreground">
            Respondemos as principais dúvidas sobre energia solar por assinatura.
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="bg-card border border-border/50 rounded-xl px-6 data-[state=open]:border-primary/30 transition-smooth"
              >
                <AccordionTrigger className="text-left font-semibold text-foreground hover:text-primary py-5">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground pb-5 leading-relaxed">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}
