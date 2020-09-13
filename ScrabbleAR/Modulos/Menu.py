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
import sys
import os
import pickle
import Modulos.Ranking as Ranking
import Modulos.Tablero as Tablero
import Modulos.Configuracion as Configuracion
import Modulos.Ayuda as Ayuda

def verificar_partida_guardada():
	'''Retorna una estructura que contiene la información de la partida guardada'''
	estructura=None
	if os.path.isfile('partida_guardada.pickle'):
		verificar=sg.PopupYesNo("Hay una partida guardada,¿desea retomarla?",no_titlebar=True)
		try:
			if verificar=="Yes":
				with open('partida_guardada.pickle',"rb")as archivo:
					estructura=pickle.load(archivo)
				archivo.close()
				os.remove('partida_guardada.pickle')
		except:
			sg.PopupOK('El archivo no fue encontrado. Por tal motivo debe empezar una partida nueva.')    
	return estructura
    
def main():
    '''Función que define el tema y que muestra el menú principal'''
    sg.theme('DarkTanBlue')
    menu=[
		[sg.Text("ScrabbleAR",font=("Ravie",110)) ],
		[sg.Button("",image_filename='Imagenes/jugar.png',key='Jugar')],
		[sg.Button("",image_filename='Imagenes/configuracion.png',key='Configuración')],
		[sg.Button("",image_filename='Imagenes/ranking.png',key='Ranking')],
		[sg.Button("",image_filename='Imagenes/ayuda.png',key='Ayuda')], 
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
            Configuracion.Configuracion_de_juego(diccionario)
            if sys.platform=="win32":
                window.Enable()
                window.BringToFront()
        elif event=='Ranking':
            window.Hide()
            Ranking.ranking_por_nivel()
            window.UnHide()
            window.maximize()
        elif event=='Ayuda':
            window.Hide()
            Ayuda.ayuda_usuario()
            window.UnHide()
            window.maximize()
        elif event == 'Salir':
            break
        if event ==None:
            exit()
    window.close()
