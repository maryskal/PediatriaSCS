import streamlit as st
import pandas as pd
import json as js

protocolo_json = {
    'start':{
        'padre':"",
        "tipo": "pregunta",
        "pregunta": "¿Que te sucede?",
        'respuestas': {
            "Fiebre": "fiebre",
            "Masa en el cuello": "masa cervical"
        },
    },

    'fiebre': {
        'padre': "start",
        "tipo": "formulario"
    },

    'masa cervical': {
        'padre': "start",
        "tipo": "formulario"
    }

}

antecedentes = {
    'primarios':{
        'checkbox':{
            'Fue prematuro': 'prematuridad',
            'Lactante (< 2 años)': 'lactante',
            'Tiene dermatitis atópica': 'dermatitis atopica',
            'El padre o la madre tuvieron o tienen asma o alergias': 'AF atopia',
            'Presenta alguna alergia': 'alergias',
            'Tiene el calendario vacunal al día o casi al día': 'vacunas',
            'Presenta una enfermedad crónica': 'enfermedades',
            'Tiene tratamiento de base': 'tto base'

        },
        'selectbox':{
            'Episodios de bronquiolitis/broncoespasmo': ['No',
                                                         'Un unico episodio de bronquiolitis',
                                                         'Más de un episodio de bronquiolitis',
                                                         'Más de un episodio y ha precisado inahaladores',
                                                         'Más de un episodio y tiene tratamiento diario'],
        }
    }
}

formularios = {
    'fiebre':{
        'checkbox': {
            'Diarrea': 'Diarrea',
            'Mocos y tos': 'Mocos y tos',
        },

        'selectbox':{
        'Dolor abdominal': ['no', 'leve', 'fuerte'],
        'Vomitos': ['no', 'si, menos de 2 al día', 'si, más de dos al día']
        },

        'num':{
        'Tiempo de fiebre (horas)': [1,120,1],
        'Temperatura maxima (ºC)': [35.0,42.0,0.1]
        }

    },


    'masa cervical': {
        'checkbox': {
            'Es dolorosa': 'dolor',
            'Crece rápido': 'crecimiento rapido',
            'Es dura': 'dura',
            'Se mueve con facilidad': 'no adherida',
            'Se mueve al sacar la lengua o aguantar la respiracion': 'desplaza con valsalva',
            'Duele al masticar' : 'dolor al comer',
            'Tiene la boca seca': 'sequedad de boca',
            'Ha presentado lo mismo otras veces': 'episodios previos',
            'Fiebre': 'fiebre',
            'Ha perdido peso': 'perdida de peso',
            'Suda por las noches': 'sudoracion nocturna',
            'Dificultad para respirar': 'disnea',
            'Dolor al tragar': 'odinofagia',
            'Perdida de oido': 'pérdida audicion',
            'Está afonico': 'afonia',
            'Vómitos': 'vómitos',
            'Ojos salidos hacia fuera': 'exoftalmos',
            'Secreción por la nariz': 'secrecion nasal',
            'Madre con Enf. Graves': 'AF de Graves'
        },

        'selectbox': {
            'Localizacion': ['Angulo de la mandibula', 'Zona media superior',
                             'Zona media inferior', 'Triángulo anterior',
                             'Triángulo posterior', 'Esternocleidomastoideo'],
            'Ha recibido medicacion': ['No', 'Si, Litio', 'Si, anticolinergicos',
                                       'Si, antihistaminicos', 'Si, yoduros', 'Si, amiodarona',
                                       'Si, varios de los anteriores']
        }
    }
}




#FUNCIONES PARA LA RECOGIDA DE VALORES
def numerico (json, nodo_name): #Se introduce un json y el nombre de un nodo
    sintoma_guia = json.get(nodo_name)
    preguntas_numericas = sintoma_guia.get('num')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_numericas.keys():
        # Recogemos valores máximo y minimo para el rango
        max_min_step = list(preguntas_numericas.get(pregunta))
        preg.append(pregunta)
        rspss.append(st.slider(
            pregunta, max_min_step[0], max_min_step[1], step = max_min_step[2]))

    return crear_diccionario(preg, rspss) #Esta función está definida más adelante



def selectbox(json, nodo_name):
    sintoma_guia = json.get(nodo_name)
    preguntas_select = sintoma_guia.get('selectbox')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_select.keys():
        preg.append(pregunta)
        rspss.append(st.selectbox(
            pregunta, list(preguntas_select.get(pregunta))))

    return crear_diccionario(preg, rspss) #Esta función está definida más adelante



def checkbox(json, nodo_name):
    sintoma_guia = json.get(nodo_name)
    preguntas_check = sintoma_guia.get('checkbox')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_check.keys():
        preg.append(preguntas_check.get(pregunta))
        rspss.append(st.checkbox(pregunta))

    return crear_diccionario(preg, rspss) #Esta función está definida más adelante


#FUNCIONES PARA JSON
#Crear un objeto json con las respuestas
def crear_diccionario(lista_1, lista_2):
    archivo = {}

    #Se recorre la lista 1 y se introducen los datos según lista_1 : lista_2
    for i in range(len(lista_1)):
        dic = {lista_1[i]:lista_2[i]}
        archivo.update(dic)
    print(archivo)
    return(archivo)


#Crea un archivo json con el objeto json introducido
def guardar_json (nombre_archivo, archivo_json):
    with open(nombre_archivo, 'w') as file:
        js.dump(archivo_json, file, indent=4)



#FUNCIONES PRINCIPALES
def inicio(respuestas = [], protocolo_json=protocolo_json):
    nodo = protocolo_json.get('start')

    #ANTECEDENTES
    st.title('ANTECEDENTES')
    antecedente()

    #SÍNTOMAS GUIA
    st.write()
    st.title('SÍNTOMA PRINCIPAL')
    respuestas = respuestas + [st.selectbox(nodo.get("pregunta"), ['none'] + list(nodo.get("respuestas").keys()))]
    if respuestas[len(respuestas) - 1] != 'none':
        st.write()
        formulario(nodo.get("respuestas").get(respuestas[len(respuestas) - 1]))

    st.write('¿Quieres añadir una foto?')
    #Añadir funcion de subir foto



def antecedente():
    st.write('Rellena tus antecedentes')

    antecedentes_dic = {}

    #Con esto se muestran todas las preguntas tipo checkbox y se devuelve un diccionario (ver funcion)
    antecedentes_dic.update(checkbox(antecedentes, 'primarios'))
    #Con esto se muestran todas las preguntas tipo selectbox y se devuelve un diccionario (ver funcion)
    antecedentes_dic.update(selectbox(antecedentes, 'primarios'))

    #Se recoge como es la variable lactante del diccionario y según eso se pregunta la edad en meses o en años
    lactante = antecedentes_dic.get('lactante')
    # Edad
    if lactante:
        edad = st.slider('Edad (Meses)', 0, 24)
    else:
        edad = st.slider('Edad (Años)', 2, 18)

    #Se recoge como es la variable enfermedades del diccionario y según eso se pregunta o no cuales son esas enfermedades
    enfermedades_cronicas = antecedentes_dic.get('enfermedades')
    que_enfermedades = ''
    if enfermedades_cronicas:
       que_enfermedades = st.text_input('Describe sus enfermedades')

    #Se recoge como es la variable tto_base del diccionario y según eso se pregunta o no cual es el tto
    tto_base = antecedentes_dic.get('tto base')
    que_tto_base = ''
    if tto_base:
        que_tto_base = st.text_input('¿Que tratamiento de base tiene?')

    #Texto libre para otros antecedentes
    otros_antecedentes = st.text_input('Rellena otros datos de interés si lo crees necesario')

    #Se crean un nuevo diccionaro con los nuevos datos y se añade a antedecentes
    otros = {'edad': edad, 'que enfermedades': que_enfermedades, 'que tto base': que_tto_base,
             'otros antecedentes': otros_antecedentes}
    antecedentes_dic.update(otros)

    st.write(antecedentes_dic)
    #Creamos un archivo json con el diccionario (ver funcion)
    guardar_json('antecedentes respuestas', antecedentes_dic)



def formulario (nodo_name):
    st.subheader('Responda a las siguientes cuestiones')
    st.write()

    #Se recoge el síntomam guia que se ha introducido desde inicio()
    sintoma_guia = formularios.get(nodo_name)

    #Los objetos json que recogen los resultados según el tipo de pregunta que sea (checkbox, selectbox o numerica)
    sintomas_dic = {}

    # Según si es bool o numérico se hace una cosa u otra
    for tipo_pregunta in sintoma_guia.keys():

        #Si tipo checkbox
        if (tipo_pregunta == 'checkbox'):
            sintomas_dic.update(checkbox(formularios, nodo_name))

        # Si tipo selectbox
        elif (tipo_pregunta == 'selectbox'):
            sintomas_dic.update(selectbox(formularios, nodo_name))

        # Si tipo numerico
        elif (tipo_pregunta == 'num'):
            sintomas_dic.update(numerico(formularios, nodo_name))

    comentario = st.text_input('¿Quieres añadir más información?')
    otros = {'otros': comentario}
    sintomas_dic.update(otros)

    st.write(sintomas_dic)
    guardar_json(nodo_name + ' respuestas', sintomas_dic)



inicio(respuestas = [], protocolo_json=protocolo_json)