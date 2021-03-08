import streamlit as st
import pandas as pd
import json as js
import copy
import shutil
import os

#Cargo los json
with open('protocolo_json.json') as file:
    protocolo_json = js.load(file)

with open('formularios.json') as file:
    formularios = js.load(file)


# FUNCIONES PARA LA RECOGIDA DE VALORES
def numerico (json, nodo_name): # Se introduce un json y el nombre de un nodo
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



def selectbox(json, nodo_name, default=None):
    sintoma_guia = json.get(nodo_name)
    preguntas_select = sintoma_guia.get('selectbox')

    respuestas_al_formulario = list()
    preguntas_del_formulario = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_select.keys():
        #Para que se añada cada respuesta posible del selectbox con True o False
        respuestas_a_pregunta = list()
        bool_respuestas_a_pregunta = list()

        #Se guardan todas las opciones como false
        for x in list(preguntas_select.get(pregunta)):
            respuestas_a_pregunta.append(x)
            bool_respuestas_a_pregunta.append(False)

        #Se comprueba la respuesta seleciconada
        if default is not None:
            respuesta_seleccionada = default.get(pregunta)
            #Miramos que indice es la respuesta seleccionada para dejarlo marcado predeterminado
            for z in range(len(list(preguntas_select.get(pregunta)))):
                if list(preguntas_select.get(pregunta))[z] == respuesta_seleccionada:
                    index = z
            respuesta_seleccionada=st.selectbox(pregunta, list(preguntas_select.get(pregunta)), z)

        else:
            respuesta_seleccionada=st.selectbox(pregunta, list(preguntas_select.get(pregunta)))

        #La respuesta seleccionada se cambia de False a True
        for z in range(len(list(preguntas_select.get(pregunta)))):
            if list(preguntas_select.get(pregunta))[z] == respuesta_seleccionada:
                bool_respuestas_a_pregunta[z] = True

        #Se guarda tb como antes
        preguntas_del_formulario.append(pregunta)
        respuestas_al_formulario.append(respuesta_seleccionada)

        #Se añaden todas las opciones con su correspondiente valor (true o false) al formulario
        preguntas_del_formulario = preguntas_del_formulario + respuestas_a_pregunta
        respuestas_al_formulario = respuestas_al_formulario + bool_respuestas_a_pregunta

    return crear_diccionario(preguntas_del_formulario, respuestas_al_formulario) #Esta función está definida más adelante



def checkbox(json, nodo_name, default=None):
    sintoma_guia = json.get(nodo_name)
    preguntas_check = sintoma_guia.get('checkbox')

    rspss = list()
    preg = list()

    # Recorro todas las preguntas
    for pregunta in preguntas_check.keys():
        preg.append(preguntas_check.get(pregunta))
        if default is not None:
            rspss.append(st.checkbox(pregunta, value=default.get(preguntas_check.get(pregunta))))
        else:
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
    return(archivo)


#Crea un archivo json con el objeto json introducido
def guardar_json (nombre_archivo, archivo_json, usuario):
    with open("usuarios/" + usuario + "/" + nombre_archivo+'.json', 'w') as file:
        js.dump(archivo_json, file, indent=4)



#FUNCIONES PRINCIPALES
def inicio(respuestas = [], protocolo_json=protocolo_json):
    nodo = protocolo_json.get('start')
    usuario = st.text_input('Introduce tu identificador')
    if len(usuario) > 4:
        crear_carpeta(usuario)
        #ANTECEDENTES
        st.title('ANTECEDENTES')
        antecedente(usuario)

        #SÍNTOMAS GUIA
        st.write()
        st.title('SÍNTOMA PRINCIPAL')
        respuestas = respuestas + [st.selectbox(nodo.get("pregunta"), ['none'] + list(nodo.get("respuestas").keys()))]
        if respuestas[len(respuestas) - 1] != 'none':
            st.write()
            formulario(nodo.get("respuestas").get(respuestas[len(respuestas) - 1]), usuario)

        if st.checkbox('¿Quieres añadir una foto?'):
            upload_image(usuario, respuestas[len(respuestas) - 1], n_images=1)
        #Añadir funcion de subir foto


def crear_carpeta(usuario):
    directorio = "./usuarios/" + str(usuario) + "/"
    try:
        os.stat(directorio)
    except:
        os.mkdir(directorio)


def upload_image(usuario, sintoma, n_images):
    imagenak_ = {}
    for i in range(n_images):
        img_name = sintoma + str(i) # aqui se puede poner para que eliga un nombre
        imagenak_[img_name] = st.file_uploader(img_name)
        if st.button('Save ' + img_name):
            # crear_carpeta(jasotzeko_balorek[0])
            im_to_save = copy.copy(imagenak_[img_name])
            im_path = "./usuarios/" + usuario + "/" +  img_name + ".png"
            with open(im_path, 'wb') as f:
                shutil.copyfileobj(im_to_save, f, length=131072)


def antecedente(usuario):
    st.write('Rellena tus antecedentes')
    try:
        with open("usuarios/" + usuario + '/antecedentes respuestas.json') as file:
            antecedentes_dic = js.load(file)
    except:
        antecedentes_dic = {}

    #Con esto se muestran todas las preguntas tipo checkbox y se devuelve un diccionario (ver funcion)
    antecedentes_dic.update(checkbox(formularios, 'antecedentes', antecedentes_dic))
    if antecedentes_dic is not None:
        fecha_nacimiento = st.text_input('Fecha nacimiento:', antecedentes_dic.get('Fecha nacimiento'))
    else:
        fecha_nacimiento = st.text_input('Fecha nacimiento:')

    #Con esto se muestran todas las preguntas tipo selectbox y se devuelve un diccionario (ver funcion)
    antecedentes_dic.update(selectbox(formularios, 'antecedentes', antecedentes_dic))

    #Se recoge como es la variable enfermedades del diccionario y según eso se pregunta o no cuales son esas enfermedades
    enfermedades_cronicas = antecedentes_dic.get('enfermedades')
    que_enfermedades = ''
    if enfermedades_cronicas:
        if antecedentes_dic is not None:
            que_enfermedades = st.text_input('Describe sus enfermedades', antecedentes_dic.get('Describe sus enfermedades'))
        else:
            que_enfermedades = st.text_input('Describe sus enfermedades')

    #Se recoge como es la variable tto_base del diccionario y según eso se pregunta o no cual es el tto
    tto_base = antecedentes_dic.get('tto base')
    que_tto_base = ''
    if tto_base:
        if antecedentes_dic is not None:
            que_tto_base = st.text_input('¿Que tratamiento de base tiene?', antecedentes_dic.get('¿Que tratamiento de base tiene?'))
        else:
            que_tto_base = st.text_input('¿Que tratamiento de base tiene?')

    #Texto libre para otros antecedentes
    if antecedentes_dic is not None:
        otros_antecedentes = st.text_input('Rellena otros datos de interés si lo crees necesario',
                                     antecedentes_dic.get('Rellena otros datos de interés si lo crees necesario'))
    else:
        otros_antecedentes = st.text_input('Rellena otros datos de interés si lo crees necesario')

    #Se crean un nuevo diccionaro con los nuevos datos y se añade a antedecentes
    otros = {'Fecha nacimiento': fecha_nacimiento, 'Describe sus enfermedades': que_enfermedades, '¿Que tratamiento de base tiene?': que_tto_base,
             'Rellena otros datos de interés si lo crees necesario': otros_antecedentes}
    antecedentes_dic.update(otros)

    st.write(antecedentes_dic)
    #Creamos un archivo json con el diccionario (ver funcion)
    guardar_json('antecedentes respuestas', antecedentes_dic, usuario)



def formulario (nodo_name, usuario):
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

    #st.write(sintomas_dic)
    guardar_json(nodo_name + ' respuestas', sintomas_dic, usuario)



inicio(respuestas = [], protocolo_json=protocolo_json)