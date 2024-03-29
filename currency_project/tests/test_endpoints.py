import asyncio

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
import pytest as pt

from main import app
import app.api.schemas.currency as scc
import app.api.schemas.user as scu
import tests.config as cfg
import app.api.schemas.token as sct
import app.db.models as md

JWT_TOKEN = ""
client = TestClient(app)

@pt.fixture(scope='session', autouse='True')
def _test_create_db():
    global JWT_TOKEN
    cfg.clear_test_db()    
    asyncio.run(cfg.create_models())
    yield
    asyncio.run(cfg.drop_models())
    cfg.clear_test_db()
    JWT_TOKEN = ""




class TestUser:
    correct_user = scu.UserInput(
        email='test1@email.com',
        password='`1Aaaaaa',
        name='test1'
    )
  
    
    def test_correct_signup(self):
        response = client.post('/auth/register',
                               json=self.correct_user.model_dump())        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == f'Пользователь: {self.correct_user.name}, id: {1}'
    
    
    def test_user_already_exists(self):
        response = client.post('/auth/register',
                               json=self.correct_user.model_dump())        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['detail'] == "Пользователь с такой почтой уже существует!"

    
    def test_correct_login(self):
        global JWT_TOKEN
        response = client.post('/auth/login',
                               data={"username": self.correct_user.email,
                                     "password": self.correct_user.password}
                               )
        assert response.status_code == status.HTTP_200_OK
        r_json = response.json()
        assert "access_token" in r_json
        JWT_TOKEN = r_json["access_token"]
        assert "token_type" in r_json


    def test_auth_error(self):
        response = client.post('/auth/login',
                               data={"username": self.correct_user.email,
                                     "password": "WrOnG_PassW0rd"}
                               )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()['detail'] == "Ошибка аутентификации!"


class TestCurrency:
    def test_get_currency_list(self):
        global JWT_TOKEN
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        response = client.get("/currency/list", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        currency_list = response.json()
        assert len(currency_list) > 1
        assert "code" in currency_list[0]
        assert "description" in currency_list[0]


    @pt.mark.parametrize("amount, amount_param", enumerate(("", "&amount=2", "&amount=3"), 1))
    def test_get_exchange(self, amount, amount_param):
        global JWT_TOKEN
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        response = client.get(f"/currency/exchange/?from_currency=usd&to_currency=rub{amount_param}",
                              headers=headers)

        assert response.status_code == status.HTTP_200_OK
        r_json = response.json()
        assert "amount" in r_json
        assert r_json["amount"] == float(amount)
    
    
    def test_invalid_currency(self):
        global JWT_TOKEN
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}

        response = client.get("/currency/exchange/?from_currency=abc&to_currency=cde",
                              headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Такие валюты не найдены."

    
    def test_not_authenticated(self):
        response = client.get("/currency/list")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Not authenticated"

    