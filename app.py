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
from baseBd import usuario
from baseBd import presencaUser
from baseBd import quantidadePresencaUser
from baseBd import id_usuario
from baseBd import deletarUsuario
from baseBd import editUser

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

@app.route('/presenca')
def presenca():
    nome = []
    for i in range(quantidadepresenca(datetime.date.today())):
        # for e in range(2):
        nome.append(checar(datetime.date.today())[i][0])
    return render_template('presenca.html', nome=nome)


@app.route('/presencaUser', methods=['GET'])
def presencaUsers():
    nome = request.args.get('nome')
    data = []
    resultados = presencaUser(nome)
    #faz com que as informaçoes saiam bunitinhas
    #de 2023-05-13
    #para 13/05/2023
    for result in resultados:
        date_obj = result[0]
        date_str = date_obj.strftime('%d/%m/%Y')
        data.append(date_str)

    return render_template('presencaUser.html', nome=nome, data=data)



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

@app.route('/cadastro')
def cadastro():
    primeiro_cadastro = True
    return render_template('cadastro.html', primeiro_cadastro=primeiro_cadastro)

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


@app.route('/editUser', methods=['POST'])
def editUserForm():
    id = int(request.form.get("id"))
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    data = request.form.get("data")
    return render_template('editUser.html', id=id, nome=nome, cpf=cpf, data=data)

@app.route('/usuarioDeletado', methods=['GET'])
def usuariosForm():
    urlExclui = True
    id = request.args.get('excluir')
    userDeletado = deletarUsuario(id)
    usuarios = usuario()
    return render_template('usuarios.html', usuarios=usuarios, userDeletado=userDeletado, urlExclui=urlExclui)

@app.route('/usuarios')
def usuarios():
    usuarios = usuario()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuariosEdit', methods=['POST'])
def usuariosEdit():
    urlEdit = True
    id = int(request.form.get("id"))
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    data_nascimento: int = int(request.form.get('data_nascimento').replace('-', ''))
    imagem = request.files['image']
    #o os com o app.config pega a onde esta setado no UPLOAD_FOLDER a pasta pra salvar a imagem temporariamente
    caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
    imagem.save(caminho_imagem)
    userEditado = editUser(id,nome, cpf, data_nascimento, caminho_imagem)
    usuarios = usuario()
    return render_template('usuarios.html', usuarios=usuarios, urlEdit=urlEdit, userEditado=userEditado)

if __name__=='__main__':
    app.run(debug=True)
