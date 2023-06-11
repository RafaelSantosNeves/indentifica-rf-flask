import base64
import cv2
import mysql.connector
import numpy as np
import face_recognition
import os
from conecta import conectaBD
from conecta import conectaBDretorno
from conecta import conectaBDAll


def cadastroUser(nome: str, cpf: str, data_nascimento: int, caminho_imagem):
    try:
        # Codifica imagem em base 64
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        my_string = encoded_string.decode('utf-8')

        # Insere o registro no banco de dados
        comando = f'INSERT INTO alunos_cadastrados (nome, cpf, data_nascimento, foto_aluno) VALUES ("{nome}", "{cpf}", "{data_nascimento}", "{my_string}")'
        conectaBD(comando)

        # Exclui arquivo da pasta UPLOAD_FOLDER
        os.remove(caminho_imagem)

        return True
    except:
        return False

def presenca(data: int, id_aluno: int, presenca = 1):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()

    # Insere o registro no banco de dados
    comando = f'INSERT INTO data (data, id_aluno, presente) VALUES ("{data}", "{id_aluno}", "{presenca}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

#essa parate do codigo em especifico n pode fazer parte da funcao pq o cursor dele é fetchall e n fetchone
def checar(data):
    #retorna o quem teve presente no dia que vc coloca na var data
    comando = f"SELECT alunos_cadastrados.nome, data.data, data.presente FROM alunos_cadastrados LEFT JOIN data ON alunos_cadastrados.id = data.id_aluno AND data.data = '{data}' WHERE data.data IS NOT NULL"
    resultados = conectaBDAll(comando)
    # Retornar os resultados
    return resultados

def presencaUser(nome):
    comando = f"SELECT data.data FROM data LEFT JOIN alunos_cadastrados ON alunos_cadastrados.id = data.id_aluno WHERE alunos_cadastrados.nome = '{nome}' AND data.data IS NOT NULL"
    resultados = conectaBDAll(comando)
    return resultados

def quantidadePresencaUser(nome):
    comando = f"SELECT data.data FROM data LEFT JOIN alunos_cadastrados ON alunos_cadastrados.id = data.id_aluno WHERE alunos_cadastrados.nome = '{nome}' AND data.data IS NOT NULL"
    resultados = conectaBDAll(comando)
    quantidade = len(resultados)
    return quantidade



def id_usuario(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    comando = f"SELECT id FROM alunos_cadastrados WHERE nome = '{nome}'"
    cursor.execute(comando)
    id = cursor.fetchone()
    return id

# print(id_usuario("Dirce Mendes"))

def deletarUsuario(id):
    comando = f"UPDATE alunos_cadastrados SET ativo = 0 WHERE id = '{id}'"
    conectaBD(comando)

# deletarUsuario(id_usuario("Dirce Mendes"))

def usuario():
    comando = f"SELECT nome, cpf, data_nascimento FROM alunos_cadastrados WHERE ativo = 1"
    id = conectaBDAll(comando)
    return id

def imagemUser(posicao: int):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    comando = f'SELECT foto_aluno FROM alunos_cadastrados LIMIT 1 OFFSET {posicao}'
    cursor.execute(comando)
    imagemDocumento = cursor.fetchone()
    decodificaString = base64.b64decode(imagemDocumento[0])
    processoImagem = np.frombuffer(decodificaString, np.uint8)
    imagem = cv2.imdecode(processoImagem, cv2.IMREAD_COLOR)
    imagemFinal =face_recognition.face_encodings(imagem)[0]
    cursor.close()
    conexao.close()
    return imagemFinal


def nomeUser(posicao: int):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    comando = f'SELECT nome FROM alunos_cadastrados LIMIT 1 OFFSET {posicao}'
    cursor.execute(comando)
    nome = cursor.fetchone()
    return nome

def quantidadeUser():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    comando = f'SELECT COUNT(*) FROM alunos_cadastrados'
    cursor.execute(comando)
    num_rows = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return num_rows

def quantidadepresenca(data):
    comando = f'SELECT COUNT(*) FROM data WHERE data = "{data}"'
    num_rows = conectaBDretorno(comando)[0]
    return int(num_rows)
