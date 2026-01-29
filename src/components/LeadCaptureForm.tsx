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
  { value: "acougue", label: "Açougue" },
  { value: "mercado", label: "Mercado / Supermercado" },
  { value: "padaria", label: "Padaria" },
  { value: "farmacia", label: "Farmácia" },
  { value: "condominio", label: "Condomínio" },
  { value: "restaurante", label: "Restaurante / Lanchonete" },
  { value: "industria", label: "Indústria" },
  { value: "outro", label: "Outro" },
];

const consumoRanges = [
  { value: "500-1000", label: "R$ 500 - R$ 1.000" },
  { value: "1000-2000", label: "R$ 1.000 - R$ 2.000" },
  { value: "2000-5000", label: "R$ 2.000 - R$ 5.000" },
  { value: "5000-10000", label: "R$ 5.000 - R$ 10.000" },
  { value: "10000+", label: "Acima de R$ 10.000" },
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

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    setIsSubmitting(false);
    setIsSuccess(true);

    toast({
      title: "Proposta enviada com sucesso! 🎉",
      description: "Em breve nossa equipe entrará em contato.",
    });
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
          <Label>Valor Médio da Conta de Luz</Label>
          <Select
            value={formData.consumoMensal}
            onValueChange={(value) => handleInputChange("consumoMensal", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Selecione a faixa" />
            </SelectTrigger>
            <SelectContent>
              {consumoRanges.map((range) => (
                <SelectItem key={range.value} value={range.value}>
                  {range.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
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
      </form>
    </div>
  );
}
