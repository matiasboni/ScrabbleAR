'''
    Copyright 2020 Denis Daibes Cruz Sanchez
    Copyright 2020 Matias Ezequiel Bonifacio
    
    This file is part of ScrabbleAR.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.'''


import PySimpleGUI as sg
import os
import json
import sys


def Armar_estructura():
    '''Función que arma y retorna la estructura donde se mostrara el top 10 de puntajes'''
    estructura=[]
    for i in range(10):
            estructura.append([sg.Frame("",background_color="#48B7F9",layout=[[sg.T('',key='T'+str(i), size=(75,1))]])])
    return estructura

def Armar_string(datos):
    '''Función que arma y retorna una lista de strings con los datos que se reciben por párametro '''
    String=[]
    for clave, valor in datos.items():
        frase='Nombre: {}, Puntos: {}, Tiempo: {}, Fecha: {}, Hora: {}'.format(clave, valor['Puntaje'], valor['Tiempo'],valor["Fecha"],valor["Hora"])
        String.append(frase)
    return String

def Actualizar_texto(window, string, cant):
    '''Función que actualiza los textos en la ventana para mostrar los datos'''
    for i in range(10):
        if string!=None and i<cant:
            window.FindElement('T'+str(i)).Update(value=string[i])
        else:
            window.FindElement('T'+str(i)).Update(value="")

def mostrar_ranking(window,nivel):
    '''Función que arma los strings y muestra el top 10 correspondiente al nivel recibido como parámetro'''
    string=None
    cant=0
    if (os.path.isfile('ranking_por_nivel.json')):
        archivo=open('ranking_por_nivel.json','r')
        datos=json.load(archivo)
        if len(datos[nivel])!=0:
            string=Armar_string(datos[nivel])
            cant=len(string)
            Actualizar_texto(window,string,cant)     
        else:
            frase='No se guardo ningun jugador en el nivel '+nivel
            Actualizar_texto(window, string,cant)
            window.FindElement('T0').Update(value=frase)
        archivo.close()
    else:
        frase='No se guardo ningun jugador en el nivel '+nivel
        Actualizar_texto(window,string,cant)
        window.FindElement('T0').Update(value=frase)

def retornar_botones():
    '''Función que arma y retorna los botones que se utilizan para seleccionar el nivel'''
    botones=[[sg.Button('',image_filename="Imagenes/facil.png",key="Facil")],
				[sg.Button('', image_filename="Imagenes/medio.png",key="Medio")],
				[sg.Button('', image_filename="Imagenes/dificil.png",key="Dificil")],
				[sg.Button('', image_filename="Imagenes/salir.png", key='Salir')]
                ]
    return botones
    
def ranking_por_nivel():
    '''Función que define la pantalla del ranking para que el jugador pueda visualizar
    el top 10 de cada nivel'''
    estructura=Armar_estructura()
    botones=retornar_botones()
    
    ranking=[	[sg.Text('Ranking',font=("Ravie",110),text_color="#ffffff",justification='center' )],
				[sg.Column(botones),sg.Column(estructura)]
				]
    estilo={"element_justification":"center","font":("Helvetica",15)}
    if sys.platform=="linux":
        estilo["resizable"]=True

   
    window=sg.Window('', ranking,**estilo).Finalize()
    window.maximize()
    while True:
        event, values=window.read()
        if event in('Facil','Medio','Dificil'):
            mostrar_ranking(window,event)
        elif event=='Salir':
            break
        elif event==None:
            exit()
    window.close()
