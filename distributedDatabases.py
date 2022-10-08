from PyQt5 import QtWidgets, uic
from conexion_postgresql import *

# Iniciamos el programa
app = QtWidgets.QApplication([])

# Cargamos los archivos de la GUI
mainNodeWindow = uic.loadUi("GUI/mainNodeWindow.ui")
secondarieNodeWindow = uic.loadUi("GUI/secondarieNodeWindow.ui")
verticalWindow = uic.loadUi("GUI/verticalWindow.ui")

def guiMainNodeWindow():
    name = mainNodeWindow.inputName.text()
    host = mainNodeWindow.inputHost.text()
    port = mainNodeWindow.inputPort.text()
    database = mainNodeWindow.inputDatabase.text()
    user = mainNodeWindow.inputUser.text()
    password = mainNodeWindow.inputPassword.text()

    # makeConnection(host, port, user, password, database)

    # if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(database) == 0 or len(user) == 0 or len(password) == 0:
    #     mainNodeWindow.lblMessage.setText("Por favor llena todos los espacios")
    # else:
    guiSecondarieNodeWindow(name)


def guiSecondarieNodeWindow(name):
    mainNodeWindow.hide()
    mainNodeWindow.lblMessage.setText("") 
    secondarieNodeWindow.lstInsertedNodes.addItem(name + "(Main node)")
    secondarieNodeWindow.show()


def guiVerticalWindow():
    secondarieNodeWindow.hide()
    nodes = []
    for node in range(secondarieNodeWindow.lstInsertedNodes.count()):
        nodes.append(secondarieNodeWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        verticalWindow.cbNodes.addItem(node)   
    verticalWindow.show()


def guiAddNode():
    name = secondarieNodeWindow.inputName.text()
    host = secondarieNodeWindow.inputHost.text()
    port = secondarieNodeWindow.inputPort.text()
    database = secondarieNodeWindow.inputDatabase.text()
    user = secondarieNodeWindow.inputUser.text()
    password = secondarieNodeWindow.inputPassword.text()

    # if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(database) == 0 or len(user) == 0 or len(password) == 0:
    #     mainNodeWindow.lblMessage.setText("Por favor llena todos los espacios")
    # else:
    # makeConnection(host, port, user, password, database)
    secondarieNodeWindow.lstInsertedNodes.addItem(name)

    secondarieNodeWindow.inputName.setText("") 
    secondarieNodeWindow.inputHost.setText("") 
    secondarieNodeWindow.inputPort.setText("") 
    secondarieNodeWindow.inputDatabase.setText("") 
    secondarieNodeWindow.inputUser.setText("") 
    secondarieNodeWindow.inputPassword.setText("") 


def guiAddAttribute():
    attributeName = verticalWindow.inputAttributeName.text()
    attributeType = verticalWindow.inputAttributeType.text()
    if verticalWindow.chbPK.checkState() == 0:
        verticalWindow.lstAttributes.addItem(attributeName + " " + attributeType)
    else:
        verticalWindow.lstAttributes.addItem(attributeName + " " + attributeType + " (pk)")
        verticalWindow.chbPK.setChecked(False)
    verticalWindow.inputAttributeName.setText("")
    verticalWindow.inputAttributeType.setText("")

def guiSelectNode():
    node = verticalWindow.cbNodes.currentText()
    verticalWindow.lstNodes.addItem(node)


# Botonoes
mainNodeWindow.btnInsert.clicked.connect(guiMainNodeWindow)
secondarieNodeWindow.btnInsert.clicked.connect(guiAddNode)
secondarieNodeWindow.btnVertical.clicked.connect(guiVerticalWindow)
verticalWindow.btnAdd.clicked.connect(guiAddAttribute)
verticalWindow.btnAddNode.clicked.connect(guiSelectNode)

# Ejecutable
mainNodeWindow.show()
app.exec()