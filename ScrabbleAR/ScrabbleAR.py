import PySimpleGUI as sg
import random

def todas_letras():
    dic={'A':11, 'E':11, 'O':8, 'S':7, 'I':6, 'U':6, 'N':5, 'L':4, 'R':4, 'T':4, 'C':4, 'D':4, 'G':2,'M':3, 'B':3, 'P':2,
             'F':2, 'H':2, 'V':2, 'Y':1, 'J':2, 'K':1, 'LL':1, 'Ñ':1, 'Q':1, 'RR':1, 'W':1, 'X':1, 'Z':1}
    return dic

def puntaje_por_letra(lista):
    dic={"AEOSIUNLRT":lista[0],"CDG":lista[1], 'MBP':lista[2], 'FHVY':lista[3], 'J':lista[4], 'KLLÑQRRWX':lista[5], 'Z':lista[6]}
    return dic

def generar_letras(dic):
    letras_jugador=[]
    for i in range(0,7):
        letra=random.choice(list(dic.keys()))
        letras_jugador.append(letra)
        dic[letra]=dic[letra]-1
        if dic[letra]==0:
            del dic[letra]
    return letras_jugador

def descuento3 (nivel):
    if nivel=="NF" :
        return [(0,6),(0,8),(6,0),(6,14),(8,0),(8,14),(14,6),(14,8)]
    elif nivel=='ND':
        return[(0,3),(0,7),(0,10),(1,2),(2,1),(3,0),(2,5),(4,1),(3,10),(4,14),(5,5),(7,0),(7,14),(9,9),(10,0),(10,13),
    				(11,4),(11,14),(12,13),(13,12),(14,11),(14,4),(14,7),(12,9)]
    else:
        return []
        #son los puntos del color rojo [(1,1),(2,2),(3,3),(4,4),(5,5),(9,9),(10,10),(11,11),(12,12),(13,13),
        #(1,12),(2,12),(3,11),(4,10),(5,9),(9,5),(10,4),(11,3),(12,2),(13,1)]
        #color clarito :[(0,0),(0,7),(0,14),(7,0),(7,7),(7,14),(14,0),(14,7),(14,14)]... esos aun no se como separarlo
        #los separe por que tenemos q usarlo para identificar los puntos cuando el jugador ingrese una palabra al tablero y ver si se posiciono en una de ellas
def descuento2(nivel):
    if nivel=='NF':
        return [(0,4),(0,10),(4,0),(4,14),(10,0),(10,14),(14,4),(14,10)]
    if nivel=='ND':
        return [(1,9),(3,4),(5,13),(9,1),(11,10),(13,5)]
    else:
        return []

def descuento1(nivel):
    if nivel=='NF':
        return [(0,2),(0,12),(2,0),(2,14),(12,0),(12,14),(14,2),(14,12)]
    elif nivel=='ND':
        return [(1,6),(3,7),(4,6),(6,1),(6,4),(7,3),(7,11),(8,10),(8,13),(10,8),(11,7),(13,8)]
    else:
        return []

def pos_palabra3(nivel):
    if nivel=='NF':
        return [(0,0),(0,14),(1,1),(1,13),(2,2),(2,12),(12,2),(12,12),(13,1),(13,13),(14,0),(14,14)]
    elif nivel=='ND':
        return [(0,0),(0,14),(14,0),(14,14)]
    else:
        return []

def pos_palabra2(nivel):
    if nivel=='NF':
        return [(3,3),(3,11),(4,4),(4,10),(5,5),(5,9),(6,6),(6,8),(8,6),(8,8),(9,5),(9,9),(10,4),(10,10),(11,3),(11,11)]
    elif nivel=='ND':
        return [(5,9),(6,8),(8,6),(9,5)]
    else:
        return []

def pos_letra3(nivel):
    if nivel =='NF':
        return [(1,7),(3,7),(7,1),(7,3),(7,11),(7,13),(11,7),(13,7)]
    elif nivel == 'ND':
        return [(4,10),(7,7),(10,4)]
    else:
        return [(1,5),(1,9),(5,1),(5,13),(6,6),(6,8),(8,6),(8,8),(9,1),(9,13),(13,5),(13,9)]

def pos_letra2(nivel):
    if nivel=='NF':
        return [(5,7),(7,5),(7,9),(9,7)]
    elif nivel=='ND':
        return [(0,11),(1,12),(2,13),(2,8),(3,14),(5,2),(6,12),(8,2),(9,12),(11,0),(12,1),(12,6),(13,2),(14,3)]
    else:
        return [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,12),(7,3),(7,11),(8,2),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)]

def asignar_color_facil(coordenadas):
    nivel='NF'
    letra2=pos_letra2(nivel)
    letra3=pos_letra3(nivel)
    palabra2=pos_palabra2(nivel)
    palabra3=pos_palabra3(nivel)
    descuen1=descuento1(nivel)
    descuen2=descuento2(nivel)
    descuen3=descuento3(nivel)
    if coordenadas in letra2:
        return ("sky blue","sky blue")
    elif coordenadas in letra3:
        return ("blue","blue")
    elif coordenadas in palabra2:
        return ("green","green")
    elif coordenadas in palabra3:
        return ("green2", "green2")
    elif coordenadas in descuen1:
        return ("orange","orange")
    elif coordenadas in descuen2:
        return ("red","red")
    elif coordenadas in descuen3:
        return ("DarkRed","DarkRed")
    elif coordenadas==(7,7):
        return ("yellow","yellow")
    else:
        return  ("azure","azure")

def asignar_color_dificil(coordenadas):
    nivel='ND'
    letra2=pos_letra2(nivel)
    letra3=pos_letra3(nivel)
    palabra2=pos_palabra2(nivel)
    palabra3=pos_palabra3(nivel)
    descuen1=descuento1(nivel)
    descuen2=descuento2(nivel)
    descuen3=descuento3(nivel)
    if coordenadas in letra2:
        return ("green yellow","green yellow")
    elif coordenadas in letra3:
        return ("blue","blue")
    elif coordenadas in palabra2:
        return ("green","green")
    elif coordenadas in palabra3:
        return ("red", "red")
    elif coordenadas in descuen1:
        return ("red","red")
    elif coordenadas in descuen2:
        return ("red2","red2")
    elif coordenadas in descuen3:
        return ("red3","red3")
    else:
        return  ("azure","azure")

def asignar_color_medio(coordenadas):
    nivel='NM'
    letra2=pos_letra2(nivel)
    letra3=pos_letra3(nivel)
    palabra2=pos_palabra2(nivel)
    palabra3=pos_palabra3(nivel)
    descuen1=descuento1(nivel)
    descuen2=descuento2(nivel)
    descuen3=descuento3(nivel)
    if coordenadas in letra2:
        return ("green yellow","green yellow")
    elif coordenadas in letra3:
        return ("blue","blue")
    elif coordenadas in palabra2:
        return ("green","green")
    elif coordenadas in palabra3:
        return ("red", "red")
    elif coordenadas in descuen1:
        return ("red","red")
    elif coordenadas in descuen2:
        return ("red2","red2")
    elif coordenadas in descuen3:
        return ("red3","red3")
    else:
        return  ("azure","azure")

def retornar_tablero_facil():
    datos={'size':(4,2), 'pad':(0,0), 'border_width':1}
    tablero=[
            [sg.Button('',key=(i,j),button_color=asignar_color_facil((i,j)), **datos,) for j in range(15)]for i in range(15)]
    return tablero

def retornar_tablero_medio():
    datos={'size':(4,2), 'pad':(0,0), 'border_width':1}
    tablero=[
            [sg.Button('',key=(i,j), **datos, button_color=asignar_color_medio((i,j))) for j in range(15)]for i in range(15)]
    return tablero

def retornar_tablero_dificil():
    datos={'size':(4,2), 'pad':(0,0), 'border_width':1}
    tablero=[
            [sg.Button('',key=(i,j),button_color=asignar_color_dificil((i,j)), **datos) for j in range(15)]for i in range(15)
            ]

    return tablero

def main():
	cantidad_letras_compu=todas_letras()
	cantidad_letras_jugador=todas_letras()

	vector_jugador=generar_letras(cantidad_letras_jugador)
	vector_compu=generar_letras(cantidad_letras_compu)

	tablero=retornar_tablero_dificil()

	columna1=[  [sg.Button('Iniciar', size=(15,1))],
				[sg.Button('Ranking', size=(15,1))],
				[sg.Text('Tiempo: ', size=(30,1))],
				[sg.Button('Salir', size=(15,1))]]

	letras_complu=[            [sg.Button("",key=i ,size=(5,2)) for i in range(7)]]

	letras_usuario=[           [sg.Button(vector_jugador[a],key=a, size=(5,2)) for a in range(7)]]

	letras_con_otro_button=[   [sg.Column(letras_usuario), sg.Button('Cambiar', size=(5,2))]]

	columna2=[  [sg.Text(' '* 19), sg.Column(letras_complu)],
				[sg.Column(tablero)],
				[sg.Text(' '*10), sg.Column(letras_con_otro_button)]]

	columna3=[  [sg.Text('Consideraciones')],
				[sg.Listbox(values=[], size=(30,20))]]

	layout= [   [sg.Text('ScrabbleAR', size=(140,1), justification='center')],
			    [sg.Column(columna1), sg.Column(columna2, pad=(0,0)), sg.Column(columna3)]]

	window=sg.Window('ScrabbleAR', layout, default_element_size=(30, 1), return_keyboard_events=True, no_titlebar=False,
						grab_anywhere=True,margins=(0,0))
	while True:
		event, values=window.read()
		print(event)
		if event in (None, 'Salir'):
			break
	window.close()

if __name__=='__main__':
    main()
