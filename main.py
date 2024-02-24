from typing import Union
from fastapi import FastAPI, HTTPException
from class_moldes.class_trasacoes import *
import json


import uvicorn


app = FastAPI(
    title="API de Transações Financeiras",
    description="Uma API simples para gerenciar transações de entrada e saída",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)




with open("transacoes.json") as f: transacoes = json.load(f)



@app.post("/transacao", status_code=201)
def cadastrar_transacao(transacao: Transacao):
    """Cadastra uma nova transação na lista de transações.

    Parâmetros:
        transacao (Transacao): o objeto com os dados da transação.

    Retornos:
        Transacao: o objeto com os dados da transação cadastrada.

    Exceções:
        HTTPException: se algum campo da transação for inválido ou faltar.
    """
    
    if not (transacao.descricao and transacao.valor and transacao.data and transacao.tipo_da_transacao):
        raise HTTPException(status_code=400, detail="Todos os campos são obrigatórios")
    
    if transacao.tipo_da_transacao not in [TipoTransacao.ENTRADA, TipoTransacao.SAIDA]: # usando o valor do Enum na validação
        raise HTTPException(status_code=400, detail="O tipo da transação deve ser entrada ou saída")
    valor_formatado = transacao.formatar_reais(transacao.valor)
    transacao.valor = valor_formatado
    transacoes.append(transacao.dict() )

    with open("transacoes.json", "w") as f:
        json.dump(transacoes, f)
    print(transacao)
    
    return {"transacao": transacao, "valor_formatado": valor_formatado}

@app.get("/", status_code=204)
def listar_transacao():
    """Lista todas as transações cadastradas.

    Retornos:
        dict: um dicionário com a chave "transacoes" e o valor sendo uma lista de todas as transações.
    """
    
    return {"transacoes": transacoes}


@app.put("/transacoes/{id}")
def editar_transacao(id:int, nova_transacao: Transacao):
    """Edita uma transação existente com base no id informado.

    Parâmetros:
        id (int): o id da transação a ser editada.
        nova_transacao (Transacao): o objeto com os novos dados da transação.

    Retornos:
        dict: um dicionário com a chave "mensagem" e o valor sendo uma string de sucesso.

    Exceções:
        HTTPException: se o id não existir ou algum campo da transação for inválido ou faltar.
    """
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
    """Remove uma transação existente com base no id informado.

    Parâmetros:
        id (int): o id da transação a ser removida.

    Retornos:
        dict: um dicionário com a chave "mensagem" e o valor sendo uma string de sucesso.

    Exceções:
        HTTPException: se o id não existir.
    """
    
    
    novas_transacoes = [transacao for transacao in transacoes if transacao["id"] != id]
    
    if len(novas_transacoes) == len(transacoes):
        
        return {"erro": "Transação não encontrada"}
    
    else:
        with open("transacoes.json", "w") as f:
            json.dump(novas_transacoes, f)
        
        return {"mensagem": "Transação removida com sucesso"}


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8001)