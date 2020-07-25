import PySimpleGUI as sg

def maximo_de_tiempo(nivel):
    '''Función que retorna el rango de tiempo para cada nivel'''
    if nivel=='Dificil':
        return (1, 8)
    elif nivel=='Facil':
        return (1,12)
    else:
        return (1,10)

def Actualizar_diccionario(diccionario, values):
	'''Función que actualiza la estructura del diccionario segun la configuración realizada del juego'''
	print(values)
	if values['time']!=None:
		diccionario['Tiempo2']=values['time2']
		diccionario['Tiempo']=values['time']
		

def Actualizar_Configuracion(diccionario):
    '''Función que retorna y actualiza los valores por defecto de la pantalla configuración'''
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
	Estilo1={'pad':(3,5),'button_color':('#000000','LightBlue')}
	Estilo2={'size':(4,1),'pad':(6,5),'button_color':('#000000','LightBlue')}
	Puntos=[[sg.Button('◄',key='P0'+str(i),**Estilo1),sg.Button(str(defaultP[i]),key='P1'+str(i),**Estilo2),sg.Button('►',key='P2'+str(i),**Estilo1)]for i in range(7)]
	Cantidad=[[sg.Button('◄',key='C0'+str(i),**Estilo1),sg.Button(str(defaultC[i]),key='C1'+str(i),**Estilo2),sg.Button('►',key='C2'+str(i),**Estilo1)]for i in range(7)]
	pun=[[sg.T('PUNTOS',auto_size_text=True,**Estilo_tex)]]
	can=[[sg.T('CANTIDAD',auto_size_text=True,**Estilo_tex)]]
	pun.extend(Puntos)
	can.extend(Cantidad)
	return [[sg.Column(letras),sg.VerticalSeparator(),sg.Column(pun,key='puntos_letras'),sg.VerticalSeparator(),sg.Column(can)]]
    
def Retornar_nivel(lista):
	dato={'size':(12,1),'font':('Calibri',20), 'enable_events':True}
	nivel=[ [sg.T('NIVEL',pad=(6,5),relief=sg.RELIEF_SOLID,justification='center',background_color="LightBlue",text_color='#0F0F4C',font=('Calibri',23),size=(13,1))],
			[sg.Radio('Difícil',1,default=lista[0],key='Dificil',**dato)],
			[sg.Radio('Medio',1,default=lista[1],key='Medio',**dato)],
			[sg.Radio('Fácil',1,default=lista[2],key='Facil',**dato)]]
	return nivel
    
def retornar_tiempo(dic):
	estilo={'size':(27,1),'font':('calibre',13)}
	tiempo=[[sg.T('TIEMPO',pad=(6,5),size=(15,1),font=('Calibri',23),justification='center',background_color="LightBlue",text_color='#0F0F4C')],
			[sg.T('Tiempo de Partida',**estilo)],
			[sg.Slider(default_value=dic['Tiempo'],key='time', orientation='h')],
			[sg.T('Tiempo de Jugada (En seg)',**estilo)],
			[sg.Slider(range=(1,60),default_value=dic['Tiempo2'],key='time2',orientation='h')]]
	return tiempo

def Actualizar_texto(window,reaccion,event,key1,key2, Claves):
	pos=Claves[key1].index(event)
	clave=Claves[key2][pos]
	if reaccion =='descontar':
		dato=int(window.FindElement(clave).GetText())
		if dato>=2:
			dato-=1
			window.FindElement(clave).Update(str(dato))
	elif reaccion=='incrementar':
		dato=int(window.FindElement(clave).GetText())
		if dato<=10:
			dato+=1
			window.FindElement(clave).Update(str(dato))

def generar_claves():
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

	estilo={'size':(32,1) , 'justification':'center', 'font':('Helvetica', 20), 'relief':sg.RELIEF_RIDGE}

	Configuracion=[ [sg.T('CONFIGURACIÓN',**estilo, background_color="LightBlue",text_color='#0F0F4C')],
					[sg.T('')],
					[sg.Frame('',layout=[[sg.Column(nivel),sg.VerticalSeparator(), sg.Column(tiempo)]],pad=(3,0))],
					[sg.Frame('',layout=fichas,pad=(3,0))],
					[sg.Button('', image_filename='Imagenes/Guardar Configuración.png',image_size=(200,40),key='Guardar Configuración')]
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
			Actualizar_diccionario(diccionario, values)
			break
		if event in Claves['P0']:
			Actualizar_texto(window,'descontar',event,'P0','P1',Claves)
		if event in Claves['P2']:
			Actualizar_texto(window,'incrementar',event,'P2','P1',Claves)
		if event in Claves['C0']:
			pos=Claves['C0'].index(event)
			Actualizar_texto(window,'descontar',event,'C0','C1',Claves)
		if event in Claves['C2']:
			Actualizar_texto(window,'incrementar',event,'C2','C1',Claves)
	window.close()

