from flask import Flask, render_template, request
import base64
import requests
import json

app = Flask(__name__)

artists = []

albuns = []

tracks = []


# função para acessar o token
@app.route('/teste')
def acessando_token():

    # codigos do client id e client secret
    client_id = '8cc826683e004fdd94a1d868e881e659'
    client_secret = '54546ed0318c4bc897b3ac7c6f602e09'

    # convertendo o cliente id e o cliente secreto para base64
    credentials = f"{client_id}:{client_secret}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    # definindo a api e a payload
    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'client_credentials'
    }

    # definindo headers com o codigo convertido 
    headers = {
        'Authorization': f'Basic {base64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # fazendo uma request POST para conseguir o ecesso do token
    response = requests.request('POST', url = url, data=payload, headers=headers)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        return None
    
@app.route('/')
def index():
    return 'Testando para ver se ta funcionando'

# listando os artistas 
@app.route('/artists', methods=['GET'])
def listando_artistas():
    url = 'https://api.spotify.com/v1/artists?ids=2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6,06HL4z0CvFAxyc27GXpf02,0EmeFodog0BfCgMzAIvKQp,6eUKZXaKkcviH0Ku9w2n3V,41MozSoPIsD1dJM0CLPjZF,0du5cEVh5yTK9QJze8zA0C,3Nrfpe0tUJi4K4DXYWgMUX,66CXWjxzNUsdJxJ2JdwvnR,6M2wZ9GZgrQXHCFfjv46we,4nDoRrQiYLoBzwC5BhVJzF,6S2OmqARrzebs0tKUEyXyp,7n2wHs1TKAczGzO7Dd2rGr,3zgnrYIltMkgeejmvMCnes'

    acesso = acessando_token()
    if acesso:
        headers = {
            'Authorization': f'Bearer {acesso}'
        }
        response = requests.request('GET', url = url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
        else:
            dados = []
        return render_template('index.html', artists=dados)
    else:
        return 'Deu erro smt'

#listando albuns 
@app.route('/albuns', methods=['GET'])
def listando_albuns():
    url = 'https://api.spotify.com/v1/albums/3zgnrYIltMkgeejmvMCnes'

    acesso = acessando_token()
    if acesso:
        headers = {
            'Authorization': f'Bearer {acesso}'
        }
        response = requests.request('GET', url = url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
        else:
            dados = []
        return render_template('albuns.html', albuns=dados)
    else:
        return 'Deu erro smt'

# listando top 5 musicas dos artistas 
@app.route('/songs', methods=['GET'])
def listando_top5_musicas():

    url = f'https://api.spotify.com/v1/artists?ids=3zgnrYIltMkgeejmvMCnes/top-tracks'

    acesso = acessando_token()
    if acesso:
        headers = {
            'Authorization': f'Bearer {acesso}'
        }
        response = requests.request('GET', url = url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
        else:
            dados = []
        return render_template('songs.html', tracks=dados)
    else:
        return 'Deu erro smt'

@app.route('/index')
def pagina1():
    return render_template('index.html')  

    
#Principal
if __name__ == "__main__":
    app.run(debug=True)