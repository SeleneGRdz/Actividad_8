from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow

#Controlador
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui = Ui_MainWindow()
        ui.setupUi(self)
        #Conexión del Slot
        ui.pushButton.clicked.connect(self.click_agregar)

    @Slot() #Definición de Slot
    def click_agregar(self):
        print('click')