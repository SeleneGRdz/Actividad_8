from particula import Particula

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


#L1 = Particula(id=1234, origen_x=45, origen_y=12,destino_x=32, destino_y=12, velocidad=203, red=1, green=0, blue=120)
#L2 = Particula(id=3421, origen_x=51, origen_y=2,destino_x=98, destino_y=1, velocidad=10, red=13, green=12, blue=132)
#administrador = Administrador()
#administrador.agregar_final(L1)
#administrador.agregar_final(L2)
#administrador.mostrar()