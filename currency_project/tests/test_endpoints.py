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
    JWT_TOKEN = ''




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
        response = client.post('/auth/login',
                               data={"username": self.correct_user.email,
                                     "password": self.correct_user.password}
                               )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        JWT_TOKEN = response.json()["access_token"]


    def test_auth_error(self):
        response = client.post('/auth/login',
                               data={"username": self.correct_user.email,
                                     "password": "WrOnG_PassW0rd"}
                               )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()['detail'] == "Ошибка аутентификации!"


class TestCurrency:
    headers = {"Authorization": f"bearer {JWT_TOKEN}"}

    def test_get_currency_list(self):

        response = client.get("/currency/list", headers=self.headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['']
        #  добавить в таблицу с курсами поле даты
