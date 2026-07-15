import logo from "@/assets/logo-aesolar-horizontal.png";
import { MapPin, Phone, Mail } from "lucide-react";
import { Link } from "react-router-dom";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-foreground py-12 md:py-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <img
              src={logo}
              alt="AESOLAR"
              className="h-10 md:h-12 w-auto brightness-0 invert mb-4"
            />
            <p className="text-primary-foreground/70 max-w-md mb-6">
              Energia solar por assinatura para empresários em Goiás. Economize até 26% na conta de luz sem investimento inicial.
            </p>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-primary-foreground font-semibold mb-4">Contato</h4>
            <ul className="space-y-3">
              <li>
                <div className="flex flex-col gap-1 text-primary-foreground/70">
                  <a
                    href="https://wa.me/5562992727645?text=Ol%C3%A1!%20Gostaria%20de%20saber%20mais%20sobre%20a%20energia%20solar%20por%20assinatura%20da%20AESOLAR."
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 hover:text-primary transition-smooth"
                  >
                    <Phone className="w-4 h-4" />
                    (62) 99272-7645 (WhatsApp)
                  </a>
                  <span className="text-xs pl-7 text-primary-foreground/50">
                    Fixo oficial: (62) 3638-2770
                  </span>
                </div>
              </li>
              <li>
                <a
                  href="mailto:contato@aesolar.com.br"
                  className="flex items-center gap-3 text-primary-foreground/70 hover:text-primary transition-smooth"
                >
                  <Mail className="w-4 h-4" />
                  contato@aesolar.com.br
                </a>
              </li>
              <li className="flex items-start gap-3 text-primary-foreground/70">
                <MapPin className="w-4 h-4 mt-1 flex-shrink-0" />
                <span>Av. Deputado Jamel Cecílio, 3455, Sala 806, Jd. Goiás - Goiânia/GO</span>
              </li>
            </ul>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-primary-foreground font-semibold mb-4">Links</h4>
            <ul className="space-y-3">
              <li>
                <Link
                  to="/?sec=beneficios"
                  className="text-primary-foreground/70 hover:text-primary transition-smooth"
                >
                  Benefícios
                </Link>
              </li>
              <li>
                <Link
                  to="/?sec=como-funciona"
                  className="text-primary-foreground/70 hover:text-primary transition-smooth"
                >
                  Como Funciona
                </Link>
              </li>
              <li>
                <Link
                  to="/?sec=depoimentos"
                  className="text-primary-foreground/70 hover:text-primary transition-smooth"
                >
                  Depoimentos
                </Link>
              </li>
              <li>
                <Link
                  to="/?sec=faq"
                  className="text-primary-foreground/70 hover:text-primary transition-smooth"
                >
                  Perguntas Frequentes
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="pt-8 border-t border-primary-foreground/10">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-primary-foreground/50 text-center md:text-left">
              © {currentYear} AESOLAR. Todos os direitos reservados. <br />
              <span className="text-xs opacity-80">ASSOCIACAO DE ENERGIA SOLAR COMPARTILHADA - AESOLAR | CNPJ: 46.520.853/0001-55</span>
            </p>
            <div className="flex gap-6">
              <a
                href="#"
                className="text-sm text-primary-foreground/50 hover:text-primary transition-smooth"
              >
                Política de Privacidade
              </a>
              <a
                href="#"
                className="text-sm text-primary-foreground/50 hover:text-primary transition-smooth"
              >
                Termos de Uso
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
