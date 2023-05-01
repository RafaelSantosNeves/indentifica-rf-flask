import cv2
import face_recognition
from baseBd import quantidadeUser
from baseBd import nomeUser
from baseBd import imagemUser
import mysql.connector

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

def gen_frames():
    # Inicialize a câmera
    cap = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    for i in range(quantidadeUser()):

            # Armazene as codificações de rosto de todas as imagens conhecidas
        known_face_encodings.append(imagemUser(i))
        known_face_names.append(nomeUser(i)[0])
        print(i)

    # import datetime

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

            while True:
                # Se o rosto corresponder a um rosto conhecido
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index -1]
                    # print(matches.index(True))
                    # presença(name)
                    # known_face_encodings.pop(first_match_index -1)
                    # known_face_names.pop(first_match_index -1)



            # Desenhe um retângulo em volta do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Adicione um rótulo com o nome abaixo do retângulo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom),(0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




import cv2
import face_recognition
from baseBd import quantidadeUser
from baseBd import nomeUser
from baseBd import imagemUser
import mysql.connector

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

def gen_frames():
    # Inicialize a câmera
    cap = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    for i in range(quantidadeUser()):

            # Armazene as codificações de rosto de todas as imagens conhecidas
        known_face_encodings.append(imagemUser(i))
        known_face_names.append(nomeUser(i)[0])
        print(i)

    # import datetime

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

    count = 0
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
                first_match_index = matches.index(True)
                print(known_face_names)
                if first_match_index < len(known_face_names):
                    name = known_face_names[first_match_index]
                    known_face_encodings.pop(first_match_index)
                    known_face_names.pop(first_match_index)
                else:
                    name = "Unknown"

            # Desenhe um retângulo em volta do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Adicione um rótulo com o nome abaixo do retângulo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


import cv2
import face_recognition
from baseBd import quantidadeUser
from baseBd import nomeUser
from baseBd import imagemUser
import mysql.connector

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

def gen_frames():
    # Inicialize a câmera
    cap = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    for i in range(quantidadeUser()):
        # Armazene as codificações de rosto de todas as imagens conhecidas
        known_face_encodings.append(imagemUser(i))
        known_face_names.append(nomeUser(i)[0])
        print(i)

    # Variáveis para controlar o número de vezes que um rosto foi reconhecido e o índice do último rosto reconhecido
    count = 0
    last_recognized_index = None

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
                first_match_index = matches.index(True)
                first_match_index = first_match_index -1
                name = known_face_names[first_match_index]

                # Se o rosto reconhecido é o mesmo que o último rosto reconhecido
                if first_match_index == last_recognized_index:
                    # Incrementa o contador de reconhecimento
                    count += 1
                else:
                    # Reseta o contador de reconhecimento e atualiza o índice do último rosto reconhecido
                    count = 1
                    last_recognized_index = first_match_index

                # Se o rosto foi reconhecido 10 vezes, exclua-o
                if count == 10:
                    if first_match_index < len(known_face_names):
                        name = known_face_names[first_match_index]
                        known_face_encodings.pop(first_match_index)
                        known_face_names.pop(first_match_index)
                        break
                    else:
                        name = "Unknown"

                    # Reseta o contador de reconhecimento e o índice do último rosto reconhecido
                    count = 0
                    last_recognized_index = None

            # Desenhe um retângulo em volta do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Adicione um rótulo com o nome abaixo do retângulo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(name), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
