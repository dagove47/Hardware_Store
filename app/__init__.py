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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/admin/categorias')
def obtener_categorias():
    conn, cursor = get_db_connection()
    # Crear un cursor para el procedimiento almacenado
    categorias_cursor = cursor.var(cx_Oracle.CURSOR)
    # Llamar al procedimiento almacenado con el cursor como argumento de salida
    cursor.callproc('ObtenerCategorias', [categorias_cursor])

    # Obtener los resultados del cursor
    categorias = categorias_cursor.getvalue()
    
    # Convertir el objeto LOB BLOB a base64 y decodificarlo a UTF-8
    categorias_con_base64 = []
    for categoria in categorias:
        id = categoria[0] #  el id está en la posición 0
        nombre = categoria[1]  #  el nombre está en la posición 1
        archivo_blob = categoria[2]  # el objeto LOB BLOB está en la posición 2
        archivo_base64 = base64.b64encode(archivo_blob.read()).decode('utf-8')
        categorias_con_base64.append((id,nombre, archivo_base64))

    cursor.close()
    conn.close()
    return render_template('/admin/categorias.html', categorias=categorias_con_base64)

@app.route('/admin/categorias/eliminar/<int:id_categoria>')
def eliminarCategoria(id_categoria):
    conn, cursor = get_db_connection()
    with conn.cursor() as cursor:
        cursor.callproc('EliminarCategoria', (id_categoria,))
        conn.commit()

   
    return redirect(url_for('obtener_categorias'))


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

#return redirect(url_for('obtener_categorias'))