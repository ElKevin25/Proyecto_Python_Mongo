from ast import Expression
from glob import glob
from optparse import Values
from sqlite3 import Row
from webbrowser import BackgroundBrowser
from xml.dom.minidom import Document, Identified
from gridfs import ClientSession
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]
ID_ALUMNO=""




def mostrarDatos(nombre="",sexo="",calificacion=""):
    objetoBuscar={}
    if len(nombre)!=0:
        objetoBuscar["nombre"]=nombre
    if len(sexo)!=0:
        objetoBuscar["sexo"]=sexo
    if len(calificacion)!=0:
        objetoBuscar["calificacion"]=calificacion
    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find(objetoBuscar):  
            tabla.insert('',0,text=documento ["_id"],values=documento["nombre"])
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo excedido"+errorTiempo)
    except pymongo.errors.ConectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB"+errorConexion)
        

def crearRegistro():
    if len(nombre.get())!=0 and len(calificacion.get())!=0 and len(sexo.get())!=0 :
        try: 
            documento={"nombre":nombre.get(),"calificacion":calificacion.get(),"sexo":sexo.get()}
            coleccion.insert_one(documento)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")

    mostrarDatos() 

        
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO=str(tabla.item(tabla.selection())["text"])
    documento=coleccion.find({"_id":ObjectId(ID_ALUMNO)})[0]
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    sexo.delete(0,END)
    sexo.insert(0,documento["sexo"])
    calificacion.delete(0,END)
    calificacion.insert(0,documento["calificacion"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"

def editarRegistro():
    global ID_ALUMNO
    if len(nombre.get())!=0 and len(sexo.get())!=0 and len(calificacion.get())!=0 :
        try:
            idBuscar={"_id":ObjectId(ID_ALUMNO)}
            nuevosValores={"$set":{"nombre":nombre.get(),"sexo":sexo.get(),"calificacion":calificacion.get()}}
            coleccion.update_many(idBuscar,nuevosValores)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"

def borrarRegistro():
    global ID_ALUMNO
    try:
        idBuscar={"_id":ObjectId(ID_ALUMNO)}
        coleccion.delete_one(idBuscar)
        nombre.delete(0,END)
        sexo.delete(0,END)
        calificacion.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    crear["state"]="normal"
    editar["state"]="disabled" 
    borrar["state"]="disabled"
    mostrarDatos()
        
def buscarRegistro():
    mostrarDatos(buscarNombre.get(),buscarSexo.get(),buscarCalificacion.get())

ventana=Tk()
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="NOMBRE")
tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana,text="Nombre").grid(row=2,column=0)
nombre=Entry(ventana)
nombre.grid(row=2,column=1)
nombre.focus()

#Sexo
Label(ventana,text="Sexo").grid(row=3,column=0)
sexo=Entry(ventana) 
sexo.grid(row=3,column=1)

#Calificacion 
Label(ventana,text="Calificacion").grid(row=4,column=0)
calificacion=Entry(ventana)
calificacion.grid(row=4,column=1)
#Boton para crear
crear=Button(ventana,text="Crear Alumno",command=crearRegistro,background="yellow",fg="black")
crear.grid(row=5,columnspan=2)


#boton para editar
editar=Button(ventana,text="Editar Alumno",command=editarRegistro,background="lawnGreen",fg="black")
editar.grid(row=6,columnspan=2)
editar["state"]="disabled"

#boton para borrar
borrar=Button(ventana,text="Borrar Alumno",command=borrarRegistro,background="red",fg="black")
borrar.grid(row=7,columnspan=2)
borrar["state"]="disabled"

#Nombre buscar
Label(ventana,text="Buscar Nombre").grid(row=8,column=0)
buscarNombre=Entry(ventana)
buscarNombre.grid(row=8,column=1)

#Sexo buscar
Label(ventana,text="Buscar por Sexo").grid(row=9,column=0)
buscarSexo=Entry(ventana) 
buscarSexo.grid(row=9,column=1)

#Calificacion buscar
Label(ventana,text="Buscar por Calificacion").grid(row=10,column=0)
buscarCalificacion=Entry(ventana)
buscarCalificacion.grid(row=10,column=1)

#boton para buscar
buscar=Button(ventana,text="Buscar Alumno",command=buscarRegistro,background="cyan2",fg="black")
buscar.grid(row=11,columnspan=2)


mostrarDatos()






ventana.mainloop()