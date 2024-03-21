from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, abort
from config import DB_CONNECTION_STRING, SECRET_KEY, VAR_ENV_1, VAR_ENV_2, VAR_ENV_3
import cx_Oracle
import base64
import pdb


app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configurar temporalmente las variables de entorno

VAR_ENV_1
VAR_ENV_2
VAR_ENV_3

def get_db_connection():
    try:
        connection = cx_Oracle.connect(DB_CONNECTION_STRING)
        cursor = connection.cursor()
        return connection, cursor
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 1047:
            print("DPI-1047: No se pudo encontrar la biblioteca del cliente de Oracle. Verifica la configuración.")
        else:
            print(f"Error de base de datos: {error}")
        return None, None

def close_db_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/homec')
def homec():
    return render_template('home copy.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

#Formulario Categoria
@app.route('/admin/AddCategoria' ,methods = [ 'GET','POST'])

def Acategorias():
    if request.method == 'POST':
        conn, cursor = get_db_connection()
        # Obtener datos del formulario
        nombreCategoria = request.form ['nombreCategoria']
        archivo = request.files['archivo'].read()

        # Llamar al procedimiento PL/SQL para crear un proveedor
        cursor.callproc('CrearCategoria', [nombreCategoria,archivo])
        conn.commit()

    return render_template('/Admin/AddCategory.html')