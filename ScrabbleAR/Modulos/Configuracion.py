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

def maximo_de_tiempo(nivel):
    '''Función que retorna el rango de tiempo para cada nivel'''
    if nivel=='Dificil':
        return (1, 8)
    elif nivel=='Facil':
        return (1,12)
    else:
        return (1,10)

def Actualizar_diccionario(diccionario, values,Claves,window):
	'''Función que actualiza la estructura del diccionario segun la configuración realizada del juego'''
	if values['time']!=None:
		diccionario['Tiempo2']=values['time2']
		diccionario['Tiempo']=values['time']
		key=['P1','C1']
		key2=['ListaPuntos','ListaFichas']
		for i in range(2):
			diccionario[key2[i]]=[]
			for j in Claves[key[i]]:
				diccionario[key2[i]].append(int(window.FindElement(j).GetText()))
				
def Actualizar_Configuracion(diccionario):
    '''Función que retorna y actualiza las variables de la pantalla configuración'''
    if diccionario['Nivel']=='Facil':
        lista=[False,False,True]
    elif diccionario['Nivel']=='Medio':
        lista=[False,True,False]
    else:
        lista=[True,False,False]
    puntos=diccionario['ListaPuntos']
    cantidad=diccionario['ListaFichas']    
    return (puntos, cantidad,lista)    

def conjunto_letras_confi(defaultP,defaultC):
	'''Función que retorna la estructura de los conjuntos de letras con los puntos y cantidades a configurar'''
	dato={'size':(20,1),'font':('Calibri', 15)} 
	Estilo_tex={'font':('Calibri',20), 'background_color':"LightBlue",'text_color':'#0F0F4C','pad':(5,5)}
	letras=[[sg.T('LETRAS',size=(15,1),justification='center',**Estilo_tex)],
			[sg.T('A, E, O, S, I, U, N, L, R, T:',**dato)],
			[sg.T('C, D, G: ',**dato)],
			[sg.T('M, B, P: ',**dato)],
			[sg.T('F, H, V, Y: ',**dato)],
			[sg.T('J: ',**dato)],
			[sg.T('K, LL, Ñ, Q, RR, W, X:',**dato)],
			[sg.T('Z: ',**dato)]]
	if sys.platform!='linux':
		Estilo1={'pad':(3,5),'button_color':('#000000','LightBlue')}
		Estilo2={'size':(4,1),'pad':(6,5),'button_color':('#000000','LightBlue')}
	else:
		Estilo1={'pad':(3,1),'button_color':('#000000','LightBlue'),'size':(1,1)}
		Estilo2={'size':(1,1),'pad':(5,3),'button_color':('#000000','LightBlue')}
	Puntos=[[sg.Button('◄',key='P0'+str(i),**Estilo1),sg.Button(str(defaultP[i]),key='P1'+str(i),**Estilo2),sg.Button('►',key='P2'+str(i),**Estilo1)]for i in range(7)]
	Cantidad=[[sg.Button('◄',key='C0'+str(i),**Estilo1),sg.Button(str(defaultC[i]),key='C1'+str(i),**Estilo2),sg.Button('►',key='C2'+str(i),**Estilo1)]for i in range(7)]
	pun=[[sg.T('PUNTOS',auto_size_text=True,**Estilo_tex)]]
	can=[[sg.T('CANTIDAD',auto_size_text=True,**Estilo_tex)]]
	pun.extend(Puntos)
	can.extend(Cantidad)
	return [[sg.Column(letras),sg.VerticalSeparator(),sg.Column(pun,key='puntos_letras'),sg.VerticalSeparator(),sg.Column(can)]]
    
def Retornar_nivel(lista):
	'''Función que retorna la estructura de los niveles'''
	dato={'size':(12,1),'font':('Calibri',20), 'enable_events':True}
	nivel=[ [sg.T('NIVEL',pad=(6,5),relief=sg.RELIEF_SOLID,justification='center',background_color="LightBlue",text_color='#0F0F4C',font=('Calibri',23),size=(13,1))],
			[sg.Radio('Difícil',1,default=lista[0],key='Dificil',**dato)],
			[sg.Radio('Medio',1,default=lista[1],key='Medio',**dato)],
			[sg.Radio('Fácil',1,default=lista[2],key='Facil',**dato)]]
	return nivel
    
def retornar_tiempo(dic):
	'''Función que retorna la estructura del tiempo de jugada y tiempo de partida'''
	estilo2={'pad':(5,5),'size':(15,1),'font':('Calibri',23)}
	if sys.platform!="linux":
		estilo={'size':(25,1),'font':('calibre',13)}
	else:
		estilo={'size':(30,1),'font':('calibre',11)}
		estilo2['size']=(14,1)
	tiempo=[[sg.T('TIEMPO',justification='center',background_color="LightBlue",text_color='#0F0F4C',**estilo2)],
			[sg.T('Tiempo de Partida',**estilo)],
			[sg.Slider(default_value=dic['Tiempo'],key='time', orientation='h')],
			[sg.T('Tiempo de Jugada (En seg)',**estilo),sg.T('',size=(1,1),font=('calibri',7 if (sys.platform!='linux') else 1))],
			[sg.Slider(range=(10,60),default_value=dic['Tiempo2'],key='time2',orientation='h')]]
	return tiempo

def Actualizar_texto(window,accion,event,key1,key2, Claves):
	'''Función que actualiza el texto de un botón que contiene la estructura de los puntos y las cantidades'''
	pos=Claves[key1].index(event)
	clave=Claves[key2][pos]
	if accion =='descontar':
		dato=int(window.FindElement(clave).GetText())
		if dato>=2:
			dato-=1
			window.FindElement(clave).Update(str(dato))
	elif accion=='incrementar':
		dato=int(window.FindElement(clave).GetText())
		if dato<=10:
			dato+=1
			window.FindElement(clave).Update(str(dato))

def generar_claves():
	'''Función que genera las claves de los botones que contiene la estructura de los puntos y las cantidades'''
	dic_claves={'P0':[],'P1':[],'P2':[],'C0':[],'C1':[],'C2':[]}
	for i in range(3):
		for j in range(7):
			dic_claves['P'+str(i)].append('P'+str(i)+str(j))
			dic_claves['C'+str(i)].append('C'+str(i)+str(j))
	return dic_claves

def Configuracion_de_juego(diccionario):
	'''Función que define y muestra la pantalla de configuración para que
	se realizen los cambios por parte del jugador'''
	puntos, cantidad, lista=Actualizar_Configuracion(diccionario)
	fichas=conjunto_letras_confi(puntos,cantidad)
	nivel=Retornar_nivel(lista)
    
	tiempo=retornar_tiempo(diccionario)
	estilo={'size':(32,1) if (sys.platform!='linux') else (30,1), 'justification':'center', 'font':('Calibri', 24), 'relief':sg.RELIEF_RIDGE}
	Configuracion=[ [sg.T('CONFIGURACIÓN',**estilo, background_color="LightBlue",text_color='#0F0F4C')],
					[sg.T('')],
					[sg.Frame('',layout=[[sg.Column(nivel),sg.VerticalSeparator(), sg.Column(tiempo)]],pad=(3,0))],
					[sg.Frame('',layout=fichas,pad=(3,0))],
					[sg.Button('', image_filename='Imagenes/guardar configuracion.png',key='Guardar Configuración')]
					]
					
	Configuracion_conFrame=[[sg.Frame('',layout=Configuracion)]]
	window=sg.Window('Configuración', Configuracion_conFrame,keep_on_top=True,no_titlebar=True)
	Claves=generar_claves()
	while True:
		event,values=window.read()
		if event in ('Dificil','Medio', 'Facil'):
			diccionario['Nivel']=event
			maximo=maximo_de_tiempo(event)
			window.FindElement('time').Update(range=maximo)
		elif event in ('Guardar Configuración', None):     
			Actualizar_diccionario(diccionario, values,Claves,window)
			break
		if event in Claves['P0']:
			Actualizar_texto(window,'descontar',event,'P0','P1',Claves)
		if event in Claves['P2']:
			Actualizar_texto(window,'incrementar',event,'P2','P1',Claves)
		if event in Claves['C0']:
			Actualizar_texto(window,'descontar',event,'C0','C1',Claves)
		if event in Claves['C2']:
			Actualizar_texto(window,'incrementar',event,'C2','C1',Claves)
	window.close()


