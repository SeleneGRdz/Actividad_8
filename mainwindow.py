from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
from administrador import Administrador
from administrador import Particula

#Controlador
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() #Se llama a la ventana
        
        self.administrador = Administrador()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #Conexión del Slot
        self.ui.agregarFinal_pushButton.clicked.connect(self.click_agregar)
        self.ui.agregarInicio_pushButton.clicked.connect(self.click_agregarInicio)
        self.ui.mostrar_pushButton.clicked.connect(self.click_mostrar)
        
        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)
    
    @Slot()
    def action_abrir_archivo(self):
        #print('abrir_archivo')
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
       #print('guardar_archivo')
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