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
from baseBd import quantidadeUser
from baseBd import nomeUser
from baseBd import imagemUser
from indentificar import gen_frames
from baseBd import cadastroUser
from baseBd import checar
from baseBd import quantidadepresenca

video = Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


#cria url e renderiza template html
@app.route('/')
@app.route('/index')
def index():
    return render_template('pgPrincipal.html')

#executa a função gen_frames e renderiza mandando para o arquibo pgPrincipal.html
@app.route('/video_feed')
def video_feed():
    return video

@app.route('/cadastro')
def cadastro():
    primeiro_cadastro = True
    return render_template('cadastro.html', primeiro_cadastro=primeiro_cadastro)

@app.route('/presenca')
def presenca():
    nome = []
    for i in range(quantidadepresenca(datetime.date.today())):
        # for e in range(2):
        nome.append(checar(datetime.date.today())[i][0])
    return render_template('presenca.html', nome=nome)

@app.route('/escolha_data')
def escolha_data():
    return render_template('escolha_data.html')


@app.route('/escolha_data', methods=['POST'] )
def escolha_dataForm():
    data = request.form.get('escolha_data')
    nome = []
    for i in range(quantidadepresenca(data)):
        nome.append(checar(data)[i][0])
    return render_template('presenca.html', nome=nome)

@app.route('/cadastro', methods=['POST'])
def cadastroForm():
    primeiro_cadastro = False
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    data_nascimento: int = request.form.get('data_nascimento')
    imagem = request.files['image']
    #o os com o app.config pega a onde esta setado no UPLOAD_FOLDER a pasta pra salvar a imagem temporariamente
    caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
    imagem.save(caminho_imagem)
    retorno = cadastroUser(nome, cpf, data_nascimento, caminho_imagem)
    return render_template('cadastro.html', retorno=retorno)

if __name__=='__main__':
    app.run(debug=True)
