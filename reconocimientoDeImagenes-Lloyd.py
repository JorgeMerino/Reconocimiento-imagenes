# -*- coding: utf-8 -*-

from PIL import Image
from math import sqrt
from bottle import route, run, static_file, post, request

class Kmedias(object):
    __tolerancia = 0.1
    __gamma = 0.1
    __b = 2
    __dimPixel = None
    
    def __init__(self, imgEntrenamiento, imgClasificacion):
        self.__imagen = Image.open(imgEntrenamiento)
        self.__pixelMap = self.__imagen.load()
        self.__numCentros = 5
        self.__dimPixel = 3
        
        nuevosCentros = self.__entrenamiento([(0, 0, 0)]*self.__numCentros)
        self.__imagen = Image.open(imgClasificacion)
        self.__pixelMap = self.__imagen.load()
        self.__clasificacion(nuevosCentros)
        self.__imagen.show()
        
    def __entrenamiento(self, centros):
        distancias = [0.0]*self.__numCentros
        posicionMinima = 0
        nuevosCentros = centros
        criteriosFinalizacion = [0]*self.__numCentros
        
        for i in range(self.__imagen.size[0]):
            for j in range(self.__imagen.size[1]):
                for k in range(self.__numCentros):
                    distancias[k]=self.__distanciaEuclidea(self.__pixelMap[i, j], centros[k])
                posicionMinima = self.__posicionMinima(distancias)
                nuevosCentros[posicionMinima] = self.__sumaListas(nuevosCentros[posicionMinima] ,self.__multiplicaLista(self.__restaListas(self.__pixelMap[i, j], nuevosCentros[posicionMinima]), self.__gamma))

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
                if matrizPertenencias[i][j][n] < 0.30:
                    self.__pixelMap[i, j] = (0, 0, 0)
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
       
        
    def __posicionMinima(self, distancias):
        minPosicion = 0
        for k in range(self.__numCentros):
            if distancias[minPosicion] > distancias[k]:
                minPosicion = k
                
        return minPosicion
        
        
    def __sumaListas(self, lista1, lista2):
        aux = []
        for i in range(len(lista1)):
            aux.append(lista1[i] + lista2[i])
            
        return aux
        
        
    def __restaListas(self, lista1, lista2):
        aux = []
        for i in range(len(lista1)):
            aux.append(lista1[i] - lista2[i])
            
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
    

path = 'C:\Users\Jorge\Desktop'
        
#miObjeto = Kmedias()
@route('/')
def funcion():
    return static_file ('reconocimientoImagenes.html', path)
    
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root=path)
  
@post('/procesarImagen')
def procesar():
    imgEntrenamiento = request.files['imgEntrenamiento']
    imgClasificacion = request.files['imgClasificacion']
    
    imgEntrenamiento = path + "\\" + imgEntrenamiento.filename
    imgClasificacion = path + "\\" + imgClasificacion.filename
    Kmedias(imgEntrenamiento, imgClasificacion)

run(host='0.0.0.0', port=8080)