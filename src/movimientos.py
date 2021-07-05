#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Este módulo contiene todas las funciones que realizan el movimiento """


# Devuelve la direccion que no debe volver a tomar
def volver(direccion_anterior):
    """ Devuelve el opuesto a la dirección ingresada """
    if direccion_anterior == 'izquierda':
        return 'derecha'
    elif direccion_anterior == 'derecha':
        return 'izquierda'
    elif direccion_anterior == 'arriba':
        return 'abajo'
    elif direccion_anterior == 'abajo':
        return 'arriba'


# Métodos que realizan el movimiento
def izquierda(x, y, nuevo_estado, valor_anterior):
    """ Realiza el movimiento hacia la izquierda """
    actual = nuevo_estado[x, y]
    proximo = nuevo_estado[x, y-1]
    if proximo != 6:
        valor_anterior = proximo
    nuevo_estado[x, y] = proximo
    nuevo_estado[x, y-1] = actual
    return valor_anterior


def derecha(x, y, nuevo_estado, valor_anterior):
    """ Realiza el movimiento hacia la derecha """
    actual = nuevo_estado[x, y]
    proximo = nuevo_estado[x, y+1]
    if proximo != 6:
        valor_anterior = proximo
    nuevo_estado[x, y] = proximo
    nuevo_estado[x, y+1] = actual
    return valor_anterior


def arriba(x, y, nuevo_estado, valor_anterior):
    """ Realiza el movimiento hacia abajo """
    actual = nuevo_estado[x, y]
    proximo = nuevo_estado[x-1, y]
    if proximo != 6:
        valor_anterior = proximo
    nuevo_estado[x, y] = proximo
    nuevo_estado[x-1, y] = actual
    return valor_anterior


def abajo(x, y, nuevo_estado, valor_anterior):
    """ Realiza el movimiento hacia arriba """
    actual = nuevo_estado[x, y]
    proximo = nuevo_estado[x+1, y]
    if proximo != 6:
        valor_anterior = proximo
    nuevo_estado[x, y] = proximo
    nuevo_estado[x+1, y] = actual
    return valor_anterior
