#importa o flask
import datetime
import os

from flask import Flask, render_template, Response

#cria uma istancia flask e coloca ela na var app
app = Flask(__name__)

#acha o lugar aonde faz o upload da foto para conseguir mandar pro sql
app.config['UPLOAD_FOLDER'] = 'static/imguser'

#impoerta as bibliotecas necessarias
from flask import render_template
from flask import request
from flask import redirect
import cv2
import face_recognition
from baseBd import quantidadeUser
from baseBd import nomeUser
from baseBd import imagemUser
from indentificar import gen_frames
from baseBd import cadastroUser
from baseBd import checar
from baseBd import quantidadepresenca


#cria url e renderiza template html
@app.route('/')
@app.route('/index')
def index():
    return render_template('pgPrincipal.html')

#executa a função gen_frames e renderiza mandando para o arquibo pgPrincipal.html
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login')
def login():
    primeiro_cadastro = True
    return render_template('login.html', primeiro_cadastro=primeiro_cadastro)

@app.route('/presenca')
def presenca():
    nome = []
    for i in range(quantidadepresenca(datetime.date.today().strftime("%Y%m%d"))):
        print(i)
        # for e in range(2):
        nome.append(checar(datetime.date.today().strftime("%Y%m%d"))[i][0])
    print(nome)
    return render_template('presenca.html', nome=nome)


# # Converter a data para uma string no formato "20230428"
# data_atual_str = data_atual.strftime("%Y%m%d")
# print(checar(data_atual_str))

@app.route('/cadastro', methods=['POST'])
def cadastro():
    primeiro_cadastro = False
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    data_nascimento: int = request.form.get('data_nascimento')
    imagem = request.files['image']
    #o os com o app.config pega a onde esta setado no UPLOAD_FOLDER a pasta pra salvar a imagem temporariamente
    caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
    imagem.save(caminho_imagem)
    retorno = cadastroUser(nome, cpf, data_nascimento, caminho_imagem)
    return render_template('login.html', retorno=retorno)

if __name__=='__main__':
    app.run(debug=True)
