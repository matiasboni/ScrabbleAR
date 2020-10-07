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



def descuento3 (nivel):
    '''Función que retorna las coordenadas de las casillas de descuento 3 correspondientes a cada tablero '''
    if nivel=="Facil" :
        return [(0,6),(0,8),(6,0),(6,14),(8,0),(8,14),(14,6),(14,8)]
    elif nivel=='Dificil':
        return[(0,3),(0,7),(0,10),(1,2),(2,1),(3,0),(2,5),(4,1),(3,10),(4,14),(5,5),(7,0),(7,14),(9,9),(10,0),(10,13),
    				(11,4),(11,14),(12,13),(13,12),(14,11),(14,4),(14,7),(12,9)]
    else:
        return [(1,1),(13,13),(1,13),(13,1)]
    
def descuento2(nivel):
    '''Función que retorna las coordenadas de las casillas de descuento 2 correspondientes a cada nivel'''
    if nivel=='Facil':
        return [(0,4),(0,10),(4,0),(4,14),(10,0),(10,14),(14,4),(14,10)]
    if nivel=='Dificil':
        return [(1,9),(3,4),(5,13),(9,1),(11,10),(13,5)]
    else:
        return [(2,2),(4,4),(10,10),(12,12),(2,12),(4,10),(12,2),(10,4)]

def descuento1(nivel):
    '''Función que retorna las coordenadas de las casillas de descuento 1 correspondientes a cada tablero'''
    if nivel=='Facil':
        return [(0,2),(0,12),(2,0),(2,14),(12,0),(12,14),(14,2),(14,12)]
    elif nivel=='Dificil':
        return [(1,6),(3,7),(4,6),(6,1),(6,4),(7,3),(7,11),(8,10),(8,13),(10,8),(11,7),(13,8)]
    else:
        return [(3,3),(5,5),(9,9),(11,11),(3,11),(5,9),(11,3),(9,5)]

def pos_palabra3(nivel):
    '''Función que retorna las coordenadas de las casillas de palabra x3 correspondientes a cada tablero'''
    if nivel=='Facil':
        return [(0,0),(0,14),(1,1),(1,13),(2,2),(2,12),(12,2),(12,12),(13,1),(13,13),(14,0),(14,14)]
    else:
        return [(0,0),(0,14),(14,0),(14,14)]
        
def pos_palabra2(nivel):
    '''Función que retorna las coordenadas de las casillas de palabra x2 correspondientes a cada tablero'''
    if nivel=='Facil':
        return [(3,3),(3,11),(4,4),(4,10),(5,5),(5,9),(6,6),(6,8),(8,6),(8,8),(9,5),(9,9),(10,4),(10,10),(11,3),(11,11)]
    elif nivel=='Dificil':
        return [(5,9),(6,8),(8,6),(9,5)]
    else:
        return [(0,7),(7,0),(7,14),(14,7)]

def pos_letra3(nivel):
    '''Función que retorna las coordenadas de las casillas de letra x3 correspondientes  a cada tablero'''
    if nivel =='Facil':
        return [(1,7),(3,7),(7,1),(7,3),(7,11),(7,13),(11,7),(13,7)]
    elif nivel == 'Dificil':
        return [(4,10),(10,4)]
    else:
        return [(1,5),(1,9),(5,1),(5,13),(6,6),(6,8),(8,6),(8,8),(9,1),(9,13),(13,5),(13,9)]

def pos_letra2(nivel):
    '''Función que retorna las coordenadas de las casillas de letra x2 correspondientes a cada tablero'''
    if nivel=='Facil':
        return [(5,7),(7,5),(7,9),(9,7)]
    elif nivel=='Dificil':
        return [(0,11),(1,12),(2,13),(2,8),(3,14),(5,2),(6,12),(8,2),(9,12),(11,0),(12,1),(12,6),(13,2),(14,3)]
    else:
        return [(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,12),(7,3),(7,11),(8,2),(8,12),(11,0),(11,7),(11,14),(12,6),(12,8),(14,3),(14,11)]


def retornar_coordenadas(nivel):
    '''Retorna un diccionario de las coordenadas especiales segun el nivel'''
    coordenadas={"letra2":pos_letra2(nivel),"letra3":pos_letra3(nivel),"palabra2":pos_palabra2(nivel),
    "palabra3":pos_palabra3(nivel),"descuen1":descuento1(nivel),"descuen2":descuento2(nivel),"descuen3":descuento3(nivel)}
    return coordenadas


def asignar_imagen(coordenada,nivel,letra):
    '''Función que recibe como parametros la coordenada de una casilla, el nivel y una letra
    y retorna la imagen correspondiente'''
    dic=retornar_coordenadas(nivel)
    if letra=="ñ":
        letra="nn" 
    if coordenada in dic["letra2"]:
        return "Imagenes/Letras/"+letra+"_Lx2.png"
    elif coordenada in dic["letra3"]:
        return "Imagenes/Letras/"+letra+"_Lx3.png"
    elif coordenada in dic["palabra2"]:
        return "Imagenes/Letras/"+letra+"_Px2.png"
    elif coordenada in dic["palabra3"]:
        return "Imagenes/Letras/"+letra+"_Px3.png"
    elif coordenada in dic["descuen1"]:
        return "Imagenes/Letras/"+letra+"d1.png"
    elif coordenada in dic["descuen2"]:
        return "Imagenes/Letras/"+letra+"d2.png"
    elif coordenada in dic['descuen3']:
        return "Imagenes/Letras/"+letra+"d3.png"
    elif coordenada==(7,7):
        return "Imagenes/Letras/"+letra+"c.png"
    else:
        return  "Imagenes/Letras/"+letra+"_fondo.png"
