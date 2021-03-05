import streamlit as st
import pandas as pd

protocolo_json = {
    'start':{
        'padre':"",
        "tipo": "pregunta",
        "pregunta": "Sintoma principal",
        'respuestas': {
            "Fiebre": "fiebre",
            "Dolor abdominal": "abdominal",
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

    'abdominal': {
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

formularios = {
    'fiebre':{
        'checkbox': {
            'Diarrea': 'diarrea',
            'Mocos y tos': 'catarro',
        },

        'selectbox':{
        'Dolor abdominal': ['no', 'leve', 'fuerte'],
        'Vomitos': ['no', 'si, menos de 2 al día', 'si, más de dos al día']
        },

        'num':{
        'Tiempo de fiebre (horas)': [1,120,1],
        'Temperatura maxima (ºC)': [35.0,42.0,0.1]
        }

    }
}


def funcion_protocolo(respuestas = [], nodo_name= "start", protocolo_json=protocolo_json):
    nodo = protocolo_json.get(nodo_name)
    tipo = nodo.get('tipo')

    if tipo == "pregunta":
        respuestas = respuestas + [st.selectbox(
            nodo.get("pregunta"),
            ['none'] + list(nodo.get("respuestas").keys())
        )]
        if respuestas[len(respuestas) - 1] != 'none':
            st.write()
            funcion_protocolo(respuestas, nodo_name=nodo.get("respuestas").get(respuestas[len(respuestas) - 1]), protocolo_json=protocolo_json)

    elif tipo == 'foto':
        st.write('Sube la foto XX')
        funcion_protocolo(respuestas + ['Se ha subido la foto'], nodo_name='final', protocolo_json=protocolo_json)

    elif tipo == 'formulario':
        formulario(nodo_name)



def numerico (nodo_name):
    sintoma_guia = formularios.get(nodo_name)
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

def selectbox(nodo_name):
    sintoma_guia = formularios.get(nodo_name)
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

def checkbox(nodo_name):
    sintoma_guia = formularios.get(nodo_name)
    preguntas_check = sintoma_guia.get('checkbox')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_check.keys():
        # Recogemos valores máximo y minimo para el rango
        max_min = list(preguntas_check.get(pregunta))
        preg.append(pregunta)
        rspss.append(st.checkbox(pregunta))
    resultados = pd.DataFrame(rspss, preg)
    return resultados


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
            resultados = pd.concat([resultados, checkbox(nodo_name)], axis=0)

        # Si tipo selectbox
        elif (tipo_pregunta == 'selectbox'):
            resultados = pd.concat([resultados, selectbox(nodo_name)], axis=0)

        # Si tipo numerico
        elif (tipo_pregunta == 'num'):
            resultados = pd.concat([resultados, numerico(nodo_name)], axis=0)

    st.write(resultados)


funcion_protocolo(respuestas = [], nodo_name="start", protocolo_json=protocolo_json)