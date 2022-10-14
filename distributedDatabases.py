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
    generateTables(nodes, table)
    
    # print(table, "\n")
    # print(nodes)


def generateTables(nodes, table):
    mainName = ""
    mainHost = ""
    maindDbName = ""
    mainPort = ""
    mainUser = ""
    mainPassword = ""
    
    for node in nodes:
        for searchedNode in nodeList:
            if node["name"] == searchedNode["name"]:
                if node["main"] == True:
                    mainName = node["name"]
                    mainHost = node["host"]
                    maindDbName = node["database"]
                    mainPort = node["port"]
                    mainUser = node["user"]
                    mainPassword = node["password"] 
            
    for node in nodes:
        for searchedNode in nodeLIst:
            if node["name"] == searchedNode["name"]:
                if node["main"] == True:
                    connection = makeConnection(mainHost, mainPort, mainUser,mainPassword, maindDbName)
                    cursor = connection.cursor()
                    cursor.execute(table) 
                else:
                    connection = makeConnection(searchedNode["host"], 
                                                searchedNode["port"], 
                                                searchedNode["user"],
                                                searchedNode["password"], 
                                                searchedNode["database"])
                    cursor = connection.cursor()
                    cursor.execute("""
                        create extension postgres_fdw;

                        CREATE SERVER {}_postgres_fdw
                        FOREIGN DATA WRAPPER postgres_fdw
                        OPTIONS(host '{}', dbname '{}', port '{}');

                        CREATE USER MAPPING FOR postgres
                        SERVER {}_postgres_fdw
                        OPTIONS (user '{}', password '{}');
                        """.format(mainName, mainHost, maindDbName, mainPort, mainName, mainUser, mainPassword)
                    )
        
            






def guiGoBackV():
    verticalWindow.hide()
    verticalWindow.lstNodes.clear()
    verticalWindow.inputTable.setPlainText("")
    nodesWindow.show()


def guiDeleteSelectedNodes():
    verticalWindow.lstNodes.clear()


# Botonoes
nodesWindow.btnInsert.clicked.connect(guiAddNode)
nodesWindow.btnVertical.clicked.connect(guiVerticalWindow)
verticalWindow.btnAddNode.clicked.connect(guiSelectNode)
verticalWindow.btnGenerate.clicked.connect(guiGenerateVerticalSegmentation)
verticalWindow.btnGoBack.clicked.connect(guiGoBackV)
verticalWindow.btnDelete.clicked.connect(guiDeleteSelectedNodes)


# Ejecutable
nodesWindow.show()
app.exec()