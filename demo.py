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
        'bool':{
        'Mocos y tos': ['si', 'no'],
        'Vomitos': ['si', 'no']
        },

        'num':{
        'Tiempo de fiebre (horas)': [1,120],
        'Temperatura maxima (ºC)': [37.0,42.0]
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

    elif tipo == 'final':
        st.write('Con esta informacion se recomienda que')

    elif tipo == 'formulario':
        sintoma_guia = formularios.get(nodo_name)
        rspss = list()
        preg = list()

        #Según si es bool o numérico se hace una cosa u otra
        for tipo_pregunta in sintoma_guia.keys():

            #Recogemos el tipo de pregunta
            tipo = sintoma_guia.get(tipo_pregunta)

            #Si tipo bool
            if(tipo_pregunta == 'bool'):
                #Recorro todas las preguntas y recojo las respuestas
                for pregunta in tipo.keys():
                    preg.append(pregunta)
                    rspss.append(st.selectbox(
                        pregunta,
                        ['none'] + list(tipo.get(pregunta))
                    ))
            #Si es tipo numerico
            elif (tipo_pregunta == 'num'):
                # Recorro todas las preguntas
                for pregunta in tipo.keys():
                    #Recogemos valores máximo y minimo para el rango
                    max_min= list(tipo.get(pregunta))
                    preg.append(pregunta)
                    rspss.append(st.slider(
                        pregunta, max_min[0], max_min[1]))


        resultados = pd.DataFrame(rspss, preg)
        st.write(resultados)

funcion_protocolo(respuestas = [], nodo_name="start", protocolo_json=protocolo_json)