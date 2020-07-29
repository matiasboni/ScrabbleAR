import PySimpleGUI as sg 
import random
import time
import itertools
import sys
import os
import json
import pickle
import Coordenadas
import pattern.es
from pattern.es import parse
from datetime import datetime


def asociar_estructura():
    '''Función que retorna un diccionario con los numeros asociados a una letra'''
    valores_letras={}
    caracter=65
    for i in range(1,27):
        valores_letras[i]=chr(caracter)
        caracter+=1
    valores_letras[27]="LL"
    valores_letras[28]="RR"
    valores_letras[29]="Ñ"
    return valores_letras

def crear_tablero_aux():
    '''Función que retorna la matriz de 15x15 sin letras(todos en 0) '''
    tablero_aux=[]
    for i in range(0,15):
        lista=[]
        for j in range(0,15):
            lista.append(0)
        tablero_aux.append(lista)
    return tablero_aux


def generar_letras(cantidad,dic,valores_letras):
    '''Función que recibe como parametro la cantidad de letras que se deben generar
     de forma aleatoria para que sean retornadas en una lista '''
    letras=[]
    aux=[]
    suma=0
    for i in valores_letras.keys():
        if dic[valores_letras[i]]["Cantidad"]!=0:
            suma+=dic[valores_letras[i]]["Cantidad"]
            aux.append(i)
    if suma>=cantidad:
        for i in range(cantidad):
            num=random.choice(aux)
            letras.append(num)
            dic[valores_letras[num]]['Cantidad']-=1
            if dic[valores_letras[num]]==0:
                aux.remove(num)
    return letras


def buscar_combinacion(vector_compu,valores_letras,tipo_de_palabras):
    '''Función que retorna la 1er palabra que logro armar la computadora con
    las posiciones de las letras usadas'''
    letras=[]
    tipos=[]
    if tipo_de_palabras=="Verbos y Adjetivos":
        tipos=["VB","JJ"]
    elif tipo_de_palabras=="Verbos":
        tipos=["VB"]
    elif tipo_de_palabras=="Adjetivos":
        tipos=["JJ"]
    for i in range(0,len(vector_compu)):
        letras.append(valores_letras[vector_compu[i]].upper())
    palabra=""
    posiciones=[]
    conjuntos=set()
    for i in range(1,len(letras)+1):
        permutaciones=list(itertools.permutations(letras,i))
        for j in permutaciones:
            conjuntos.add(j)
    for i in conjuntos:
        aux="".join(i)
        if (aux.lower() in pattern.es.lexicon.keys() and aux.lower() in pattern.es.spelling.keys()) and len(i)>=2:
            tipo_palabra=parse(aux).split("/")[1]
            if tipo_palabra in tipos or len(tipos)==0:
                palabra=aux
                conjunto=i
                break
    if palabra!="":
        for i in conjunto:
            posicion=letras.index(i)
            posiciones.append(posicion)
            letras[posicion]="0"
    return(palabra,posiciones)

def actualizar_tablero(posiciones,orientacion,pos,window,valores_letras,vector_compu,nivel):
    '''Función que actualiza el tablero con la palabra que logro armar la computadora'''
    if orientacion=="Vertical":
        for i in range(0,len(posiciones)):
            window.FindElement((pos[0]+i,pos[1])).Update(image_filename=Coordenadas.asignar_color((pos[0]+i,pos[1]),nivel,valores_letras[vector_compu[posiciones[i]]].lower()))
    elif orientacion=="Horizontal":
        for i in range(0,len(posiciones)):
             window.FindElement((pos[0],pos[1]+i)).Update(image_filename=Coordenadas.asignar_color((pos[0],pos[1]+i),nivel,valores_letras[vector_compu[posiciones[i]]].lower()))

def actualizar_matriz(tablero_aux,orientacion,pos,posiciones,vector_compu):
    '''Función que actualiza la matriz con la palabra que ingresó la computadora y
    retorna las posiciones actualizadas'''
    cant=0
    posiciones_matriz=[]
    if orientacion=="Vertical":
        for i in posiciones:
            tablero_aux[pos[0]+cant][pos[1]]=vector_compu[i]
            posiciones_matriz.append((pos[0]+cant,pos[1]))
            cant+=1
    elif orientacion=="Horizontal":
        for i in posiciones:
            tablero_aux[pos[0]][pos[1]+cant]=vector_compu[i]
            posiciones_matriz.append((pos[0],pos[1]+cant))
            cant+=1
    return posiciones_matriz

def verificar_orientacion(pos,tablero_aux,posiciones,orientacion):
    '''Función que verifica si la palabra se puede ubicar en el tablero'''
    ok=False
    if orientacion=="Vertical" and pos[0]+len(posiciones)<=14:
        ok=True
        i=0
        while ok and i<len(posiciones):
            if tablero_aux[pos[0]+i][pos[1]]==0:
                ok=False
                i+=1
    elif orientacion=="Horizontal" and pos[1]+len(posiciones)<=14:
        ok=True
        i=0
        while ok and i<len(posiciones):
            if tablero_aux[pos[0]][pos[1]+i]!=0:
                ok=False
            i+=1
    return ok

def actualizar_vector_compu(vector_compu,posiciones,valores_letras,letras_compu):
    '''Función que actualiza el atril de la computadora'''
    ok=True
    letras=generar_letras(len(posiciones),letras_compu,valores_letras)
    if len(letras)!=0:
        indice=0
        for i in range(0,len(letras)):
            vector_compu[posiciones[indice]]=letras[i]
            indice+=1
        ok=False
    return ok

def calcular_puntos(botones_del_tablero,tablero_aux,nivel,valores_letras,letras):
    '''Función que calcula y retorna los puntos logrados en una jugada'''
    dic=Coordenadas.retornar_coordenadas(nivel)
    total=0
    cant_pal2=0
    cant_pal3=0
    for i in botones_del_tablero:
        valor_letra=letras[valores_letras[tablero_aux[i[0]][i[1]]]]["Puntos"]
        if i in dic["letra2"]:
            valor_letra=valor_letra*2
        elif i in dic["letra3"]:
            valor_letra=valor_letra*3
        elif i in dic["descuen1"]:
            valor_letra=valor_letra-1
        elif i in dic["descuen2"]:
            valor_letra=valor_letra-2
        elif i in dic['descuen3']:
            valor_letra=valor_letra-3
        elif i in dic['palabra2']:
            cant_pal2+=1
        elif i in dic['palabra3']:
            cant_pal3+1
        total=total+valor_letra
    if cant_pal2!=0:
        for i in range(0,cant_pal2):
            total=total*2
    if cant_pal3!=0:
        for i in range(0,cant_pal3):
            total=total*3
    return total

def borrar_pos_usadas(coordenadas,pos_0):
	for i in coordenadas:
		pos_0.remove(i)


def turno_compu(window,tablero_aux,valores_letras,vector_compu,iniciar_tiempo_partida,letras_compu,nivel,tipo_de_palabra,contador_partida,pos_0):
    '''Función que ejecuta el turno de la computadora '''
    contador_partida=int(round(time.time() * 100)) -iniciar_tiempo_partida
    window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
    palabra,posiciones=buscar_combinacion(vector_compu,valores_letras,tipo_de_palabra)
    total_palabra=0
    ok=False
    if palabra!="":
        if tablero_aux[7][7]==0:
            orientacion=random.choice(["Vertical","Horizontal"])
            if orientacion=="Vertical":
                pos=(random.randint(7-len(posiciones)+1,7),7)
            else:
                pos=(7,random.randint(7-len(posiciones)+1,7))
            ok=True
        else:
            cant=1
            while not ok:
                pos=random.choice(pos_0)
                while tablero_aux[pos[0]][pos[1]]!=0 and cant!=len(pos_0):
                    pos=random.choice(pos_0)
                    cant+=1
                if cant!=len(pos_0):
                    orientacion=random.choice(["Vertical","Horizontal"])
                    ok=verificar_orientacion(pos,tablero_aux,posiciones,orientacion)
                    if not ok and orientacion=="Vertical":
                        orientacion="Horizontal"
                        ok=verificar_orientacion(pos,tablero_aux,posiciones,orientacion)
                    elif not ok:
                        orientacion="Vertical"
                        ok=verificar_orientacion(pos,tablero_aux,posiciones,orientacion)
        if ok:
            actualizar_tablero(posiciones,orientacion,pos,window,valores_letras,vector_compu,nivel)
            posiciones_matriz=actualizar_matriz(tablero_aux,orientacion,pos,posiciones,vector_compu)
            total_palabra=calcular_puntos(posiciones_matriz,tablero_aux,nivel,valores_letras,letras_compu)
            borrar_pos_usadas(posiciones_matriz,pos_0)
            terminar=actualizar_vector_compu(vector_compu,posiciones,valores_letras,letras_compu)
    else:
        terminar=False
        for i in vector_compu:
            letras_compu[valores_letras[i]]["Cantidad"]+=1
        actualizar_vector_compu(vector_compu,[0,1,2,3,4,5,6],valores_letras,letras_compu)
    return ("Terminar" if terminar else "",contador_partida,total_palabra,palabra)


def actualizar_letras_jugador(window, letras_a_cambiar, nuevos, valores_letras, vector_jugador):
    '''Actualiza el atril del jugador con nuevas letras'''
    cant=0
    for i in letras_a_cambiar:
        vector_jugador[i[1]]=nuevos[cant]
        window.FindElement(i).Update(image_filename="Letras/"+valores_letras[nuevos[cant]].lower()+"_fondo.png")
        cant+=1 

def todas_las_pos(coordenadas_palabras, movimiento):
    '''Función que retorna las posiciones válidas para el jugador segun la orientación
    o si es la primer letra ingresada '''
    if movimiento=='':
        evento=coordenadas_palabras[0]
        posiciones_validas=[(evento[0]+1, evento[1]), (evento[0], evento[1]+1)]
    ultimo=coordenadas_palabras[len(coordenadas_palabras)-1]
    if movimiento=='horizontal':
        posiciones_validas=[(ultimo[0],ultimo[1]+1)]
    if movimiento =='vertical':
        posiciones_validas =[(ultimo[0]+1,ultimo[1])]
    return posiciones_validas

def Verificar_palabra(palabra, nivel, tipo_de_palabra):
    '''Función que valida la palabra ingresada por el jugador segun el nivel y el tipo de palabra'''
    if palabra in pattern.es.lexicon.keys() and palabra in pattern.es.spelling.keys():
        palabra_analizada=parse(palabra).split('/')
        tipo=palabra_analizada[1]
        if nivel=='Facil':
            return True
        if nivel=='Medio' and tipo in('JJ','VB'):
            return True
        tipo_random='VB' if tipo_de_palabra=='Verbos' else 'JJ'
        if nivel=='Dificil' and tipo==tipo_random:
            return True
        else:
            return False
    else:
        return False

def volver_letras_a_posicion(window,tablero_aux,coordenada_letras, letras_usadas, vector_jugador, valores_letra,nivel):
    '''Función que coloca las letras en sus posiciones anteriores en el caso de que la palabra no sea
    válida, actualizando el tablero y la matriz auxiliar'''
    for i in letras_usadas:
        window.FindElement(i).Update(image_filename="Letras/"+valores_letra[vector_jugador[i[1]]].lower()+"_fondo.png")
    for i in coordenada_letras:
        window.FindElement(i).Update(image_filename=Coordenadas.asignar_color(i,nivel,''))
        tablero_aux[i[0]][i[1]]=0
	
def ActivarDesactivarBoton(window, pos_letras, accion, event=None):
    '''Función que  habilita o deshabilita los botones del atril jugador'''
    aux={'disabled':True} if (accion=='deshabilitar') else {'disabled':False}
    for i in pos_letras:
        if i!=event:
            window.FindElement(i).Update(**aux)

def Devolver_letras_a_cambiar(window, valores_letras, vector_jugador, pos_de_letras, tiempo_maximo,tiempo_jugada,iniciar_tiempo_partida,iniciar_tiempo_jugada,contador_partida,contador_jugada):
	'''Función en la cual el jugador elije las letras que quiere cambiar de las disponibles en sus botones'''
	letras_a_cambiar=[]
	ActivarDesactivarBoton(window,('Verificar','Posponer'),'deshabilitar',event=None)
	evento=None
	while True and contador_partida<tiempo_maximo  :
		evento, values1=window.read(timeout=10)
		contador_partida=int(round(time.time() * 100)) -iniciar_tiempo_partida
		contador_jugada=int(round(time.time() * 100)) -iniciar_tiempo_jugada
		window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100)// 60, (contador_partida// 100)% 60))
		window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: "+'{:02d}:{:02d}'.format((contador_jugada // 100)// 60, (contador_jugada// 100)% 60))
		if evento in pos_de_letras:
			if evento in letras_a_cambiar:
				window.FindElement(evento).Update(image_filename="Letras/"+valores_letras[vector_jugador[evento[1]]].lower()+"_fondo.png")
				letras_a_cambiar.remove(evento)
			else:
				letras_a_cambiar.append(evento)
				window.FindElement(evento).Update(image_filename="Letras/_fondo.png")
		if evento =='Aceptar' or evento=='Terminar' or contador_jugada>=tiempo_jugada :
			break
		if evento == None:
			exit()
	ActivarDesactivarBoton(window,('Verificar','Posponer'),'habilitar',event=None)
	return (evento,letras_a_cambiar, contador_partida,contador_jugada)

def selecionar_letra(window, contador_partida,contador_jugada,tiempo_maximo,tiempo_jugada,iniciar_tiempo_partida,iniciar_tiempo_jugada,tablero_aux,event,pos_validas):
	'''Selecciona una posicion en el tablero'''
	evento=None
	while True and contador_partida<tiempo_maximo:
		evento, values1= window.read(timeout=10)
		contador_partida=int(round(time.time() * 100)) -iniciar_tiempo_partida
		contador_jugada=int(round(time.time() * 100)) -iniciar_tiempo_jugada
		window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60,(contador_partida// 100) % 60 ))
		window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: "+'{:02d}:{:02d}'.format((contador_jugada // 100) // 60,(contador_jugada// 100) % 60 ))
		if evento==event:
			break
		try:
			if tablero_aux[evento[0]][evento[1]]==0:
				if pos_validas!=None:
					if evento in pos_validas:
						break
				else:
					break
		except(TypeError):
			if evento==None:
				exit()
		if contador_jugada>=tiempo_jugada:
			evento=None
			break
		if evento=='Terminar' or evento=='Posponer':
			break
	return (evento,contador_partida,contador_jugada)
	
def turno_jugador(window,tablero_aux,vector_jugador, letras_jugador, valores_letras,nivel,tipo_de_palabra,iniciar_tiempo_partida, 
	tiempo_maximo, cantidad_veces_cambiado,contador_partida,tiempo_jugada,iniciar_tiempo_jugada,contador_jugada,pos_0):
    '''Funcion que ejecuta el turno del jugador'''
    pos_de_letras=[('a',0),('a',1),('a',2),('a',3),('a',4),('a',5),('a',6)]
    pos_validas=None
    palabra=[]
    coordenada_de_letras=[]
    letras_usadas=[]
    movimiento=''
    puntos_palabra=0
    while True:
        event, values=window.read(timeout=10)
        contador_partida=int(round(time.time() * 100)) -iniciar_tiempo_partida
        contador_jugada=int(round(time.time()*100))-iniciar_tiempo_jugada
        window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
        window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: "+'{:02d}:{:02d}'.format((contador_jugada // 100) // 60, (contador_jugada// 100) % 60))
        if event in pos_de_letras and (not event in letras_usadas):
            ActivarDesactivarBoton(window, pos_de_letras,'deshabilitar',event)
            evento,contador_partida,contador_jugada=selecionar_letra(window,contador_partida,contador_jugada,tiempo_maximo,tiempo_jugada,iniciar_tiempo_partida,iniciar_tiempo_jugada,tablero_aux,event,pos_validas)  
            if evento!=event and evento!=None and evento!='Terminar' and evento!='Posponer':
                if len(palabra)==1:
                    movimiento='horizontal' if (evento[1]>coordenada_de_letras[0][1]) else 'vertical'
                letra=valores_letras[vector_jugador[event[1]]]
                tablero_aux[evento[0]][evento[1]]=vector_jugador[event[1]]
                window.FindElement(evento).Update(image_filename=Coordenadas.asignar_color(evento,nivel,letra.lower()))
                window.FindElement(event).Update(image_filename='Letras/_fondo.png')
                coordenada_de_letras.append(evento)
                pos_validas=todas_las_pos(coordenada_de_letras, movimiento)
                palabra.append(letra)
                letras_usadas.append(event)
            if evento=='Posponer':
                window.FindElement(event).Update(image_filename="Letras/"+valores_letras[vector_jugador[event[1]]].lower()+"_fondo.png")
                event=evento
            if evento=='Terminar':
                event=evento
            ActivarDesactivarBoton(window, pos_de_letras,'habilitar',event)
        if event =='Verificar' and len(palabra)>=2: 
            verificacion=Verificar_palabra(''.join(palabra).lower(), nivel, tipo_de_palabra)
            if verificacion and tablero_aux[7][7]!=0 :
                nuevos=generar_letras(len(letras_usadas), letras_jugador, valores_letras)
                if len(nuevos)!=0:
                    actualizar_letras_jugador(window, letras_usadas, nuevos, valores_letras, vector_jugador)
                    puntos_palabra=calcular_puntos(coordenada_de_letras,tablero_aux,nivel,valores_letras,letras_jugador)
                    borrar_pos_usadas(coordenada_de_letras,pos_0)
                else:
                    event='Terminar'
                break
            else:
                volver_letras_a_posicion(window, tablero_aux, coordenada_de_letras, letras_usadas, vector_jugador, valores_letras,nivel)
                pos_validas=None
                palabra=[]
                letras_usadas=[]
                coordenada_de_letras=[]
                movimiento=''
        if event!=None:
            ActivarDesactivarBoton(window, ('Cambiar Fichas','Aceptar'),'habilitar' if (len(palabra)==0)else 'deshabilitar',event=None)
        if event=='Cambiar Fichas' and cantidad_veces_cambiado<3 and len(palabra)==0:
            tiempo_pausado=int(round(time.time() * 100))
            confirmar=sg.PopupYesNo("¿Está seguro que desea cambiar fichas? Recuerde que perdera su turno y no olvide clickear aceptar una vez seleccionadas las letras a cambiar",no_titlebar=True)
            if confirmar=="Yes":
                iniciar_tiempo_partida=iniciar_tiempo_partida+int(round(time.time() * 100))-tiempo_pausado
                iniciar_tiempo_jugada=iniciar_tiempo_jugada+int(round(time.time()*100))-tiempo_pausado 
                evento,letras_a_cambiar, contador_partida,contador_jugada =Devolver_letras_a_cambiar(window, valores_letras, vector_jugador, pos_de_letras,tiempo_maximo,tiempo_jugada, iniciar_tiempo_partida,iniciar_tiempo_jugada,contador_partida,contador_jugada)
                if evento!='Terminar' and contador_jugada<tiempo_jugada and evento!='Posponer':
                    nuevos=generar_letras(len(letras_a_cambiar), letras_jugador, valores_letras)
                    for i in letras_a_cambiar:
                        letras_jugador[valores_letras[vector_jugador[i[1]]]]['Cantidad']+=1
                    actualizar_letras_jugador(window, letras_a_cambiar, nuevos, valores_letras, vector_jugador)
                    cantidad_veces_cambiado+=1
                    if cantidad_veces_cambiado==3:
                        window.FindElement('Cambiar Fichas').Update(disabled=True)
                    break
                if (evento!='Terminar' and contador_jugada>=tiempo_jugada) or evento=='Terminar':
                    if evento=='Terminar':
                        event=evento
                    for i in letras_a_cambiar:
                        window.FindElement(i).Update(image_filename="Letras/"+valores_letras[vector_jugador[i[1]]].lower()+"_fondo.png")
            else:
                iniciar_tiempo_partida=iniciar_tiempo_partida+int(round(time.time() * 100))-tiempo_pausado
                iniciar_tiempo_jugada=iniciar_tiempo_jugada+int(round(time.time()*100))-tiempo_pausado 
        if event=='Posponer':
            tiempo_pausado=int(round(time.time() * 100))
            confirmar=sg.PopupYesNo("¿Esta seguro que desea posponer la partida?",no_titlebar=True)
            if confirmar=='Yes':
                volver_letras_a_posicion(window,tablero_aux, coordenada_de_letras, letras_usadas, vector_jugador, valores_letras,nivel)
                iniciar_tiempo_partida=iniciar_tiempo_partida+int(round(time.time()*100))-tiempo_pausado
                iniciar_tiempo_jugada=iniciar_tiempo_jugada+int(round(time.time()*100))-tiempo_pausado
                break
            iniciar_tiempo_partida=iniciar_tiempo_partida+int(round(time.time() * 100))-tiempo_pausado
            iniciar_tiempo_jugada=iniciar_tiempo_jugada+int(round(time.time()*100))-tiempo_pausado
        if contador_partida>=tiempo_maximo or event=='Terminar' :
            break
        if contador_jugada>=tiempo_jugada:
            volver_letras_a_posicion(window, tablero_aux, coordenada_de_letras, letras_usadas, vector_jugador, valores_letras,nivel)
            break
        if event ==None:
            exit()
    return (contador_partida, puntos_palabra, cantidad_veces_cambiado,''.join(palabra), event,iniciar_tiempo_partida,iniciar_tiempo_jugada,contador_jugada)

def Actualizar_lista_jugadas(window,lista,puntos=0,palabra="",id=""):
    if id=='Jugador':
        if len(palabra)!=0:
            if puntos==1 or puntos==-1:
                string='JUGADOR INGRESO {}, VALE {} PUNTO'.format(palabra, puntos)
            else:
                string='JUGADOR INGRESO {}, VALE {} PUNTOS'.format(palabra, puntos)
        else:
            string='JUGADOR NO INGRESO NINGUNA PALABRA'
    elif id=='Computadora':
        if len(palabra)!=0:
            if puntos==1 or puntos==-1:
                string="COMPU INGRESO {}, VALE {} PUNTO ".format(palabra,puntos)
            else:
                string="COMPU INGRESO {}, VALE {} PUNTOS ".format(palabra,puntos)
        else:
            string="COMPU NO INGRESO NINGUNA PALABRA"
    if id!="":
        lista.append(string)
    window.FindElement("datos").Update(values=lista)

def armar_diccionario_ordenado(datos,nivel):
    lista_ordenada=sorted(datos[nivel].items(),key=lambda valor:valor[1]["Puntaje"],reverse=True)
    if len(lista_ordenada)>=11:
        lista_ordenada=lista_ordenada[:10]
    diccionario={}
    for i in lista_ordenada:
        diccionario.setdefault(i[0],i[1])
    return diccionario 

def menor_tiempo(tiempo_anterior,tiempo_nuevo):
    nuevo=tiempo_nuevo.split(":")
    anterior=tiempo_anterior.split(':')
    ok=False
    if int(nuevo[0])<int(anterior[0]):
        ok=True
    elif  int(nuevo[0])==int(anterior[0])and int(nuevo[1])>int(anterior[1]):
        ok=True
    return ok

def guardar_resultado(puntos_total_jugador,contador_partida,nivel,nombre,fecha):
    if os.path.isfile("ranking_por_nivel.json"):
        with open("ranking_por_nivel.json","r")as archivo_ranking:
            datos=json.load(archivo_ranking)
            archivo_ranking.close()
    else:
        datos={"Facil":{},"Medio":{},"Dificil":{}}
    archivo_ranking=open("ranking_por_nivel.json","w")
    estructura={"Puntaje":puntos_total_jugador,"Tiempo":"{:02d}:{:02d}".format((contador_partida // 100) // 60, (contador_partida// 100) % 60),
    "Fecha":fecha.strftime("%d/%m/%Y"),"Hora":fecha.strftime("%H:%M:%S")}
    if  not nombre in datos[nivel].keys():
        datos[nivel].setdefault(nombre,estructura)
        diccionario=armar_diccionario_ordenado(datos,nivel)
        datos[nivel]=diccionario 
    elif (datos[nivel][nombre]['Puntaje']<puntos_total_jugador)or(datos[nivel][nombre]['Puntaje']==puntos_total_jugador and menor_tiempo(datos[nivel][nombre]["Tiempo"],estructura["Tiempo"])):
        datos[nivel][nombre]=estructura
        diccionario=armar_diccionario_ordenado(datos, nivel)
        datos[nivel]=diccionario   
    json.dump(datos,archivo_ranking,indent=4)
    archivo_ranking.close()          

def guardar_partida(*args):
    datos_de_partida={'puntos_total_jugador':args[0], 'vector_jugador':args[1],'letras_jugador':args[2],'cantidad_veces_cambiado':args[3],
    'puntos_total_computadora':args[4],'vector_compu':args[5],'letras_compu':args[6],"contador_partida":args[7],"iniciar_tiempo_partida":args[8],
    "tablero_aux":args[9],"Tiempo":args[10],'tipo_de_palabra':args[11],"lista_jugadas":args[12],"turno":args[13],"tiempo_act":args[14],
    "contador_jugada":args[15],"iniciar_tiempo_jugada":args[16],"tiempo_act_jugada":args[17],'dic':args[18]}
    archivo=open('partida_guardada.pickle','wb')
    pickle.dump(datos_de_partida,archivo)
    archivo.close()

def mostrar_resultado_partida(puntos_total_jugador,puntos_total_computadora):    
    if puntos_total_jugador>puntos_total_computadora:
        sg.PopupOK('Felicidades Ganaste!!!',no_titlebar=True)
    elif puntos_total_jugador<puntos_total_computadora:
        sg.PopupOK("Perdiste, vuelve a intentarlo",no_titlebar=True)
    else:
        sg.PopupOK('Has empatado con la computadora',no_titlebar=True)
        
def retornar_nombre():
	layout=[[sg.T('Registrar Partida', size=(50,1), justification='center')],
		   [sg.T("Ingrese un nombre: "),sg.InputText(key="Input")],
		   [sg.Button("OK", size=(7,1))],
		   [sg.T("El nombre debe tener más de 3 caracteres y menos de 12 caracteres",visible=False,key="advertencia")]   
	]
	window=sg.Window('',layout,no_titlebar=True,keep_on_top=True)
	while True:
		event, value=window.read()
		if event=='OK' and len(value["Input"])>=3 and len(value["Input"])<=12:
			break
		else:
			window.FindElement("advertencia").Update(visible=True)
	window.close()
	return value["Input"]

def Actualizar_variables_jugar(Dic_Letras_puntos_cantidad,dic,estructura):
    valores_letras=asociar_estructura()
    if estructura==None:
        tablero_aux=crear_tablero_aux()
        letras_compu=Dic_Letras_puntos_cantidad.copy()
        letras_jugador=Dic_Letras_puntos_cantidad.copy()
        iniciar_tiempo_partida=int(round(time.time()*100))  
        vector_jugador=generar_letras(7,letras_jugador,valores_letras)
        vector_compu=generar_letras(7,letras_compu,valores_letras)
        contador_partida=0
        puntos_total_jugador=0
        puntos_total_computadora=0
        lista_jugadas=[]
        turno=random.choice([True,False])
        cantidad_veces_cambiado=0
    else:
        tablero_aux=estructura['tablero_aux']
        letras_compu=estructura["letras_compu"]
        letras_jugador=estructura["letras_jugador"]
        iniciar_tiempo_partida=estructura['iniciar_tiempo_partida']
        vector_jugador=estructura["vector_jugador"]
        vector_compu=estructura["vector_compu"]
        contador_partida=estructura["contador_partida"]
        puntos_total_jugador=estructura["puntos_total_jugador"]
        puntos_total_computadora=estructura["puntos_total_computadora"]
        lista_jugadas=estructura["lista_jugadas"]
        turno=estructura["turno"]
        cantidad_veces_cambiado=estructura["cantidad_veces_cambiado"]
    tupla=(tablero_aux,letras_compu,letras_jugador,iniciar_tiempo_partida,vector_jugador,
            vector_compu,contador_partida,puntos_total_jugador,puntos_total_computadora,lista_jugadas,turno,
            cantidad_veces_cambiado, valores_letras)   
    
    return tupla

def restar_puntaje(puntos_total_jugador,puntos_total_computadora,vector_jugador,vector_compu,valores_letras,Dic_Letras_puntos_cantidad):
    total_atril_jugador=0
    total_atril_compu=0
    for i in vector_compu:
        total_atril_compu+=Dic_Letras_puntos_cantidad[valores_letras[i]]['Puntos']
    for i in vector_jugador:
        total_atril_jugador+=Dic_Letras_puntos_cantidad[valores_letras[i]]['Puntos']
    return(puntos_total_jugador-total_atril_jugador,puntos_total_computadora-total_atril_compu)

def posiciones_en_0(tablero_aux):
	pos_0=[]
	for i in range(0,15):
		for j in range(0,15):
			if tablero_aux[i][j]==0:
				pos_0.append((i,j))
	return pos_0

def iniciar_juego(window,Dic_Letras_puntos_cantidad,dic, tipo_de_palabra, tiempo_maximo,estructura):
	'''Función que inicializa las variables del juego y se empieza a jugar'''
	tupla_de_variables=Actualizar_variables_jugar(Dic_Letras_puntos_cantidad,dic,estructura)
	tablero_aux=tupla_de_variables[0]
	letras_compu=tupla_de_variables[1]
	letras_jugador=tupla_de_variables[2]
	iniciar_tiempo_partida=tupla_de_variables[3]
	vector_jugador=tupla_de_variables[4]
	vector_compu=tupla_de_variables[5]
	contador_partida=tupla_de_variables[6]
	puntos_total_jugador=tupla_de_variables[7]
	puntos_total_computadora=tupla_de_variables[8]
	lista_jugadas=tupla_de_variables[9]
	turno=tupla_de_variables[10]
	cantidad_veces_cambiado=tupla_de_variables[11]
	valores_letras=tupla_de_variables[12]
	maximo_jugada=dic['Tiempo2']*100
	pos_0=posiciones_en_0(tablero_aux)
	for i in range(0,7):
		window.FindElement(('a',i)).Update(image_filename="Letras/"+valores_letras[vector_jugador[i]].lower()+"_fondo.png")
	if estructura!=None:
		tiempo_act=estructura["tiempo_act"]
		iniciar_tiempo_partida=iniciar_tiempo_partida+int(round(time.time() * 100))-tiempo_act
		window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
	event=None
	ok=False
	while  contador_partida<tiempo_maximo and event!='Terminar' and event!='Posponer':
		if turno:
			if estructura==None or ok :
				iniciar_tiempo_jugada=int(round(time.time()*100))
				contador_jugada=0
			else:
				tiempo_act_jugada=estructura["tiempo_act_jugada"]
				iniciar_tiempo_jugada=estructura["iniciar_tiempo_jugada"]
				contador_jugada=estructura["contador_jugada"]
				iniciar_tiempo_jugada=iniciar_tiempo_jugada+int(round(time.time()*100))-tiempo_act_jugada
				window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: "+'{:02d}:{:02d}'.format((contador_jugada // 100) // 60, (contador_jugada// 100) % 60))
				ok=True
			contador_partida,puntos_palabra,cantidad_veces_cambiado,palabra, event,iniciar_tiempo_partida,iniciar_tiempo_jugada,contador_jugada=turno_jugador(window, tablero_aux, 
			vector_jugador, letras_jugador, valores_letras,dic['Nivel'],tipo_de_palabra,iniciar_tiempo_partida, tiempo_maximo, cantidad_veces_cambiado,contador_partida,maximo_jugada,iniciar_tiempo_jugada,contador_jugada,pos_0)
			if event!="Posponer":
				window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: 00:00")
				Actualizar_lista_jugadas(window,lista_jugadas,puntos_palabra,palabra='' if (contador_jugada>=maximo_jugada) else palabra,id="Jugador")
				puntos_total_jugador=puntos_total_jugador+puntos_palabra
				window.FindElement('Puntaje Jugador').Update('Tu Puntaje: '+str(puntos_total_jugador))
				if cantidad_veces_cambiado==5:
					break
				turno=False
		else:
			event,contador_partida,total_palabra,palabra=turno_compu(window,tablero_aux,valores_letras,vector_compu,iniciar_tiempo_partida,letras_compu,dic["Nivel"],tipo_de_palabra,contador_partida,pos_0)
			if event!="Posponer":
				Actualizar_lista_jugadas(window,lista_jugadas,total_palabra,palabra,"Computadora")
				puntos_total_computadora=puntos_total_computadora+total_palabra
				window.FindElement("Puntaje Computadora").Update("Puntaje Computadora: "+str(puntos_total_computadora),font=("Helvetica",15))
				turno=True
	if event !='Posponer':
		if sys.platform=="win32":
			window.Disable()
		for i in range(0,7):
			window.FindElement(i).Update(image_filename="Letras/"+valores_letras[vector_compu[i]].lower()+"_fondo.png")
		puntos_total_jugador,puntos_total_computadora=restar_puntaje(puntos_total_jugador,puntos_total_computadora,vector_jugador,vector_compu,valores_letras,Dic_Letras_puntos_cantidad)
		mostrar_resultado_partida(puntos_total_jugador,puntos_total_computadora)
		if puntos_total_jugador>puntos_total_computadora:
			window.BringToFront()
			nombre=retornar_nombre()
			fecha=datetime.now()
			guardar_resultado(puntos_total_jugador,contador_partida,dic["Nivel"],nombre,fecha)
	else:
		tiempo_act_jugada=int(round(time.time()*100))
		tiempo_act=int(round(time.time() * 100))
		guardar_partida(puntos_total_jugador,vector_jugador,letras_jugador,cantidad_veces_cambiado,puntos_total_computadora,vector_compu,
		letras_compu,contador_partida,iniciar_tiempo_partida,tablero_aux,tiempo_maximo,tipo_de_palabra,lista_jugadas,turno,tiempo_act,
		contador_jugada,iniciar_tiempo_jugada,tiempo_act_jugada,dic)
