from pydantic import BaseModel
from enuns.enuns import TipoTransacao
from datetime import datetime



class Transacao(BaseModel):
    """Modelo de dados para uma transação financeira."""
    id: int
    valor: float
    descricao: str
    data: str 
    tipo_da_transacao: TipoTransacao

    def formatar_reais(self, valor: int) -> float:
        """ Converte os centavos em reais, usando ponto como separador decimal"""
        reais = self.valor * 100
        return reais

