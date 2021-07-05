#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import QUIT
import numpy as np
import os
import sys
from escenario import Escenario
import time
import random
from persona import Persona
from celdas import evalua_celda_vecina
from fuego import Fuego


# Crea una instancia de escenario
plano = Escenario()

# Crea una instancia de fuego
fueguito = Fuego()

directorio = os.path.dirname(__file__)

# Obtiene ruta de la matriz cargada por el usuario
ruta_archivo = os.path.join(directorio, 'path.txt')

# Abre archivo - Ejecuta - Cierra
with open(ruta_archivo, "r") as archivo:  
    plano.archivo = archivo.read()

# Obtiene lo indicado por el usuario sobre el sistema contra incendios
archivo_extintores = os.path.join(directorio, 'extintores.txt')
with open(archivo_extintores, "r") as extintores:
    fueguito.contra_incendios = bool(extintores.read())

# Almacena la ruta al archivo de informes
archivo_informe = os.path.join(directorio, 'informe.txt')

# Configuración de valores iniciales
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

COLOR_FONDO = 25, 25, 25

DIMENSION_CELDA = 20


# Tamaño de la matriz
nxC, nyC = plano.cantidad_celdas()

# Establece el ancho y alto de la pantalla
ancho_pantalla = nxC * DIMENSION_CELDA
alto_pantalla = nyC * DIMENSION_CELDA

screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))

# Color de fondo de la pantalla
screen.fill(COLOR_FONDO)

# Establece el nombre de la pantalla según el nombre del archivo
pygame.display.set_caption(plano.nombre_archivo())


def main():

    # Inicia pygame
    pygame.init()

    # Variable bandera para pausar la simulacion
    pauseExect = False

    # Variable bandera para finalizar la simulacion
    Terminar = 0

    # Crea el estado del juego a partir del archivo provisto por el usuario
    estado_juego = plano.escenario()

    # Contadores de estado de las personas
    muertos = 0
    heridos = 0
    salvados = 0

    # Crea una lista con las posiciones de las personas
    personas = []

    # Recorre la matriz y crea una persona en la posición correspondiente (9)
    ide = 0
    for y in range(0, nxC):
        for x in range(0, nyC):
            if estado_juego[x, y] == 9:
                personas.append(Persona(ide, estado_juego, x, y))
                ide += 1

    # Establece un valor inicial de propagación que disminuye en cada iteración
    # si se cuenta con sistema contra incendios
    propagacion = 100

    # -------- Loop principal -----------
    while True:

        # Disminuye velocidad
        time.sleep(0.3)

        # Crea un nuevo estado sobre el que se producen las modificaciones
        nuevo_estado = np.copy(estado_juego)

        screen.fill(COLOR_FONDO)

        # Maneja los eventos
        ev = pygame.event.get()

        for event in ev:

            # Detectamos si se presiona una tecla pra controlar la pausa
            if event.type == pygame.KEYDOWN:
                pauseExect = not pauseExect

            # Cierra la simulacion si se cierra la ventana
            if event.type == QUIT:
                # Guarda el estado de las personas al cerrar la simulacion
                with open(archivo_informe, "a") as informe:
                    informe.write(f'Salvados ilesos: {salvados}')
                    informe.write('\n')
                    informe.write(f'Salvados heridos: {heridos}')
                    informe.write('\n')
                    informe.write(f'Muertos: {muertos}')
                pygame.quit()
                sys.exit()

        # Variable bandera para controlar el movimiento
        mover = True

        # Recorre la matriz
        for y in range(0, nxC):
            for x in range(0, nyC):

                # Calcula el polígono (cuadrado) que forma la celda.
                poly = [(y * DIMENSION_CELDA, (x) * DIMENSION_CELDA),
                        (y * DIMENSION_CELDA, (x+1) * DIMENSION_CELDA),
                        ((y+1) * DIMENSION_CELDA, (
                            (x+1) * DIMENSION_CELDA)),
                        ((y+1) * DIMENSION_CELDA, (
                            (x) * DIMENSION_CELDA))]

                # Dibuja cada elemento según el número
                if estado_juego[x, y] == 0:
                    pygame.draw.polygon(screen, (40, 40, 40), poly, 1)
                elif estado_juego[x, y] == 2:
                    pygame.draw.polygon(screen, (40, 40, 40), poly, 0)
                elif estado_juego[x, y] == 5:
                    pygame.draw.polygon(screen, (VERDE), poly, 0)
                elif estado_juego[x, y] == 6:
                    pygame.draw.polygon(screen, (NEGRO), poly, 0)
                elif estado_juego[x, y] == 7:
                    pygame.draw.polygon(screen, (ROJO), poly, 0)
                elif estado_juego[x, y] == 8:
                    pygame.draw.polygon(screen, (ROJO), poly, 0)
                elif estado_juego[x, y] == 9:
                    pygame.draw.polygon(screen, (0, 255, 255), poly, 0)
                elif estado_juego[x, y] == 1:
                    pygame.draw.polygon(screen, (BLANCO), poly, 0)
                else:
                    pygame.draw.polygon(screen, (40, 40, 40), poly, 0)

                # Movimientos

                celdas_vecinas = {}
                celdas_vecinas_fuego = {}

                if not pauseExect:

                    # Propagación del fuego
                    if estado_juego[x, y] == 7:

                        # Controla que disminuya la propagacion del fuego hasta detenerse 
                        # si hay sistema contra incendios
                        if fueguito.contra_incendios and propagacion > 20:
                            if (random.choice(range(20)) <= 4):
                                celdas_vecinas_fuego = evalua_celda_vecina(x, y, nuevo_estado)
                                fueguito.propagacion_fuego(x, y, nxC, nyC, celdas_vecinas_fuego, nuevo_estado)
                                propagacion -= 1
                        elif fueguito.contra_incendios and propagacion <= 20 and propagacion > 0:
                            if (random.choice(range(20)) <= 1):
                                celdas_vecinas_fuego = evalua_celda_vecina(x, y, nuevo_estado)
                                fueguito.propagacion_fuego(x, y, nxC, nyC, celdas_vecinas_fuego, nuevo_estado)
                                propagacion -= 1
                        # Detiene la propagacion
                        elif fueguito.contra_incendios and propagacion <= 0:
                            propagacion = 0

                        # Propagación del fuego constante sin sistema contra incendios
                        else:
                            if (random.choice(range(20)) <= 4):
                                celdas_vecinas_fuego = evalua_celda_vecina(x, y, nuevo_estado)
                                fueguito.propagacion_fuego(x, y, nxC, nyC, celdas_vecinas_fuego, nuevo_estado)

                    # Movimiento de las personas
                    if estado_juego[x, y] == 9:
                        if len(personas) > 0:
                            if mover:
                                for person in personas:
                                    celdas_vecinas = evalua_celda_vecina(person.x, person.y, nuevo_estado)
                                    person.elegir_direccion(
                                        nuevo_estado, celdas_vecinas)

                                    # Si muere
                                    if person.muerto == True:
                                        personas.remove(person)
                                        muertos += 1

                                    # Si nunca toca el fuego y se salva
                                    elif person.salvado == True and person.herido2 == False:
                                        personas.remove(person)
                                        salvados += 1 #Salvado ileso

                                    # Si se salvo y se quemo 1 vez
                                    elif person.salvado == True and person.herido2 == True:
                                        personas.remove(person) 
                                        heridos += 1 #Salvado herido

                                    # Si toca el fuego una vez (no muere)
                                    elif person.herido == True and person.herido2 == False:
                                        person.herido2 = True 
                                        person.herido = False

                                    # Si toca el fuego más de una vez muere(muere y se elimina la persona de la lista)
                                    elif person.herido == True and person.herido2 == True:
                                        personas.remove(person) 
                                        muertos += 1

                            mover = False

        # Si todas las personas mueren o evacuan
        if (len(personas) == 0):
            # Borra archivo que controla extintores
            with open(archivo_extintores, "w") as extintores:
                extintores.write('')

            Terminar += 1
            if Terminar == 6:

                # Guarda el estado de las personas al finalizar la simulacion
                with open(archivo_informe, "a") as informe:
                    informe.write(f'Salvados ilesos: {salvados}')
                    informe.write('\n')
                    informe.write(f'Salvados heridos: {heridos}')
                    informe.write('\n')
                    informe.write(f'Muertos: {muertos}')

                time.sleep(1)
                break

        # Copia las modificaciones al estado general
        estado_juego = np.copy(nuevo_estado)

        # Recarga la pantalla
        pygame.display.flip()


if __name__ == '__main__':
    main()
