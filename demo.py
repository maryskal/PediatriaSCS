import streamlit as st

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
        'Tiempo de fiebre': ['1d', '2d'],
        'Temperatura maxima': ['38','39','40'],
        'Mocos y tos':['si', 'no'],
        'Vomitos':['si', 'no']
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
        form = formularios.get(nodo_name)
        rspss = list()
        preg = list()
        for pregunta in form.keys():
            preg.append(pregunta)
            rspss.append(st.selectbox(
                pregunta,
                ['none'] + list(form.get(pregunta))
            ))
        st.write(preg)
        st.write(rspss)

funcion_protocolo(respuestas = [], nodo_name="start", protocolo_json=protocolo_json)