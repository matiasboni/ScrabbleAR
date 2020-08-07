import PySimpleGUI as sg
import sys
import os
import pickle
import Modulos.Ranking as Ranking
import Modulos.Tablero as Tablero
import Modulos.Configuración as Configuración

def verificar_partida_guardada():
    '''Retorna una estructura que contiene la información de la partida guardada'''
    estructura=None
    if os.path.isfile('partida_guardada.pickle'):
        verificar=sg.PopupYesNo("Hay una partida guardada,¿desea retomarla?",no_titlebar=True)
        if verificar=="Yes":
            with open('partida_guardada.pickle',"rb")as archivo:
                estructura=pickle.load(archivo)
            archivo.close()
            os.remove('partida_guardada.pickle')    
    return estructura
    
def main():
    '''Función que define el tema y que muestra el menú principal'''
    sg.theme('DarkTanBlue')
    menu=[
		[sg.Text("ScrabbleAR",font=("Ravie",110)) ],
		[sg.Button("",image_filename='Imagenes/jugar.png',key='Jugar')],
		[sg.Button("",image_filename='Imagenes/configuracion.png',key='Configuración')],
		[sg.Button("",image_filename='Imagenes/ranking.png',key='Ranking')],
		[sg.Button("",image_filename='Imagenes/salir_m.png',key='Salir')] 
		]
    estilo={'element_justification':"center"}
    if sys.platform=='linux':
        estilo['resizable']=True  
    window=sg.Window("SCRABBLEAR",menu,**estilo).finalize()
    window.maximize()
    diccionario={'Nivel':'Medio', 'Tiempo':6, 'ListaPuntos':[1,2,3,4,5,6,7], 'ListaFichas':[11,6,5,4,3,3,1], 'Tiempo2':40 }
    while True:
        event,values=window.read()
        if event=='Jugar':
            estructura=verificar_partida_guardada()
            window.Hide()
            Tablero.tablero_de_juego(diccionario,estructura)
            window.UnHide()
            window.maximize()
        elif event=='Configuración':
            if sys.platform=="win32":
                window.Disable()
            Configuración.Configuracion_de_juego(diccionario)
            if sys.platform=="win32":
                window.Enable()
                window.BringToFront()
        elif event=='Ranking':
            window.Hide()
            Ranking.ranking_por_nivel()
            window.UnHide()
            window.maximize()
        elif event == 'Salir':
            break
        if event ==None:
            exit()
    window.close()
