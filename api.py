from flask import Flask, make_response, request, jsonify
import mariadb
import sys
import jwt
from functools import wraps
import datetime


#Conectando Banco
try:
    banco = mariadb.connect(user='furb', password='furb', host='127.0.0.1', port=3306, database='filmes_teste')
except mariadb.Error as erro:
    print(f"Erro no banco de dados {erro}")
    sys.exit(1)

cursor = banco.cursor() #Cursor para manipular os dados recebidos

#Inicialização do app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'furb@123' #senha do token

def teste_token(a):
    @wraps(a)
    def decorador(*args, **kwargs):
        token = None
        if 'Token' in request.headers: #Se houver o token no cabecalho
            token = request.headers['Token']
        if not token: #nao há token
            return make_response(jsonify(mensagem='Não há token'),401)
        try:
            entrada = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256') #decodifica
            cursor.execute(f"SELECT * FROM Usuario WHERE usuario_username=\'{entrada['usuario_username']}\'")
            usuario_atual = cursor.fetchone() #buscando usuario
        except:
            return make_response(jsonify(mensagem='Token invalido'))
        return a(usuario_atual, *args, **kwargs)
    return decorador
@app.route('/login', methods=['POST']) #para autenticar
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(jsonify(mensagem='Não foi possível fazer a verificacao'))
    cursor.execute(f"SELECT * FROM Usuario WHERE usuario_username=\'{auth.username}\'")
    usuario = cursor.fetchone()
    username = usuario[2]
    senha = usuario[3]
    if not usuario:
        return make_response(jsonify(mensagem="Não foi possível verificar"), 401)
    if senha == auth.password:
        token = jwt.encode({'usuario_username': username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return make_response(jsonify(token=token))
    return make_response(jsonify(mensagem="Não foi possível verificar"))

#Rotas e funções:
@app.route('/titulos', methods = ['GET'])
@teste_token
def get_titulo(usuario_atual):
    cursor.execute('SELECT * FROM Titulo')
    tds_titulos = cursor.fetchall()
    titulos = list()
    for titulo in tds_titulos:
        titulos.append(
            {
                'id': titulo[0],
                'nome': titulo[1],
                'lancamento': titulo[2],
                'idade': titulo[3],
                'sinopse': titulo[4]
            }
        )
    return make_response(jsonify(mensagem='Lista de filmes:', titulos=titulos))
@app.route('/titulos', methods = ['POST'])
@teste_token
def criar_titulo(usuario_atual):
    titulo = request.json
    comando = f"INSERT INTO Titulo (titulo_nome, titulo_data_lancamento,titulo_idade, titulo_sinopse) VALUES ('{titulo['nome']}', '{titulo['lancamento']}','{titulo['idade']}','{titulo['sinopse']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Título cadastrado com sucesso', titulo=titulo))
@app.route('/titulos', methods=['DELETE'])
@teste_token
def del_titulo(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Titulo WHERE titulo_id={indice}")
        titulo = cursor.fetchone()
        if type(titulo) != None:
            comando = f"DELETE FROM Titulo WHERE titulo_id={titulo[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status= 'Ok', mensagem='Titulo deletado com sucesso'))
    except :
        return make_response(jsonify(status= 'Erro', mensagem='Erro ao deletar titulo.' + f'titulo={indice}' + ' não existe'),500)
@app.route('/pessoas', methods = ['GET'])
@teste_token
def get_pessoas(usuario_atual):
    cursor.execute('SELECT * FROM Pessoa')
    tds_pessoas = cursor.fetchall()
    pessoas = list()
    for pessoa in tds_pessoas:
        pessoas.append(
            {
                'id': pessoa[0],
                'nome': pessoa[1],
                'descricao': pessoa[2]
            }
        )
    return make_response(jsonify(mensagem='Lista de Pessoas:', pessoa=pessoas))
@app.route('/pessoas', methods=['POST'])
@teste_token
def criar_pessoas(usuario_atual):
    pessoa = request.json
    comando = f"INSERT INTO Pessoa (pessoa_nome, pessoa_desc) VALUES ('{pessoa['nome']}','{pessoa['descricao']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Pessoa cadastrada com sucesso', pessoa=pessoa))
@app.route('/pessoas', methods=['DELETE'])
@teste_token
def del_pessoa(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Pessoa WHERE pessoa_id={indice}")
        pessoa = cursor.fetchone()
        if type(pessoa) != None:
            comando = f"DELETE FROM Pessoa WHERE pessoa_id={pessoa[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Pessoa deletada com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar pessoa.' + f'pessoa={indice}' + ' não existe'),500)
@app.route('/episodio', methods=['GET'])
@teste_token
def get_epi(usuario_atual):
    cursor.execute('SELECT * FROM Episodio')
    tds_epis = cursor.fetchall()
    episodios = list()
    print(tds_epis)
    for episodio in tds_epis:
        episodios.append(
            {
                'titulo': episodio[0],
                'temporada': episodio[1],
                'id': episodio[2],
                'nome': episodio[3],
                'descricao': episodio[4],
                'numero': episodio[5],
                'duracao': episodio[6]
            }
        )
    return make_response(jsonify(mensagem='Lista de Episodios:', episodio=episodios))
@app.route('/episodio', methods=['POST'])
@teste_token
def criar_epi(usuario_atual):
    episodio = request.json
    comando = f"INSERT INTO Episodio (titulo_id, temporada_id, episodio_nome, episodio_desc, episodio_num,episodio_duracao) VALUES ('{episodio['titulo']}','{episodio['temporada']}','{episodio['nome']}','{episodio['descricao']}', '{episodio['numero']}','{episodio['duracao']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Pessoa cadastrada com sucesso', episodio=episodio))
@app.route('/episodio', methods=['DELETE']) #OLHAR -> FAZER A MESMA COISA QUE EM Titulo_Genero
@teste_token
def del_episodio(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Episodio WHERE episodio_id={indice}")
        episodio = cursor.fetchone()
        if type(episodio) != None:
            comando = f"DELETE FROM Episodio WHERE episodio_id={episodio[2]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Episodio deletado com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar episodio.' + f'episodio={indice}' + ' não existe'),500)
@app.route('/filme', methods=['GET'])
@teste_token
def get_filme(usuario_atual):
    cursor.execute('SELECT * FROM Filme')
    tds_filmes = cursor.fetchall()
    filmes = list()
    for filme in tds_filmes:
        filmes.append(
            {
                'id': filme[0],
                'duracao': filme[1]
            }
        )
    return make_response(jsonify(mensagem='Lista de Filmes:', filme=filmes))
@app.route('/filme', methods=['POST'])
@teste_token
def criar_filme(usuario_atual):
    filme = request.json
    comando = f"INSERT INTO Filme (titulo_id, filme_duracao) VALUES ('{filme['id']}','{filme['duracao']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Filme cadastrada com sucesso', filme=filme))
@app.route('/filme', methods=['DELETE'])
@teste_token
def del_filme(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Filme WHERE titulo_id={indice}")
        filme = cursor.fetchone()
        if type(filme) != None:
            comando = f"DELETE FROM Filme WHERE titulo_id={filme[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Filme deletado com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar filme.' + f'filme={indice}' + ' não existe'),500)
@app.route('/funcao', methods=['GET'])
@teste_token
def get_funcao(usuario_atual):
    cursor.execute('SELECT * FROM Funcao')
    tds_funcoes = cursor.fetchall()
    funcoes = list()
    for funcao in tds_funcoes:
        funcoes.append(
            {
                'id': funcao[0],
                'nome': funcao[1]
            }
        )
    return make_response(jsonify(mensagem='Lista de funções:', funcao=funcoes))
@app.route('/funcao', methods=['POST'])
@teste_token
def criar_funcao(usuario_atual):
    funcao = request.json
    comando = f"INSERT INTO Funcao (funcao_nome) VALUES ('{funcao['nome']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Função cadastrada com sucesso', funcao=funcao))
@app.route('/funcao', methods=['DELETE'])
@teste_token
def del_funcao(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Funcao WHERE funcao_id={indice}")
        funcao = cursor.fetchone()
        if type(funcao) != None:
            comando = f"DELETE FROM Funcao WHERE funcao_id={funcao[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Funcao deletada com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar funcao.' + f'funcao={indice}' + ' não existe'),500)
@app.route('/genero', methods=['GET'])
@teste_token
def get_genero(usuario_atual):
    cursor.execute('SELECT * FROM Genero')
    tds_generos = cursor.fetchall()
    generos = list()
    for genero in tds_generos:
        generos.append(
            {
                'id': genero[0],
                'nome': genero[1]
            }
        )
    return make_response(jsonify(mensagem='Lista de generos:', genero=generos))
@app.route('/genero', methods=['POST'])
@teste_token
def criar_genero(usuario_atual):
    genero = request.json
    comando = f"INSERT INTO Genero (genero_nome) VALUES ('{genero['nome']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Gênero cadastrada com sucesso', genero=genero))
@app.route('/genero', methods=['DELETE'])
@teste_token
def del_genero(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Genero WHERE genero_id={indice}")
        genero = cursor.fetchone()
        if type(genero) != None:
            comando = f"DELETE FROM Genero WHERE genero_id={genero[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Genero deletado com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar genero.' + f'genero={indice}' + ' não existe'),500)

@app.route('/serie', methods=['GET'])
@teste_token
def get_serie(usuario_atual):
    cursor.execute('SELECT * FROM Serie')
    tds_series = cursor.fetchall()
    series = list()
    for serie in tds_series:
        series.append(
            {
                'id': serie[0],
                'temporadas': serie[1],
                'duracao_epi': serie[2]
            }
        )
    return make_response(jsonify(mensagem='Lista de séries:', serie=series))
#Deletar essa posteriormente? Não tem o que criar
@app.route('/serie', methods=['POST'])
@teste_token
def criar_serie(usuario_atual):
    serie = request.json
    print(serie)
    comando = f"INSERT INTO Serie (titulo_id, serie_temporadas, serie_duracao_epi) VALUES ('{serie['id']}', '{serie['temporadas']}', '{serie['duracao_epi']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Serie cadastrada com sucesso', serie=serie))
@app.route('/serie', methods=['DELETE'])
@teste_token
def del_serie(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Serie WHERE titulo_id={indice}")
        serie = cursor.fetchone()
        if type(serie) != None:
            comando = f"DELETE FROM Serie WHERE titulo_id={serie[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Serie deletada com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar serie.' + f'serie={indice}' + ' não existe'),500)
@app.route('/temporada', methods=['GET'])
@teste_token
def get_temp(usuario_atual):
    cursor.execute('SELECT * FROM Temporada')
    tds_temps = cursor.fetchall()
    temps = list()
    for temp in tds_temps:
        temps.append(
            {
                'titulo_id': temp[0],
                'temporada_id': temp[1],
                'nome': temp[2],
                'descricao': temp[3]
            }
        )
    return make_response(jsonify(mensagem='Lista de temporadas:', temporada=temps))
@app.route('/temporada', methods=['POST'])
@teste_token
def criar_temp(usuario_atual):
    temp = request.json
    comando = f"INSERT INTO Temporada (titulo_id, temporada_nome, temporada_desc) VALUES ('{temp['titulo_id']}','{temp['nome']}','{temp['descricao']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Temporada cadastrada com sucesso', temporada=temp))
@app.route('/temporada', methods=['DELETE'])
@teste_token
def del_temporada(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Temporada WHERE temporada_id={indice}")
        temporada = cursor.fetchone()
        print(temporada)
        if type(temporada) != None:
            comando = f"DELETE FROM Temporada WHERE temporada_id={temporada[1]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Temporada deletada com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar temporada.' + f'temporada={indice}' + ' não existe'),500)
@app.route('/titulo_genero', methods=['GET'])
@teste_token
def get_titulo_genero(usuario_atual):
    cursor.execute('SELECT * FROM Titulo_Genero')
    tds_t_g = cursor.fetchall()
    t_g = list()
    for tit_gen in tds_t_g:
        t_g.append(
            {
                'titulo_id': tit_gen[0],
                'genero_id': tit_gen[1]
            }
        )
    return make_response(jsonify(mensagem='Lista de Titulo_Genero:', t_g=t_g))
@app.route('/titulo_genero', methods=['POST'])
@teste_token
def criar_titulo_genero(usuario_atual):
    tit_gen = request.json
    comando = f"INSERT INTO Titulo_Genero (titulo_id, genero_id) VALUES ('{tit_gen['titulo_id']}','{tit_gen['genero_id']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Titulo_Genero cadastrado com sucesso', t_g=tit_gen))
@app.route('/titulo_genero', methods=['DELETE'])
@teste_token
def del_titulo_genero(usuario_atual):
    indice = request.json
    print(indice)
    print(type(indice))
    indice1 = str(indice['titulo_id'])
    print(indice1)
    indice2 = str(indice['genero_id'])
    print(indice2)
    try:
        cursor.execute(f"SELECT * FROM Titulo_Genero WHERE titulo_id={indice1} and genero_id={indice2}")
        tit_gen = cursor.fetchone()
        if type(tit_gen) != None:
            comando = f"DELETE FROM Titulo_Genero WHERE titulo_id={tit_gen[0]} and genero_id={tit_gen[1]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Titulo_Genero deletado com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar titulo_genero.' + f'tit_gen={indice1}_{indice2}' + ' não existe'),500)
@app.route('/usuario', methods=['GET'])
@teste_token
def get_usuarios(usuario_atual):
    cursor.execute('SELECT * FROM Usuario')
    tds_usuarios = cursor.fetchall()
    usuarios = list()
    for usuario in tds_usuarios:
        usuarios.append(
            {
                'id': usuario[0],
                'email': usuario[1],
                'username': usuario[2],
                'senha': usuario[3],
                'newsletter': usuario[4]
            }
        )
    return make_response(jsonify(mensagem='Lista de usuários:', usuario=usuarios))
@app.route('/usuario', methods=['POST'])
@teste_token
def criar_usuario(usuario_atual):
    usuario = request.json
    comando = f"INSERT INTO Usuario (usuario_email, usuario_username, usuario_senha, usuario_recebe_news) VALUES ('{usuario['email']}','{usuario['username']}','{usuario['senha']}','{usuario['newsletter']}')"
    cursor.execute(comando)
    banco.commit()
    return make_response(jsonify(mensagem='Usuário cadastrado com sucesso', usuario=usuario))
@app.route('/usuario', methods=['DELETE'])
@teste_token
def del_usuario(usuario_atual):
    indice = request.json
    indice = str(indice['id'])
    try:
        cursor.execute(f"SELECT * FROM Usuario WHERE usuario_id={indice}")
        usuario = cursor.fetchone()
        if type(usuario) != None:
            comando = f"DELETE FROM Usuario WHERE usuario_id={usuario[0]}"
            cursor.execute(comando)
            banco.commit()
        return make_response(jsonify(status='Ok', mensagem='Usuário deletado com sucesso'))
    except:
        return make_response(jsonify(status='Erro', mensagem='Erro ao deletar usuário.' + f'usuario={indice}' + ' não existe'),500)

app.run()