from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from enum import Enum
import uvicorn

app = FastAPI()

class TipoTransacao(str,Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class Transacao(BaseModel):
    id: int
    valor: float
    descricao: str
    data: str
    tipo_da_transacao: TipoTransacao

with open("transacoes.json") as f: transacoes = json.load(f)

# Definindo a rota POST /transacao
@app.post("/transacao")
def cadastrar_transacao(transacao: Transacao):
    # Validando os campos obrigatórios
    if not (transacao.descricao and transacao.valor and transacao.data and transacao.tipo_da_transacao):
        # Levantando uma exceção HTTP com status code 400 e mensagem de erro
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios")
    # Validando se o tipo da transação é entrada ou saída
    if transacao.tipo_da_transacao not in [TipoTransacao.ENTRADA, TipoTransacao.SAIDA]: # usando o valor do Enum na validação
        # Levantando uma exceção HTTP com status code 400 e mensagem de erro
        raise HTTPException(status_code=400, detail="O tipo da transação deve ser entrada ou saída")
    # Cadastrando a transação na lista de transacoes
    transacoes.append(transacao.dict())
    # Atualizando o arquivo transacoes.json com a nova transação
    with open("transacoes.json", "w") as f:
        json.dump(transacoes, f)
    # Retornando as informações da transação cadastrada
    return transacao


@app.get("/")
def listar_transacao():
    
    return {"transacoes": transacoes}


@app.put("/transacoes/{id}")
def editar_transacao(id:int, nova_transacao: Transacao):
    for transacao in transacoes:
        if transacao["id"] == id:
            transacao["descricao"] = nova_transacao.descricao
            transacao["valor"] = nova_transacao.valor
            transacao["data"] = nova_transacao.data
            transacao["tipo_da_transacao"] = nova_transacao.tipo_da_transacao
            with open("transacoes.json", "w") as f:
                json.dump(transacoes, f)

            return {"mensagem": "Transação editada com sucesso"}
        
    return {"erro": "Transação não encontrada"}


@app.delete("/transacoes/{id}")
def remover_transacao(id: int):
    # Imprimindo o id recebido
    print(f"Removendo a transação com id {id}")
    # Criando uma nova lista sem a transação com o id informado
    novas_transacoes = [transacao for transacao in transacoes if transacao["id"] != id]
    # Se a nova lista tiver o mesmo tamanho da lista original, significa que a transação não foi encontrada
    if len(novas_transacoes) == len(transacoes):
        # Retornando uma mensagem de erro
        return {"erro": "Transação não encontrada"}
    # Se a nova lista tiver um tamanho menor, significa que a transação foi removida
    else:
        # Abrindo o arquivo transacoes.json em modo de escrita e salvando a nova lista
        with open("transacoes.json", "w") as f:
            json.dump(novas_transacoes, f)
        # Retornando uma mensagem de sucesso
        return {"mensagem": "Transação removida com sucesso"}


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8001)