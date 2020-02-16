"""
José Miguel Calderón Terol
15/02/2020
version 1.0
"""
import numpy as np
import lib


class Wumpus(object):
    """
    Programa del clásico Hunt the Wumpus.
    Al inicio pedirá el tamaño del tablero (lado), el número de pozos y la cantidad de munición.
    Movimientos del jugador:
        Girar 90º a izquierda o derecha.
        Avanzar una casilla
        Disparar
        Salir, solo cuando tenga el tesoro y este en la casilla de salida
    Movimientos del Wumpus.
        Girar (50% de posibilidad, izquierda o a derecha)
        Avanzar (50% de posilidad)
    """

    def __init__(self):
        self.juego = True  # flag que determina si el juego continua True, o ha acabado False
        self.acierto_disparo = False  # flag que determina si el disparo se ha acertado al Wumpus

        def check_data_input(_data):  # para comprobar si los datos son válidos
            try:
                _data = int(_data)
            except Exception:
                Exception('Valor introducido no válido')
            if not isinstance(_data, int) and _data <= 0:
                raise Exception('Introduce un valor numérico válido.')
            return _data

        print("Bienvenido a Hunt the Wumpus")
        # introducción de datos
        data = input("\nDefine los parámetros del juego:\n\nTamaño de la mazmorra (lado):\n")
        data = check_data_input(data)
        self.size = data
        data = input("Cantidad de pozos:\n")
        data = check_data_input(data)
        self.n_pool = np.abs(data)
        data = input("Cantidad munición:\n")
        data = check_data_input(data)
        self.pj_ammo = np.abs(data)
        # creación mapa, personaje y wumpus
        self.mapa = lib.Mapa(self.size, self.n_pool)
        self.pj = lib.Personaje(self.pj_ammo)
        self.wumpus = lib.Wumpus()

    def test(self):
        print(f"hedor %s"%self.mapa.posicion_hedor)
        print(f"wumpus %s"%self.mapa.posicion_wumpus)
        print(f"orientacion wumpus %i"%self.wumpus.orientacion)
        print(f"pozos %s"%self.mapa.posicion_pozo)
        print(f"brisas %s"%self.mapa.posicion_brisa)
        print(f"jugador %s"%self.mapa.posicion_jugador)
        print(f"orientacion jugador %i"%self.pj.orientacion)
        print(f"tesoro %s"%self.mapa.posicion_tesoro)

    def ini(self):
        self.check_reglas()
        while self.juego:  # bucle principal del programa
            # self.test()
            self.peticion_accion()  # método que muestra los movimientos posibles y recoge la elección
            self.wumpus.movimiento(self.mapa)  # método que mueve al wumpus
            self.check_reglas()  # método que aplica las reglas del juego
        print("Gracias por jugar")

    def check_reglas(self):
        if not self.juego:  # si el juego ya ha acabado no checkeo las reglas
            return
        if self.mapa.posicion_jugador == self.mapa.posicion_wumpus and self.wumpus.vivo:
            print("Percives al Wumpus, te alcanzo")
            self.juego = False
            return
        if self.mapa.posicion_jugador in self.mapa.posicion_pozo:
            print("Caistes en un pozo")
            self.juego = False
            return
        if self.mapa.posicion_jugador == self.mapa.posicion_tesoro and not self.pj.tesoro:
            print("Percibes brillo")
            self.pj.coger_tesoro()
        if self.mapa.posicion_jugador in self.mapa.posicion_hedor and self.wumpus.vivo:
            print("Percibes hedor")
        if self.mapa.posicion_jugador in self.mapa.posicion_brisa:
            print("Percibes brisa")
        if self.mapa.posicion_jugador == self.mapa.posicion_salida and self.pj.tesoro:
            print("Alcanzaste la salida")
            return
        if self.acierto_disparo:
            print("Percibes grito")
            self.acierto_disparo = False
        if self.mapa.posicion_jugador[1] == self.size - 1 and self.pj.orientacion == 0:
            print("percibes pared")
        if self.mapa.posicion_jugador[0] == self.size - 1 and self.pj.orientacion == 1:
            print("percibes pared")
        if self.mapa.posicion_jugador[1] == 0 and self.pj.orientacion == 2:
            print("percibes pared")
        if self.mapa.posicion_jugador[0] == 0 and self.pj.orientacion == 3:
            print("percibes pared")

    def peticion_accion(self):
        print("introduzca acción a realizar:\n"
              "1 - girar 90º izquierda\n"
              "2 - girar 90º derecha\n"
              "3 - avanzar una casilla")
        if self.pj.ammo > 0:
            print("4 - disparar")
        if self.pj.tesoro and self.mapa.posicion_jugador == self.mapa.posicion_salida:
            print("5 - salir")
        while True:
            data = input()
            try:
                data = int(data)
            except Exception:
                raise Exception("valor introducido erroneo")
            if 0 <= data < 4:
                break
            if data == 4:
                if self.pj.ammo > 0:
                    break
                else:
                    print("munición insuficiente")
            if data == 5:
                if self.pj.tesoro and self.mapa.posicion_jugador == self.mapa.posicion_salida:
                    break
                else:
                    print("no se cumplen las condiciones")
            if data < 0 or data > 4:
                print("orden no valida")
        # aplicación de la acción
        if data == 1:
            self.pj.giro_izquierda()
        if data == 2:
            self.pj.giro_derecha()
        if data == 3:
            self.mapa.movimiento_pj(self.pj.orientacion)
        if data == 4:
            self.pj.disparo()
            self.acierto_disparo = self.mapa.check_disparo(self.pj.orientacion, self.wumpus)
        if data == 5 and self.pj.tesoro and self.mapa.posicion_jugador == self.mapa.posicion_salida:
            self.juego = False


if __name__ == '__main__':
    game = Wumpus()
    game.ini()
