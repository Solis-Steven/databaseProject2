from PyQt5 import QtWidgets, uic
from conexion_postgresql import *

# Lista para almacenar los nodos
nodeList = []

# Iniciamos el programa
app = QtWidgets.QApplication([])

# Cargamos los archivos de la GUI
nodesWindow = uic.loadUi("GUI/nodesWindow.ui")
verticalWindow = uic.loadUi("GUI/verticalWindow.ui")
horizontalWindow = uic.loadUi("GUI/horizontalWindow.ui")
mainHorizontalWindow = uic.loadUi("GUI/mainHorizontalWindow.ui")

"""
Esta funcion abre la ventana para la creacion
de una segmentacion vertical. Asimismo, obtiene
los nodos que han sido creados por el usuario
y los muestra en la ventada de la segmentacion
para que los mismos puedan ser seleccionados en
la segmentacion
"""
def guiVerticalWindow():
    nodesWindow.hide()
    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()):
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        verticalWindow.cbNodes.addItem(node)   
    verticalWindow.show()

"""
Esta funcion se encarga de agregar
nodos a la segmentacion vertical
"""
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


"""
Esta funcion le permite al usuario seleccionar
los nodos que desea para la segmentacion vertical
"""
def guiSelectNode():
    node = verticalWindow.cbNodes.currentText()
    if verticalWindow.chbMain.checkState() == 2:
        verticalWindow.lstNodes.addItem(node + " (Main)")
        verticalWindow.chbMain.setChecked(False)
    else:
        verticalWindow.lstNodes.addItem(node)

"""
Esta funcion va a obtener los datos introducidos 
por el usuario y los cuales a partir de ellos,
va a generar la segmentacion vertical
"""
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
    generateVTables(nodes, table)
    

"""
Esta funcion es la funcion encargada de crear la segmentacion vertical de la tabla
en el nodo principal y secundarios

Parametros:
    nodes -- Lista de los nodos seleccionados por el usuario
    table -- Tabla que sera creada con segmentacion vertical 
"""
def generateVTables(nodes, table):
    mainName = "" 
    mainHost = ""
    maindDbName = ""  #se declaran los atributos del nodo principal para usarlos posterior
    mainPort = ""     # en los data wrappers
    mainUser = ""
    mainPassword = ""
    
    #se crea un ciclo para recolectar los atributos del nodo principal
    for node in nodes: 
        for searchedNode in nodeList:
            if node["name"] == searchedNode["name"]: #se compara que el nombre del nodo de la lista de los seleccionados sea igual al de la lista de nodos general para obtener los atributos
                if node["main"] == True: #se compara que sea el nodo main
                    mainName = searchedNode["name"] #se asignan los valores a los atributos del nodo main
                    mainHost = searchedNode["host"]
                    maindDbName = searchedNode["database"]
                    mainPort = searchedNode["port"]
                    mainUser = searchedNode["user"]
                    mainPassword = searchedNode["password"] 

    #se crea un ciclo para ir creando las tablas en los nodos seleccionados
    for node in nodes:
        for searchedNode in nodeList:
            if node["name"] == searchedNode["name"]: #se compara que el nombre del nodo de la lista de los seleccionados sea igual al de la lista de nodos general para obtener los atributos
                if node["main"] == True: #se asignan los valores a los atributos del nodo main
                    
                    connection = makeConnection(mainHost, mainPort, mainUser,mainPassword, maindDbName) #se crea la conexion con los datos del nodo
                    connection.autocommit = True #se habilita los commits automaticos
                    cursor = connection.cursor() #se crea cursor para ejecutar queries
                    cursor.execute(table) #se ejecuta el string con la creacion de la tabla
                    cursor.close() 
                else:
                    connection = makeConnection(searchedNode["host"], # se establece la coneccion con los datos
                                                searchedNode["port"], 
                                                searchedNode["user"],
                                                searchedNode["password"], 
                                                searchedNode["database"])
                    connection.autocommit = True 
                    cursor = connection.cursor()
                    cursor.execute(table) 
                    cursor.execute("""
                        create extension postgres_fdw;

                        CREATE SERVER {}_postgres_fdw
                        FOREIGN DATA WRAPPER postgres_fdw
                        OPTIONS(host '{}', dbname '{}', port '{}');

                        CREATE USER MAPPING FOR postgres
                        SERVER {}_postgres_fdw
                        OPTIONS (user '{}', password '{}');
                        """.format(mainName, 
                                   mainHost, 
                                   maindDbName, 
                                   mainPort, mainName, mainUser, mainPassword)
                    )
                    cursor.close() 
        
            
"""
Esta funcion se encarga de cerrar la ventana para crear la segmentacion vertical
y abre la ventana de nodos es decir vuelve a atras
"""
def guiGoBackV():
    verticalWindow.hide()
    verticalWindow.lstNodes.clear()
    verticalWindow.inputTable.setPlainText("")
    nodesWindow.show()


"""
Esta funcion elimina todos los nodos listados los cuales
han sido seleccionados por el usuario, es decir,
limpia la lista de nodos seleccionados para la segmentacion
vertical
"""
def guiDeleteSelectedNodes():
    verticalWindow.lstNodes.clear()


def guiMainHorizontalWindow():
    nodesWindow.hide()
    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()):
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        mainHorizontalWindow.cbNodes.addItem(node)
    mainHorizontalWindow.show()


def guiHorizontalWindow():
    mainHorizontalWindow.hide()

    table = mainHorizontalWindow.inputTable.toPlainText()
    mainHorizontalWindow.inputTable.setPlainText("")

    mainNode = {
        "mainName": mainHorizontalWindow.cbNodes.currentText(),
        "mainHost": "",
        "mainDbName": "",  #se declaran los atributos del nodo principal para usarlos posterior
        "mainPort": "",     # en los data wrappers
        "mainUser": "",
        "mainPassword": ""
    }

    for node in nodeList:
        if node["name"] == mainNode["mainName"]:
            mainNode["mainHost"] = node["host"]
            mainNode["mainDbName"] = node["database"]
            mainNode["mainPort"] = node["port"]
            mainNode["mainUser"] = node["user"]
            mainNode["mainPassword"] = node["password"]
    
    horizontalWindow.show()
    generateMHTable(table, mainNode)


def generateMHTable(table, mainNode):
    connection = makeConnection(mainNode["mainHost"], 
                                mainNode["mainPort"], 
                                mainNode["mainUser"], 
                                mainNode["mainPassword"], 
                                mainNode["mainDbName"]) #se crea la conexion con los datos del nodo
  
    connection.autocommit = True #se habilita los commits automaticos
    cursor = connection.cursor() #se crea cursor para ejecutar queries
    cursor.execute(table) #se ejecuta el string con la creacion de la tabla
    cursor.close() 


# Eventos que se activan cuando se presiona un boton
nodesWindow.btnInsert.clicked.connect(guiAddNode)
nodesWindow.btnVertical.clicked.connect(guiVerticalWindow)
verticalWindow.btnAddNode.clicked.connect(guiSelectNode)
verticalWindow.btnGenerate.clicked.connect(guiGenerateVerticalSegmentation)
verticalWindow.btnGoBack.clicked.connect(guiGoBackV)
verticalWindow.btnDelete.clicked.connect(guiDeleteSelectedNodes)
nodesWindow.btnHorizontal.clicked.connect(guiMainHorizontalWindow)
mainHorizontalWindow.btnCreate.clicked.connect(guiHorizontalWindow)


# Ejecutable
nodesWindow.show()
app.exec()