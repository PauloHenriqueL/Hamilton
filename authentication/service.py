import requests


#  Faça um authetication jwt na url e me traga o access e o refresh
class Auth:
    
    def __init__(self):
        self.__base_url = 'https://localhost:8000/api/v1/'
        self.__auth_url = f'{self.__base_url}authentication/token/'
    
    def get_token(self, username, password):  # Faça um get token me passando o usuário e a senha e guarde em auth_payload
        url = "http://localhost:8000/api/v1/authentication/token/"
        auth_payload = {
            "username": username,
            "password": password,
        }
        auth_response = requests.post(  # Faça um Post na url __auth_url com os dados do auth_payload
            url,
            json=auth_payload
        )
        if auth_response.status_code == 200:  # Se o status_code for 200 retorne o json
            return auth_response.json()
        return {'error': f'Erro ao autentificar. Status code: {auth_response.status_code}'}