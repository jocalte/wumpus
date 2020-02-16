"""
José Miguel Calderón Terol
15/02/2020
version 1.0
"""
import numpy as np
import copy

class Mapa(object):
    """
    Clase que crea el mapa, recoje los movimientos de avance del jugador y comprueba el disparo.
    Los objetos se almacenan en listas que contienen sus coordenadas.
    """

    def __init__(self, size, n_pool):
        self.posicion_salida = []
        self.posicion_pozo = []
        self.posicion_brisa = []
        self.posicion_wumpus = []
        self.posicion_hedor = []
        self.posicion_jugador = []
        self.posicion_tesoro = []
        self.size = size
        self.n_pool = n_pool
        # casillas libres, según se crea un objeto se saca su casilla para no crear dos objetos en el mismo lugar
        self.casillas = [i for i in np.arange(size**2)]
        if self.size < 3:
            raise Exception("valor mínimo 3 de lado")

        # calculo índice
        def indice(elemento):
            if elemento < self.size:
                y, x = 0, elemento
            else:
                y = int(elemento // self.size)
                x = elemento % self.size
            return [x, y]

        # posición salida
        self.posicion_salida = [0, 0]
        self.casillas.remove(0)
        self.casillas.remove(1)
        self.casillas.remove(self.size)

        # posición inicial
        self.posicion_jugador = [0, 0]

        # posición pozos
        for _ in range(self.n_pool):
            if len(self.casillas) < 3:
                raise Exception("demasiados pozos")
            _posicion = self.casillas[np.random.randint(len(self.casillas))]
            self.posicion_pozo.append(indice(_posicion))
            self.casillas.remove(_posicion)

        # posición brisa
        for ind in self.posicion_pozo:
            self.posicion_brisa = self.posicion_brisa + FuncionesAuxiliares.generador_posiciones_alrededor(ind,
                                                                                                           self.size)

        # posición wumpus
        posicion = self.casillas[np.random.randint(len(self.casillas))]
        self.posicion_wumpus = indice(posicion)
        self.casillas.remove(posicion)

        # posición hedor
        self.posicion_hedor = FuncionesAuxiliares.generador_posiciones_alrededor(self.posicion_wumpus, self.size)

        # posición tesoro
        posicion = self.casillas[np.random.randint(len(self.casillas))]
        self.posicion_tesoro = indice(posicion)
        self.casillas.remove(posicion)
        print()

    def movimiento_pj(self, ori):
        """
        avanza una casilla en la orientación indicado por ori, siempre que no nos salgamos del tablero
        :param ori: orientacion
        :return:
        """
        if ori == 0 and self.posicion_jugador[1] < self.size - 1:
            self.posicion_jugador[1] = self.posicion_jugador[1] + 1
        elif ori == 1 and self.posicion_jugador[0] < self.size - 1:
            self.posicion_jugador[0] = self.posicion_jugador[0] + 1
        elif ori == 2 and self.posicion_jugador[1] > 0:
            self.posicion_jugador[1] = self.posicion_jugador[1] - 1
        elif ori == 3 and self.posicion_jugador[0] > 0:
            self.posicion_jugador[0] = self.posicion_jugador[0] - 1
        else:
            print("pared alcanzada, orden no realizada")

    def check_disparo(self, ori, wumpus):
        acierto = False
        if wumpus.vivo:
            if ori == 0:  # dispara hacia arriba
                if self.posicion_wumpus[0] == self.posicion_jugador[0] and \
                        self.posicion_wumpus[1] > self.posicion_jugador[1]:
                    acierto = True
            if ori == 1:  # dispara hacia la derecha
                if self.posicion_wumpus[1] == self.posicion_jugador[1] and \
                        self.posicion_wumpus[0] > self.posicion_jugador[0]:
                    acierto = True
            if ori == 2:  # dispara hacia abajo
                if self.posicion_wumpus[0] == self.posicion_jugador[0] and \
                        self.posicion_wumpus[1] < self.posicion_jugador[1]:
                    acierto = True
            if ori == 3:  # dispara hacia la izquierda
                if self.posicion_wumpus[1] == self.posicion_jugador[1] and \
                        self.posicion_wumpus[0] < self.posicion_jugador[0]:
                    acierto = True
            if acierto:
                wumpus.mata_wumpus()
                return True
            else:
                return False


class Wumpus(object):
    def __init__(self):
        self.vivo = True
        self.orientacion = 0  # 0 arriba, 1 derecha, 2 abajo, 3 izquierda

    def mata_wumpus(self):
        self.vivo = False

    def movimiento(self, mapa):
        if self.vivo:
            if np.random.randint(2) == 0:  # aleatoriamente decide si girar o avanzar
                self.girar()
            else:
                self.avanza(mapa)

    def girar(self):
        if np.random.randint(2) == 0:  # aleatoriamente decide si girar a la izquierda o a la derecha
            self.orientacion = (self.orientacion - 1) % 4
        else:
            self.orientacion = (self.orientacion + 1) % 4

    def avanza(self, mapa):
        posicion = copy.deepcopy(mapa.posicion_wumpus)
        if self.orientacion == 0 and mapa.posicion_wumpus[1] < mapa.size - 1:
            posicion[1] = posicion[1] + 1  # me guardo la nueva posicion actualizada
        if self.orientacion == 1 and mapa.posicion_wumpus[0] < mapa.size - 1:
            posicion[0] = posicion[0] + 1  # me guardo la nueva posicion actualizada
        if self.orientacion == 2 and mapa.posicion_wumpus[1] > 0:
            posicion[1] = posicion[1] - 1  # me guardo la nueva posicion actualizada
        if self.orientacion == 3 and mapa.posicion_wumpus[0] > 0:
            posicion[0] = posicion[0] - 1  # me guardo la nueva posicion actualizada
        if posicion not in mapa.posicion_pozo:  # checkeo la validez
            mapa.posicion_wumpus = posicion  # actualizo si no tropieza con nada
            mapa.posicion_hedor = FuncionesAuxiliares.generador_posiciones_alrededor(posicion, mapa.size)


class Personaje(object):
    def __init__(self, ammo):
        self.ammo = ammo
        self.orientacion = 0  # 0 arriba, 1 derecha, 2 abajo, 3 izquierda
        self.tesoro = False  # True cuando encuentre al tesoro

    def disparo(self):
        self.ammo -= 1

    def giro_derecha(self):
        self.orientacion = (self.orientacion + 1) % 4

    def giro_izquierda(self):
        self.orientacion = (self.orientacion - 1) % 4

    def coger_tesoro(self):
        self.tesoro = True


class FuncionesAuxiliares:
    @staticmethod
    def generador_posiciones_alrededor(ind, size):
        salida = []
        x, y = ind[0], ind[1]
        if x > 0:
            salida.append([x - 1, y])
        if y > 0:
            salida.append([x, y - 1])
        if x < size - 1:
            salida.append([x + 1, y])
        if y < size - 1:
            salida.append([x, y + 1])
        return salida
