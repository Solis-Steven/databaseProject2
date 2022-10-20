
import random
from PyQt5 import QtWidgets, uic
from conexion_postgresql import *

# Lista para almacenar los nodos
nodeList = []


attributesList = []


mainNode = {
    "name": "",
    "host": "",
    "port": "",
    "database": "",
    "user": "",
    "password": ""
}

# Iniciamos el programa
app = QtWidgets.QApplication([])

# Cargamos los archivos de la GUI
nodesWindow = uic.loadUi("GUI/nodesWindow.ui")
verticalWindow = uic.loadUi("GUI/verticalWindow.ui")
horizontalWindow = uic.loadUi("GUI/horizontalWindow.ui")
mainHorizontalWindow = uic.loadUi("GUI/mainHorizontalWindow.ui")
mainHorizontalWindow = uic.loadUi("GUI/mainHorizontalWindow.ui")
deleteWindow = uic.loadUi("GUI/deleteWindow.ui")
mainBothWindow = uic.loadUi("GUI/mainBothWindow.ui")
bothWindow = uic.loadUi("GUI/bothWindow.ui")

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
Esta funcion establece a coneccion con el servidor
localizado en la base de datos con los datos brindados
por el usuario
"""
def doConnection(query, node):
    connection = makeConnection(node["host"], 
                                node["port"], 
                                node["user"], 
                                node["password"], 
                                node["database"]) #se crea la conexion con los datos del n
  
    connection.autocommit = True #se habilita los commits automaticos
    cursor = connection.cursor() #se crea cursor para ejecutar queries
    cursor.execute(query) #se ejecuta el string con la creacion de la tabla
    cursor.close()


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


def guiAddAttributeV():
    attributeName = verticalWindow.inputAttributeName.text()
    attributeType = verticalWindow.cbAttributesType.currentText()
    primaryKey = verticalWindow.chbPrimaryKey.isChecked()

    if primaryKey:
        verticalWindow.lstAttributes.addItem("{} {} (pk)".format(attributeName, attributeType))
    else:
        verticalWindow.lstAttributes.addItem("{} {}".format(attributeName, attributeType))

    verticalWindow.inputAttributeName.setText("")
    verticalWindow.chbPrimaryKey.setChecked(False)

    attribute = {
        "attributeName": attributeName,
        "attributeType": attributeType,
        "primaryKey": primaryKey
    }

    attributesList.append(attribute)

"""
Esta funcion va a obtener los datos introducidos 
por el usuario y los cuales a partir de ellos,
va a generar la segmentacion vertical
"""
def guiGenerateVerticalSegmentation():
    tableName = verticalWindow.inputName.text()
    
    table = "CREATE TABLE {} (\n".format(tableName)

    global attributesList
    for i in attributesList:
        if i["primaryKey"]:
            table += ("{} {} PRIMARY KEY,\n".format(i["attributeName"].lower(), i["attributeType"]))
        else:
            table += ("{} {},\n".format(i["attributeName"].lower(), i["attributeType"]))

    table = table[:len(table)-2]
    table += "\n);"

    verticalWindow.inputName.setText("")
    verticalWindow.inputAttributeName.setText("")

    nodes = []
    for node in range(verticalWindow.lstNodes.count()): #se recorre la ventana con los nodos

        readedNode = verticalWindow.lstNodes.item(node).text()
        readedNode = readedNode.split()

        if len(readedNode) > 1:  #se pregunta si es el main node en ese caso lo guarda con main true
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
    verticalWindow.lstAttributes.clear()
    attributesList = []
    generateVTables(nodes, table) #se llama a la funcion para general las tablas con segmentacion vertical
    

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
                    randomID= str(random.randint(500, 50000))
                    connection = makeConnection(searchedNode["host"], # se establece la coneccion con los datos
                                                searchedNode["port"], 
                                                searchedNode["user"],
                                                searchedNode["password"], 
                                                searchedNode["database"])
                    connection.autocommit = True 
                    cursor = connection.cursor()
                    cursor.execute(table) 
                    cursor.execute("""
                        create extension if not exists postgres_fdw;

                        CREATE SERVER {}{}_postgres_fdw
                        FOREIGN DATA WRAPPER postgres_fdw
                        OPTIONS(host '{}', dbname '{}', port '{}');

                        CREATE USER MAPPING IF NOT EXISTS FOR postgres
                        SERVER {}{}_postgres_fdw
                        OPTIONS (user '{}', password '{}');
                        """.format(mainName,
                                   randomID,
                                   mainHost, 
                                   maindDbName, 
                                   mainPort, mainName,randomID, mainUser, mainPassword)
                    )
                    cursor.close() 
        
            
"""
Esta funcion se encarga de cerrar la ventana para crear la segmentacion vertical
y abre la ventana de nodos es decir vuelve a atras
"""
def guiGoBackV():
    verticalWindow.hide()
    verticalWindow.lstNodes.clear()
    verticalWindow.lstAttributes.clear()
    verticalWindow.cbNodes.clear()
    verticalWindow.inputName.setText("")
    verticalWindow.inputAttributeName.setText("")
    nodesWindow.show()


"""
Esta funcion elimina todos los nodos listados los cuales
han sido seleccionados por el usuario, es decir,
limpia la lista de nodos seleccionados para la segmentacion
vertical
"""
def guiDeleteSelectedNodes():
    verticalWindow.lstNodes.clear()


"""
Esta funcion se encarga de presentar la ventana para la segmentacion horizontal
de las tablas en el nodo principal.
"""
def guiMainHorizontalWindow():
    nodesWindow.hide() 
    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()): #se recorre la lista de nodos seleccionados y se añaden a la local
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        mainHorizontalWindow.cbNodes.addItem(node) #se añaden los nodos creados en la ventana principal al combobox
    mainHorizontalWindow.show()


"""
Esta funcion se encarga de mostrar la interfaz para crear la segmentacion vertical con el nodo
principal (main)
"""
def guiHorizontalWindow():
    mainHorizontalWindow.hide()

    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()):
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text()) #se añaden los nodos existentes al combobox    

    tableName = mainHorizontalWindow.inputName.text()
    

    query = "CREATE TABLE {} (\n".format(tableName) #se crea la query para crear la tabla
    global attributesList
    for i in attributesList:
        if i["primaryKey"]:
            query += ("{} {} PRIMARY KEY,\n".format(i["attributeName"].lower(), i["attributeType"]))
        else:
            query += ("{} {},\n".format(i["attributeName"].lower(), i["attributeType"]))

    
    query = query[:len(query)-2]
    query += "\n);"

    global mainNode
    mainNode["name"] = mainHorizontalWindow.cbNodes.currentText() #se guarda el nombre del nodo principal

    for node in nodeList: #se guardan los datos del nodo principal
        if node["name"] == mainNode["name"]:
            mainNode["host"] = node["host"]
            mainNode["database"] = node["database"]
            mainNode["port"] = node["port"]
            mainNode["user"] = node["user"]
            mainNode["password"] = node["password"]

    for node in nodes:
        if node != mainNode["name"]: #se añaden el resto de nodos al combobox menos el principal
            horizontalWindow.cbNodes.addItem(node)
    
    horizontalWindow.show()
    doConnection(query, mainNode)
    attributesList = []
    horizontalWindow.inputName.setText(tableName)

    for i in range(mainHorizontalWindow.lstInsertedNodes.count()):
        attribute = mainHorizontalWindow.lstInsertedNodes.item(i).text()
        horizontalWindow.cbAttributes.addItem(attribute)


"""
Esta funcion se encarga de ir creando la tabla con segmentacion vertical
en los nodos secundarios y creando de una vez las conexiones hacia el nodo
principal
"""
def guiHorizontalWindow2():

    tableName = horizontalWindow.inputName.text()
    nodeName = horizontalWindow.cbNodes.currentText()

    node = {
        "name": "",
        "host": "",
        "port": "",
        "database": "",
        "user": "",
        "password": ""
    }


    for i in nodeList: #se obtienen los datos del nodo
        if i["name"] == nodeName:
            node["name"] = i["name"]
            node["host"] = i["host"]
            node["port"] = i["port"]
            node["database"] = i["database"]
            node["user"] = i["user"]
            node["password"] = i["password"] 

    table = "CREATE TABLE {} (\n".format(tableName)

    global attributesList
    for i in attributesList:
        if i["primaryKey"]:
            table += ("{} {} PRIMARY KEY,\n".format(i["attributeName"].lower(), i["attributeType"]))
        else:
            table += ("{} {},\n".format(i["attributeName"].lower(), i["attributeType"]))

    table = table[:len(table)-2]
    table += "\n);"

    doConnection(table, node) #se crea la conexion con los datos del nodo
    horizontalWindow.inputAttributeName.setText("")
    horizontalWindow.lstInsertedNodes.clear()

    randomID = str(random.randint(500, 50000))
    query = """
    create extension if not exists  postgres_fdw;

    create server {}{}_postgres_fdw
    foreign data wrapper postgres_fdw
    options (host '{}', dbname '{}', port '{}');

    create user mapping if not exists for postgres
    server {}{}_postgres_fdw
    options(user '{}', password '{}');
    """.format(mainNode["name"], randomID, mainNode["host"], mainNode["database"], 
    mainNode["port"], mainNode["name"],randomID, mainNode["user"], mainNode["password"])

    doConnection(query,node) #se crea la query para los data wrappers y el user mapping
    attributesList = []


"""
Esta funcion se encarga de darle funcion al boton de volver atras
"go back" en la interfaz grafica en la parte de creacion de tabla
en el nodo principal
"""
def guiGoBackMH():
    mainHorizontalWindow.hide()
    nodesWindow.show()
    mainHorizontalWindow.inputName.setText("")
    mainHorizontalWindow.inputAttributeName.setText("")
    mainHorizontalWindow.cbNodes.clear()
    mainHorizontalWindow.lstInsertedNodes.clear()


def guiAddAttributeMH():
    attributeName = mainHorizontalWindow.inputAttributeName.text()
    attributeType = mainHorizontalWindow.cbAttributesType.currentText()
    primaryKey = mainHorizontalWindow.chbPrimaryKey.isChecked()

    if primaryKey:
        mainHorizontalWindow.lstInsertedNodes.addItem("{} {} (pk)".format(attributeName, attributeType))
    else:
        mainHorizontalWindow.lstInsertedNodes.addItem("{} {}".format(attributeName, attributeType))

    mainHorizontalWindow.inputAttributeName.setText("")
    mainHorizontalWindow.chbPrimaryKey.setChecked(False)

    attribute = {
        "attributeName": attributeName,
        "attributeType": attributeType,
        "primaryKey": primaryKey
    }

    attributesList.append(attribute)

"""
Esta funcion se encarga de darle funcion al boton de volver atras
"go back" en la interfaz grafica en la parte de creacion de tabla
en los nodos secundarios
"""
def guiGoBackH():
    horizontalWindow.hide()
    nodesWindow.show()
    
    horizontalWindow.inputName.setText("")
    horizontalWindow.inputAttributeName.setText("")
    horizontalWindow.cbNodes.clear()
    horizontalWindow.lstInsertedNodes.clear()
    horizontalWindow.cbAttributes.clear()


def guiAddAttributeH():
    attributeName = horizontalWindow.inputAttributeName.text()
    attributeType = horizontalWindow.cbAttributesType.currentText()
    primaryKey = horizontalWindow.chbPrimaryKey.isChecked()

    if primaryKey:
        horizontalWindow.lstInsertedNodes.addItem("{} {} (pk)".format(attributeName, attributeType))
    else:
        horizontalWindow.lstInsertedNodes.addItem("{} {}".format(attributeName, attributeType))

    horizontalWindow.inputAttributeName.setText("")
    horizontalWindow.chbPrimaryKey.setChecked(False)

    attribute = {
        "attributeName": attributeName,
        "attributeType": attributeType,
        "primaryKey": primaryKey
    }

    attributesList.append(attribute)
    

def guiAddAttributeH2():
    attribute = horizontalWindow.cbAttributes.currentText()
    horizontalWindow.lstInsertedNodes.addItem(attribute)

def guiDeleteNodeWindow():
    nodesWindow.hide()

    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()): #se recorre la lista de nodos seleccionados y se añaden a la local
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        deleteWindow.cbNodes.addItem(node) #se añaden los nodos creados en la ventana principal al combobox

    deleteWindow.show()


def guiDeleteNode():
    currentNode = deleteWindow.cbNodes.currentText()
    
    for i in nodeList:
        if i["name"] == currentNode:
            nodeList.remove(i)
    
    deleteWindow.cbNodes.clear()

    for node in nodeList:
        deleteWindow.cbNodes.addItem(node["name"])

    
def guiGoBackD():
    deleteWindow.hide()

    nodesWindow.lstInsertedNodes.clear()

    for i in nodeList:
        nodesWindow.lstInsertedNodes.addItem(i["name"])


    nodesWindow.show()


def guiMainBothWindow():
    nodesWindow.hide()

    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()): #se recorre la lista de nodos seleccionados y se añaden a la local
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text())
    
    for node in nodes:
        mainBothWindow.cbNodes.addItem(node) #se añaden los nodos creados en la ventana principal al combobox

    mainBothWindow.show()


def guiGoBackMB():
    mainBothWindow.hide()
    nodesWindow.show()
    mainBothWindow.cbNodes.clear()
    mainBothWindow.lstInsertedNodes.clear()
    mainBothWindow.inputName.setText("")
    mainBothWindow.inputAttributeName.setText("")


def guiBothWindow():
    mainBothWindow.hide()

    nodes = []
    for node in range(nodesWindow.lstInsertedNodes.count()):
        nodes.append(nodesWindow.lstInsertedNodes.item(node).text()) #se añaden los nodos existentes al combobox    

    tableName = mainBothWindow.inputName.text()

    table = "CREATE TABLE {}(\n".format(tableName)

    global attributesList
    for i in attributesList:
        if i["primaryKey"]:
            table += ("{} {} PRIMARY KEY,\n".format(i["attributeName"].lower(), i["attributeType"]))
        else:
            table += ("{} {},\n".format(i["attributeName"].lower(), i["attributeType"]))

    
    table = table[:len(table)-2]
    table += "\n);"

    global mainNode
    mainNode["name"] = mainBothWindow.cbNodes.currentText() #se guarda el nombre del nodo principal

    for node in nodeList: #se guardan los datos del nodo principal
        if node["name"] == mainNode["name"]:
            mainNode["host"] = node["host"]
            mainNode["database"] = node["database"]
            mainNode["port"] = node["port"]
            mainNode["user"] = node["user"]
            mainNode["password"] = node["password"]

    for node in nodes:
        if node != mainNode["name"]: #se añaden el resto de nodos al combobox menos el principal
            bothWindow.cbNodes.addItem(node)
    
    bothWindow.show()
    doConnection(table, mainNode)

    bothWindow.inputName.setText(tableName)

    for i in range(mainBothWindow.lstInsertedNodes.count()):
        attribute = mainBothWindow.lstInsertedNodes.item(i).text()
        bothWindow.cbAttributes.addItem(attribute)

    mainBothWindow.inputName.setText("")
    mainBothWindow.inputAttributeName.setText("")
    mainBothWindow.lstInsertedNodes.clear()
    mainBothWindow.cbNodes.clear()
    attributesList = []


def guiAddAttributeMB():
    attributeName = mainBothWindow.inputAttributeName.text()
    attributeType = mainBothWindow.cbAttributesType.currentText()
    primaryKey = mainBothWindow.chbPrimaryKey.isChecked()

    if primaryKey:
        mainBothWindow.lstInsertedNodes.addItem("{} {} (pk)".format(attributeName, attributeType))
    else:
        mainBothWindow.lstInsertedNodes.addItem("{} {}".format(attributeName, attributeType))

    mainBothWindow.inputAttributeName.setText("")
    mainBothWindow.chbPrimaryKey.setChecked(False)

    attribute = {
        "attributeName": attributeName,
        "attributeType": attributeType,
        "primaryKey": primaryKey
    }

    attributesList.append(attribute)


def guiSelectNodeB():
    node = bothWindow.cbNodes.currentText()
    bothWindow.lstNodes.addItem(node)


def guiGoBackB():
    bothWindow.hide()
    nodesWindow.show()

    bothWindow.cbNodes.clear()
    bothWindow.lstNodes.clear()
    bothWindow.lstAttributes.clear()
    bothWindow.inputName.setText("")
    bothWindow.inputAttributeName.setText("")


def guiGenerateBothSegmentation():

    tableName = bothWindow.inputName.text()

    table = "CREATE TABLE {} (\n".format(tableName)
    global attributesList
    for i in attributesList:
        if i["primaryKey"]:
            table += ("{} {} PRIMARY KEY,\n".format(i["attributeName"].lower(), i["attributeType"]))
        else:
            table += ("{} {},\n".format(i["attributeName"].lower(), i["attributeType"]))

    table = table[:len(table)-2]
    table += "\n);"


    nodes = []
    for node in range(bothWindow.lstNodes.count()): #se recorre la ventana con los nodos
        readedNode = bothWindow.lstNodes.item(node).text()
        nodes.append(readedNode)

    node = {
        "name": "",
        "host": "",
        "port": "",
        "database": "",
        "user": "",
        "password": ""
    }

    for n in nodes:
        for i in nodeList: #se obtienen los datos del nodo
            if i["name"] == n:
                node["name"] = i["name"]
                node["host"] = i["host"]
                node["port"] = i["port"]
                node["database"] = i["database"]
                node["user"] = i["user"]
                node["password"] = i["password"] 
        doConnection(table, node) #se crea la conexion con los datos del nodo
        randomID = str(random.randint(500, 50000))
        query = """
        create extension if not exists postgres_fdw;

        create server {}{}_postgres_fdw
        foreign data wrapper postgres_fdw
        options (host '{}', dbname '{}', port '{}');

        create user mapping if not exists for postgres
        server {}{}_postgres_fdw
        options(user '{}', password '{}');
        """.format(mainNode["name"], randomID, mainNode["host"], mainNode["database"], 
        mainNode["port"], mainNode["name"], randomID, mainNode["user"], mainNode["password"])
        doConnection(query,node) #se crea la query para los data wrappers y el user mapping

    bothWindow.lstNodes.clear()
    bothWindow.lstAttributes.clear()
    nodeList = []
    attributesList = []
    
        
def guiAddAttributeB():
    attributeName = bothWindow.inputAttributeName.text()
    attributeType = bothWindow.cbAttributesType.currentText()
    primaryKey = bothWindow.chbPrimaryKey.isChecked()

    if primaryKey:
        bothWindow.lstAttributes.addItem("{} {} (pk)".format(attributeName, attributeType))
    else:
        bothWindow.lstAttributes.addItem("{} {}".format(attributeName, attributeType))

    bothWindow.inputAttributeName.setText("")
    bothWindow.chbPrimaryKey.setChecked(False)

    attribute = {
        "attributeName": attributeName,
        "attributeType": attributeType,
        "primaryKey": primaryKey
    }

    attributesList.append(attribute)

def guiAddAttributeB2():
    attribute = bothWindow.cbAttributes.currentText()
    bothWindow.lstAttributes.addItem(attribute)

# Eventos que se activan cuando se presiona un boton
nodesWindow.btnInsert.clicked.connect(guiAddNode)
nodesWindow.btnVertical.clicked.connect(guiVerticalWindow)
nodesWindow.btnHorizontal.clicked.connect(guiMainHorizontalWindow)
nodesWindow.btnDelete.clicked.connect(guiDeleteNodeWindow) 
nodesWindow.btnBoth.clicked.connect(guiMainBothWindow) 
verticalWindow.btnAddNode.clicked.connect(guiSelectNode)
verticalWindow.btnAddAttribute.clicked.connect(guiAddAttributeV)
verticalWindow.btnGenerate.clicked.connect(guiGenerateVerticalSegmentation)
verticalWindow.btnGoBack.clicked.connect(guiGoBackV)
verticalWindow.btnDelete.clicked.connect(guiDeleteSelectedNodes)
mainHorizontalWindow.btnCreate.clicked.connect(guiHorizontalWindow)
mainHorizontalWindow.btnGoBack.clicked.connect(guiGoBackMH)
mainHorizontalWindow.btnAddAttribute.clicked.connect(guiAddAttributeMH)
horizontalWindow.btnCreate.clicked.connect(guiHorizontalWindow2)
horizontalWindow.btnGoBack.clicked.connect(guiGoBackH)
horizontalWindow.btnAddAttribute.clicked.connect(guiAddAttributeH)
horizontalWindow.btnAddAttribute_2.clicked.connect(guiAddAttributeH2)
deleteWindow.btnDelete.clicked.connect(guiDeleteNode)
deleteWindow.btnGoBack.clicked.connect(guiGoBackD)
mainBothWindow.btnGoBack.clicked.connect(guiGoBackMB)
mainBothWindow.btnCreate.clicked.connect(guiBothWindow)
mainBothWindow.btnAddAttribute.clicked.connect(guiAddAttributeMB)
bothWindow.btnAddNode.clicked.connect(guiSelectNodeB)
bothWindow.btnGoBack.clicked.connect(guiGoBackB)
bothWindow.btnCreate.clicked.connect(guiGenerateBothSegmentation)
bothWindow.btnAddAttribute.clicked.connect(guiAddAttributeB)
bothWindow.btnAddAttribute_2.clicked.connect(guiAddAttributeB2)


# Ejecutable
nodesWindow.show()
app.exec()