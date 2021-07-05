#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Este módulo contiene la clase que crea el escenario"""

import numpy as np
import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog


class Escenario(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.archivo = ''  

    def buscarRutaArchivo(self):
        """ Abre una ventana en donde se puede buscar un archivo .txt con el plano"""
        archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', '/home')
        self.archivo = archivo[0]

    def crear_matriz_desde_archivo(self):
        """ Transforma una matriz de números en un array de 2 dimensiones """
        try:
            matriz = np.genfromtxt(self.archivo, delimiter=',')
        except UnicodeDecodeError:
            print('Archivo inválido')
            print('Los archivos deben ser de extension .txt')
            sys.exit()
        except OSError:
            print('La ruta especificada no existe')
            print('Por favor cambie la ruta a un archivo válido')
            sys.exit()
        except ValueError:
            print('La matriz no es válida')
            sys.exit()
        else:
            return matriz

    def nombre_archivo(self):
        """ Obtiene el nombre del archivo """
        auxlist = list(self.archivo.split('/'))
        nombre = auxlist[len(auxlist)-1]
        return nombre

    def cantidad_celdas(self):
        """ Devuelve el valor de las celdas horizontales y verticales """
        grid = self.crear_matriz_desde_archivo()
        return len(grid[0])-1, len(grid)

    def escenario(self):
        grid = self.crear_matriz_desde_archivo()
        return grid
