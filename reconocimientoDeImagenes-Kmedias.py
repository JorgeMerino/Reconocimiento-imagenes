# -*- coding: utf-8 -*-

from PIL import Image
from math import sqrt
imagenOriginal = Image.open("C:\Users\Jorge\Desktop\imagen.jpg")
pixelMap = imagenOriginal.load()

imagenProcesada = Image.new( imagenOriginal.mode, imagenOriginal.size)
pixelsNew = imagenProcesada.load()
for i in range(imagenProcesada.size[0]):
    for j in range(imagenProcesada.size[1]):
        if 100 in pixelMap[i,j]:
            pixelsNew[i,j] = (255,0,255,40)
        else:
            pixelsNew[i,j] = pixelMap[i,j]
#imagenProcesada.show()





class Kmedias(object):
    __tolerancia = 0.1
    __b = 2
    __dimPixel = None    
    
    def __init__(self):
        self.__imagen = Image.open("C:\Users\Jorge\Desktop\imagen.jpg")
        self.__pixelMap = self.__imagen.load()
        self.__numCentros = 4
        self.__dimPixel = 3
        
        nuevosCentros = self.__entrenamiento([(63, 63, 191), (25, 76, 25), (197, 197, 92), (92, 197, 197)])
        self.__clasificacion(nuevosCentros)
        #self.__clasificacion([(63, 63, 191), (25, 76, 25), (197, 197, 92), (92, 197, 197)])
        self.__imagen.show()
        
    def __entrenamiento(self, centros):
        distancias = [0.0]*self.__numCentros
        matrizPertenencias = [[[0.0]*self.__numCentros]*self.__imagen.size[1]]*self.__imagen.size[0]
        denominadorPertenencias = 0
        
        nuevosCentros = [[0]*self.__dimPixel]*self.__numCentros
        numeradorNuevoCentro = [[0]*self.__dimPixel]*self.__numCentros
        denominadorNuevoCentro = [0]*self.__numCentros
        
        criteriosFinalizacion = [0]*self.__numCentros
        for i in range(self.__imagen.size[0]):
            for j in range(self.__imagen.size[1]):
                denominadorPertenencias = 0
                for k in range(self.__numCentros):
                    distancias[k]=self.__distanciaEuclidea(self.__pixelMap[i, j], centros[k]) ** 2
                    if(distancias[k] != 0):
                        denominadorPertenencias += ((1 / distancias[k]) ** (1 / (self.__b - 1)))
                for k in range(self.__numCentros):
                    if(distancias[k] != 0):
                        matrizPertenencias[i][j][k] = ((1/distancias[k]) ** (1/(self.__b-1))) / denominadorPertenencias
       
        for i in range(self.__imagen.size[0]):
            for j in range(self.__imagen.size[1]):
                for k in range(self.__numCentros):
                    numeradorNuevoCentro[k] = self.__sumaListas(numeradorNuevoCentro[k], self.__multiplicaLista(self.__pixelMap[i, j], (matrizPertenencias[i][j][k] ** self.__b)))
                    denominadorNuevoCentro[k] += (matrizPertenencias[i][j][k] ** self.__b)
                    
        for k in range(self.__numCentros):    
            nuevosCentros[k] = self.__divideLista(numeradorNuevoCentro[k], denominadorNuevoCentro[k])
                
        for k in range(self.__numCentros):
            criteriosFinalizacion[k] = self.__distanciaEuclidea(nuevosCentros[k], centros[k])
            
        for k in range(self.__numCentros):
            if criteriosFinalizacion[k] >= self.__tolerancia:
                return self.__entrenamiento(nuevosCentros)
                break
        
        return nuevosCentros
            
            
    def __clasificacion(self, centros):
        distancias = [0.0]*self.__numCentros
        matrizPertenencias = [[[0.0]*self.__numCentros]*self.__imagen.size[1]]*self.__imagen.size[0]
        denominadorPertenencias = 0
        for i in range(self.__imagen.size[0]):
            for j in range(self.__imagen.size[1]):
                denominadorPertenencias = 0
                for k in range(self.__numCentros):
                    distancias[k]=self.__distanciaEuclidea(self.__pixelMap[i, j], centros[k])
                    if(distancias[k] != 0):
                        denominadorPertenencias += ((1 / distancias[k]) ** (1 / (self.__b - 1)))
                for k in range(self.__numCentros):
                    if(distancias[k] != 0):
                        matrizPertenencias[i][j][k] = ((1/distancias[k]) ** (1/(self.__b-1))) / denominadorPertenencias

                n = self.__posicionMaxima(matrizPertenencias[i][j])
                if matrizPertenencias[i][j][n] < 0.0:
                    self.__pixelMap[i, j] = (0, 0, 0, 0)
                else:
                    self.__pixelMap[i, j] = (int(centros[n][0]), int(centros[n][1]), int(centros[n][2]))

                    
    def __distanciaEuclidea(self, punto, centro):
        distancia = 0
        for i in range(self.__dimPixel):
            distancia += ((punto[i] - centro[i]) ** 2)
            
        return sqrt(distancia)
        
        
    def __posicionMaxima(self, pertenenciaPixel):
        maxPosicion = 0
        for k in range(self.__numCentros):
            if pertenenciaPixel[maxPosicion] < pertenenciaPixel[k]:
                maxPosicion = k
                
        return maxPosicion
       
        
    def __sumaListas(self, lista1, lista2):
        aux = []
        for i in range(len(lista1)):
            aux.append(lista1[i] + lista2[i])
            
        return aux
    
        
    def __multiplicaLista(self, lista, factor):
        aux = []
        for elemento in lista:
            aux.append(elemento * factor)
            
        return aux
            
    
    def __divideLista(self, lista, dividendo):
        aux = []
        for elemento in lista:
            aux.append(elemento / dividendo)
            
        return aux
    
        
miObjeto = Kmedias()