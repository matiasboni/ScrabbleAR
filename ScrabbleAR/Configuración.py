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
    if values['time']!=None:
        diccionario['Tiempo2']=values['time2']
        diccionario['Tiempo']=values['time']
        diccionario['ListaPuntos']=[values['p1'],values['p2'],values['p3'],values['p4'],values['p5'],values['p6'],values['p7']]
        diccionario['ListaFichas']=[values['c1'],values['c2'],values['c3'],values['c4'],values['c5'],values['c6'],values['c7']]

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

def conjunto_letras_confi(maximo, default, clave): 
    letras=[[sg.T('A, E, O, S, I, U, N, L, R, T: ', size=(20,1)),sg.InputCombo(maximo,default_value=default[0],size=(5,1), key=clave+'1')],
            [sg.T('C, D, G: ',size=(20,1)),sg.InputCombo(maximo,default_value=default[1],size=(5,1), key=clave+'2')],
            [sg.T('M, B, P: ',size=(20,1)),sg.InputCombo(maximo,default_value=default[2],size=(5,1), key=clave+'3')],
            [sg.T('F, H, V, Y: ',size=(20,1)),sg.InputCombo(maximo,default_value=default[3],size=(5,1), key=clave+'4')],
            [sg.T('J: ',size=(20,1)),sg.InputCombo(maximo,default_value=default[4],size=(5,1), key=clave+'5')],
            [sg.T('K, LL, Ñ, Q, RR, W, X: ',size=(20,1)),sg.InputCombo(maximo,default_value=default[5],size=(5,1), key=clave+"6")],
            [sg.T('Z: ',size=(20,1)),sg.InputCombo(maximo,default_value=default[6],size=(5,1), key=clave+"7")]]
    return letras
    
def Retornar_nivel(lista):
    dato={'font':('Helvetica'), 'enable_events':True}
    nivel=[ [sg.T('')],
            [sg.Radio('Difícil',1, size=(20,1),default=lista[0],key='Dificil',**dato)],
            [sg.Radio('Medio',1, size=(20,1),default=lista[1],**dato)],
            [sg.Radio('Fácil',1, size=(20,1),default=lista[2],key='Facil',**dato)]]
    return nivel
    
def retornar_tiempo(dic):
    tiempo=[[sg.T('Tiempo de Partida',justification='center')],
            [sg.Slider(default_value=dic['Tiempo'],key='time', orientation='h')],
            [sg.T('Tiempo de Jugada (En seg)', justification='center')],
            [sg.Slider(range=(1,60),default_value=dic['Tiempo2'],key='time2',orientation='h')]]
    return tiempo
    
def Configuracion_de_juego(diccionario):
    '''Función que define y muestra la pantalla de configuración para que
    se realizen los cambios por parte del jugador'''
    maximo_de_cantidad=[1,2,3,4,5,6,7,8,9,10,11]
    puntos, cantidad, lista=Actualizar_Configuracion(diccionario)
    fichas_puntos=conjunto_letras_confi(maximo_de_cantidad,puntos,"p")
    fichas_cantidad=conjunto_letras_confi(maximo_de_cantidad, cantidad,'c')
    nivel=Retornar_nivel(lista)
    
    tiempo=retornar_tiempo(diccionario)

    estilo={'size':(30,1) , 'justification':'center', 'font':('Helvetica', 20), 'relief':sg.RELIEF_RIDGE}

    Configuracion=[ [sg.T('CONFIGURACIÓN',**estilo)],
                    [sg.Text('NIVEL',**estilo)],
                    [sg.Column(nivel), sg.Column(tiempo)],
                    [sg.Text('Puntaje de las Fichas',**estilo)],
                    [sg.Column(fichas_puntos)],
                    [sg.T('Cantidad de Fichas por Letra', **estilo)],
                    [sg.Column(fichas_cantidad)],
                    [sg.Button('Guardar Configuracion', size=(20,1))]
                    ]
    window=sg.Window('Configuración', Configuracion,keep_on_top=True,no_titlebar=True)
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

