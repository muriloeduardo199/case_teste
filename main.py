from typing import Union
from fastapi import FastAPI, HTTPException, Path
from class_moldes.class_trasacoes import *
import json


import uvicorn


app = FastAPI(
    title="API de Transações Financeiras",
    
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

@app.get("/")
def listar_transacao():
    """Lista todas as transações cadastradas.

    Retornos:
        dict: um dicionário com a chave "transacoes" e o valor sendo uma lista de todas as transações.
    """
    
    return {"transacoes": transacoes}


@app.get("/transacoes/{id}")
def obter_transacao(id: int = Path(...)):
    """Obtém uma transação financeira pelo id.

    :param int id: o id da transação a ser obtida.
    :return: um dicionário com a chave "transacao" e o valor sendo um objeto da classe Transacao com os dados da transação encontrada, e o status code 200.
    :raises HTTPException: se o id não existir na lista de transações.
    """
    
    for transacao in transacoes:
        
        if transacao["id"] == id:
            return {"transacao": Transacao(**transacao)}, 200
    
    raise HTTPException(status_code=404, detail="Transação não encontrada")

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
    valor_formatado = nova_transacao.formatar_reais(nova_transacao.valor)
    for transacao in transacoes:
        if transacao["id"] == id:
            transacao["descricao"] = nova_transacao.descricao
            transacao["valor"] = valor_formatado
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
    uvicorn.run(app, host = "0.0.0.0", port = 8001, reload=True)