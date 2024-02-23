from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)



def test_transacao():
    response =  client.get("/")
    assert response.status_code == 200


def test_criar_transacao():
    transacao = {
        "descricao": "teste", 
        "valor": 50000.0, 
        "data": "teste", 
        "tipo_da_transacao": "entrada", 
        "id": 1
    }

    response = client.post("/transacao",json=transacao)


# Criando uma função de teste para a rota PUT /transacoes/{id}
def test_editar_transacao():
    # Definindo o id da transação a ser editada
    id = 1
    # Definindo os novos dados da transação
    data = {
        "id": 1,
        "valor": 200.0,
        "descricao": "Recebimento de salário",
        "data": "2024-02-23",
        "tipo_da_transacao": "entrada"
    }
    # Enviando uma requisição PUT para a rota /transacoes/{id} com os novos dados da transação
    response = client.put(f"/transacoes/{id}", json=data)
    # Verificando se o status code é 200
    assert response.status_code == 200
    # Verificando se o conteúdo da resposta é uma mensagem de sucesso
    assert response.json() == {"mensagem": "Transação editada com sucesso"}



# Criando uma função de teste para a rota DELETE /transacoes/{id}
def test_remover_transacao():
    # Definindo o id da transação a ser removida
    id = 1
    # Enviando uma requisição DELETE para a rota /transacoes/{id}
    response = client.delete(f"/transacoes/{id}")
    # Verificando se o status code é 200
    assert response.status_code == 200
    # Verificando se o conteúdo da resposta é uma mensagem de sucesso
    assert response.json() == {"mensagem": "Transação removida com sucesso"}
