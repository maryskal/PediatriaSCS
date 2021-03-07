import streamlit as st
import json as js


#Cargo el json
with open('formularios.json') as file:
    diccionario = js.load(file)


def main():
    st.title('Introduce los datos de cada tipo de sintoma')

    st.write()
    st.subheader('SÍNTOMA PRINCIPAL')
    sintoma = st.text_input('Introduce el síntoma', "")
    print(sintoma)

    if sintoma != "":
        diccionario.update(introducir_signos(sintoma))

    with open('formularios.json', 'w') as file:
        js.dump(diccionario, file, indent=4)



def introducir_signos(signo):
    st.subheader('Tienes que elegir cuantas preguntas va a haber de cada tipo')

    st.subheader('CHECKBOX')
    n_check = st.number_input('Tipo checkbox',0)
    signos_check = {}
    for i in range(n_check):
        st.write('Sintoma '+ str(i))
        a = st.text_input('Como deseas realizar la pregunta '+ str(i))
        b = st.text_input('Nombre del sintoma ' + str(i))
        signos_check.update({a:b})
        st.write()

    st.sidebar.subheader('DESPLEGABLE')
    n_desplegable = st.number_input('Tipo desplegable',0)
    signos_desplegable = {}
    for i in range(n_desplegable):
        st.write('Sintoma ' + str(i))
        a = st.text_input('Nombre del desplegable ' + str(i))
        n_opciones = st.number_input('Numero de opciones que puede tomar '+ str(i), 3)
        opciones = []
        for j in range(n_opciones):
            b = st.text_input('Opcion ' + str(i) + ','+ str(j))
            opciones.append(b)
        signos_desplegable.update({a:opciones})
        st.write()

    st.subheader('RESPUESTA NUMÉRICA')
    n_number = st.number_input('Tipo numerico',0)
    signos_number = {}
    for i in range(n_number):
        st.write('Sintoma ' + str(i))
        a = st.text_input('Pregunta numerica ' + str(i))
        b = st.text_input('minimo valor que puede tomar ' + str(i))
        c = st.text_input('maximo valor que puede tomar ' + str(i))
        signos_number.update({a:[b,c]})
        st.write()

    diccionario = {signo:{'checkbox': signos_check, 'selectbox':signos_desplegable, 'num': signos_number}}
    return diccionario




main()