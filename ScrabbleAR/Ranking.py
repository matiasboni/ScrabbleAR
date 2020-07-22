import PySimpleGUI as sg
import os
import json
import sys


def Armar_estructura():
    estructura=[]
    for i in range(10):
            estructura.append([sg.T('',key='T'+str(i), size=(40,1))])
    return estructura

def Armar_string(datos):
    String=[]
    for clave, valor in datos.items():
        frase='Nombre: {}, Puntos: {}, Tiempo: {}'.format(clave, valor['Puntaje'], valor['Tiempo'])
        String.append(frase)
    return String

def Actualizar_texto(window, string, cant):
    for i in range(cant):
        if string!=None:
            window.FindElement('T'+str(i)).Update(value=string[i])
        else:
            window.FindElement('T'+str(i)).Update(value='')

def mostrar_ranking(window,nivel, cant):
    string=None
    if (os.path.isfile('ranking_por_nivel.json')):
        archivo=open('ranking_por_nivel.json','r')
        datos=json.load(archivo)
        if len(datos[nivel])!=0:
            string=Armar_string(datos[nivel])
            cant=len(string)
            Actualizar_texto(window,string, cant)     
        else:
            frase='No se guardo ningun jugador en Nivel '+nivel
            Actualizar_texto(window, string,cant)
            window.FindElement('T0').Update(value=frase)
        archivo.close()
    else:
        frase='No hay ningun ranking de todos los niveles'
        Actualizar_texto(window,string, cant)
        window.FindElement('T0').Update(value=frase)
    return cant

def ranking_por_nivel():
    estructura=Armar_estructura()

    botones=[[sg.Button('Facil', size=(40,3))],
				[sg.Button('Medio', size=(40,3))],
				[sg.Button('Dificil', size=(40,3))],
				[sg.Button('Salir', size=(40,3))]
                ]
    ranking=[	[sg.T('Ranking', justification='center', auto_size_text=True, font=('Helvetica',120) )],
				[sg.Column(botones),sg.Column(estructura)]
				]
    estilo={"element_justification":"center","font":("Helvetica",15),"location":(0,0)}
    if sys.platform=="linux":
        estilo["resizable"]=True

    cant=0
    window=sg.Window('', ranking,**estilo).Finalize()
    window.maximize()
    while True:
        event, values=window.read()
        if event in('Facil','Medio','Dificil'):
            cant=mostrar_ranking(window,event, cant)
        if event in(None,'Salir'):
            break
    window.close()