import PySimpleGUI as sg
import random
import time
import sys
import Coordenadas
import JuegoTablero



def Tablero_actualizado(window,tablero_aux,valores_letras):
    '''Actualiza el tablerop'''
    for i in range(0,15):
        for j in range(0,15):
            if tablero_aux[i][j]!=0:
                window.FindElement((i,j)).Update(text=valores_letras[tablero_aux[i][j]])

def Letras_Cantidad_y_Puntos(puntos, cantidad):
    ''''''
    letras=['A','E','O','S','I','U','N','L','R','T','C','D','G','M','B','P','F','H','V','Y','J','K','LL','Ñ',"Q",'G','RR','W','X','Z']
    dic={}
    cant=0
    for i in range(len(letras)):
        dic.setdefault(letras[i],{'Puntos':puntos[cant], 'Cantidad':cantidad[cant]} )
        if i in (9,12,15,19,20,27):
            cant+=1
    return dic


def asignar_color(coordenadas,nivel):
    '''Función que recibe como parámetro las coordenadas de una casilla y retorna el color
    que le corresponde a esa casilla'''
    dic=Coordenadas.retornar_coordenadas(nivel)   
    if coordenadas in dic["letra2"]:
        return ("black","DarkBlue")
    elif coordenadas in dic["letra3"]:
        return ("black","DeepSkyBlue")
    elif coordenadas in dic["palabra2"]:
        return ("black","MediumSlateBlue")
    elif coordenadas in dic["palabra3"]:
        return ("black", "SlateBlue4")
    elif coordenadas in dic["descuen1"]:
        return ("black","VioletRed")
    elif coordenadas in dic["descuen2"]:
        return ("black","pale violet red")
    elif coordenadas in dic['descuen3']:
        return ("black","PaleVioletRed4")
    elif coordenadas==(7,7):
        return ("black","#97755c")
    else:
        return  ("black","LightBlue")

def retornar_tablero(nivel):
    '''Función que recibe como parametro el nivel y retorna el tablero que le corresponde'''  
    if sys.platform=="linux":
        datos={"size":(2,2),"pad":(0,0),"border_width":1}
    else:    
        datos={"size":(4,2),"pad":(0,0),"border_width":1}
    tablero=[
            [sg.Button('',key=(i,j),button_color=asignar_color((i,j),nivel), **datos,) for j in range(15)]for i in range(15)]
    return tablero

def retornar_columna1():
    if sys.platform=="win32":
        datos={1:{"size":(11,2)},2:{"font":("Helvetica",15)},3:{"font":("Helvetica",15),"size":(25,1)}
        ,4:{"size":(40,22),"key":"datos","text_color":"grey6"},5:{"size":(11,2)}}
    elif sys.platform=="linux":
        datos={1:{"size":(11,2)},2:{"font":("Helvetica",15)},3:{"font":("Helvetica",15),"size":(25,1)}
        ,4:{"size":(44,25),"key":"datos"},5:{"size":(11,2)}}
    
    columna1=[  [sg.Button('Iniciar',**datos[1]),sg.Button("Posponer",**datos[1]),sg.Button('Terminar', **datos[1])],
                 [sg.Text("",size=(1,2))],
                 [sg.Frame("",
                 layout=[[sg.Text('Tiempo Partida: 00:00',key="Tiempo Partida",**datos[2])],
                 [sg.Text("Tiempo Jugada: 00:00",key="Tiempo Jugada",**datos[2])],
                 [sg.Text("Tu Puntaje: 00",key="Puntaje Jugador",**datos[3])],
                 [sg.Text("Puntaje Computadora: 00",key="Puntaje Computadora",**datos[3])],
                 [sg.Listbox(values=[],**datos[4])]])],
                 [sg.Text("",size=(1,2))],
                 [sg.Button('Verificar',**datos[5]),sg.Button("Cambiar Fichas",**datos[5]), sg.Button('Aceptar',**datos[5])]
                 ]
    return columna1   

def tipo_de_palabras(nivel):
    '''Función que recibe como parámetro el nivel y retorna los tipos de palabras validas'''
    if nivel=='Facil':
        return 'Todas Las Palabras'
    elif nivel=='Medio':
        return 'Verbos y Adjetivos'
    else:
        lista=['Adjetivos', 'Verbos']
        palabra=random.randrange(len(lista))
        return lista[palabra]

def conjunto_de_letras(Dic_Letras_puntos_cantidad,estilo_col3):
    '''Funcion que retorna una estructura de las letras con sus puntos y la cantidad de letras 
    segun la configuración que se específico'''
    texto= [[sg.Text("LETRAS", **estilo_col3)],
            [sg.Text("A,E,O,S,I,U,N,L,R,T: ",**estilo_col3)],
            [sg.Text("C,D,G: ",**estilo_col3)],
            [sg.Text("M,B,P: ",**estilo_col3)],
            [sg.Text("F,H,V,Y: ",**estilo_col3)],
            [sg.Text("J: ",**estilo_col3)],
            [sg.Text("K,LL,Ñ,Q,RR,W,X: ",**estilo_col3)],
            [sg.Text("Z: ",**estilo_col3)]]
    saltos=["A","C","M","F","J","K","Z"]
    estilo_col3['size']=(3,0)
    puntos=[[sg.T(str(Dic_Letras_puntos_cantidad[i]["Puntos"]),**estilo_col3)]for i in saltos]
    cantidad=[[sg.T(str(Dic_Letras_puntos_cantidad[i]['Cantidad']),**estilo_col3)]for i in saltos]
    estilo_col3['size']=(8,0)
    pun=[[sg.Text("PUNTOS", **estilo_col3)]]
    pun.extend(puntos)
    can=[[sg.Text("CANT", **estilo_col3)]]
    can.extend(cantidad)
    conjunto=[
                [sg.Column(texto),sg.Column(pun),sg.Column(can)]]
    return conjunto


def retornar_Columna2(dic):

    if sys.platform=='linux':
        T=(3,2)
    else:
        T=(5,2)
    letras_compu=[[sg.Button("",key=i ,size=T) for i in range(7)]]

    letras_usuario=[[sg.Button("",key=('a',a), size=T )for a in range(7)]]
    
    tablero=retornar_tablero(dic['Nivel'])
    
    columna2=[  
                [sg.Column(letras_compu, justification='right')],
				[sg.Column(tablero,justification="center")],
				[sg.Column(letras_usuario,justification="left")]]
    return columna2
    
def retornar_Columna3(dic, Dic_Letras_puntos_cantidad, tipo_de_palabra):
    
    estilo_col3={"justification":'left',"font":('Helvetica',12), 'relief':sg.RELIEF_RIDGE, 'size':(16,0)}
    estilo_boton={'justification':'left', 'size':(11,0),"font":('Helvetica',12)}
    conjunto1=conjunto_de_letras(Dic_Letras_puntos_cantidad, estilo_col3)
    estilo_col3['size']=(33,0)
    conjunto2=[
        [sg.Text("NIVEL: "+dic["Nivel"],**estilo_col3)],
        [sg.Text('Tipo de Palabras: '+tipo_de_palabra, **estilo_col3)],
        [sg.Text("Tiempo de Partida: "+str(dic["Tiempo"])[0]+" Min",**estilo_col3)],
        [sg.T('Tiempo de Jugada: '+str(dic['Tiempo2'])+' Seg',**estilo_col3)]
    ]
    conjunto3=[
        [sg.Button("",size=(2,1),button_color=("red","VioletRed")),sg.Text("Descuento 1",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","DarkBlue")),sg.Text("Letra x2",**estilo_boton)],
        [sg.Button("",size=(2,1),button_color=("red","pale violet red")),sg.Text("Descuento 2",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","DeepSkyBlue")),sg.Text("Letra x3",**estilo_boton)],
        [sg.Button("",size=(2,1),button_color=("red","PaleVioletRed4")),sg.Text("Descuento 3",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","MediumSlateBlue")),sg.Text("Palabra x2",**estilo_boton)],
        [sg.Button("",size=(2,1),button_color=("red","#97755c")),sg.Text("Comienzo",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","SlateBlue4")),sg.Text("Palabra x3",**estilo_boton)],
    ]
    columna3=[  [sg.Text("",size=(1,3))],[sg.Frame('', 
                layout=[[sg.Text('CONSIDERACIONES',justification="center",auto_size_text=True,font=("Helvetica",20))],
                [sg.Column(conjunto1, pad=(0,0))],
                [sg.Column(conjunto2)],
                [sg.Column(conjunto3)]])]
             ]
    return columna3

def tablero_de_juego(dic, estructura):
    '''Función que inicializa y muestra toda la pantalla del tablero'''
    if estructura!=None:
        tipo_de_palabra=estructura['tipo_de_palabra']
        dic=estructura['dic']
    tipo_de_palabra=tipo_de_palabras(dic['Nivel'])
    Dic_Letras_puntos_cantidad=Letras_Cantidad_y_Puntos(dic["ListaPuntos"],dic["ListaFichas"])
    tiempo_maximo=dic['Tiempo']*6000

    columna1=retornar_columna1()
    
    columna2=retornar_Columna2(dic)

    columna3=retornar_Columna3(dic, Dic_Letras_puntos_cantidad,tipo_de_palabra)

    layout= [
			    [sg.Column(columna1),sg.Text("",size=(3,1)),sg.Column(columna2),sg.T("",size=(3,1)),sg.Column(columna3)]]
    
    estilo= {"return_keyboard_events":True,"margins":(0,0),"location":(0,0)}
    if sys.platform=='linux':
        estilo['resizable']=True
    window=sg.Window('ScrabbleAR', layout,**estilo).Finalize()
    window.maximize()
    window.read(timeout=10)
    if estructura!=None:
        JuegoTablero.Actualizar_lista_jugadas(window,estructura["lista_jugadas"])
        Tablero_actualizado(window,estructura["tablero_aux"],JuegoTablero.asociar_estructura())
        contador_partida=estructura["contador_partida"]
        contador_jugada=estructura["contador_jugada"]
        window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
        window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: "+'{:02d}:{:02d}'.format((contador_jugada // 100) // 60, (contador_jugada// 100) % 60))
        window.FindElement('Puntaje Jugador').Update('Tu Puntaje: '+str(estructura['puntos_total_jugador']))
        window.FindElement("Puntaje Computadora").Update("Puntaje Computadora: "+str(estructura['puntos_total_computadora']),font=("Helvetica",15))
    while True:
        event,values=window.read()
        if event=="Iniciar":
            break
        if event in (None,'Terminar'):
            break
    if not event in (None,"Terminar"):
        JuegoTablero.iniciar_juego(window,Dic_Letras_puntos_cantidad,dic, tipo_de_palabra, tiempo_maximo,estructura)
    elif event==None:
        exit()
    window.close()