from flask import Flask, render_template, request
import base64
import requests
import oracledb

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
    url = 'https://api.spotify.com/v1/artists?ids=06HL4z0CvFAxyc27GXpf02,6eUKZXaKkcviH0Ku9w2n3V,41MozSoPIsD1dJM0CLPjZF,0du5cEVh5yTK9QJze8zA0C,66CXWjxzNUsdJxJ2JdwvnR,6M2wZ9GZgrQXHCFfjv46we'

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
    url = 'https://api.spotify.com/v1/artists/06HL4z0CvFAxyc27GXpf02/albums'

    acesso = acessando_token()
    if acesso:
        headers = {
            'Authorization': f'Bearer {acesso}'
        }
        response = requests.request('GET', url = url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
        else:
            dados = {'items': []}
        return render_template('albuns.html', albuns=dados)
    else:
        return 'Deu erro'

# listando top 5 musicas dos artistas 
@app.route('/songs', methods=['GET'])
def listando_top5_musicas():

    url = 'https://api.spotify.com/v1/albums/151w1FgRZfnKZA9FEcg9Z3/tracks'

    acesso = acessando_token()
    if acesso:
        headers = {
            'Authorization': f'Bearer {acesso}'
        }
        response = requests.request('GET', url = url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
        else:
            dados = {'tracks': []}
        return render_template('songs.html', tracks=dados)
    else:
        return 'Deu erro smt'
    

# função para se conectar com banco de dados
def getConnection():
    try:
        conn = oracledb.connect(user="rm99553", password="020904", host=1521, service_name= "ORCL")
    except Exception as e:
        print(f'Erro ao obter a conexão: {e}')
    return conn

#Execução de um select na tabela T_ARTIST
def selectArtists():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_select = 'SELECT * FROM T_ARTIST'
        cursor.execute(sql_select)
        i = 1  
        for result in cursor: 
            print(f'\nlinha {i}: {result}')
            i += 1
    except Exception as e:
        print(f'Erro ao executar select: {e}')

#Execução de um select na tabela T_ALBUM
def selectAlbums():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_select = 'SELECT * FROM T_ALBUM'
        cursor.execute(sql_select)
        i = 1  
        for result in cursor: 
            print(f'\nlinha {i}: {result}')
            i += 1
    except Exception as e:
        print(f'Erro ao executar select: {e}')

#Execução de um select na tabela T_MUSIC
def selectMusics():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_select = 'SELECT * FROM T_MUSIC'
        cursor.execute(sql_select)
        i = 1  
        for result in cursor: 
            print(f'\nlinha {i}: {result}')
            i += 1
    except Exception as e:
        print(f'Erro ao executar select: {e}')

#Inserção de um artista na tabela T_ARTIST
def insertArtist():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_insert = f"INSERT INTO T_ARTIST VALUES ('fw56htg84tyi', 'BTS', 'artist.png', 9085)"
        cursor.execute(sql_insert)
        conn.commit()
        print('\nDados inseridos com sucesso!\n')
    except Exception as e:
        print(f'Erro ao executar insert: {e}')

#Inserção de um álbum na tabela T_ALBUM
def insertAlbum():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_insert = "INSERT INTO T_ALBUM VALUES ('ws59loy92dv', 'op5thbd9362ds', 'Born Pink', 'album.png')"
        cursor.execute(sql_insert)
        conn.commit()
        print('\nDados inseridos com sucesso!\n')
    except Exception as e:
        print(f'Erro ao executar insert: {e}')

#Inserção de uma música na tabela T_MUSIC
def insertMusic():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql_insert = "INSERT INTO T_MUSIC VALUES ('2w5d6pyzx63', '312plm84sde', 'Imagine', 10800)"
        cursor.execute(sql_insert)
        conn.commit()
        print('\nDados inseridos com sucesso!\n')
    except Exception as e:
        print(f'Erro ao executar insert: {e}')


#Fechando a conexão com o banco de dados
def closeConnection(conn):
    try:
        conn.close()
        print('\nConexão fechada com sucesso!')
    except Exception as e:
        print(f'Erro ao fechar conexão: {e}')

@app.route('/index')
def pagina1():
    return render_template('index.html')  

    
#Principal
if __name__ == "__main__":
    app.run(debug=True)
    conn = getConnection()