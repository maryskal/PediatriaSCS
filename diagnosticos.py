import json as js
import copy as copy

class enfermedades:
    nombre = ''
    sintomas = list()
    tratamiento = ''


lista = [1,2,3,4]
resps = ['a', 'b', 'c', 'd']

def archivo(nombre, lista_1, lista_2):
    archivo = {}
    archivo[nombre] = []

    for i in range(len(lista_1)):
        archivo[nombre].append({lista_1[i]:lista_2[i]})
    return(archivo)

comentario = 'aefasdd'
otro = archivo('otros', list('a'), list(comentario))
print(otro)


a = archivo('a', resps, lista)
print(a)
resps = ['<', 'bas', 'cs', 'dsfa']
b = archivo('b',resps, lista)
print(b)
z = {**a, **b}
print(z)


for x in z.keys():
    print('keys')
    print(x)
for x in z.values():
    print('values')
    print(x)

print('a')
nodo = z.get('a')
dentro_z = z.get('a')
print(dentro_z)

print('dentro de z')
for x in dentro_z:
    print(x)

print(dentro_z[1].get('b'))

def buscar_resultado(doc_json, nombre_grupo, nombre_pregunta):
    grupo = doc_json.get(nombre_grupo)
    for x in grupo:
        r = x.get(nombre_pregunta)
        if r != None:
            respuesta = r
    return respuesta


print('FUNCION')
print(buscar_resultado(z, 'b', '<'))


with open('data.json', 'w') as file:
    js.dump(a, file, indent=4)

z = {
    'start':{
        'padre':"",
        "tipo": "pregunta",
        "pregunta": "¿Que te sucede?",
        'respuestas': {
            "Fiebre": "fiebre",
            "Masa en el cuello": "masa cervical"
        }
    }}


def crear_json(lista_1, lista_2):
    archivo = {}

    #Se recorre la lista 1 y se introducen los datos según lista_1 : lista_2
    for i in range(len(lista_1)):
        dic = {lista_1[i]:lista_2[i]}
        archivo.update(dic)
    print(archivo)
    return(archivo)

def buscar_resultado(doc_json, nombre_pregunta):
    respuesta = doc_json.get(nombre_pregunta)
    return respuesta

prueba = crear_json(lista, resps)

print('asdfasdf')

print(buscar_resultado(prueba, 2))

with open('data.json') as file:
    data = js.load(file)

print(data)