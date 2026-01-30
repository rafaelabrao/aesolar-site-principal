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
import { CityCombobox } from "@/components/CityCombobox";

const N8N_WEBHOOK_URL = import.meta.env.VITE_N8N_WEBHOOK_URL as string | undefined;

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
  cidade: string;
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
    cidade: "",
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
  if (!N8N_WEBHOOK_URL) {
    toast({
      title: "Configuração ausente",
      description: "A URL do webhook não está configurada. Defina VITE_N8N_WEBHOOK_URL no Vercel.",
      variant: "destructive",
    });
    setIsSubmitting(false);
    return;
  }

  const whatsappDigits = formData.whatsapp.replace(/\D/g, "");
  const valorContaLuz = Number((formData.consumoMensal || "").replace(/\D/g, "")) || 0;

  const payload = {
    // Campos atuais do seu formulário
    nome: formData.nome,
    empresa: formData.empresa,
    whatsapp: formData.whatsapp,
    whatsapp_digits: whatsappDigits,
    email: formData.email,
    cidade: formData.cidade,
    tipoEstabelecimento: formData.tipoEstabelecimento,
    valorContaLuz: valorContaLuz,

    // Campos para compatibilidade com a página de proposta e o workflow do n8n
    tipo_cliente: formData.empresa && formData.empresa.trim() ? "Empresa" : "Pessoal",
    nome_cliente_final: formData.nome,
    documento_cliente_final: "",
    consumo_total: "",
    desconto_base: 20,
  };

  const response = await fetch(N8N_WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  let data: any = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    toast({
      title: "Erro ao enviar proposta",
      description: "O servidor retornou um erro. Tente novamente em instantes.",
      variant: "destructive",
    });
    setIsSubmitting(false);
    return;
  }

  const urlFinal = Array.isArray(data) ? data?.[0]?.url_final : data?.url_final;

  const url = data?.url || data?.link || urlFinal;
  const path = data?.path;

  setIsSubmitting(false);
  setIsSuccess(true);

  toast({
    title: "Proposta enviada com sucesso!",
    description: "Redirecionando para sua proposta...",
  });

  if (typeof url === "string" && url.startsWith("http")) {
    window.location.href = url;
    return;
  }

  if (typeof path === "string" && path.startsWith("/")) {
    window.location.href = window.location.origin + path;
    return;
  }

  toast({
    title: "Resposta inesperada",
    description: "Não encontrei o link da proposta na resposta do servidor.",
    variant: "destructive",
  });
} catch (error) {
  setIsSubmitting(false);
  toast({
    title: "Erro ao enviar proposta",
    description: "Falha de conexão. Verifique sua internet e tente novamente.",
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
          <Label>Cidade</Label>
          <CityCombobox
            value={formData.cidade}
            onValueChange={(value) => handleInputChange("cidade", value)}
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
