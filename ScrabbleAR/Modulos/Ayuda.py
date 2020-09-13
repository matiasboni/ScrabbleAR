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
    
def imagenes():
    '''Función que retorna los botones del tablero'''

    botones=['iniciar','posponer','terminar','verificar','cambiar','aceptar']
    estructura=[[sg.Button('',image_filename='Imagenes/'+i+'.png',key=i)]for i in botones]
    return estructura

def texto():
    '''Función que retorna un texto con la explicación de cada boton del tablero'''
    
    explicaciones=['El botón Iniciar permite iniciar la partida.',"El botón Posponer permite guardar la partida y retomarla en otro momento","El botón Terminar permite finalizar el juego",
    "El botón Verificar permite verificar si la palabra ingresada es valida","El botón Cambiar Fichas permite canjear las fichas que se deseen por otras fichas que se encuentren en la bolsa.",
    "El botón Aceptar permite confirmar el cambio de fichas"]
    if sys.platform !='linux':
        estilo={'size':(90,1),'font':("Calibri",16)}
    else:
        estilo={'size':(76,1),'font':("Calibri",17)}
    estructura=[[sg.Frame("",layout=[[sg.T(i,**estilo)]])] for i in explicaciones]
    return estructura

def reglas():
    '''Función que retorna una estructura con las reglas del juego'''
    
    estilo={'font':('calibri',13)} if sys.platform !='linux' else {'font':('Calibri',11)}
    layout_fichas=[[sg.Text("-El juego cuenta con una bolsa que contiene la cantidad de fichas por letra.", **estilo)],
                   [sg.Text("-Las letras se encuentran en conjuntos estos son:",**estilo)],
                   [sg.Text("      1: A, E, O, S, I, U, N, L, R, T.      2:C, D, G.       3:-M, B, P.",**estilo)],
                   [sg.Text("      4: F, H, V, Y.                        5: J.            6:K, LL, Ñ, Q, RR, W, X.        7: Z.",**estilo)],
                   [sg.Text("-Cada uno de los conjuntos tiene un puntaje y una cantidad de fichas asociadas.",**estilo)],
                   [sg.Text("-El jugador cuenta con 3 oportunidades para cambiar fichas, devolviéndolas a la bolsa, en cada una se puede seleccionar mas de una ficha.",**estilo)],
                   [sg.Text("Luego de realizar el maximo permitido el botón se deshabilitara. La computadora no tiene acceso a esta opción.",**estilo)],
                   ]
    layout_tiempo=[[sg.Text("-El juego cuenta con un tiempo de partida definido.",**estilo)],
                   [sg.Text("-El turno jugador cuenta con un tiempo de jugada, si en cualquier momento alcanza el tiempo maximo de jugada perdera el turno",**estilo)],
                   [sg.Text("-La computadora demora diez segundos en armar una palabra o en pasar de turno.Mientras ese tiempo transcurre, el jugador no puede realizar ninguna acción.",**estilo)],
                  ]
    layout_atriles=[[sg.T('-Cada participante posee un atril que le permite tener a su disposición 7 fichas.',**estilo)],
                    [sg.T('-El atril de la computadora es visible para el jugador, pero este no distingue las letras.',**estilo)],
                    [sg.T('-Cada atril debe contener en todo momento 7 fichas.',**estilo)],
                   ]
    layout_inicio=[ [sg.T('-Se determina aleatoriamente quien empieza jugando, si el jugador o la computadora.',**estilo)],
                    [sg.T('-Se reparten 7 fichas a cada participante de forma aleatoria.',**estilo)],
                    [sg.T('-En la primera jugada una de las letras de la palabra armada debe estar situada en la casilla de inicio.',**estilo)]
                    ]
    
    layout_armado=[[sg.T('-Tanto el jugador como la computadora deben formar una palabra usando 2 o más letras',**estilo)],
                   [sg.T('-Las fichas pueden colocarse en el tablero de forma vertical(en orden descendente) o en forma horizontal(de izquierda a derecha).',**estilo)],
                   [sg.T('-Las palabras no deben cruzarse,pero si pueden quedar "pegadas".',**estilo)],
                   [sg.T('-Una vez que se desea verificar la palabra, se revisa si es una palabra admitida. Si la palabra es correcta se repondrá la cantidad',**estilo)],
                   [sg.T(' de fichas que utilizó, y si la palabra no es correcta las fichas se devuelven al jugador para que vuelva a intentar.',**estilo)],
                   [sg.T('-La computadora toma como válida la primera combinación que encuentre. En caso de no encontrar combinación posible,pasa de turno.',**estilo)],
                   ]
    layout_fin=[[sg.T('-El juego termina cuando:')],
                [sg.T('         -el jugador en turno no puede completar sus 7 fichas luego de una jugada.',**estilo)],
                [sg.T('         -el tiempo de la partida se termina.',**estilo)],
                [sg.T('         -el botón Terminar es presionado.',**estilo)],
                [sg.T('-Al finalizar se muestran las fichas que posee cada jugador y se resta el valor de dichas fichas para que el puntaje sea recalculado.',**estilo)],
                [sg.T('-También se incluye la posibilidad de posponer la partida presionando el botón "Posponer". Esta acción permite guardar la partida actual',**estilo)],
                [sg.T('teniendo en cuenta la información del tablero, los puntajes y el tiempo restante.Se debe tener en cuenta que siempre habrá una sola partida guardada.',**estilo)]    
                    ]
    layout_importante=[[sg.T("Tenga en cuenta que la cantidad de fichas, el puntaje de cada ficha, el tiempo de partida, el tiempo de jugada y los tipos de palabras válidas",**estilo)],
                       [sg.T("pueden ser configurables. El juego tiene una configuración predefinida.",**estilo)]
                    ]
                    
    estructura=[sg.TabGroup([[  sg.Tab('         Fichas          ', layout_fichas),
                                sg.Tab('         Tiempo          ',layout_tiempo),
                                sg.Tab('         Atriles         ',layout_atriles),
                                sg.Tab('     Inicio de juego     ',layout_inicio),
                                sg.Tab('  Armado de una palabra  ',layout_armado),
                                sg.Tab('      Fin del juego      ',layout_fin,),
                                sg.Tab('       Importante        ',layout_importante)]],font=("Calibri",14) if sys.platform!='linux' else ('Calibri',11))]
    return estructura

def ayuda_usuario():
    '''Función que muestra una ventana con información que el usuario debe tener en cuenta'''
    img=imagenes()
    text=texto()
    reglas_juego=reglas()
    layout=[
        [sg.T('',size=(12,1) if sys.platform !='linux' else (0,0) ),sg.Button('',image_filename='Imagenes/flecha.png', key='Salir'),sg.T('',size=(4,1) if sys.platform != 'linux' else (27,1)),sg.T("    Ayuda    ",font=("Ravie",60)),sg.T('',size=(45,1))],
        [sg.T('', size=(11,1) if sys.platform != 'linux' else (7,1)),sg.Column(text), sg.Column(img)],
        [sg.Frame('',layout=[[sg.T('Reglas del Juego',font=('Calibri',20),size=(50,1),justification='center')]])],
        reglas_juego,
    ]
    estilo={'element_justification':"center"}
    if sys.platform=='linux':
        estilo['resizable']=True  
    window=sg.Window("Ayuda",layout,**estilo).finalize()
    window.maximize()
    while True:
        event,values=window.read()
        if event=="Salir":
            break
        elif event==None:
            exit()
    window.close()
