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

@app.route('/admin/categorias/editar/<int:id_categoria>', methods=['GET', 'POST'])
def editarCategoria(id_categoria):
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        # Obtener datos del formulario
        nombreCategoria = request.form['nombreCategoria']
        archivo = request.files['archivo'].read()

        # Llamar al procedimiento PL/SQL para editar la categoría
        cursor.callproc('editar_categoria', [id_categoria, nombreCategoria, archivo])
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('obtener_categorias'))
    
    # Obtener la información de la categoría para mostrarla en el formulario de edición
    cursor.execute("SELECT nombre, archivo FROM categorias WHERE id_categoria = :id", {"id": id_categoria})
    categoria = cursor.fetchone()
    categoria_con_base64 = (id_categoria, categoria[0], base64.b64encode(categoria[1].read()).decode('utf-8'))
    
    cursor.close()
    conn.close()
    return render_template('/admin/EditCategory.html', categoria=categoria_con_base64)


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

        cursor.close()
        conn.close()
        return redirect(url_for('obtener_categorias'))
        
    return render_template('/Admin/AddCategory.html')


# ------   SUBCATEGORIAS   ------

@app.route('/admin/AddSubCategoria', methods=['GET', 'POST'])
def SubCategory():
    # Conexión a la base de datos y obtener categorías
    conn, cursor = get_db_connection()
    categorias_cursor = cursor.var(cx_Oracle.CURSOR)
    cursor.callproc('ObtenerCategorias', [categorias_cursor])

    # Obtener los resultados del cursor
    categorias = categorias_cursor.getvalue()
    categorias_con_formato = [{'id': categoria[0], 'nombre': categoria[1]} for categoria in categorias]

    if request.method == 'POST':
        
        # Obtener datos del formulario
        category_id = request.form['categoria']
        nombre_sub_categoria = request.form['nombreSubCategoria']
        
        # Llamar al procedimiento PL/SQL para agregar la subcategoría
        cursor.callproc('AgregarSubCategoria', [nombre_sub_categoria, category_id])
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for('mostrar_subcategorias'))
#return render_template('/admin/AddSubCategory.html', categorias=categorias_con_formato)

@app.route('/admin/subcategorias')
def mostrar_subcategorias():
    # Conexión a la base de datos
    conn, cursor = get_db_connection()
    
    # Llamar al procedimiento almacenado para obtener subcategorías
    subcategorias_cursor = cursor.var(cx_Oracle.CURSOR)
    cursor.callproc('ObtenerSubcategorias', [subcategorias_cursor])

    # Obtener resultados del cursor de salida
    subcategorias = subcategorias_cursor.getvalue()

    subcategoria_array = []
    for subcategoria in subcategorias:
        id_subcategoria = subcategoria[0] # ID de subcategoría
        nombre_subcategoria = subcategoria[1] # Nombre de subcategoría
        id_categoria = subcategoria[2] # ID de categoría

        # Llamar al procedimiento almacenado para obtener los datos de la categoría
        categorias_cursor = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc('ObtenerCategorias', [categorias_cursor])
        categorias = categorias_cursor.getvalue()

        # Buscar la categoría por su ID
        nombre_categoria = None
        for categoria in categorias:
            if categoria[0] == id_categoria:
                nombre_categoria = categoria[1]
                break

        subcategoria_array.append((id_subcategoria, nombre_subcategoria, nombre_categoria))

    # Pasar subcategorías a la plantilla HTML
    return render_template('/admin/subcategorias.html', subcategorias=subcategoria_array)


@app.route('/admin/subcategorias/eliminar/<int:id_subcategoria>')
def eliminarSubCategoria(id_subcategoria):
    conn, cursor = get_db_connection()
    with conn.cursor() as cursor:
        cursor.callproc('EliminarSubCategoria', (id_subcategoria,))
        conn.commit()

   
    return redirect(url_for('mostrar_subcategorias'))


@app.route('/admin/subcategorias/editar/<int:id_subcategoria>', methods=['GET', 'POST'])
def editarSubCategoria(id_subcategoria):
    conn, cursor = get_db_connection()

    #obtener la lista de categorias
    categorias_cursor = cursor.var(cx_Oracle.CURSOR)
    # Llamar al procedimiento almacenado con el cursor como argumento de salida
    cursor.callproc('ObtenerCategorias', [categorias_cursor])

    # Obtener los resultados del cursor
    categorias = categorias_cursor.getvalue()
    
    # Convertir el objeto LOB BLOB a base64 y decodificarlo a UTF-8
    categoriasF = []
    for categoria in categorias:
        id = categoria[0] #  el id está en la posición 0
        nombre = categoria[1]  #  el nombre está en la posición 1
        categoriasF.append((id,nombre))



    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombreSubCategoria = request.form['nombreSubCategoria']
        id_categoria = request.form['categoria']

        # Llamar al procedimiento PL/SQL para editar la subcategoría
        cursor.callproc('editar_subcategoria', [id_subcategoria, nombreSubCategoria, id_categoria])
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('mostrar_subcategorias'))
    
    # Obtener la información de la subcategoría para mostrarla en el formulario de edición
    cursor.execute("SELECT id_subcategoria, nombre, id_categoria FROM subcategorias WHERE id_subcategoria = :id", {"id": id_subcategoria})
    subcategoria = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('/admin/EditSubCategory.html', categorias= categoriasF, subcategoria=subcategoria)


####################PRODUCTOS########################


from contextlib import contextmanager
@app.route('/')
def prin():
    return 'Hola Mundo desde Flask!'

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    data = request.form
    try:
        # Convertir datos a tipos apropiados
        id_producto = int(data['id_producto'])
        nombre = data['nombre']
        descripcion = data['descripcion']
        proveedor = data['proveedor']
        precio = float(data['precio'])  # Cambiar a float si el precio puede tener decimales
        descuento = float(data['descuento'])
        cantidad_stock = int(data['cantidad_stock'])
        
        with get_db_connection() as connection:
            cursor = connection.cursor()
            # Llamar al procedimiento almacenado con los parámetros adecuados
            cursor.callproc("crear_producto", [
                id_producto,
                nombre,
                descripcion,
                proveedor,
                precio,
                descuento,
                cantidad_stock
            ])
            connection.commit()
            cursor.close()
        print(f"Producto {nombre} creado con éxito.")
    except cx_Oracle.DatabaseError as e:
        print(f"Error al crear producto: {e}")
    except Exception as e:
        print(f"Error general: {e}")
    return redirect(url_for('listar_productos'))



@app.route('/productos')
def listar_productos():
    print("Fetching products...")
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM PRODUCTOS ORDER BY ID_PRODUCTO")
        productos = cursor.fetchall()  # Esto recupera todos los productos de la base de datos
        print(productos)  
        cursor.close()
    return render_template('productos.html', productos=productos)



@app.route('/actualizar_producto/<int:id_producto>', methods=['POST'])
def actualizar_producto(id_producto):
    data = request.form
    try:
        # Convertir los datos del formulario a los tipos correctos, si es necesario.
        nombre = data.get('nombre', type=str)
        descripcion = data.get('descripcion', type=str)
        proveedor = data.get('proveedor', type=str)
        precio = data.get('precio', type=float)
        descuento = data.get('descuento', type=float)
        cantidad_stock = data.get('cantidad_stock', type=int)

        # Usar el contexto de la base de datos para llamar al procedimiento.
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.callproc("actualizar_producto", [
                id_producto,
                nombre,
                descripcion,
                proveedor,
                precio,
                descuento,
                cantidad_stock
            ])
            connection.commit()
        print(f"Producto con ID {id_producto} actualizado con éxito.")
    except cx_Oracle.DatabaseError as e:
        print(f"Error al actualizar producto: {e}")
        return str(e), 500
    except Exception as e:
        print(f"Error inesperado: {e}")
        return str(e), 500
    return redirect(url_for('listar_productos'))



@app.route('/eliminar_producto/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.callproc("eliminar_producto", [id_producto])
        connection.commit()
        cursor.close()
    return redirect(url_for('listar_productos'))


@app.route('/database')
def test_database():

    
    conn = cx_Oracle.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT 'Conectado a Oracle Database!' FROM DUAL")
    message = cursor.fetchone()

    cursor.close()
    conn.close()

    return message[0]  

@contextmanager
def get_db_connection():
    conn = cx_Oracle.connect(DB_CONNECTION_STRING)
    try:
        yield conn
    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
