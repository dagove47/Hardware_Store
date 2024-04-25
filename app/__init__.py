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


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/menu')
def menu():
    return render_template('homeA.html')


@app.route('/admin/categorias')
def obtener_categorias():
    #conn, cursor = get_db_connection()
    with get_db_connection() as connection:
        cursor = connection.cursor()
        categorias_cursor = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc('ObtenerCategorias', [categorias_cursor])
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
        return render_template('/admin/categorias.html', categorias=categorias_con_base64)

@app.route('/categorias')
def obtener_categorias2():
    #conn, cursor = get_db_connection()
    with get_db_connection() as connection:
        cursor = connection.cursor()
        categorias_cursor = cursor.var(cx_Oracle.CURSOR)
        cursor.callproc('ObtenerCategorias', [categorias_cursor])
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
        return render_template('/categoriasmenu.html', categorias=categorias_con_base64)


@app.route('/admin/categorias/eliminar/<int:id_categoria>')
def eliminarCategoria(id_categoria):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.callproc('EliminarCategoria', (id_categoria,))
            connection.commit()
    return redirect(url_for('obtener_categorias'))


@app.route('/admin/categorias/editar/<int:id_categoria>', methods=['GET', 'POST'])
def editarCategoria(id_categoria):
    with get_db_connection() as connection:
        cursor = connection.cursor()
    if request.method == 'POST':
        # Obtener datos del formulario
        nombreCategoria = request.form['nombreCategoria']
        archivo = request.files['archivo'].read()

        # Llamar al procedimiento PL/SQL para editar la categoría
        cursor.callproc('editar_categoria', [id_categoria, nombreCategoria, archivo])

        cursor.close()
        return redirect(url_for('obtener_categorias'))
    
    # Obtener la información de la categoría para mostrarla en el formulario de edición
    cursor.execute("SELECT nombre, archivo FROM categorias WHERE id_categoria = :id", {"id": id_categoria})
    categoria = cursor.fetchone()
    categoria_con_base64 = (id_categoria, categoria[0], base64.b64encode(categoria[1].read()).decode('utf-8'))
    
    cursor.close()
    return render_template('/admin/EditCategory.html', categoria=categoria_con_base64)


#Formulario Categoria
@app.route('/admin/AddCategoria' ,methods = [ 'GET','POST'])

def Acategorias():
    if request.method == 'POST':
        with get_db_connection() as connection:
            cursor = connection.cursor()
        # Obtener datos del formulario
            nombreCategoria = request.form ['nombreCategoria']
            archivo = request.files['archivo'].read()

            # Llamar al procedimiento PL/SQL para crear un proveedor
            cursor.callproc('CrearCategoria', [nombreCategoria,archivo])

            cursor.close()
            return redirect(url_for('obtener_categorias'))
    return render_template('/Admin/AddCategory.html')


# ------   SUBCATEGORIAS   ------

@app.route('/admin/AddSubCategoria', methods=['GET', 'POST'])
def SubCategory():
    # Conexión a la base de datos y obtener categorías
    with get_db_connection() as connection:
        cursor = connection.cursor()
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
            connection.commit()
            cursor.close()
            return redirect(url_for('mostrar_subcategorias'))
    return render_template('/admin/AddSubCategory.html', categorias=categorias_con_formato)


@app.route('/admin/subcategorias')
def mostrar_subcategorias():
    # Conexión a la base de datos
    with get_db_connection() as connection:
        cursor = connection.cursor()
    
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

@app.route('/subcategorias')
def mostrar_subcategorias2():
    # Conexión a la base de datos
    with get_db_connection() as connection:
        cursor = connection.cursor()
    
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
        return render_template('/user-subcategory.html', subcategorias=subcategoria_array)


@app.route('/admin/subcategorias/eliminar/<int:id_subcategoria>')
def eliminarSubCategoria(id_subcategoria):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.callproc('EliminarSubCategoria', (id_subcategoria,))
            connection.commit()
    return redirect(url_for('mostrar_subcategorias'))


@app.route('/admin/subcategorias/editar/<int:id_subcategoria>', methods=['GET', 'POST'])
def editarSubCategoria(id_subcategoria):
    with get_db_connection() as connection:
        cursor = connection.cursor()

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

            cursor.close()
            return redirect(url_for('mostrar_subcategorias'))
        
        # Obtener la información de la subcategoría para mostrarla en el formulario de edición
        cursor.execute("SELECT id_subcategoria, nombre, id_categoria FROM subcategorias WHERE id_subcategoria = :id", {"id": id_subcategoria})
        subcategoria = cursor.fetchone()

        cursor.close()
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


#SIGNUP

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.form
    try:
        # Convertir datos a tipos apropiados
        id_usuario = data['ID_Usuario']
        contrasena = data['Contrasena']
        nombre = data['NombreUsuario']
        direccion = data['Direccion']
        telefono = data['Telefono']  
        
        rol = 2  # Establecer un valor predeterminado para el rol (el 2 significa que es un cliente)

        if "@admin.com" in id_usuario: 
            rol=1

        with get_db_connection() as connection:
            cursor = connection.cursor()
            # Llamar al procedimiento almacenado con los parámetros adecuados
            cursor.callproc("crear_usuario", [
                id_usuario,
                contrasena,
                nombre,
                direccion,
                telefono,
                rol
            ])
            connection.commit()
            cursor.close()
        print(f"Usuario {nombre} creado con éxito.")
    except cx_Oracle.DatabaseError as e:
        print(f"Error al crear usuario: {e}")
    except Exception as e:
        print(f"Error general: {e}")
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        return redirect(url_for('login'))  # Redirige a la página de inicio de sesión después del registro
    else:
        
        return render_template('signup.html')


#####################################RESENAS################################
@app.route('/resenas')
def resenas():     
    with get_db_connection() as conn:         
        cursor = conn.cursor()         
        cursor.execute("SELECT * FROM Resenas")        
        resenas = cursor.fetchall()     
        return render_template('resenas.html', resenas=resenas)
 
from datetime import datetime 
@app.route('/crear_resena', methods=['POST'])
def crear_resena():     
    with get_db_connection() as conn:         
        cursor = conn.cursor()         
        id_resena = request.form['id_resena']         
        comentario = request.form['comentario']         
        calificacion = request.form['calificacion']         
        fecha_resena = datetime.strptime(request.form['fecha_resena'], '%Y-%m-%d').date()                   
        cursor.callproc("crear_resena", [id_resena, comentario, calificacion, fecha_resena])         
        conn.commit()     
        return redirect(url_for('resenas'))
 
 
@app.route('/borrar_resena/<int:id_resena>', methods=['GET'])
def borrar_resena(id_resena):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.callproc("borrar_resena", [id_resena])
        conn.commit()
 
    return redirect(url_for('resenas'))



#@app.route('/empleados')
#def empleados():
 #   return render_template('empleados.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    with get_db_connection() as conn:
        if request.method == 'POST':
            cursor = conn.cursor()
            ID_Usuario = request.form['ID_Usuario']
            Contrasena = request.form['Contrasena']

            cursor.execute("SELECT * FROM Usuarios WHERE ID_Usuario = :ID_Usuario AND Contrasena = :Contrasena",
                           {"ID_Usuario": ID_Usuario, "Contrasena": Contrasena})
            user = cursor.fetchone()

            if user:
                session['ID_Usuarios'] = user[0]
                session['id_rol'] = user[5]  # Campo del role

                # Condicional rol
                if session['id_rol'] == 1:
                    return redirect(url_for('listar_empleados'))
                elif session['id_rol'] == 2:
                    return redirect(url_for('home'))

            else:
                error = "Invalid credentials. Please try again."
                return render_template('login.html', error=error)

    return render_template('login.html')


#ROLES 

from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'id_rol' in session and session['id_rol'] == required_role:
                return func(*args, **kwargs)
            else:
                flash('You do not have the required permissions to access this page.', 'danger')
                return redirect('/')
        return decorated_function
    return decorator    


##Empleados

@app.route('/crear_empleado', methods=['POST'])
def crear_empleado():
    data = request.form
    try:
        # Convertir datos a tipos apropiados
        Id_empleado = int(data['Id_empleado'])
        Nombre_empleado = data['Nombre_empleado']
        Apellido_empleado = data['Apellido_empleado']
        CargoEmpleado = data['CargoEmpleado']
        Departamento = data['Departamento']  
        Salario = float(data['Salario'])
        
        with get_db_connection() as connection:
            cursor = connection.cursor()
            # Llamar al procedimiento almacenado con los parámetros adecuados
            cursor.callproc("crear_empleado", [
                Id_empleado,
                Nombre_empleado,
                Apellido_empleado,
                CargoEmpleado,
                Departamento,
                Salario
            ])
            connection.commit()
            cursor.close()
        print(f"Empleado {Nombre_empleado} creado con éxito.")
    except cx_Oracle.DatabaseError as e:
        print(f"Error al crear empleado: {e}")
    except Exception as e:
        print(f"Error general: {e}")
    return redirect(url_for('listar_empleados'))



@app.route('/empleados')
def listar_empleados():
    print("Fetching products...")
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM EMPLEADOS ORDER BY Id_empleado")
        empleados = cursor.fetchall()  # Esto recupera todos los empleados de la base de datos
        print(empleados)  
        cursor.close()
    return render_template('empleados.html', empleados=empleados)



@app.route('/actualizar_empleado/<int:Id_empleado>', methods=['POST'])
def actualizar_empleado(Id_empleado):
    data = request.form
    try:
        # Convertir los datos del formulario a los tipos correctos, si es necesario.
        Nombre_empleado = data.get('Nombre_empleado', type=str)
        Apellido_empleado = data.get('Apellido_empleado', type=str)
        CargoEmpleado = data.get('CargoEmpleado', type=str)
        Departamento = data.get('Departamento', type=str)
        Salario = data.get('Salario', type=float)

        # Usar el contexto de la base de datos para llamar al procedimiento.
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.callproc("actualizar_empleado", [
                Id_empleado,
                Nombre_empleado,
                Apellido_empleado,
                CargoEmpleado,
                Departamento,
                Salario
            ])
            connection.commit()
        print(f"Empleado con ID {Id_empleado} actualizado con éxito.")
    except cx_Oracle.DatabaseError as e:
        print(f"Error al actualizar producto: {e}")
        return str(e), 500
    except Exception as e:
        print(f"Error inesperado: {e}")
        return str(e), 500
    return redirect(url_for('listar_empleados'))



@app.route('/eliminar_empleado/<int:Id_empleado>', methods=['POST'])
def eliminar_empleado(Id_empleado):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.callproc("eliminar_empleado", [Id_empleado])
        connection.commit()
        cursor.close()
    return redirect(url_for('listar_empleados'))


# ------------------ PEDIDOS ------------------

@app.route('/pedidos')
def pedidos():
    with get_db_connection() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID_Pedido, ID_Usuario, Fecha_Pedido, Metodo_Pago, Envio, Estado FROM Pedido")
            pedidos = cursor.fetchall()
            cursor.close()
            return render_template('pedidos.html', pedidos=pedidos)
        else:
            return "Error: No se pudo conectar a la base de datos."

@app.route('/crear_pedido', methods=['POST'])
def crear_pedido():
    if request.method == 'POST':
        data = request.form
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO Pedido VALUES (:1, :2, :3, :4, :5, :6)",
                                   (data['ID_Pedido'], data['ID_Usuario'], data['Fecha_Pedido'],
                                    data['Metodo_Pago'], data['Envio'], data['Estado']))
                    conn.commit()
                    flash('Pedido creado exitosamente!', 'success')
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    flash(f'Error al crear el pedido: {error}', 'error')
                cursor.close()
            else:
                flash('Error: No se pudo conectar a la base de datos.', 'error')
        return redirect(url_for('pedidos'))

@app.route('/editar_pedido/<int:id_pedido>', methods=['GET', 'POST'])
def editar_pedido(id_pedido):
    with get_db_connection() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pedido WHERE ID_Pedido = :1", (id_pedido,))
            pedido = cursor.fetchone()
            cursor.close()
            if request.method == 'POST':
                data = request.form
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE Pedido SET ID_Usuario = :1, Fecha_Pedido = :2, Metodo_Pago = :3, Envio = :4, Estado = :5 WHERE ID_Pedido = :6",
                                   (data['ID_Usuario'], data['Fecha_Pedido'], data['Metodo_Pago'], data['Envio'], data['Estado'], id_pedido))
                    conn.commit()
                    flash('Pedido editado exitosamente!', 'success')
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    flash(f'Error al editar el pedido: {error}', 'error')
                cursor.close()
                return redirect(url_for('pedidos'))
            return render_template('editar_pedido.html', pedido=pedido)
        else:
            flash('Error: No se pudo conectar a la base de datos.', 'error')
            return redirect(url_for('pedidos'))

@app.route('/eliminar_pedido/<int:id_pedido>', methods=['POST'])
def eliminar_pedido(id_pedido):
    with get_db_connection() as conn:
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Pedido WHERE ID_Pedido = :1", (id_pedido,))
                conn.commit()
                cursor.close()
                flash('Pedido eliminado exitosamente!', 'success')
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                flash(f'Error al eliminar el pedido: {error}', 'error')
        else:
            flash('Error: No se pudo conectar a la base de datos.', 'error')
    return redirect(url_for('pedidos'))

