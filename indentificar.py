import cv2
import face_recognition
from baseBd import quantidadeUser
from baseBd import nomeUser
from baseBd import imagemUser
import mysql.connector
from baseBd import id_usuario
import datetime
from baseBd import presenca
from baseBd import imagemUserAtivo


def nomeUser(posicao: int):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='projetotcc'
    )
    cursor = conexao.cursor()
    comando = f'SELECT nome FROM alunos_cadastrados WHERE ativo = 1 LIMIT 1 OFFSET {posicao}'
    cursor.execute(comando)
    nome = cursor.fetchone()
    return nome

def gen_frames():
    # Inicialize a câmera
    cap = cv2.VideoCapture(0)

    #cria os arreys pra que de pra fazer append neles no for
    known_face_encodings = []
    known_face_names = []

    for i in range(quantidadeUser()):

        # Armazene as codificações de rosto de todas as imagens conhecidas
        if imagemUserAtivo(i) != None:
            known_face_encodings.append(imagemUser(i))
            known_face_names.append(nomeUser(i)[0])

    # def pode_executar():
    #     # Verifica se a hora atual está entre 1:30 pm e 5:00 pm
    #     now = datetime.datetime.now().time()
    #     start_time = datetime.time(hour=13, minute=30)
    #     end_time = datetime.time(hour=17)
    #
    #     if now < start_time or now >= end_time:
    #         nahora = False
    #         return nahora
    #     else:
    #         nahora = True
    #         return nahora
    # while pode_executar():

    # Variáveis para controlar o número de vezes que um rosto foi reconhecido e o índice do último rosto reconhecido
    count = 0
    first_match_index = None
    presentes = []

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Converte o frame para a escala de cores de BGR para RGB
        rgb_frame = frame[:, :, ::-1]

        # Encontre todas as faces e as codificações de rosto no frame atual
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)



        # Loop sobre cada face e as codificações de rosto
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare o rosto desconhecido com todos os rostos conhecidos
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # Se o rosto corresponder a um rosto conhecido
            if True in matches:
                if first_match_index == matches.index(True):
                    # Incrementa o contador de reconhecimento
                    count += 1
                else:
                    count = 0
                if count == 5:

                    #se o nome do known_face_names[first_match_index] estiver no arrye presença faça
                    if known_face_names[first_match_index] not in presentes:
                        #abre o SQL e registra uma presença
                        presenca(datetime.date.today(), id_usuario(known_face_names[first_match_index])[0])

                    #adiciona o nome do known_face_names[first_match_index] pra que ele n seja registrado duas vezes no SQL
                    presentes.append(known_face_names[first_match_index])

                #pega a posição que esta a nos arrey knowns que esta sendo indentificado na tela
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print(known_face_names[first_match_index])


            # Desenhe um retângulo em volta do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Adicione um rótulo com o nome abaixo do retângulo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom),(0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

