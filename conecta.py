import base64
import cv2
import mysql.connector
import numpy as np
import face_recognition
import os

def conectaBD(comandoSql):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()

    # Insere o registro no banco de dados
    comando = comandoSql
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()


def conectaBDretorno(comandoSql):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    # Executa o comando SQL
    comando = comandoSql
    cursor.execute(comando)
    # Obtém os resultados
    retorno = cursor.fetchone()
    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()
    return retorno


def conectaBDAll(comandoSql):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    # Executa o comando SQL
    comando = comandoSql
    cursor.execute(comando)
    # Obtém os resultados
    retorno = cursor.fetchall()
    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()
    return retorno












