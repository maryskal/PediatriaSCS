import json as js
import pandas as pd

with open('diagnosticos.json') as file:
    diagnosticos = js.load(file)


def comprobar_diagnostico(usuario, sintoma_principal):
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

    #Se recorre cada diagnóstico posible de ese sintoma guia
    for diagnostico in diagnosticos_posibles.keys():
        print('-------------DIAGNOSTICO-------------')
        print(diagnostico)
        #Aqui se van a recoger los síntomas totales que tiene ese dignósitco y cuantos de ellos coinciden
        sintomas_dco_totales = 0
        sintomas_coincidentes = 0

        #Aqui se entra en el apartado de sintomas dentro del diagnostico (hay otro apartado que es obligatorios)
        clinica_del_dco = diagnosticos_posibles.get(diagnostico)
        print('Clínica')
        print(clinica_del_dco)

        #Se recorre cada uno de los síntomas de ese diagnóstico
        for sintomas_del_dco in clinica_del_dco.get('sintomas'):
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
                    print('\n')
            #En este diagnóstico comprobamos cuantos trues ha habido de todos los síntomas
            porcentaje_coincidencia_dco = sintomas_coincidentes / sintomas_dco_totales * 100

        print(diagnostico + ': coinciden ' + str(sintomas_coincidentes) + ' de ' + str(sintomas_dco_totales))

        #Aqui se recogen todas las coincidencias en sínotmas de cada diagnóstico
        lista_coincidencias_diagnosticas.append(sintomas_coincidentes)
        lista_numero_sintomas_dco.append(sintomas_dco_totales)
        lista_porcentaje_coincidencia.append(porcentaje_coincidencia_dco)
        print('---------------------- \n \n')


        print('\n')

    #Aqui se crea una tabla con todos los posibles diagnosticos y sus coincidencias
    df = pd.DataFrame()
    df['diagnosticos'] = diagnosticos_posibles.keys()
    df['coincidencias'] = lista_coincidencias_diagnosticas
    df['sintomas posibles'] = lista_numero_sintomas_dco
    df['% coincidencia'] = lista_porcentaje_coincidencia

    print(df)





comprobar_diagnostico('mrollan', 'masa cervical')
