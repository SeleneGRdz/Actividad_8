from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsScene
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
from administrador import Administrador
from administrador import Particula
from PySide2.QtGui import QPen, QColor, QTransform
from random import randint
from pprint import pprint, pformat

#Controlador
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() #Se llama a la ventana
        
        self.administrador = Administrador()
        self.grafo = dict()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #Conexión del Slot
        self.ui.agregarFinal_pushButton.clicked.connect(self.click_agregar)
        self.ui.agregarInicio_pushButton.clicked.connect(self.click_agregarInicio)
        self.ui.mostrar_pushButton.clicked.connect(self.click_mostrar)
        
        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)
        self.ui.actionGrafo.triggered.connect(self.to_graph)
        self.ui.actionRecorrido.triggered.connect(self.action_recorrido)

        self.ui.mostrar_tabla_pushButton.clicked.connect(self.mostrar_tabla)
        self.ui.buscar_pushButton.clicked.connect(self.buscar_id)

        self.ui.dibujar.clicked.connect(self.dibujar)
        self.ui.limpiar.clicked.connect(self.limpiar)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.ui.ordenar_id_pushButton.clicked.connect(self.order_id)
        self.ui.ordenar_distancia_pushButton.clicked.connect(self.order_distancia)
        self.ui.ordenar_velocidad_pushButton.clicked.connect(self.order_velocidad)

    
    def order_id(self):
        self.administrador.order_by_id()

    def order_distancia(self):
        self.administrador.order_by_distancia()

    def order_velocidad(self):
        self.administrador.order_by_velocidad()

    def wheelEvent(self, event):
        print(event.delta())
        if event.delta() > 0:
            self.ui.graphicsView.scale(1.2, 1.2)
        else:
            self.ui.graphicsView.scale(0.8, 0.8)

    @Slot()
    def action_recorrido(self):
        
        #Amplitud
        cola = []
        visitados = []
        recorrido = []

        self.to_graph()

        x = self.ui.origenX_spinBox.value() 
        y = self.ui.origenY_spinBox.value()
        cola.append((x,y))
        visitados.append((x,y))
        while cola:
            padre = cola[-1] #En esta parte, se saca el tope de la lista
            recorrido.append(padre)
            del cola[-1]
            adyacentes = self.grafo[padre] #Aquí se sacan los adyacentes
            for a in adyacentes:
                if a[0] not in visitados:
                    visitados.append(a[0])
                    cola.append(a[0])
                else:
                    break
        print(visitados)
        self.ui.salida.insertPlainText("\nAmplitud\n")
        self.ui.salida.insertPlainText(str(recorrido))

        #Profundidad
        pila = []
        visitados = []
        recorrido = []
        
        x = self.ui.origenX_spinBox.value()
        y = self.ui.origenY_spinBox.value()
        pila.append((x,y))
        visitados.append((x,y))
        while pila:
            padre = pila[0] #Sacamos el tope de la lista
            recorrido.append(padre)
            del pila[0]
            adyacentes = self.grafo[padre] #Sacamos los adyacentes
            for a in adyacentes:
                if a[0] not in visitados:
                    visitados.append(a[0])
                    pila.append(a[0])
                else:
                    break
        print(visitados)
        self.ui.salida.insertPlainText("\n\nProfundidad\n")
        self.ui.salida.insertPlainText(str(visitados))

    @Slot()
    def to_graph(self):
        self.ui.salida.clear()
        for particula in self.administrador:
            origen = (particula.origen_x, particula.origen_y)
            destino = (particula.destino_x, particula.destino_y)
            distancia = (particula.distancia)

            arista_origen = (origen, distancia)
            arista_destino = (destino, distancia)

            if origen in self.grafo:
                self.grafo[origen].append(arista_destino)
            else:
                self.grafo[origen] = [arista_destino]
            if destino in self.grafo:
                self.grafo[destino].append(arista_origen)
            else:
                self.grafo[destino] = [arista_origen]
            
            impresion = pformat(self.grafo, width=40)
            impresion+='\n'

        self.ui.salida.insertPlainText(impresion)

    @Slot()
    def dibujar(self):
        #print('dibujar')

        pen = QPen()
        pen.setWidth(2)

        for particula in self.administrador:
            r = particula.red
            g = particula.green
            b = particula.blue

            color = QColor(r, g, b)
            pen.setColor(color)

            x_origen = particula.origen_x
            y_origen = particula.origen_y
            x_destino = particula.destino_x
            y_destino = particula.destino_y

            self.scene.addEllipse(x_origen, y_origen, 6, 6, pen)
            self.scene.addEllipse(x_destino, y_destino, 6, 6, pen)
            self.scene.addLine(x_origen+3, y_origen+3, x_destino+3, y_destino+3, pen)


    @Slot()
    def limpiar(self):
        #print('limpiar')
        self.scene.clear()
        self.ui.graphicsView.setTransform(QTransform())

    @Slot()
    def buscar_id(self):
        id = self.ui.buscar_lineEdit.text()
        encontrado = False
        

        for particula in self.administrador:
            if id == particula.id:
                self.ui.tabla.clear()
                self.ui.tabla.setRowCount(1)

                #Construir widgets
                id_widget = QTableWidgetItem(particula.id)
                origen_x_widget = QTableWidgetItem(str(particula.origen_x))
                origen_y_widget = QTableWidgetItem(str(particula.origen_x))
                destino_x_widget = QTableWidgetItem(str(particula.destino_x))
                destino_y_widget = QTableWidgetItem(str(particula.destino_x))
                velocidad_widget = QTableWidgetItem(str(particula.velocidad))
                red_widget = QTableWidgetItem(str(particula.red))
                green_widget = QTableWidgetItem(str(particula.green))
                blue_widget = QTableWidgetItem(str(particula.blue))
                distancia_widget = QTableWidgetItem(str(particula.distancia))

                #Agregar widgets a cada columna
                self.ui.tabla.setItem(0, 0, id_widget)
                self.ui.tabla.setItem(0, 1, origen_x_widget)
                self.ui.tabla.setItem(0, 2, origen_y_widget)
                self.ui.tabla.setItem(0, 3, destino_x_widget)
                self.ui.tabla.setItem(0, 4, destino_y_widget)
                self.ui.tabla.setItem(0, 5, velocidad_widget)
                self.ui.tabla.setItem(0, 6, red_widget)
                self.ui.tabla.setItem(0, 7, green_widget)
                self.ui.tabla.setItem(0, 8, blue_widget)
                self.ui.tabla.setItem(0, 9, distancia_widget)

                encontrado = True
                return

        if not encontrado:
            QMessageBox.warning(
                self,
                "Atención",
                f'La particula con el id "{id}" no fue encontrada'
            )

    @Slot()
    def mostrar_tabla(self):
        self.ui.tabla.setColumnCount(10) #Genera 10 columnas
        headers = ["ID", "Origen x", "Origen y", "Destino x", "Destino y", "Velocidad", "Red", "Green", "Blue", "Distancia"]
        self.ui.tabla.setHorizontalHeaderLabels(headers)

        self.ui.tabla.setRowCount(len(self.administrador))

        row = 0
        for particula in self.administrador:
            #Construir widgets
            id_widget = QTableWidgetItem(particula.id)
            origen_x_widget = QTableWidgetItem(str(particula.origen_x))
            origen_y_widget = QTableWidgetItem(str(particula.origen_x))
            destino_x_widget = QTableWidgetItem(str(particula.destino_x))
            destino_y_widget = QTableWidgetItem(str(particula.destino_x))
            velocidad_widget = QTableWidgetItem(str(particula.velocidad))
            red_widget = QTableWidgetItem(str(particula.red))
            green_widget = QTableWidgetItem(str(particula.green))
            blue_widget = QTableWidgetItem(str(particula.blue))
            distancia_widget = QTableWidgetItem(str(particula.distancia))

            #Agregar widgets a cada columna
            self.ui.tabla.setItem(row, 0, id_widget)
            self.ui.tabla.setItem(row, 1, origen_x_widget)
            self.ui.tabla.setItem(row, 2, origen_y_widget)
            self.ui.tabla.setItem(row, 3, destino_x_widget)
            self.ui.tabla.setItem(row, 4, destino_y_widget)
            self.ui.tabla.setItem(row, 5, velocidad_widget)
            self.ui.tabla.setItem(row, 6, red_widget)
            self.ui.tabla.setItem(row, 7, green_widget)
            self.ui.tabla.setItem(row, 8, blue_widget)
            self.ui.tabla.setItem(row, 9, distancia_widget)

            row += 1
    
    @Slot()
    def action_abrir_archivo(self):
        ubicacion = QFileDialog.getOpenFileName(
            self,
            'Abrir archivo',
            '.',
            'JSON (*.json)'
        )[0]
        if self.administrador.abrir(ubicacion):
            QMessageBox.information(
                self,
                "Éxito",
                "Se abrió el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + ubicacion
            )
    
    @Slot()
    def action_guardar_archivo(self):
       ubicacion = QFileDialog.getSaveFileName(
           self,
           'Guardar Archivo',
           #Lo abrirá desde donde se corre
           '.',
           #Extensión del archivo
           'JSON (*.json)'
       )[0]
       print(ubicacion)
       if self.administrador.guardar(ubicacion):
           QMessageBox.information(
               self,
               "Éxito",
               "Se pudo crear el archivo " + ubicacion
           )
       else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo " + ubicacion
            )

    @Slot()
    def click_mostrar(self):
        #self.administrador.mostrar()
        self.ui.salida.clear()
        self.ui.salida.insertPlainText(str(self.administrador))

    @Slot() #Definición de Slot
    def click_agregar(self):
        ID = self.ui.ID_lineEdit.text()
        origenX = self.ui.origenX_spinBox.value()
        origenY = self.ui.origenY_spinBox.value()
        destinoX = self.ui.destinoX_spinBox.value()
        destinoY = self.ui.destinoY_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        red = self.ui.red_spinBox.value()
        green = self.ui.green_spinBox.value()
        blue = self.ui.blue_spinBox.value()

        particula = Particula(ID, origenX, origenY, destinoX, destinoY, velocidad, red, green, blue)
        self.administrador.agregar_final(particula)

    @Slot() #Definición de Slot
    def click_agregarInicio(self):
        ID = self.ui.ID_lineEdit.text()
        origenX = self.ui.origenX_spinBox.value()
        origenY = self.ui.origenY_spinBox.value()
        destinoX = self.ui.destinoX_spinBox.value()
        destinoY = self.ui.destinoY_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        red = self.ui.red_spinBox.value()
        green = self.ui.green_spinBox.value()
        blue = self.ui.blue_spinBox.value()

        particula = Particula(ID, origenX, origenY, destinoX, destinoY, velocidad, red, green, blue)
        self.administrador.agregar_inicio(particula)