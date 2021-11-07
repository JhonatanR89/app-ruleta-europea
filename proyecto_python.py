
import pymongo
from pymongo import MongoClient
from pymongo.message import insert
from statistics import mean

MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)


from tkinter import (Button, E, Entry, Frame, Label, Menu, StringVar, Tk, W,
                     messagebox, ttk)
from tkinter.constants import END, FALSE
from typing import Text

raiz = Tk()

raiz.title("RULETA EUROPEA")
raiz.geometry("450x680")

raiz.iconbitmap(r'C:\Users\jotic\Desktop\python\graficos\ruleta.ico')
miframe = Frame(raiz)
miframe.pack()


miframe2 = Frame(raiz)
miframe2.pack()

miframe3 = Frame(raiz)
miframe3.pack()

miframe4 = Frame(raiz)
miframe4.pack()

miframe5 = Frame(raiz)
miframe5.pack()


# ------- ------ titulo-------------------------------

titleButton = Label(miframe, text='Sistema Predictivo Ruleta Europea 💯')
titleButton.config(fg="black", font=("Segoe UI Black", 14))
titleButton.grid(row=0, column=6, columnspan=200)

# -----------numero seleccionado--------------------
numeros_ruleta = {
    '0': 1, '26': 2, '3': 3, '35': 4, '12': 5, '28': 6, '7': 7, '29': 8,
    '18': 9, '22': 10, '9': 11, '31': 12, '14': 13, '20': 14, '1': 15,
    '33': 16, '16': 17, '24': 18, '5': 19, '10': 20, '23': 21, '8': 22,
    '30': 23, '11': 24, '36': 25, '13': 26, '27': 27, '6': 28, '34': 29,
    '17': 30, '25': 31, '2': 32, '21': 33, '4': 34, '19': 35, '15': 36,
    '32': 37
}

numero_historico = StringVar()

num_selec = Entry(miframe3, textvariable=numero_historico)
num_selec.grid(row=4, column=6, padx=10, pady=20)
num_selec.config(
    fg="old lace", bg="black", font=("DejaVu Sans", 9), justify="right"
)
# -----------------------Base de datos-----------------

DB = client['HISTORICO']
num = DB['numeros']
mov = DB['Desplazamiento']
pron = DB['Pronostico']


def limpiar_campos():
    DB.numeros.drop()
    DB.Desplazamiento.drop()
    for i in tabla_historica.get_children():
        tabla_historica.delete(i)
    for i in tabla_desp.get_children():
        tabla_desp.delete(i)    

def crear(value, clave):
    registros = tabla_historica.get_children()
    for elemento in registros:
        tabla_historica.delete(elemento)
    num.insert_one({'numero': value, 'clave': clave}) 
    leer(tabla_historica)
    

def numero_pulsado(num):
    numero_historico.set(num)


def numero_obtenido():
    return numero_historico.get()


def leer(tabla_historica):
    for registros in num.find():
        tabla_historica.insert("", 0, text=registros['numero'])


def clave_num():
    clave = (int(numeros_ruleta[numero_obtenido()]))
    consulta(crear(numero_historico.get(), clave))
    forma()

def consulta(clave):
    Condb = num.find().sort('_id',-1).limit(2)
    ultimo = Condb[0]
    penultimo = Condb[1]
    calculo(ultimo['clave'], penultimo['clave'])


def leerMov(tabla_desp):
    for registro in mov.find():
        tabla_desp.insert("", 0, text=registro['Desplazamiento'])   
    

tabla_desp = ttk.Treeview(miframe4, height=10)
tabla_desp.grid(row=4, column=6, padx=10, pady=20, )
tabla_desp.heading("#0", text="Desplazamiento", anchor="center")
leerMov(tabla_desp)


def movimiento(value):
    registros = tabla_desp.get_children()
    for elemento in registros:
        tabla_desp.delete(elemento)
    mov.insert_one({'Desplazamiento': value}) 
    leerMov(tabla_desp)


def calculo(ultimo, penultimo):
    r_2 = (ultimo - penultimo) 
    if r_2 >= 1:
        pass
    else:
        r_2 = (ultimo - penultimo + 37)
    movimiento(r_2)

tabla_historica = ttk.Treeview(miframe4, height=10)
tabla_historica.grid(row=4, column=4, padx=10, pady=20, )
tabla_historica.heading("#0", text="Numero", anchor="center")
leer(tabla_historica)

barra_menu = Menu(raiz, tearoff=0)
raiz.config(menu=barra_menu, width=300, height=300)

tipo_menu = Menu(barra_menu, tearoff=0)
tipo_menu.add_command(label='NUEVA', command=lambda: limpiar_campos())


barra_menu.add_cascade(label='Borrar ', menu=tipo_menu)

# -------------------boton go!--------------------------
botongo = Button(
    miframe3, text='GO!', width=8, command=lambda:  clave_num()
)
botongo.grid(row=5, column=6, padx=2, pady=3, sticky=W + E)
botongo.config(fg="old lace", bg="green", font=("DejaVu Sans", 9))

#--------------------formulas------------------------------

def forma():
    listaPromedio = mov.find().sort('_id', -1).limit(2)
    valores = [valor['Desplazamiento'] for valor in listaPromedio]
    print(valores)
    primera = []
    segunda = []
    tercera = []
    cuarta = []

    for i in valores:
        if i >= 1 and i <= 9:
            primera.append(i)
        elif i >= 10 and i <= 19:
            segunda.append(i)
        elif i >= 20 and i <= 29:
            tercera.append(i)
        elif i >= 30 and i <= 37:
            cuarta.append(i)


    if len(primera) >= 1:
        avg = int(sum(primera)/len(primera))
    else:
        avg = 0
    if len(segunda) >= 1:
        avg2 = int(sum(segunda)/len(segunda))
    else:
        avg2 = 0
    if len(tercera) >= 1:
        avg3 = int(sum(tercera)/len(tercera))
    else:
        avg3 = 0
    if len(cuarta) >= 1:
        avg4 = int(sum(cuarta)/len(cuarta))
    else:
        avg4 = 0
    
    UltimoNumero = num.find().sort('_id', -1).limit(1)
    ultimo = [valor['clave'] for valor in UltimoNumero]
    a = ultimo[0]
    
    Promedios = (avg, avg2, avg3, avg4)
    z = []
    y = []
    
    for i in Promedios:
        if i != 0:
            c = a + i
            if c >= 1 and c <= 37:
                z.append(c)
            elif c >= 38:
                c = a + i - 37
                z.append(c)

    for i in z:
        if i != 0:
            y.append(list(numeros_ruleta.keys())[list(numeros_ruleta.values()).index(i)])
        else:
            pass
    print(Promedios)
    print(z)
    print(y)
    Pronosticos(y)

def Pronosticos(a=None):
    registros = tabla_pronostico.get_children()
    for elemento in registros:
        tabla_pronostico.delete(elemento)
    pron.insert_one({'Pronostico': a})
     
    leer_Pronostico(tabla_pronostico)

def leer_Pronostico(tabla_pronostico):
    for registro in pron.find().sort('_id', -1).limit(1):
        tabla_pronostico.insert("", 0, text=registro['Pronostico']), 


tabla_pronostico = ttk.Treeview(miframe5, height=2)
tabla_pronostico.grid(row=4, column=4, padx=10, pady=20)
tabla_pronostico.heading("#0", text="Numeros a Apostar", anchor="center")




# ----------------------------numeros del 0 al 36 ---------------------------
cuadronumero0 = Button(
    miframe2, text='0', width=2, height=5, command=lambda: numero_pulsado("0")
)
cuadronumero0.grid(row=0, column=1,  rowspan=3)
cuadronumero0.config(fg="old lace", bg="green", font=("DejaVu Sans", 9))

cuadronumero1 = Button(
    miframe2, text='1', width=2, command=lambda: numero_pulsado("1"))
cuadronumero1.grid(row=2, column=2, padx=1)
cuadronumero1.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero2 = Button(
    miframe2, text='2', width=2, command=lambda: numero_pulsado('2'))
cuadronumero2.grid(row=1, column=2, padx=1)
cuadronumero2.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero3 = Button(
    miframe2, text='3', width=2, command=lambda: numero_pulsado('3'))
cuadronumero3.grid(row=0, column=2, padx=1)
cuadronumero3.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero4 = Button(
    miframe2, text='4', width=2, command=lambda: numero_pulsado('4'))
cuadronumero4.grid(row=2, column=3, padx=1)
cuadronumero4.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero5 = Button(
    miframe2, text='5', width=2, command=lambda: numero_pulsado('5'))
cuadronumero5.grid(row=1, column=3, padx=1)
cuadronumero5.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero6 = Button(
    miframe2, text='6', width=2, command=lambda: numero_pulsado('6'))
cuadronumero6.grid(row=0, column=3, padx=1)
cuadronumero6.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero7 = Button(
    miframe2, text='7', width=2, command=lambda: numero_pulsado('7'))
cuadronumero7.grid(row=2, column=4, padx=1)
cuadronumero7.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero8 = Button(
    miframe2, text='8', width=2, command=lambda: numero_pulsado('8'))
cuadronumero8.grid(row=1, column=4, padx=1)
cuadronumero8.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero9 = Button(
    miframe2, text='9', width=2, command=lambda: numero_pulsado('9'))
cuadronumero9.grid(row=0, column=4, padx=1)
cuadronumero9.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero10 = Button(
    miframe2, text='10', width=2, command=lambda: numero_pulsado('10'))
cuadronumero10.grid(row=2, column=5, padx=1)
cuadronumero10.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero11 = Button(
    miframe2, text='11', width=2, command=lambda: numero_pulsado('11'))
cuadronumero11.grid(row=1, column=5, padx=1)
cuadronumero11.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero12 = Button(
    miframe2, text='12', width=2, command=lambda: numero_pulsado('12'))
cuadronumero12.grid(row=0, column=5, padx=1)
cuadronumero12.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero13 = Button(
    miframe2, text='13', width=2, command=lambda: numero_pulsado('13'))
cuadronumero13.grid(row=2, column=6, padx=1)
cuadronumero13.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero14 = Button(
    miframe2, text='14', width=2, command=lambda: numero_pulsado('14'))
cuadronumero14.grid(row=1, column=6, padx=1)
cuadronumero14.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero15 = Button(
    miframe2, text='15', width=2, command=lambda: numero_pulsado('15'))
cuadronumero15.grid(row=0, column=6, padx=1)
cuadronumero15.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero16 = Button(
    miframe2, text='16', width=2, command=lambda: numero_pulsado('16'))
cuadronumero16.grid(row=2, column=7, padx=1)
cuadronumero16.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero17 = Button(
    miframe2, text='17', width=2, command=lambda: numero_pulsado('17'))
cuadronumero17.grid(row=1, column=7, padx=1)
cuadronumero17.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero18 = Button(
    miframe2, text='18', width=2, command=lambda: numero_pulsado('18'))
cuadronumero18.grid(row=0, column=7, padx=1)
cuadronumero18.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero19 = Button(
    miframe2, text='19', width=2, command=lambda: numero_pulsado('19'))
cuadronumero19.grid(row=2, column=8, padx=1)
cuadronumero19.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero20 = Button(
    miframe2, text='20', width=2, command=lambda: numero_pulsado('20'))
cuadronumero20.grid(row=1, column=8, padx=1)
cuadronumero20.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero21 = Button(
    miframe2, text='21', width=2, command=lambda: numero_pulsado('21'))
cuadronumero21.grid(row=0, column=8, padx=1)
cuadronumero21.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero22 = Button(
    miframe2, text='22', width=2, command=lambda: numero_pulsado('22'))
cuadronumero22.grid(row=2, column=9, padx=1)
cuadronumero22.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero23 = Button(
    miframe2, text='23', width=2, command=lambda: numero_pulsado('23'))
cuadronumero23.grid(row=1, column=9, padx=1)
cuadronumero23.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero24 = Button(
    miframe2, text='24', width=2, command=lambda: numero_pulsado('24'))
cuadronumero24.grid(row=0, column=9, padx=1)
cuadronumero24.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero25 = Button(
    miframe2, text='25', width=2, command=lambda: numero_pulsado('25'))
cuadronumero25.grid(row=2, column=10, padx=1)
cuadronumero25.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero26 = Button(
    miframe2, text='26', width=2, command=lambda: numero_pulsado('26'))
cuadronumero26.grid(row=1, column=10, padx=1)
cuadronumero26.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero27 = Button(
    miframe2, text='27', width=2, command=lambda: numero_pulsado('27'))
cuadronumero27.grid(row=0, column=10, padx=1)
cuadronumero27.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero28 = Button(
    miframe2, text='28', width=2, command=lambda: numero_pulsado('28'))
cuadronumero28.grid(row=2, column=11, padx=1)
cuadronumero28.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero29 = Button(
    miframe2, text='29', width=2, command=lambda: numero_pulsado('29'))
cuadronumero29.grid(row=1, column=11, padx=1)
cuadronumero29.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero30 = Button(
    miframe2, text='30', width=2, command=lambda: numero_pulsado('30'))
cuadronumero30.grid(row=0, column=11, padx=1)
cuadronumero30.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero31 = Button(
    miframe2, text='31', width=2, command=lambda: numero_pulsado('31'))
cuadronumero31.grid(row=2, column=12, padx=1)
cuadronumero31.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero32 = Button(
    miframe2, text='32', width=2, command=lambda: numero_pulsado('32'))
cuadronumero32.grid(row=1, column=12, padx=1)
cuadronumero32.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero33 = Button(
    miframe2, text='33', width=2, command=lambda: numero_pulsado('33'))
cuadronumero33.grid(row=0, column=12, padx=1)
cuadronumero33.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero34 = Button(
    miframe2, text='34', width=2, command=lambda: numero_pulsado('34'))
cuadronumero34.grid(row=2, column=13, padx=1)
cuadronumero34.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))

cuadronumero35 = Button(
    miframe2, text='35', width=2, command=lambda: numero_pulsado('35'))
cuadronumero35.grid(row=1, column=13, padx=1)
cuadronumero35.config(fg="old lace", bg="black", font=("DejaVu Sans", 9))

cuadronumero36 = Button(
    miframe2, text='36', width=2, command=lambda: numero_pulsado('36'))
cuadronumero36.grid(row=0, column=13, padx=1)
cuadronumero36.config(fg="old lace", bg="red", font=("DejaVu Sans", 9))
# -------------------------------numeros en ruleta----------------------------
raiz.mainloop()
