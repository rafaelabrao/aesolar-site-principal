import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { Loader2, CheckCircle } from "lucide-react";

const establishmentTypes = [
  { value: "residencia", label: "Residência" },
  { value: "acougue", label: "Açougue" },
  { value: "mercado", label: "Mercado / Supermercado" },
  { value: "padaria", label: "Padaria" },
  { value: "farmacia", label: "Farmácia" },
  { value: "condominio", label: "Condomínio" },
  { value: "restaurante", label: "Restaurante / Lanchonete" },
  { value: "industria", label: "Indústria" },
  { value: "outro", label: "Outro" },
];

interface FormData {
  nome: string;
  empresa: string;
  whatsapp: string;
  email: string;
  tipoEstabelecimento: string;
  consumoMensal: string;
}

export function LeadCaptureForm() {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    nome: "",
    empresa: "",
    whatsapp: "",
    email: "",
    tipoEstabelecimento: "",
    consumoMensal: "",
  });

  const formatWhatsApp = (value: string) => {
    const numbers = value.replace(/\D/g, "").slice(0, 11);
    if (numbers.length <= 2) return numbers;
    if (numbers.length <= 7) return `(${numbers.slice(0, 2)}) ${numbers.slice(2)}`;
    return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 7)}-${numbers.slice(7)}`;
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    if (field === "whatsapp") {
      value = formatWhatsApp(value);
    }
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Basic validation
    if (!formData.nome.trim() || formData.nome.length > 100) {
      toast({
        title: "Nome inválido",
        description: "Por favor, insira um nome válido.",
        variant: "destructive",
      });
      return;
    }

    if (!formData.whatsapp || formData.whatsapp.replace(/\D/g, "").length < 10) {
      toast({
        title: "WhatsApp inválido",
        description: "Por favor, insira um número de WhatsApp válido.",
        variant: "destructive",
      });
      return;
    }

    if (!formData.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      toast({
        title: "E-mail inválido",
        description: "Por favor, insira um e-mail válido.",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch("https://n8n.borealsolar.tech/webhook/proposta_site", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nome: formData.nome,
          empresa: formData.empresa,
          whatsapp: formData.whatsapp,
          email: formData.email,
          tipoEstabelecimento: formData.tipoEstabelecimento,
          valorContaLuz: formData.consumoMensal,
        }),
      });

      const data = await response.json();
      
      setIsSubmitting(false);
      setIsSuccess(true);

      toast({
        title: "Proposta enviada com sucesso! 🎉",
        description: "Redirecionando para sua proposta...",
      });

      // Open the link returned by the webhook
      if (data.url || data.link) {
        window.open(data.url || data.link, "_blank");
      }
    } catch (error) {
      setIsSubmitting(false);
      toast({
        title: "Erro ao enviar proposta",
        description: "Por favor, tente novamente ou entre em contato pelo WhatsApp.",
        variant: "destructive",
      });
    }
  };

  if (isSuccess) {
    return (
      <div className="rounded-2xl bg-card p-8 shadow-soft animate-fade-in">
        <div className="flex flex-col items-center text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-primary" />
          </div>
          <h3 className="text-2xl font-bold text-foreground">Proposta Enviada!</h3>
          <p className="text-muted-foreground">
            Recebemos suas informações. Nossa equipe entrará em contato em até 24 horas para apresentar sua proposta personalizada de economia.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-card p-6 md:p-8 shadow-soft animate-slide-up">
      <h3 className="text-xl md:text-2xl font-bold text-primary text-center mb-6">
        Calcule sua Economia
      </h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="nome">Nome Completo *</Label>
          <Input
            id="nome"
            placeholder="Seu nome"
            value={formData.nome}
            onChange={(e) => handleInputChange("nome", e.target.value)}
            maxLength={100}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="empresa">Nome da Empresa</Label>
          <Input
            id="empresa"
            placeholder="Nome do seu negócio"
            value={formData.empresa}
            onChange={(e) => handleInputChange("empresa", e.target.value)}
            maxLength={100}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="whatsapp">WhatsApp *</Label>
          <Input
            id="whatsapp"
            placeholder="(00) 00000-0000"
            value={formData.whatsapp}
            onChange={(e) => handleInputChange("whatsapp", e.target.value)}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">E-mail *</Label>
          <Input
            id="email"
            type="email"
            placeholder="seu@email.com"
            value={formData.email}
            onChange={(e) => handleInputChange("email", e.target.value)}
            maxLength={255}
            required
          />
        </div>

        <div className="space-y-2">
          <Label>Tipo de Estabelecimento</Label>
          <Select
            value={formData.tipoEstabelecimento}
            onValueChange={(value) => handleInputChange("tipoEstabelecimento", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Selecione o tipo" />
            </SelectTrigger>
            <SelectContent>
              {establishmentTypes.map((type) => (
                <SelectItem key={type.value} value={type.value}>
                  {type.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="consumoMensal">Valor da Conta de Luz (R$)</Label>
          <Input
            id="consumoMensal"
            type="text"
            inputMode="numeric"
            placeholder="Ex: 1500"
            value={formData.consumoMensal}
            onChange={(e) => {
              const value = e.target.value.replace(/\D/g, "");
              handleInputChange("consumoMensal", value);
            }}
          />
        </div>

        <Button
          type="submit"
          variant="hero"
          size="xl"
          className="w-full mt-6"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Enviando...
            </>
          ) : (
            "Receber Proposta Gratuita"
          )}
        </Button>

        <p className="text-xs text-center text-muted-foreground mt-4">
          Ao enviar, você concorda em receber contato da AESOLAR sobre sua proposta de economia.
        </p>

        <div className="text-center mt-4 pt-4 border-t border-border">
          <p className="text-sm text-muted-foreground mb-1">Prefere falar conosco?</p>
          <a
            href="https://wa.me/556236382770?text=Ol%C3%A1!%20Gostaria%20de%20saber%20mais%20sobre%20a%20energia%20solar%20por%20assinatura%20da%20AESOLAR."
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary font-medium hover:underline"
          >
            (62) 3638-2770
          </a>
        </div>
      </form>
    </div>
  );
}
