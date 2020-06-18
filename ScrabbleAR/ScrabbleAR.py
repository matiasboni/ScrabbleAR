import PySimpleGUI as sg
import random
import time
import platform
import ctypes
import subprocess
import pattern.es
from pattern.es import parse
import itertools

def retornar_sistema_operativo():
    sistema=platform.system()
    return sistema

def retornar_tamaño_pantalla():
    if retornar_sistema_operativo()=="Windows":
        user32=ctypes.windll.user32
        user32.SetProcessDPIAware()
        ancho,alto=user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
        tamaño=(ancho,alto)
    elif retornar_sistema_operativo()=="Linux":
        tamaño= (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = subprocess.Popen(args,stdout=subprocess.PIPE)
        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            if "Screen" in line:
                tamaño = (int(line.split()[7]),  int(line.split()[9][:-1]))
    return tamaño

        
def crear_tablero_aux():
    '''Crea la matriz de 15x15 sin letras(todos 0) '''
    tablero_aux=[]
    for i in range(0,15):
        lista=[]
        for i in range(0,15):
            lista.append(0)
        tablero_aux.append(lista)
    return tablero_aux


def asociar_estructura():
    '''Crea el diccionario con los numeros asociados a una letra'''
    valores_letras={}
    caracter=65
    for i in range(1,27):
        valores_letras[i]=chr(caracter)
        caracter+=1
    valores_letras[27]="LL"
    valores_letras[28]="RR"
    return valores_letras


def puntaje_por_letra(lista):
    if len(lista)==0:
        dic1={"AEOSIUNLRT":1,"CDG":2, 'MBP':3, 'FHVY':4, 'J':6, 'KLLÑQRRWX':8, 'Z':10}
        dic2={'A':1,'E':1,'O':1,'S':1,'I':1,'U':1,'N':1,'L':1,'R':1,'T':1,'C':2,'D':2,'G':2,'M':3,'B':3,'P':3,'F':4,'H':4,'V':4,'Y':4,'J':6,'K':8,'LL':8,'Ñ':8,'Q':8,'RR':8,'W':8,'X':8,'Z':10}
    else:
        dic1={"AEOSIUNLRT":lista[0],"CDG":lista[1], 'MBP':lista[2], 'FHVY':lista[3], 'J':lista[4], 'KLLÑQRRWX':lista[5], 'Z':lista[6]}
        dic2={"A":lista[0],"E":lista[0],"O":lista[0],"S":lista[0],"I":lista[0],"U":lista[0],"N":lista[0],"L":lista[0],"R":lista[0],"T":lista[0],
        "C":lista[1],"D":lista[1],"G":lista[1],"M":lista[2],"B":lista[2],"P":lista[2],"F":lista[3],"H":lista[3],"V":lista[3],"Y":lista[3],
        "J":lista[4],"K":lista[5],"LL":lista[5],"Ñ":lista[5],"Q":lista[5],"RR":lista[5],"W":lista[5],"X":lista[5],"Z":lista[6]}
    return (dic1,dic2)

def cantidad_por_letra(lista):
    if len(lista)==0:
         dic={"AEOSIUNLRT":1,"CDG":2, 'MBP':3, 'FHVY':4, 'J':6, 'KLLÑQRRWX':8, 'Z':10}
    else:
        dic={"AEOSIUNLRT":lista[0],"CDG":lista[1], 'MBP':lista[2], 'FHVY':lista[3], 'J':lista[4], 'KLLÑQRRWX':lista[5], 'Z':lista[6]}
    return dic

def total_letras(dic):
    letras={"A":dic["AEOSIUNLRT"],"E":dic["AEOSIUNLRT"],"O":dic["AEOSIUNLRT"],"S":dic["AEOSIUNLRT"],
    "I":dic["AEOSIUNLRT"],"U":dic["AEOSIUNLRT"],"N":dic["AEOSIUNLRT"],"R":dic["AEOSIUNLRT"],
    "L":dic["AEOSIUNLRT"],"T":dic["AEOSIUNLRT"],"C":dic["CDG"],"D":dic["CDG"],
    "G":dic["CDG"],"M":dic["MBP"],"B":dic["MBP"],"P":dic["MBP"],"F":dic["FHVY"],
    "H":dic["FHVY"],"V":dic["FHVY"],"Y":dic["FHVY"],"J":dic["J"],
    "K":dic["KLLÑQRRWX"],"LL":dic["KLLÑQRRWX"],"Ñ":dic["KLLÑQRRWX"],"Q":dic["KLLÑQRRWX"],
    "RR":dic["KLLÑQRRWX"],"W":dic["KLLÑQRRWX"],"X":dic["KLLÑQRRWX"],"Z":dic["Z"]}
    return letras

def generar_letras(cantidad,dic,valores_letras):
    letras=[]
    aux=[]
    for i in valores_letras.keys():
        if valores_letras[i]!=0:
            aux.append(i)
    for i in range(cantidad):
        num=random.choice(aux)
        letras.append(num)
        dic[valores_letras[num]]=dic[valores_letras[num]]-1
        if dic[valores_letras[num]]==0:
            aux.remove(num)
    return letras

def descuento3 (nivel):
    if nivel=="NF" :
        return [(0,6),(0,8),(6,0),(6,14),(8,0),(8,14),(14,6),(14,8)]
    elif nivel=='ND':
        return[(0,3),(0,7),(0,10),(1,2),(2,1),(3,0),(2,5),(4,1),(3,10),(4,14),(5,5),(7,0),(7,14),(9,9),(10,0),(10,13),
    				(11,4),(11,14),(12,13),(13,12),(14,11),(14,4),(14,7),(12,9)]
    else:
        return [(1,1),(13,13),(1,13),(13,1)]
    
def descuento2(nivel):
    if nivel=='NF':
        return [(0,4),(0,10),(4,0),(4,14),(10,0),(10,14),(14,4),(14,10)]
    if nivel=='ND':
        return [(1,9),(3,4),(5,13),(9,1),(11,10),(13,5)]
    else:
        return [(2,2),(4,4),(10,10),(12,12),(2,12),(4,10),(12,2),(10,4)]

def descuento1(nivel):
    if nivel=='NF':
        return [(0,2),(0,12),(2,0),(2,14),(12,0),(12,14),(14,2),(14,12)]
    elif nivel=='ND':
        return [(1,6),(3,7),(4,6),(6,1),(6,4),(7,3),(7,11),(8,10),(8,13),(10,8),(11,7),(13,8)]
    else:
        return [(3,3),(5,5),(9,9),(11,11),(3,11),(5,9),(11,3),(9,5)]

def pos_palabra3(nivel):
    if nivel=='NF':
        return [(0,0),(0,14),(1,1),(1,13),(2,2),(2,12),(12,2),(12,12),(13,1),(13,13),(14,0),(14,14)]
    elif nivel=='ND':
        return [(0,0),(0,14),(14,0),(14,14)]
    else:
        return [(0,0),(0,14),(14,0),(14,14)]

def pos_palabra2(nivel):
    if nivel=='NF':
        return [(3,3),(3,11),(4,4),(4,10),(5,5),(5,9),(6,6),(6,8),(8,6),(8,8),(9,5),(9,9),(10,4),(10,10),(11,3),(11,11)]
    elif nivel=='ND':
        return [(5,9),(6,8),(8,6),(9,5)]
    else:
        return [(0,7),(7,0),(7,7),(7,14),(14,7)]

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
        return ("black","sky blue")
    elif coordenadas in letra3:
        return ("black","blue")
    elif coordenadas in palabra2:
        return ("black","green")
    elif coordenadas in palabra3:
        return ("black", "green2")
    elif coordenadas in descuen1:
        return ("black","OrangeRed")
    elif coordenadas in descuen2:
        return ("black","red")
    elif coordenadas in descuen3:
        return ("black","DarkRed")
    elif coordenadas==(7,7):
        return ("black","yellow")
    else:
        return  ("black","azure")

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
        return ("black","green yellow")
    elif coordenadas in letra3:
        return ("black","blue")
    elif coordenadas in palabra2:
        return ("black","green")
    elif coordenadas in palabra3:
        return ("black", "red")
    elif coordenadas in descuen1:
        return ("black","red")
    elif coordenadas in descuen2:
        return ("black","red2")
    elif coordenadas in descuen3:
        return ("black","red3")
    else:
        return  ("black","azure")

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
        return ("black","green yellow")
    elif coordenadas in letra3:
        return ("black","blue")
    elif coordenadas in palabra2:
        return ("black","green")
    elif coordenadas in palabra3:
        return ("black", "red")
    elif coordenadas in descuen1:
        return ("black","red")
    elif coordenadas in descuen2:
        return ("black","red2")
    elif coordenadas in descuen3:
        return ("black","red3")
    else:
        return  ("black","azure")

def retornar_tablero(nivel):
    datos={"size":(4,2),"pad":(0,0),"border_width":1}
    if nivel =='Facil':
        tablero=[
            [sg.Button('',key=(i,j),button_color=asignar_color_facil((i,j)), **datos,) for j in range(15)]for i in range(15)]
    elif nivel=='Medio':
        tablero=[
            [sg.Button('',key=(i,j), **datos, button_color=asignar_color_medio((i,j))) for j in range(15)]for i in range(15)]
    elif nivel=='Dificil':
        tablero=[
            [sg.Button('',key=(i,j),button_color=asignar_color_dificil((i,j)), **datos) for j in range(15)]for i in range(15)
            ]
    return tablero
        

def tipo_de_palabras(nivel):
    if nivel=='Facil':
        return 'Todas Las Palabras'
    elif nivel=='Medio':
        return 'Verbos y Sustantivos'
    else:
        lista=['Adjetivos', 'Verbos']
        palabra=random.randrange(len(lista))
        return lista[palabra]

def conjunto_de_letras(punto1,cantidad1, estilo_col3):
    texto= [[sg.Text("LETRAS", **estilo_col3)],
            [sg.Text("A,E,O,S,I,U,N,L,R,T: ",**estilo_col3)],
            [sg.Text("C,D,G: ",**estilo_col3)],
            [sg.Text("M,B,P: ",**estilo_col3)],
            [sg.Text("F,H,V,Y: ",**estilo_col3)],
            [sg.Text("J: ",**estilo_col3)],
            [sg.Text("K,LL,Ñ,Q,RR,W,X: ",**estilo_col3)],
            [sg.Text("Z: ",**estilo_col3)]]
    keys= punto1.keys()
    puntos=[[sg.T(str(punto1[i]),**estilo_col3)]for i in keys]
    cantidad=[[sg.T(str(cantidad1[i]),**estilo_col3)]for i in keys]

    pun=[[sg.Text("PUNTOS", **estilo_col3)]]
    pun.extend(puntos)
    can=[[sg.Text("CANTIDAD", **estilo_col3)]]
    can.extend(cantidad)
    conjunto=[
                [sg.Column(texto),sg.Column(pun),sg.Column(can)]]
    return conjunto

def buscar_combinacion(vector_compu,valores_letras):
	letras=[]
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
		if (aux.lower() in pattern.es.lexicon.keys() or aux.lower() in pattern.es.spelling.keys()) and len(i)>=2:
			palabra=aux
			conjunto=i
			break
	if palabra!="":
		for i in conjunto:
			posicion=letras.index(i)
			posiciones.append(posicion)
			letras[posicion]="0"
	return(palabra,posiciones)

def actualizar_tablero(posiciones,orientacion,pos,window,valores_letras,vector_compu):
    if orientacion=="Vertical":
        for i in range(0,len(posiciones)):
            window.FindElement((pos[0]+i,pos[1])).Update(text=valores_letras[vector_compu[posiciones[i]]])
    elif orientacion=="Horizontal":
        for i in range(0,len(posiciones)):
             window.FindElement((pos[0],pos[1]+i)).Update(text=valores_letras[vector_compu[posiciones[i]]])

def actualizar_matriz(tablero_aux,orientacion,pos,posiciones,vector_compu):
    cant=0
    if orientacion=="Vertical":
        for i in posiciones:
            tablero_aux[pos[0]+cant][pos[1]]=vector_compu[i]
            cant+=1
    elif orientacion=="Horizontal":
        for i in posiciones:
            tablero_aux[pos[0]][pos[1]+cant]=vector_compu[i]
            cant+=1


def vertical_compu(window,pos,tablero_aux,posiciones,vector_compu,valores_letras):
    ok=False
    if pos[0]+len(posiciones)<=14:
        ok=True
        for i in range(0,len(posiciones)):
            if tablero_aux[pos[0]+i][pos[1]]!=0:
                ok=False
        if ok:
            actualizar_tablero(posiciones,"Vertical",pos,window,valores_letras,vector_compu)
            actualizar_matriz(tablero_aux,"Vertical",pos,posiciones,vector_compu)
    return ok


def horizontal_compu(window,pos,tablero_aux,posiciones,vector_compu,valores_letras):
    ok=False
    if pos[1]+len(posiciones)<=14:
        ok=True
        for i in range(0,len(posiciones)):
            if tablero_aux[pos[0]][pos[1]+i]!=0:
                ok=False
        if ok:
            actualizar_tablero(posiciones,"Horizontal",pos,window,valores_letras,vector_compu)
            actualizar_matriz(tablero_aux,"Horizontal",pos,posiciones,vector_compu)
    return ok

def actualizar_vector_compu(vector_compu,posiciones,valores_letras,cantidad_letras_compu):
    letras=generar_letras(len(posiciones),cantidad_letras_compu,valores_letras)
    indice=0
    for i in range(0,len(letras)):
        vector_compu[posiciones[indice]]=letras[i]
        indice+=1

def calcular_puntos(botones_del_tablero,tablero_aux,nivel,valores_letras,puntos_de_letras):
    des1=descuento1(nivel)
    des2=descuento2(nivel)
    des3=descuento3(nivel)
    pal2=pos_palabra2(nivel)
    pal3=pos_palabra3(nivel)
    letra2=pos_letra2(nivel)
    letra3=pos_letra3(nivel)
    total=0
    cant_pal2=0
    cant_pal3=0
    for i in botones_del_tablero:
        valor_letra=puntos_de_letras[valores_letras[tablero_aux[i[0]][i[1]]]]
        if i in letra2:
            valor_letra=valor_letra*2
        elif i in letra3:
            valor_letra=valor_letra*3
        elif i in des1:
            valor_letra=valor_letra-1
        elif i in des2:
            valor_letra=valor_letra-2
        elif i in des3:
            valor_letra=valor_letra-3
        elif i in pal2:
            cant_pal2+=1
        elif i in pal3:
            cant_pal3+1
        total=total+valor_letra
    if cant_pal2!=0:
        for i in range(0,cant_pal2):
            total=total*2
    if cant_pal3!=0:
        for i in range(0,cant_pal3):
            total=total*3
    return total 
    
def turno_compu(window,tablero_aux,valores_letras,vector_compu,contador_partida,cantidad_letras_compu,nivel,puntos_de_letras):
    contador_partida+=1
    window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
    palabra,posiciones=buscar_combinacion(vector_compu,valores_letras)
    if palabra!="":
        if tablero_aux[7][7]==0:
            orientacion=random.choice(["Vertical","Horizontal"])
            if orientacion=="Vertical":
                pos=(random.randint(7-len(palabra)+1,7),7)
            else:
                pos=(7,random.randint(7-len(palabra)+1,7))
            actualizar_tablero(posiciones,orientacion,pos,window,valores_letras,vector_compu)
            actualizar_matriz(tablero_aux,orientacion,pos,posiciones,vector_compu)
        else:
            ok=False
            while not ok:
                pos=(random.randint(0,14),random.randint(0,14))
                while tablero_aux[pos[0]][pos[1]]!=0:
                    pos=(random.randint(0,14),random.randint(0,14))
                orientacion=random.choice(["Vertical","Horizontal"])
                if orientacion=="Vertical":
                    ok=vertical_compu(window,pos,tablero_aux,posiciones,vector_compu,valores_letras)
                    if not ok:
                        ok=horizontal_compu(window,pos,tablero_aux,posiciones,vector_compu,valores_letras)
                else:
                    ok=horizontal_compu(window,pos,tablero_aux,posiciones,vector_compu,valores_letras)
                    if not ok:
                        ok=vertical_compu(window,pos,tablero_aux,posiciones,vector_compu,valores_letras)
        actualizar_vector_compu(vector_compu,posiciones,valores_letras,cantidad_letras_compu)
    return contador_partida

def actualizar_letras_jugador(window, letras_a_cambiar, nuevos, valores_letras, vector_jugador):
	cant=0
	for i in letras_a_cambiar:
		vector_jugador[i[1]]=nuevos[cant]
		window.FindElement(i).Update(valores_letras[nuevos[cant]])
		cant+=1 

def forma_de_movimiento(pos_tupla, ultimo):
	#defino si las letras se ponen en horizontal o vertical
	if ultimo[1]>pos_tupla[1]:
		return 'horizontal'
	else:
		return 'vertical'

def horizontal(ultimo):
	return [(ultimo[0],ultimo[1]+1)]

def vertical(ultimo):
	return [(ultimo[0]+1,ultimo[1])]

def posPosibles(evento):
    pos_posibles=[(evento[0]+1, evento[1]), (evento[0], evento[1]+1)]
    return pos_posibles

def todas_las_pos(coordenadas_palabras, movimiento, cant, posiciones_validas):
	if cant==0:
		posiciones_validas=posPosibles(coordenadas_palabras[0])
	if movimiento=='horizontal':
		posiciones_validas=horizontal(coordenadas_palabras[len(coordenadas_palabras)-1])
	elif movimiento =='vertical':
		posiciones_validas = vertical(coordenadas_palabras[len(coordenadas_palabras)-1])
	return posiciones_validas

def Definir_tipo(tipo_de_palabra):
	if tipo_de_palabra == 'Verbos':
		return 'VB'
	elif tipo_de_palabra == 'Adjetivos':
		return 'JJ'

def Verificar_palabra(palabra, nivel, tipo_de_palabra):
	if palabra in pattern.es.lexicon.keys() or palabra in pattern.es.spelling.keys():
		palabra_analizada=parse(palabra).split('/')
		tipo=palabra_analizada[1]
		if nivel=='Facil':
			return True
		if nivel=='Medio' and tipo in('JJ','VB'):
			return True
		tipo_random=Definir_tipo(tipo_de_palabra)
		if nivel=='Dificil' and tipo==tipo_random:
			return True
		else:
			return False
	else:
		return False

def volver_letras_a_posicion(window,tablero_aux,coordenada_letras, letras_usadas, vector_jugador, valores_letra):
    for i in letras_usadas:
        window.FindElement(i).Update(valores_letra[vector_jugador[i[1]]])
    for i in coordenada_letras:
        window.FindElement(i).Update('')
        tablero_aux[i[0]][i[1]]=0
    return tablero_aux
	
def ActivarDesactivarBoton(window, pos_letras, event, accion):
	if (accion =='desabilitar'):
		aux={'disabled':True}
	else:
		aux={'disabled':False}
	for i in pos_letras:
		if i!=event:
			window.FindElement(i).Update(**aux)

def Devolver_letras_a_cambiar(window, valores_letras, vector_jugador, pos_de_letras, contador_partida, tiempo_maximo):
	letras_a_cambiar=[]
	evento=None
	while True:
		evento, values1=window.read(timeout=2)
		contador_partida+=1
		window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100)// 60, (contador_partida// 100)% 60))
		if evento in pos_de_letras:
			if evento in letras_a_cambiar:
				window.FindElement(evento).Update(valores_letras[vector_jugador[evento[1]]])
				letras_a_cambiar.remove(evento)
			else:
				letras_a_cambiar.append(evento)
				window.FindElement(evento).Update('')
		if evento =='Aceptar':
			break
		if contador_partida==tiempo_maximo:
			break
	return (letras_a_cambiar, contador_partida)

def turno_jugador(window,tablero_aux,vector_jugador, cantidad_letras_jugador, valores_letras,nivel,tipo_de_palabra, contador_partida, pos_de_letras, puntos_de_letras, tiempo_maximo):
	pos_validas=None
	palabra=[]
	coordenada_de_letras=[]
	letras_usadas=[]
	cant=0
	movimiento=''
	while True:
		event, values=window.read(timeout=2)
		contador_partida+=1
		window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
		if event in pos_de_letras:
			ActivarDesactivarBoton(window, pos_de_letras, event, 'desabilitar')
			evento=None
			while True:
				evento, values1= window.read(timeout=2)
				contador_partida+=1
				window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60,(contador_partida// 100) % 60 ))
				if evento==event:
					break
				if not evento in('__TIMEOUT__',None, event) and tablero_aux[evento[0]][evento[1]]==0:
					if pos_validas!=None:
						if evento in pos_validas:
							break
					else:
						break 
				print (evento, pos_validas)      
			if evento!=event:
				if cant==1:
					movimiento= forma_de_movimiento(coordenada_de_letras[0],evento)
				letra=valores_letras[vector_jugador[event[1]]]
				palabra.append(letra)
				tablero_aux[evento[0]][evento[1]]=vector_jugador[event[1]]
				window.FindElement(evento).Update(letra)
				window.FindElement(event).Update('')
				coordenada_de_letras.append(evento)
				pos_validas=todas_las_pos(coordenada_de_letras, movimiento, cant, pos_validas)
				print('movimiento: '+movimiento,' ', evento,' ',pos_validas)
				cant+=1
				letras_usadas.append(event)
			ActivarDesactivarBoton(window, pos_de_letras, event, 'habilitar')
		if event =='Verificar' and len(palabra)>=2: 
			verificacion=Verificar_palabra(''.join(palabra).lower(), nivel, tipo_de_palabra)
			if verificacion and tablero_aux[7][7]!=0 :
				nuevos=generar_letras(len(letras_usadas), cantidad_letras_jugador, valores_letras)
				actualizar_letras_jugador(window, letras_usadas, nuevos, valores_letras, vector_jugador)
				total_palabra_puntos=calcular_puntos(coodenada_de_letras,letras_usadas, puntos_de_letras)
			else:
				tablero_aux=volver_letras_a_posicion(window, tablero_aux, coordenada_de_letras, letras_usadas, vector_jugador, valores_letras)
				movimiento=''
				pos_validas=None
				cant=0
				palabra=[]
				letras_usadas=[]
				coordenada_de_letras=[]
		if event=='Cambiar Fichas':
			letras_a_cambiar, contador_partida =Devolver_letras_a_cambiar(window, valores_letras, vector_jugador, pos_de_letras, contador_partida,tiempo_maximo)
			nuevos=generar_letras(len(letras_a_cambiar), cantidad_letras_jugador, valores_letras)
			for i in letras_a_cambiar:
				cantidad_letras_jugador[valores_letras[vector_jugador[i[1]]]]+=1
			actualizar_letras_jugador(window, letras_a_cambiar, nuevos, valores_letras, vector_jugador)
		if event in (None, 'Terminar'):
			break
		if contador_partida==tiempo_maximo:
			break
	return contador_partida

def jugar(window,cantidad_de_letras,dic, tipo_de_palabra, tiempo_maximo):
	tablero_aux=crear_tablero_aux()
	valores_letras=asociar_estructura()
	cantidad_letras_compu=total_letras(cantidad_de_letras)
	cantidad_letras_jugador=total_letras(cantidad_de_letras)
	iniciar_tiempo_partida=int(round(time.time()*100))  
	vector_jugador=generar_letras(7,cantidad_letras_jugador,valores_letras)
	vector_compu=generar_letras(7,cantidad_letras_compu,valores_letras)
	aux=puntaje_por_letra(dic['ListaPuntos'])
	puntos_de_letras=aux[1]
	contador_partida=0
	pos_de_letras=[]
	for i in range(0,7):
		pos_de_letras.append(('a',i))
		window.FindElement(('a',i)).Update(valores_letras[vector_jugador[i]])
	turno=random.choice([True,False])
	turno=True
	while contador_partida!=tiempo_maximo:
		if turno:
			contador_partida=turno_jugador(window, tablero_aux, vector_jugador, cantidad_letras_jugador, valores_letras,dic['Nivel'],tipo_de_palabra,
			contador_partida, pos_de_letras, puntos_de_letras, tiempo_maximo)
			turno=False
		else:
			contador_partida=turno_compu(window,tablero_aux,valores_letras,vector_compu,contador_partida,cantidad_letras_compu,dic["Nivel"],puntos_de_letras)
              

def tablero_de_juego(dic):

    tablero=retornar_tablero(dic['Nivel'])
    aux=puntaje_por_letra(dic['ListaPuntos'])
    puntos_de_letras=aux[0]
    cantidad_de_letras=cantidad_por_letra(dic["ListaFichas"])
    tipo_de_palabra=tipo_de_palabras(dic['Nivel'])
    tiempo_maximo=dic['Tiempo']*6000


    columna1=[  [sg.Button('Iniciar', size=(11,2),auto_size_button=True)],
                [sg.Button("Posponer",size=(11,2))],
				[sg.Button('Terminar', size=(11,2),auto_size_button=True)],
                [sg.Text("",size=(1,3))],
                [sg.Text('Tiempo Partida: 00:00',key="Tiempo Partida",auto_size_text=True, font=("Helvetica",15))],
                [sg.Text("Tiempo Jugada: 00:00",key="Tiempo Jugada",auto_size_text=True,font=("Helvetica",15))],
                [sg.Text("Tu Puntaje: 00",auto_size_text=True,key="Puntaje Jugador",font=("Helvetica",15))],
                [sg.Text("Puntaje Computadora: 00",key="Puntaje Computadora",auto_size_text=True,font=("Helvetica",15))]
                ]

    letras_compu=[[sg.Button("",key=i ,size=(5,2)) for i in range(7)]]

    letras_usuario=[[sg.Button("",key=('a',a), size=(5,2)) for a in range(7)]]

    letras_con_otro_button=[[sg.Button('Verificar', size=(6,2)),sg.Column(letras_usuario),sg.Button("Cambiar Fichas",size=(6,2)), sg.Button('Aceptar', size=(6,2))]]

    columna2=[  [sg.Text('SCRABBLEAR', size=(100,1), justification='center')],
                [sg.Column(letras_compu, justification='center')],
				[sg.Column(tablero,justification="center")],
				[sg.Column(letras_con_otro_button, justification='center')]]

    estilo_col3={"auto_size_text":True,"justification":'left',"font":('Helvetica',10), 'relief':sg.RELIEF_RIDGE}

    conjunto1=conjunto_de_letras(puntos_de_letras,cantidad_de_letras, estilo_col3)

    columna3=[  [sg.Text("",size=(25,1))],
                [sg.Text('CONSIDERACIONES',justification="center",auto_size_text=True,font=("Helvetica",20))],
				[sg.Text("NIVEL:"+dic["Nivel"],**estilo_col3)],
                [sg.Column(conjunto1, pad=(0,0))],
                [sg.Text(tipo_de_palabra)],
                [sg.Text("TIEMPO: "+str(dic["Tiempo"])[0]+" Min",auto_size_text=True,justification="left",font=("Helvetica,12"))],
                [sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Descuento 1",justification="left",auto_size_text=True),sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Letra x2",justification="left",auto_size_text=True)],
                [sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Descuento 2",justification="left",auto_size_text=True),sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Letra x3",justification="left",auto_size_text=True)],
                [sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Descuento 3",justification="left",auto_size_text=True),sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Palabra x2",justification="left",auto_size_text=True)],
                [sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Comienzo",justification="left",size=(9,0)),sg.Button("",size=(2,1),button_color=("red","red")),sg.Text("Palabra x3",justification="left",auto_size_text=True)],
             ]

    layout= [
			    [sg.Column(columna1), sg.Column(columna2), sg.Column(columna3)]]

    window=sg.Window('ScrabbleAR', layout, default_element_size=(30, 1), return_keyboard_events=True, no_titlebar=False,
						grab_anywhere=True,margins=(0,0),size=retornar_tamaño_pantalla(),element_justification="center")
    while True:
        event,values=window.read()
        if event=="Iniciar":
            break
        if event in (None,'Terminar'):
            break
    if not event in (None,"Terminar"):
        jugar(window,cantidad_de_letras,dic, tipo_de_palabra, tiempo_maximo)
    else:
        window.close()

def maximo_de_tiempo(nivel):
    if nivel=='Dificil':
        return (1, 8)
    elif nivel=='Facil':
        return (1,12)
    else:
        return (1,10)

def Actualizar_diccionario(diccionario, values):
    diccionario['Tiempo']=values['time']
    diccionario['ListaPuntos']=[values['p1'],values['p2'],values['p3'],values['p4'],values['p5'],values['p6'],values['p7']]
    diccionario['ListaFichas']=[values['c1'],values['c2'],values['c3'],values['c4'],values['c5'],values['c6'],values['c7']]
    
def Configuracion_de_juego(diccionario):
    maximo_de_cantidad=[1,2,3,4,5,6,7,8,9,10,11]
    nivel=[
            [sg.Radio('Dificil',1, size=(20,1),key='Dificil',font=('Helvetica', 15), enable_events=True)],
            [sg.Radio('Medio',1, size=(20,1),default=True,key='Medio',font=('Helvetica', 15), enable_events=True)],
            [sg.Radio('Facil',1, size=(20,1),key='Facil',font=('Helvetica', 15), enable_events=True)],]

    tiempo=[[sg.T('Tiempo de Juego',justification='center')],
            [sg.Slider(default_value=6,key='time', orientation='h')]]

    estilo={'size':(30,1) , 'justification':'center', 'font':('Helvetica', 20), 'relief':sg.RELIEF_RIDGE}

    Configuracion=[ [sg.Text('NIVEL',**estilo)],
                    [sg.Column(nivel), sg.Column(tiempo)],
                    [sg.Text('Puntaje de las Fichas',**estilo)],
                    [sg.T('A, E, O, S, I, U, N, L, R, T: ', size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=1,size=(5,1), key='p1')],
                    [sg.T('C, D, G: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=2,size=(5,1), key='p2')],
                    [sg.T('M, B, P: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=3,size=(5,1), key='p3')],
                    [sg.T('F, H, V, Y: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=4,size=(5,1), key='p4')],
                    [sg.T('J: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=5,size=(5,1), key='p5')],
                    [sg.T('K, LL, Ñ, Q, RR, W, X: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=6,size=(5,1), key='p6')],
                    [sg.T('Z: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=7,size=(5,1), key='p7')],
                    [sg.T('Cantidad de Fichas por Letra', **estilo)],
                    [sg.T('A, E, O, S, I, U, N, L, R, T: ', size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=11,size=(5,1), key='c1')],
                    [sg.T('C, D, G: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=6,size=(5,1), key='c2')],
                    [sg.T('M, B, P: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=5,size=(5,1), key='c3')],
                    [sg.T('F, H, V, Y: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=4,size=(5,1), key='c4')],
                    [sg.T('J: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=3,size=(5,1), key='c5')],
                    [sg.T('K, LL, Ñ, Q, RR, W, X: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=3,size=(5,1), key='c6')],
                    [sg.T('Z: ',size=(20,1)),sg.InputCombo(maximo_de_cantidad,default_value=1,size=(5,1), key='c7')],
                    [sg.Button('Guardar Configuracion', size=(20,1))]
                    ]
    window=sg.Window('Configuracion', Configuracion)
    while True:
        event,values=window.read()
        if event in ('Dificil','Medio', 'Facil'):
            diccionario['Nivel']=event
            maximo=maximo_de_tiempo(event)
            window.FindElement('time').Update(range=maximo)
        elif event in ('Guardar Configuracion', None):
            Actualizar_diccionario(diccionario, values)
            break
    window.close()
    
def main():
    menu=[
         [sg.Text("SCRABBLEAR",justification="center",auto_size_text=True,font=("Helvetica",130)) ],
         [sg.Button("Jugar",size=(60,4))],
         [sg.Button("Configuración",size=(60,4))],
         [sg.Button("Ranking",size=(60,4),disabled=True)],
         [sg.Button("Salir",size=(60,4))] 
         ]
         
    window=sg.Window("SCRABBLEAR",menu,element_justification="center",font=("Helvetica",15),size=retornar_tamaño_pantalla())
    diccionario={'Nivel':'Medio', 'Tiempo':6, 'ListaPuntos':[], 'ListaFichas':[] }
    while True:
        event,values=window.read()
        if event=='Jugar':
            window.close()
            tablero_de_juego(diccionario)
        elif event=='Configuración':
            Configuracion_de_juego(diccionario)
        elif event=='Ranking':
            Ranking()
        elif event in (None, 'Salir'):
            break
    window.close()

if __name__=='__main__':
    main()
