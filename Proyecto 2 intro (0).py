from tkinter import *
import random

#___________________________________Tipos de terreno___________________________________
class Terreno:
    def __init__(self, nombre, permite_jugador, permite_cazador):
        self.nombre = nombre
        self.permite_jugador = permite_jugador
        self.permite_cazador = permite_cazador

    def permite_paso(self, entidad_es_jugador):
        if entidad_es_jugador:
            return self.permite_jugador
        return self.permite_cazador

class Camino(Terreno):
    def __init__(self):
        Terreno.__init__(self, "camino", True, True)

class Muro(Terreno):
    def __init__(self):
        Terreno.__init__(self, "muro", False, False)

class Tunel(Terreno):
    def __init__(self):
        Terreno.__init__(self, "tunel", True, False)

class Liana(Terreno):
    def __init__(self):
        Terreno.__init__(self, "liana", False, True)

#______________________________Mapa______________________________
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = []

        self.crear_matriz_vacia()   #llamada al método para crear la matriz

    def crear_matriz_vacia(self):
        self.matriz = []

        for f in range(self.filas):
            fila = []

            for c in range(self.columnas):
                fila.append(None)  

            self.matriz.append(fila)


    def generar_mapa(self):
        for f in range(self.filas):
            for c in range(self.columnas):

                if (f == 0 and c == 0) or (f == self.filas - 1 and c == self.columnas - 1):
                    self.matriz[f][c] = Camino()
                    continue

                opcion = random.randint(1, 4)

                if opcion == 1:
                    self.matriz[f][c] = Camino()
                elif opcion == 2:
                    self.matriz[f][c] = Muro()
                elif opcion == 3:
                    self.matriz[f][c] = Tunel()
                else:
                    self.matriz[f][c] = Liana()

    def mostrar_mapa(self):
        for fila in self.matriz:

            letras = []  

            for t in fila:
                letra = t.nombre[0] 
                letras.append(letra.upper())

            linea = " ".join(letras)
            print(linea)

#________________________________________________________________________________________________________
class Enemigo:
    def __init__(self, fila_inicial, columna_inicial):
        self.fila = fila_inicial
        self.columna = columna_inicial

    def mover(self, mov_fila, mov_columna, mapa):
        nueva_fila = self.fila + mov_fila
        nueva_columna = self.columna + mov_columna

        #limitar mapa
        if 0 <= nueva_fila < mapa.filas and 0 <= nueva_columna < mapa.columnas:

            terreno_destino = mapa.matriz[nueva_fila][nueva_columna]

            #ver si el cazador puede entrar
            if terreno_destino.permite_cazador:
                self.fila = nueva_fila
                self.columna = nueva_columna
                return True

        return False  #no pudo moverse

    def mover_aleatorio(self, mapa):
        posibles_movimientos = [
            (1, 0),    #abajo
            (-1, 0),   #arriba
            (0, 1),    #derecha
            (0, -1)    #izquierda
        ]

        random.shuffle(posibles_movimientos)

        for mov_fila, mov_columna in posibles_movimientos:
            if self.mover(mov_fila, mov_columna, mapa):
                return True

        return False  #no pudo moverse 

    def perseguir(self, jugador, mapa):
        
        movimiento_vertical = 0
        if jugador.fila < self.fila:
            movimiento_vertical = -1  #jugador arriba
        elif jugador.fila > self.fila:
            movimiento_vertical = 1   #jugador abajo

        if self.mover(movimiento_vertical, 0, mapa):
            return True

        movimiento_horizontal = 0
        if jugador.columna < self.columna:
            movimiento_horizontal = -1  # jugador izquierda
        elif jugador.columna > self.columna:
            movimiento_horizontal = 1   # jugador derecha

        if self.mover(0, movimiento_horizontal, mapa):
            return True

        #si todos los movimientos directos fallan moverse aleatoriamente
        return self.mover_aleatorio(mapa)


    def huir(self, jugador, mapa):

        movimiento_vertical = 0
        if jugador.fila < self.fila:
            movimiento_vertical = 1  # huir hacia abajo
        elif jugador.fila > self.fila:
            movimiento_vertical = -1 # huir hacia arriba

        if self.mover(movimiento_vertical, 0, mapa):
            return True

        movimiento_horizontal = 0
        if jugador.columna < self.columna:
            movimiento_horizontal = 1  # huir derecha
        elif jugador.columna > self.columna:
            movimiento_horizontal = -1 # huir izquierda

        if self.mover(0, movimiento_horizontal, mapa):
            return True

        #si todos los movimientos directos fallan moverse aleatoriamente
        return self.mover_aleatorio(mapa)
#________________________________________________________________________________________________________
def salir():
    ventana.destroy()
    exit()
#________________________________________________________________________________________________________
ventana = Tk()
ventana.title("Seleccionar modo")
ventana.geometry("700x730")

#Titulo
lbl_seleccion = Label(ventana, text="Seleccione un modo de juego",  font=("Times new roman", 17))
lbl_seleccion.place(x=210,y=10)

#Botones
btn_escapa=Button(ventana, text="Modo 1: Escapa", command="", font=("Times new roman", 15),bg="sky blue")
btn_escapa.place(x=260, y=200)

btn_cazador=Button(ventana, text="Modo 2: cazador", command="", font=("Times new roman", 15),bg="sky blue")
btn_cazador.place(x=250, y=400)

btn_salir=Button(ventana, text="Salir", command=salir, font=("Times new roman", 15),bg="sky blue")
btn_salir.place(x=280, y=600)


m = Mapa(10, 10)  # 10x10 o el tamaño que quieras
m.generar_mapa()
m.mostrar_mapa()

