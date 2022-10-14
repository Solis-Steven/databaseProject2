from PyQt5 import QtWidgets, uic
from conexion_postgresql import *

# Lista para almacenar los nodos
nodeList = []

# Iniciamos el programa
app = QtWidgets.QApplication([])

# Cargamos los archivos de la GUI
nodesWindow = uic.loadUi("GUI/nodesWindow.ui")
verticalWindow = uic.loadUi("GUI/verticalWindow.ui")


def guiVerticalWindow():
    nodesWindow.hide()
    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()):
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        verticalWindow.cbNodes.addItem(node)   
    verticalWindow.show()


def guiAddNode():
    name = nodesWindow.inputName.text()
    host = nodesWindow.inputHost.text()
    port = nodesWindow.inputPort.text()
    database = nodesWindow.inputDatabase.text()
    user = nodesWindow.inputUser.text()
    password = nodesWindow.inputPassword.text()

    # if len(name) == 0 or len(host) == 0 or len(port) == 0 or len(database) == 0 or len(user) == 0 or len(password) == 0:
    #     mainNodeWindow.lblMessage.setText("Por favor llena todos los espacios")
    # else:
    # makeConnection(host, port, user, password, database)
    
    nodesWindow.lstInsertedNodes.addItem(name)

    nodesWindow.inputName.setText("") 
    nodesWindow.inputHost.setText("") 
    nodesWindow.inputPort.setText("") 
    nodesWindow.inputDatabase.setText("") 
    nodesWindow.inputUser.setText("") 
    nodesWindow.inputPassword.setText("") 

    node = {
        "name": name,
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password
    }

    nodeList.append(node)

def guiSelectNode():
    node = verticalWindow.cbNodes.currentText()
    if verticalWindow.chbMain.checkState() == 2:
        verticalWindow.lstNodes.addItem(node + " (Main)")
        verticalWindow.chbMain.setChecked(False)
    else:
        verticalWindow.lstNodes.addItem(node)


def guiGenerateVerticalSegmentation():
    table = verticalWindow.inputTable.toPlainText()
    verticalWindow.inputTable.setPlainText("")

    nodes = []
    for node in range(verticalWindow.lstNodes.count()): 

        readedNode = verticalWindow.lstNodes.item(node).text()
        readedNode = readedNode.split()

        if len(readedNode) > 1:
            node = {
                "name": readedNode[0],
                "main": True
            }
        else:
            node = {
                "name": readedNode[0],
                "main": False
            }
        
        nodes.append(node)
    
    verticalWindow.lstNodes.clear()

    print(table, "\n")
    print(nodes)


def guiGoBackV():
    verticalWindow.hide()
    verticalWindow.lstNodes.clear()
    verticalWindow.inputTable.setPlainText("")
    nodesWindow.show()


def guiDeleteSelectedNodes():
    verticalWindow.lstNodes.clear()


# Botones
nodesWindow.btnInsert.clicked.connect(guiAddNode)
nodesWindow.btnVertical.clicked.connect(guiVerticalWindow)
verticalWindow.btnAddNode.clicked.connect(guiSelectNode)
verticalWindow.btnGenerate.clicked.connect(guiGenerateVerticalSegmentation)
verticalWindow.btnGoBack.clicked.connect(guiGoBackV)
verticalWindow.btnDelete.clicked.connect(guiDeleteSelectedNodes)


# Ejecutable
nodesWindow.show()
app.exec()