import PySimpleGUI as sg
import sys
import os
import pickle
import Ranking
import Tablero
import Configuración

def verificar_partida_guardada():
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
		[sg.Text("ScrabbleAR",auto_size_text=True,font=("Ravie",110)) ],
		[sg.Button("",image_size=(500,80),image_filename='Imagenes/jugar.png',key='Jugar')],
		[sg.Button("",image_size=(500,80),image_filename='Imagenes/configuracion11.png',key='Configuración')],
		[sg.Button("",image_size=(500,80),image_filename='Imagenes/Ranking.png',key='Ranking')],
		[sg.Button("",image_size=(500,80),image_filename='Imagenes/Salir_m.png',key='Salir')] 
		]
    estilo={'element_justification':"center",'font':("Helvetica",15),'location':(0,0)}
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
            Ranking.ranking_por_nivel()
        elif event == 'Salir':
            break
        if event ==None:
            exit()
    window.close()

if __name__=='__main__':
    main()
