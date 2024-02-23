
from enum import Enum


class TipoTransacao(str,Enum):
    """Enumeração dos tipos de transação possíveis: entrada ou saída."""
    ENTRADA = "entrada"
    SAIDA = "saida"