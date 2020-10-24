from particula import Particula
import json

class Administrador:
    def __init__(self):
        self.__particulas = []

    def agregar_final(self, particula:Particula):
        self.__particulas.append(particula)

    def agregar_inicio(self, particula:Particula):
        self.__particulas.insert(0, particula)

    def mostrar(self):
        for particula in self.__particulas:
            print(particula)

    def __str__(self):
        return "".join(
            str(particula) + '\n' for particula in self.__particulas
        ) 

    def guardar(self, ubicacion):
        try:
            #r significa que será escritura
            with open(ubicacion, 'w') as archivo:
                lista = [particula.to_dict() for particula in self.__particulas]
                print(lista)
                #Vaciado de la información
                json.dump(lista, archivo, indent=5)
            return 1
        except:
            return 0

    def abrir(self, ubicacion):
        try:
            with open(ubicacion,'r') as archivo:
                lista = json.load(archivo)
                self.__particulas = [Particula(**particula) for particula in lista]
            return 1
        except:
            return 0

#L1 = Particula(id=1234, origen_x=45, origen_y=12,destino_x=32, destino_y=12, velocidad=203, red=1, green=0, blue=120)
#L2 = Particula(id=3421, origen_x=51, origen_y=2,destino_x=98, destino_y=1, velocidad=10, red=13, green=12, blue=132)
#administrador = Administrador()
#administrador.agregar_final(L1)
#administrador.agregar_final(L2)
#administrador.mostrar()