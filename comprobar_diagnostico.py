import json as js
import pandas as pd

with open('diagnosticos.json') as file:
    diagnosticos = js.load(file)



def comprobar_obligatorio (dentro_de_cada_dco, sintomas_del_paciente):
    print('-----------OBLIGATORIOS-----------')
    cumple_obligatoriedad = True

    # Se recorre cada uno de los síntomas obligatorios de ese diagnóstico
    for obligatorios_del_dco in dentro_de_cada_dco.get('obligatorios'):
        print('Síntoma obligatorio: ', obligatorios_del_dco)

        # Cada síntoma del diagnóstico se compara con todos los síntomas recogidos por el paciente
        for sintoma_del_paciente in sintomas_del_paciente.keys():
            # Si el síntoma del diagnóstico coincide con el del paciente comprobamos si el paciente ha marcado ese como true o false
            if (sintoma_del_paciente == obligatorios_del_dco):
                cumple_obligatoriedad = sintomas_del_paciente.get(sintoma_del_paciente)

            #Si en algun momento alguno de los sintomas obligatorios es false finalizamos
            if (cumple_obligatoriedad == False):
                print('nos salimos del bucle -----------------------')
                break

    return cumple_obligatoriedad




def comprobar_sintomas (dentro_de_cada_dco, sintomas_del_paciente):
    print('-----------SINTOMAS ESTANDAR-----------')
    # Aqui se van a recoger los síntomas totales que tiene ese dignósitco y cuantos de ellos coinciden
    sintomas_dco_totales = 0
    sintomas_coincidentes = 0

    #Se recorre cada uno de los síntomas de ese diagnóstico
    for sintomas_del_dco in dentro_de_cada_dco.get('sintomas'):

        print('Síntoma: ', sintomas_del_dco)
        sintomas_dco_totales = sintomas_dco_totales + 1 #Se van sumando el número de síntomas de ese diagnostico
        #Cada síntoma del diagnóstico se compara con todos los síntomas recogidos por el paciente
        for sintoma_del_paciente in sintomas_del_paciente.keys():
            print('Paciente: ', sintoma_del_paciente)

            #Si el síntoma del diagnóstico coincide con el del paciente comprobamos si el paciente ha marcado ese como true o false
            if(sintoma_del_paciente == sintomas_del_dco):
                coincidencia = sintomas_del_paciente.get(sintoma_del_paciente)
                print('COINCIDENCIA: ', coincidencia)

                if coincidencia:
                    sintomas_coincidentes = sintomas_coincidentes + 1

    return sintomas_coincidentes, sintomas_dco_totales
    print('---------------------- \n \n')



def comprobar_diagnosticos(usuario, sintoma_principal):
    print('usuarios/' + usuario + '/' + sintoma_principal + ' respuestas.json')

    #Abrimos el síntoma guia de un usuario
    with open('usuarios/' + usuario + '/' + sintoma_principal + ' respuestas.json') as file:
        sintomas_del_paciente = js.load(file)

    print(sintomas_del_paciente)

    #Recogemos todos los diagnósticos posibles que puede tener ese síntoma guía
    diagnosticos_posibles = diagnosticos.get(sintoma_principal)


    #Aqui recogeremos los resultados de las comprobaciones
    lista_coincidencias_diagnosticas = list()
    lista_numero_sintomas_dco = list()
    lista_porcentaje_coincidencia = list()

    #Para cada posible diagnóstico en este síntoma guia se comprueban los sintomas obligatorios y los estandar
    for diagnostico in diagnosticos_posibles.keys():
        print('-------------DIAGNOSTICO-------------')
        print(diagnostico)

        dentro_de_cada_dco = diagnosticos_posibles.get(diagnostico)
        print(dentro_de_cada_dco)

        #Comprobamos si cumple los sintomas obligatorios
        cumple_obligatorio = comprobar_obligatorio(dentro_de_cada_dco, sintomas_del_paciente)
        print('------------------->cumple los obligatorios: '+ str(cumple_obligatorio))

        #Solo comprobamos el resto de sintomas si cumple el obligatorio
        if cumple_obligatorio:
            sintomas_coincidentes, sintomas_dco_totales = comprobar_sintomas(dentro_de_cada_dco, sintomas_del_paciente)
            # En este diagnóstico comprobamos cuantos trues ha habido de todos los síntomas
            porcentaje_coincidencia_dco = sintomas_coincidentes / sintomas_dco_totales * 100
        else:
            sintomas_coincidentes, sintomas_dco_totales = 0, 0
            porcentaje_coincidencia_dco = 0

        lista_coincidencias_diagnosticas.append(sintomas_coincidentes)
        lista_numero_sintomas_dco.append(sintomas_dco_totales)
        lista_porcentaje_coincidencia.append(porcentaje_coincidencia_dco)


    #Aqui se crea una tabla con todos los posibles diagnosticos y sus coincidencias
    df = pd.DataFrame()
    df['diagnosticos'] = diagnosticos_posibles.keys()
    df['coincidencias'] = lista_coincidencias_diagnosticas
    df['sintomas posibles'] = lista_numero_sintomas_dco
    df['% coincidencia'] = lista_porcentaje_coincidencia

    print(df)


comprobar_diagnosticos('franeko', 'masa cervical')
