#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Este módulo contiene la funcion que analiza las celdas contiguas """


# Almacena el valor de las celdas vecinas
def evalua_celda_vecina(x, y, nuevo_estado):
    """ Registra el valor de la primer celda en cada dirección """
    celdas_vecinas = {}  
    celdas_vecinas.update({'derecha': nuevo_estado[x, y+1]})
    celdas_vecinas.update({'abajo': nuevo_estado[x+1, y]})
    celdas_vecinas.update({'izquierda': nuevo_estado[x, y-1]})
    celdas_vecinas.update({'arriba': nuevo_estado[x-1, y]})
    return celdas_vecinas