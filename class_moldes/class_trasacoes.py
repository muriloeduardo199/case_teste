from pydantic import BaseModel
from enuns.enuns import TipoTransacao




class Transacao(BaseModel):
    """Modelo de dados para uma transação financeira."""
    id: int
    valor: float
    descricao: str
    data: str
    tipo_da_transacao: TipoTransacao

    def formatar_reais(self) -> float:
        # Converte os centavos em reais, usando ponto como separador decimal
        reais = self.valor * 100
        return f"R$ {reais:.2f}"

