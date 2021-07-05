#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Clase que genera objetos persona """

import random
from movimientos import volver, izquierda, derecha, arriba, abajo


class Persona():

    def __init__(self, ide, estado, x, y):
        self.ide = ide

        # Atributos de posicion
        self.estado = estado
        self.x = x
        self.y = y
        self.direccion_anterior = 'a'
        self.valor_anterior = 0

        # Atributos de estado
        self.muerto = False
        self.herido = False
        self.herido2 = False
        self.salvado = False

        # Variable bandera para controlar el ingreso a un camino de emergencia
        self.salida_emergencia = True

    def elegir_direccion(self, nuevo_estado, celdas_vecinas):
        """ Elije una de las celdas y realiza el movimiento """
        celdas_validas = []
        camino = []        
        movimiento = False

        # Para cada dirección ejecuta según el valor en la matriz
        for direccion in celdas_vecinas:

            # Camino de salida de emergencia
            if celdas_vecinas[direccion] == 6:                
                camino.append(direccion) 
                celdas_validas.append(direccion)
                self.salida(nuevo_estado, direccion)
                movimiento = True
            elif celdas_vecinas[direccion] == 5:
                camino.append(direccion)
                if self.salida_emergencia: 
                    self.ingreso_camino_emergencia(
                        nuevo_estado, direccion)
                    self.salida_emergencia = False                  
                    movimiento = True

            # Espacio vacio o puerta
            elif celdas_vecinas[direccion] == 0:
                celdas_validas.append(direccion)

            # Pared
            elif celdas_vecinas[direccion] == 1:
                continue

            # Fuego
            elif celdas_vecinas[direccion] == 7 or celdas_vecinas[direccion] == 8:
                self.herido = True
                continue

            # Personas
            elif celdas_vecinas[direccion] == 9:
                continue

        # Se ejecuta cuando está dentro de un camino de emergencia
        if len(camino) > 0 and movimiento == False:
            # No elimina elementos de listas con un solo elemento
            if len(camino) > 1:
                for direccion in camino:
                    if direccion == volver(self.direccion_anterior):
                        camino.remove(volver(self.direccion_anterior))

            # Elige entre elementos si la lista tiene al menos dos
            if len(camino) > 1:
                direccion_entre_cincos = random.choice(camino)
            elif len(camino) > 0:
                direccion_entre_cincos = camino[0]

            if len(camino) > 0:
                self.guardar_dirección_anterior(direccion_entre_cincos)
                self.eleccion(direccion_entre_cincos, nuevo_estado)

            # Vacía la lista antes de cada iteración
            camino.clear()

        # Si no es un camino de emergencia

        # Si encontró la salida
        elif self.salvado == True:
            nuevo_estado[self.x, self.y] = 6
        elif movimiento == False:
            # En el primer movimiento
            if self.direccion_anterior == 'a':
                if len(celdas_validas) > 1:
                    direccion_entre_ceros = random.choice(celdas_validas)
                elif len(celdas_validas) > 0:
                    direccion_entre_ceros = celdas_validas[0]
            # En el resto de los movimientos
            else:
                # No elimina elementos de listas con un solo elemento
                if len(celdas_validas) > 1:                     
                    for direccion in celdas_validas:
                        if direccion == volver(self.direccion_anterior):
                            celdas_validas.remove(volver(self.direccion_anterior))

                # Elige entre elementos si la lista tiene al menos dos
                if len(celdas_validas) > 1:                    
                    direccion_entre_ceros = random.choice(celdas_validas)
                elif len(celdas_validas) > 0:
                    direccion_entre_ceros = celdas_validas[0]            

            if len(celdas_validas) > 0:
                self.guardar_dirección_anterior(direccion_entre_ceros)
                self.eleccion(direccion_entre_ceros, nuevo_estado)

        # Vacía la lista antes de cada iteración
        celdas_validas.clear()

    def salida(self, nuevo_estado, direccion):
        """ Indica el movimiento al encontrar una salida """
        # Se mueve a la izquierda
        if direccion == "izquierda":
            if self.valor_anterior == 0:
                nuevo_estado[self.x, self.y-1] = 0
            elif self.valor_anterior == 5:
                nuevo_estado[self.x, self.y-1] = 5
            self.eleccion(direccion, nuevo_estado)
            self.salvado = True

        # Se mueve a la derecha
        elif direccion == "derecha":
            if self.valor_anterior == 0:
                nuevo_estado[self.x, self.y+1] = 0
            elif self.valor_anterior == 5:
                nuevo_estado[self.x, self.y+1] = 5
            self.eleccion(direccion, nuevo_estado)
            self.salvado = True

        # Se mueve hacia arriba
        elif direccion == "arriba":
            if self.valor_anterior == 0: 
                nuevo_estado[self.x-1, self.y] = 0
            elif self.valor_anterior == 5:
                nuevo_estado[self.x-1, self.y] = 5
            self.eleccion(direccion, nuevo_estado)
            self.salvado = True

        # Se mueve hacia abajo
        elif direccion == "abajo":
            if self.valor_anterior == 0:
                nuevo_estado[self.x+1, self.y] = 0
            elif self.valor_anterior == 5:
                nuevo_estado[self.x+1, self.y] = 5
            self.eleccion(direccion, nuevo_estado)
            self.salvado = True

    def ingreso_camino_emergencia(self, nuevo_estado, direccion):
        """ Controla el movimiento al ingresar a un camino de emergencia """
        # Se mueve a la izquierda
        if direccion == "izquierda":
            nuevo_estado[self.x, self.y] = 0
            nuevo_estado[self.x, self.y-1] = 9
            self.actualizar_posicion(self.x, self.y-1)
            self.direccion_anterior = "izquierda"

        # Se mueve a la derecha
        elif direccion == "derecha":
            nuevo_estado[self.x, self.y] = 0
            nuevo_estado[self.x, self.y+1] = 9
            self.actualizar_posicion(self.x, self.y+1)
            self.direccion_anterior = "derecha"

        # Se mueve hacia arriba
        elif direccion == "arriba":
            nuevo_estado[self.x, self.y] = 0
            nuevo_estado[self.x-1, self.y] = 9
            self.actualizar_posicion(self.x-1, self.y)
            self.direccion_anterior = "arriba"

        # Se mueve hacia abajo
        elif direccion == "abajo":
            nuevo_estado[self.x, self.y] = 0
            nuevo_estado[self.x+1, self.y] = 9
            self.actualizar_posicion(self.x+1, self.y)
            self.direccion_anterior = "abajo"

    def guardar_dirección_anterior(self, direccion):
        """ Almacena la última dirección elegida"""
        self.direccion_anterior = direccion

    # LLama al método que realiza el movimiento de acuerdo a la dirección
    def eleccion(self, direccion, nuevo_estado):
        """ Realiza movimiento y almacena valor de la celda anterior """
        if direccion == "izquierda":
            self.valor_anterior = izquierda(self.x, self.y, nuevo_estado, self.valor_anterior)
            self.actualizar_posicion(self.x, self.y-1)
        elif direccion == "derecha":
            self.valor_anterior = derecha(self.x, self.y, nuevo_estado, self.valor_anterior)
            self.actualizar_posicion(self.x, self.y+1)
        elif direccion == "arriba":
            self.valor_anterior = arriba(self.x, self.y, nuevo_estado, self.valor_anterior)
            self.actualizar_posicion(self.x-1, self.y)
        elif direccion == "abajo":
            self.valor_anterior = abajo(self.x, self.y, nuevo_estado, self.valor_anterior)  
            self.actualizar_posicion(self.x+1, self.y)

    def actualizar_posicion(self, x, y):
        """ Actualiza los valores de la posición después de moverse """
        self.x = x
        self.y = y
