#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Este modulo gestiona el comportamiento del fuego """
from celdas import evalua_celda_vecina
from main import extintores

class Fuego():

    def __init__(self):
        self.contra_incendios = False
        self.propagacion = 0.5

    def propagacion_fuego(self, x, y, celdasy, celdasx, celdas_vecinas_fuego, nuevo_estado):
        # Se propaga dentro de los límites del plano
        if y > 1 and y < (celdasy - 1):
            if x > 1 and x < (celdasx - 1):
                for direccion in celdas_vecinas_fuego:
                    # Ignora celdas con fuego o salidas
                    if celdas_vecinas_fuego[direccion] == 7 or (
                        celdas_vecinas_fuego[direccion] == 6 or celdas_vecinas_fuego[direccion] == 8):
                        continue

                    #Coloca 8 para no volver a evaluar la celda
                    elif celdas_vecinas_fuego[direccion] == 1:
                        nuevo_estado[x, y] = 8

                    # Se propaga hacia todos los casilleros de alrededor y coloca
                    # un 8 en el actual para no volver a evaluar la celda
                    else: 
                        if direccion == "derecha":                  
                                nuevo_estado[x, y+1] = 7
                                nuevo_estado[x, y] = 8
                        elif direccion == "arriba":                  
                                nuevo_estado[x-1, y] = 7
                                nuevo_estado[x, y] = 8
                        elif direccion == "abajo":                 
                                nuevo_estado[x+1, y] = 7
                                nuevo_estado[x, y] = 8
                        elif direccion == "izquierda":                                    
                                nuevo_estado[x, y-1] = 7
                                nuevo_estado[x, y] = 8
