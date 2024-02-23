from fastapi.testclient import TestClient
from main_app_run.main_app import app  

client = TestClient(app)



def test_transacao():
    response =  client.get("/")

    assert response.status_code == 200