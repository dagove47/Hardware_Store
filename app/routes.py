@app.route('/')
def productos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('productos.html', productos=productos)

# Ruta para crear un nuevo producto
@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    if request.method == 'POST':
        data = request.form
        cursor = conn.cursor()
        cursor.callproc("crear_producto", [data['id_producto'], data['nombre'], data['descripcion'], data['proveedor'], data['precio'], data['descuento'], data['cantidad_stock']])
        cursor.close()
        conn.commit()
    return productos()

# Ruta para actualizar un producto
@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    if request.method == 'POST':
        data = request.form
        cursor = conn.cursor()
        cursor.callproc("actualizar_producto", [data['id_producto'], data['nombre'], data['descripcion'], data['proveedor'], data['precio'], data['descuento'], data['cantidad_stock']])
        cursor.close()
        conn.commit()
    return productos()

# Ruta para eliminar un producto
@app.route('/eliminar_producto/<int:id_producto>')
def eliminar_producto(id_producto):
    cursor = conn.cursor()
    cursor.callproc("eliminar_producto", [id_producto])
    cursor.close()
    conn.commit()
    return productos()

if __name__ == '__main__':
    app.run(debug=True)