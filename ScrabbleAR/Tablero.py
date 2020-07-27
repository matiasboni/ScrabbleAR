import PySimpleGUI as sg
import random
import time
import sys
import Coordenadas
import JuegoTablero



def Tablero_actualizado(window,tablero_aux,valores_letras,nivel):
    '''Actualiza el tablero'''
    for i in range(0,15):
        for j in range(0,15):
            if tablero_aux[i][j]!=0:
                window.FindElement((i,j)).Update(image_filename=Coordenadas.asignar_color((i,j),nivel,valores_letras[tablero_aux[i][j]]))

def actualizar_ventana(window,estructura):
    JuegoTablero.Actualizar_lista_jugadas(window,estructura["lista_jugadas"])
    Tablero_actualizado(window,estructura["tablero_aux"],JuegoTablero.asociar_estructura(),dic["Nivel"])
    contador_partida=estructura["contador_partida"]
    contador_jugada=estructura["contador_jugada"]
    window.FindElement("Tiempo Partida").Update("Tiempo Partida: "+'{:02d}:{:02d}'.format((contador_partida // 100) // 60, (contador_partida// 100) % 60))
    window.FindElement("Tiempo Jugada").Update("Tiempo Jugada: "+'{:02d}:{:02d}'.format((contador_jugada // 100) // 60, (contador_jugada// 100) % 60))
    window.FindElement('Puntaje Jugador').Update('Tu Puntaje: '+str(estructura['puntos_total_jugador']))
    window.FindElement("Puntaje Computadora").Update("Puntaje Computadora: "+str(estructura['puntos_total_computadora']),font=("Helvetica",15))


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



def retornar_columna1():
    if sys.platform=="win32":
        datos={1:{"font":("Calibri",15)},2:{"font":("Calibri",15),"size":(25,1)}
        ,3:{"size":(40,22),"key":"datos","text_color":"grey6"}}
    elif sys.platform=="linux":
        datos={1:{"font":("Calibri",13)},2:{"font":("Calibri",13),"size":(25,1)}
        ,3:{"size":(35,25),"key":"datos","text_color":"grey6"}}
    
    columna1=[  [sg.Button('',image_filename="Imagenes/iniciar.png",key='Iniciar'),sg.Button("",image_filename="Imagenes/posponer.png",key='Posponer'),sg.Button('', image_filename="Imagenes/terminar.png",key='Terminar')],
                 [sg.Text("",size=(1,2))],
                 [sg.Frame("",
                 layout=[[sg.Text('Tiempo Partida: 00:00',key="Tiempo Partida",**datos[1])],
                 [sg.Text("Tiempo Jugada: 00:00",key="Tiempo Jugada",**datos[1])],
                 [sg.Text("Tu Puntaje: 00",key="Puntaje Jugador",**datos[2])],
                 [sg.Text("Puntaje Computadora: 00",key="Puntaje Computadora",**datos[2])],
                 [sg.Listbox(values=[],**datos[3])]])],
                 [sg.Text("",size=(1,2))],
                 [sg.Button('',image_filename="Imagenes/verificar.png",key='Verificar'),sg.Button("",image_filename="Imagenes/cambiar.png",key='Cambiar Fichas'), sg.Button('',image_filename="Imagenes/aceptar.png",key='Aceptar')]
                 ]
    return columna1   

def retornar_tablero(nivel):
    '''Función que recibe como parametro el nivel y retorna el tablero que le corresponde'''  
    datos={"pad":(0,0),"border_width":1}
    tablero=[
            [sg.Button('',key=(i,j),image_filename=Coordenadas.asignar_color((i,j),nivel,''), **datos,) for j in range(15)]for i in range(15)]
    return tablero


def retornar_pad(num,tipo):
    if (num==0 and tipo=="u") or (num==6 and tipo=="c") :
        return (0,0)
    else:
        return (3,0)

def retornar_Columna2(dic):

    letras_compu=[[sg.Button("",key=i,image_filename="Letras/_fondo.png",pad=retornar_pad(i,'c') ) for i in range(7)]]

    letras_usuario=[[sg.Button("",key=('a',a), image_filename="Letras/_fondo.png", pad=retornar_pad(a,'u'))for a in range(7)]]
    
    tablero=retornar_tablero(dic['Nivel'])
    
    columna2=[  
                [sg.Column(letras_compu, justification='right')],
				[sg.Column(tablero,justification="center")],
				[sg.Column(letras_usuario,justification="left")]]
    return columna2

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


def retornar_conjunto2(dic,tipo_de_palabra,estilo_col3):
    estilo_col3['size']=(33,0)
    conjunto2=[
        [sg.Text("NIVEL: "+dic["Nivel"],**estilo_col3)],
        [sg.Text('Tipo de Palabras: '+tipo_de_palabra, **estilo_col3)],
        [sg.Text("Tiempo de Partida: "+str(dic["Tiempo"])[0]+" Min",**estilo_col3)],
        [sg.T('Tiempo de Jugada: '+str(dic['Tiempo2'])+' Seg',**estilo_col3)]
    ]
    return conjunto2
    
    
def retornar_conjunto3(estilo_col3):
    estilo_boton={'size':(11,0),"font":('Helvetica',12)}
    estilo_col3['size']=(16,0)
    conjunto3=[
        [sg.Text("Casillas Especiales",**estilo_col3)],
        [sg.Button("",size=(2,1),button_color=("red","VioletRed")),sg.Text("Descuento 1",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","DarkBlue")),sg.Text("Letra x2",**estilo_boton)],
        [sg.Button("",size=(2,1),button_color=("red","pale violet red")),sg.Text("Descuento 2",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","DeepSkyBlue")),sg.Text("Letra x3",**estilo_boton)],
        [sg.Button("",size=(2,1),button_color=("red","PaleVioletRed4")),sg.Text("Descuento 3",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","MediumSlateBlue")),sg.Text("Palabra x2",**estilo_boton)],
        [sg.Button("",size=(2,1),button_color=("red","#97755c")),sg.Text("Comienzo",**estilo_boton),sg.Button("",size=(2,1),button_color=("red","SlateBlue4")),sg.Text("Palabra x3",**estilo_boton)],
    ]
    return conjunto3

def retornar_Columna3(dic, Dic_Letras_puntos_cantidad, tipo_de_palabra):
    
    estilo_col3={"font":('Calibri',12), 'relief':sg.RELIEF_SOLID, 'size':(16,0)}
    conjunto1=conjunto_de_letras(Dic_Letras_puntos_cantidad, estilo_col3)
    conjunto2=retornar_conjunto2(dic,tipo_de_palabra,estilo_col3)
    conjunto3=retornar_conjunto3(estilo_col3)
    columna3=[  [sg.Text("",size=(1,3))],[sg.Frame('',background_color="#ffffff",
                layout=[[sg.Text('CONSIDERACIONES',size=(350,1),justification="center",font=("Ravie",20),pad=(0,0))],
                [sg.Column(conjunto1, pad=(0,1),size=(350,240)if (sys.platform=="win32")else (400,240))],
                [sg.Column(conjunto2,pad=(0,1),size=(350,120)if (sys.platform=='win32')else (400,120))],
                [sg.Column(conjunto3,pad=(0,1),size=(350,150)if (sys.platform=="win32") else (400,167))]])]
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
    if sys.platform!="linux":
        layout= layout= [[sg.Column(columna1),sg.Text("",size=(3,1)),sg.Column(columna2),sg.T("",size=(3,1)),sg.Column(columna3)]]
    else:
        layout= [[sg.Column(columna1),sg.Column(columna2),sg.Column(columna3)]]
    
    estilo= {"return_keyboard_events":True}
    if sys.platform=='linux':
        estilo['resizable']=True
    window=sg.Window('ScrabbleAR', layout,**estilo).Finalize()
    window.maximize()
    window.read(timeout=10)
    if estructura!=None:
        actualizar_ventana(estructura,window)
    while True:
        event,values=window.read()
        if event=="Iniciar":
            JuegoTablero.iniciar_juego(window,Dic_Letras_puntos_cantidad,dic, tipo_de_palabra, tiempo_maximo,estructura)
            break
        if event=="Terminar":
            break
        elif event==None:
            exit()
    window.close()
