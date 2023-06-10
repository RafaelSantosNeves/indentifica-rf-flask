import base64
import cv2
import mysql.connector
import numpy as np
import face_recognition
import os
from conecta import conectaBD
from conecta import conectaBDretorno


def cadastroUser(nome: str, cpf: str, data_nascimento: int, caminho_imagem):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='projetotcc'
        )
        cursor = conexao.cursor()

        # Codifica imagem em base 64
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        my_string = encoded_string.decode('utf-8')

        # Insere o registro no banco de dados
        comando = f'INSERT INTO alunos_cadastrados (nome, cpf, data_nascimento, foto_aluno) VALUES ("{nome}", "{cpf}", "{data_nascimento}", "{my_string}")'
        cursor.execute(comando)
        conexao.commit()
        cursor.close()
        conexao.close()

        # Exclui arquivo da pasta UPLOAD_FOLDER
        os.remove(caminho_imagem)

        return True
    except:
        return False

def presenca(data: int, id_aluno: int, presenca = 1):

    # Insere o registro no banco de dados
    comando = f'INSERT INTO data (data, id_aluno, presente) VALUES ("{data}", "{id_aluno}", "{presenca}")'
    conectaBD(comando)


def checar(data):
    comando = f"SELECT alunos_cadastrados.nome, data.data, data.presente FROM alunos_cadastrados LEFT JOIN data ON alunos_cadastrados.id = data.id_aluno AND data.data = '{data}' WHERE data.data IS NOT NULL"
    resultados = conectaBDretorno(comando)
    return resultados


def id_usuario(nome):
    comando = f"SELECT id FROM alunos_cadastrados WHERE nome = '{nome}'"
    id = conectaBDretorno(comando)
    return id


def usuario():
    comando = f"SELECT nome, cpf, data_nascimento FROM alunos_cadastrados"
    id = []
    id.append(conectaBDretorno(comando))
    return id


def imagemUser(posicao: int):
    comando = f'SELECT foto_aluno FROM alunos_cadastrados LIMIT 1 OFFSET {posicao}'
    imagemDocumento = conectaBDretorno(comando)
    decodificaString = base64.b64decode(imagemDocumento[0])
    processoImagem = np.frombuffer(decodificaString, np.uint8)
    imagem = cv2.imdecode(processoImagem, cv2.IMREAD_COLOR)
    imagemFinal =face_recognition.face_encodings(imagem)[0]
    return imagemFinal


def nomeUser(posicao: int):
    comando = f'SELECT * FROM alunos_cadastrados LIMIT 1 OFFSET {posicao} '
    nome = conectaBDretorno(comando)
    return nome


def quantidadeUser():
    comando = f'SELECT COUNT(*) FROM alunos_cadastrados'
    num_rows = conectaBDretorno(comando)[0]
    return num_rows

def quantidadepresenca(data):
    comando = f'SELECT COUNT(*) FROM data WHERE data = "{data}"'
    num_rows = conectaBDretorno(comando)[0]
    return int(num_rows)


print(quantidadepresenca("2023-05-13"))


























import base64
import cv2
import mysql.connector
import numpy as np
import face_recognition
import os
from conecta import conectaBD
from conecta import conectaBDretorno


def cadastroUser(nome: str, cpf: str, data_nascimento: int, caminho_imagem):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='projetotcc'
        )
        cursor = conexao.cursor()

        # Codifica imagem em base 64
        with open(caminho_imagem, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        my_string = encoded_string.decode('utf-8')

        # Insere o registro no banco de dados
        comando = f'INSERT INTO alunos_cadastrados (nome, cpf, data_nascimento, foto_aluno) VALUES ("{nome}", "{cpf}", "{data_nascimento}", "{my_string}")'
        cursor.execute(comando)
        conexao.commit()
        cursor.close()
        conexao.close()

        # Exclui arquivo da pasta UPLOAD_FOLDER
        os.remove(caminho_imagem)

        return True
    except:
        return False

def presenca(data: int, id_aluno: int, presenca = 1):

    # Insere o registro no banco de dados
    comando = f'INSERT INTO data (data, id_aluno, presente) VALUES ("{data}", "{id_aluno}", "{presenca}")'
    conectaBD(comando)


import mysql.connector


def checar(data):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    # Executar a consulta SQL
    comando = f"SELECT alunos_cadastrados.nome, data.data, data.presente FROM alunos_cadastrados LEFT JOIN data ON alunos_cadastrados.id = data.id_aluno AND data.data = '{data}' WHERE data.data IS NOT NULL"
    cursor.execute(comando)
    # Recuperar os resultados
    resultados = cursor.fetchall()
    # Fechar a conexão com o banco de dados
    cursor.close()
    conexao.close()
    # Retornar os resultados
    return resultados


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


def usuario():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    comando = f"SELECT nome, cpf, data_nascimento FROM alunos_cadastrados"
    cursor.execute(comando)
    id = []
    id.append(cursor.fetchone())
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
    comando = f'SELECT * FROM alunos_cadastrados LIMIT 1 OFFSET {posicao} '
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


print(quantidadepresenca("2023-05-13"))