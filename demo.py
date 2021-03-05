import streamlit as st
import pandas as pd

protocolo_json = {
    'start':{
        'padre':"",
        "tipo": "pregunta",
        "pregunta": "Sintoma principal",
        'respuestas': {
            "Fiebre": "fiebre",
            "Masa en el cuello": "masa cervical",
            "Dolor de cabeza": "cefalea",
            "Tos y mocos": "catarro",
            "Diarrea": "diarrea",
            "Vómitos": "vomitos"
        },
    },

    'fiebre': {
        'padre': "start",
        "tipo": "formulario"
    },

    'masa cervical': {
        'padre': "start",
        "tipo": "formulario"
    },

    'cefalea': {
        'padre': "start",
        "tipo": "formulario"
    },

    'catarro': {
        'padre': "start",
        "tipo": "formulario"
    },

    'diarrea': {
        'padre': "start",
        "tipo": "formulario"
    },

    'vomitos': {
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
            'Presenta una enfermedad crónica': 'Enfermedades',
            'Tiene tratamiento de base': 'tto_base'

        },
        'selectbox':{
            'Episodios de bronquiolitis/broncoespasmo': ['No',
                                                         'Un único episodio de bronquiolitis',
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
            'Se mueve al sacar la lengua o aguantar la respiración': 'desplaza con valsalva',
            'Duele al masticar' : 'dolor al comer',
            'Tiene la boca seca': 'sequedad de boca',
            'Ha presentado lo mismo otras veces': 'episodios previos',
            'Fiebre': 'fiebre',
            'Ha perdido peso': 'perdida de peso',
            'Suda por las noches': 'sudoracion nocturna',
            'Dificultad para respirar': 'disnea',
            'Dolor al tragar': 'odinofagia',
            'Perdida de oido': 'pérdida audición',
            'Está afónico': 'afonía',
            'Vómitos': 'vómitos',
            'Ojos salidos hacia fuera': 'exoftalmos',
            'Secreción por la nariz': 'secrecion nasal',
            'Madre con Enf. Graves': 'AF de Graves'
        },

        'selectbox': {
            'Localización': ['Ángulo de la mandibula', 'Zona media superior',
                             'Zona media inferior', 'Triángulo anterior',
                             'Triángulo posterior', 'Esternocleidomastoideo'],
            'Ha recibido medicación': ['No', 'Si, Litio', 'Si, anticolinérgicos',
                                       'Si, antihistamínicos', 'Si, yoduros', 'Si, amiodarona',
                                       'Si, varios de los anteriores']
        }
    }
}




#FUNCIONES PARA LA RECOGIDA DE VALORES
def numerico (json, nodo_name):
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
    resultados = pd.DataFrame(rspss, preg)
    return resultados


def selectbox(json, nodo_name):
    sintoma_guia = json.get(nodo_name)
    preguntas_select = sintoma_guia.get('selectbox')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_select.keys():
        # Recogemos valores máximo y minimo para el rango
        max_min = list(preguntas_select.get(pregunta))
        preg.append(pregunta)
        rspss.append(st.selectbox(
            pregunta, list(preguntas_select.get(pregunta))))
    resultados = pd.DataFrame(rspss, preg)
    return resultados


def checkbox(json, nodo_name):
    sintoma_guia = json.get(nodo_name)
    preguntas_check = sintoma_guia.get('checkbox')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_check.keys():
        preg.append(preguntas_check.get(pregunta))
        rspss.append(st.checkbox(pregunta))
    resultados = pd.DataFrame(rspss, preg)
    return resultados





#FUNCIONES PRINCIPALES
def inicio(respuestas = [], protocolo_json=protocolo_json):
    nodo = protocolo_json.get('start')

    #ANTECEDENTES
    antecedente()

    #SÍNTOMAS GUIA
    st.write()
    respuestas = respuestas + [st.selectbox(nodo.get("pregunta"), ['none'] + list(nodo.get("respuestas").keys()))]

    if respuestas[len(respuestas) - 1] != 'none':
        st.write()
        formulario(nodo.get("respuestas").get(respuestas[len(respuestas) - 1]))

    st.write('¿Quieres añadir una foto?')
    #Añadir funcion de subir foto


def antecedente():
    st.write('Rellena tus antecedentes')

    respuestas = checkbox(antecedentes, 'primarios')
    respuestas = pd.concat([respuestas, selectbox(antecedentes, 'primarios')],axis=0)

    lactante = respuestas.iat[1,0]
    # Edad
    if lactante:
        edad = st.slider('Edad (Meses)', 0, 24)
    else:
        edad = st.slider('Edad (Años)', 2, 18)

    enfermedades_cronicas = respuestas.iat[6,0]
    if enfermedades_cronicas:
       que_enfermedades = st.text_input('Describe sus enfermedades')

    otros_antecedentes = st.text_input('Rellena otros datos de interés si lo crees necesario')

    #Faltaría de recoger en el dataFrame la edad y las enfermedades y otros antecedentes
    st.write(respuestas)



def formulario (nodo_name):
    st.write('Responda a las siguientes cuestiones')
    st.write()

    sintoma_guia = formularios.get(nodo_name)
    resultados = pd.DataFrame()

    # Según si es bool o numérico se hace una cosa u otra
    for tipo_pregunta in sintoma_guia.keys():

        # Recogemos el tipo de pregunta
        tipo = sintoma_guia.get(tipo_pregunta)

        #Si tipo bool
        if (tipo_pregunta == 'checkbox'):
            resultados = pd.concat([resultados, checkbox(formularios, nodo_name)], axis=0)

        # Si tipo selectbox
        elif (tipo_pregunta == 'selectbox'):
            resultados = pd.concat([resultados, selectbox(formularios, nodo_name)], axis=0)

        # Si tipo numerico
        elif (tipo_pregunta == 'num'):
            resultados = pd.concat([resultados, numerico(formularios, nodo_name)], axis=0)

    comentario = st.text_input('¿Quieres añadir más información?')
    st.write(resultados)
    st.write(comentario)



inicio(respuestas = [], protocolo_json=protocolo_json)