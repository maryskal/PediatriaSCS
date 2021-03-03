import streamlit as st
protocolo_json = {
    'start':{
        'padre':"",
        "tipo":"pregunta",
        "pregunta": "¿Sintoma principal?",
        'respuestas': {
            "Tengo fiebre": "fiebre",
            "Dolor abdominal": "abdominal"
        },
    },
    'fiebre': {
        'padre': "start",
        "tipo": "formulario"
    },
    'cabeza':{
        'padre':"start",
        "tipo":"pregunta",
        "pregunta": "¿Te mareas al levantarte rapido?",
        'respuestas': {
            "Si": "mareo_si",
            "No": "mareo_no"
        },
    },
    'hombro': {
        'padre': "start",
        "tipo": "pregunta",
        "pregunta": "¿Que parte del cuerpo te duele?",
        'respuestas': {
            "cabeza": "cabeza",
            "hombro": "hombro",
            "pie": "pie",
            "piel": "piel"
        },
    },
    'pie': {
        'padre': "start",
        "tipo": "pregunta",
        "pregunta": "¿Que parte del cuerpo te duele?",
        'respuestas': {
            "cabeza": "cabeza",
            "hombro": "hombro",
            "pie": "pie",
            "piel": "piel"
        },
    },
    'piel': {
        'padre': "start",
        "tipo": "foto"
    },
    'mareo_si': {
        'padre': "start",
        "tipo": "foto"
    },
    'mareo_no': {
        'padre': "start",
        "tipo": "foto"
    },
    'final':{
        'tipo':'final'
    }
}

formularios = {
    'fiebre':{
        'Tiempo de fiebre':['1d', '2d'],
        'Temperatura maxima': ['38','39','40'],
        'Mocos y tos':['si', 'no'],
        'Vomitos':['si', 'no']
    }
}
def funcion_protocolo(respuestas = [], nodo_name="start", protocolo_json=protocolo_json):
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
        form = formularios.get(nodo_name)
        rspss = list()
        for pregunta in form.keys():
                rspss.append(st.selectbox(
                    pregunta,
                    ['none'] + list(form.get(pregunta))
                )
            )
        st.write(rspss)

funcion_protocolo(respuestas = [], nodo_name="start", protocolo_json=protocolo_json)