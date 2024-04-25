CREATE TABLE productos (
    ID_PRODUCTO NUMBER PRIMARY KEY,
    NOMBRE VARCHAR2(100),
    DESCRIPCION VARCHAR2(255),
    PROVEEDOR VARCHAR2(100),
    PRECIO NUMBER,
    DESCUENTO NUMBER,
    CANTIDAD_STOCK NUMBER
);

-- Crear un nuevo producto
CREATE OR REPLACE PROCEDURE crear_producto(
    p_id_producto IN NUMBER,
    p_nombre IN VARCHAR2,
    p_descripcion IN VARCHAR2,
    p_proveedor IN VARCHAR2,
    p_precio IN NUMBER,
    p_descuento IN NUMBER,
    p_cantidad_stock IN NUMBER
)
AS
BEGIN
    INSERT INTO productos (ID_PRODUCTO, NOMBRE, DESCRIPCION, PROVEEDOR, PRECIO, DESCUENTO, CANTIDAD_STOCK)
    VALUES (p_id_producto, p_nombre, p_descripcion, p_proveedor, p_precio, p_descuento, p_cantidad_stock);
    COMMIT;
END crear_producto;
/

-- Leer un producto por su ID
CREATE OR REPLACE FUNCTION leer_producto(
    p_id_producto IN NUMBER
)
RETURN productos%ROWTYPE
AS
    producto_row productos%ROWTYPE;
BEGIN
    SELECT * INTO producto_row
    FROM productos
    WHERE ID_PRODUCTO = p_id_producto;

    RETURN producto_row;
END leer_producto;
/

-- Actualizar un producto
CREATE OR REPLACE PROCEDURE actualizar_producto(
    p_id_producto IN NUMBER,
    p_nombre IN VARCHAR2,
    p_descripcion IN VARCHAR2,
    p_proveedor IN VARCHAR2,
    p_precio IN NUMBER,
    p_descuento IN NUMBER,
    p_cantidad_stock IN NUMBER
)
AS
BEGIN
    UPDATE productos
    SET NOMBRE = p_nombre,
        DESCRIPCION = p_descripcion,
        PROVEEDOR = p_proveedor,
        PRECIO = p_precio,
        DESCUENTO = p_descuento,
        CANTIDAD_STOCK = p_cantidad_stock
    WHERE ID_PRODUCTO = p_id_producto;
    COMMIT;
END actualizar_producto;
/

-- Eliminar un producto
CREATE OR REPLACE PROCEDURE eliminar_producto(
    p_id_producto IN NUMBER
)
AS
BEGIN
    DELETE FROM productos
    WHERE ID_PRODUCTO = p_id_producto;
    COMMIT;
END eliminar_producto;
/

------------

--Tabla de usuarios

CREATE TABLE Usuarios (
    ID_Usuario VARCHAR2(100) PRIMARY KEY,
    Contrasena VARCHAR2(50),
    NombreUsuario VARCHAR2(100),
    Direccion VARCHAR2(200),
    Telefono NUMBER,
    id_rol INT
);

-- Crear un nuevo usuario
CREATE OR REPLACE PROCEDURE crear_usuario(
    u_id_usuario IN VARCHAR2,
    u_contrasena IN VARCHAR2,
    u_nombre IN VARCHAR2,
    u_direccion IN VARCHAR2,
    u_telefono IN NUMBER,
    u_rol IN INT
)
AS
BEGIN
    INSERT INTO Usuarios (ID_Usuario, Contrasena, NombreUsuario, Direccion, Telefono, id_rol)
    VALUES (u_id_usuario, u_contrasena, u_nombre, u_direccion, u_telefono, u_rol);
    COMMIT;
END crear_usuario;
/

-- Leer un usuario por su ID
CREATE OR REPLACE FUNCTION leer_usuario(
    u_id_usuario IN VARCHAR2
)
RETURN Usuarios%ROWTYPE
AS
    usuario_row Usuarios%ROWTYPE;
BEGIN
    SELECT * INTO usuario_row
    FROM Usuarios
    WHERE ID_Usuario = u_id_usuario;

    RETURN usuario_row;
END leer_usuario;
/

-- Actualizar un usuario
CREATE OR REPLACE PROCEDURE actualizar_usuario(
    u_id_usuario IN VARCHAR2,
    u_contrasena IN VARCHAR2,
    u_nombre IN VARCHAR2,
    u_direccion IN VARCHAR2,
    u_provincia IN VARCHAR2,
    u_telefono IN NUMBER,
    u_fec_nacimiento IN DATE,
    u_rol IN CHAR
)
AS
BEGIN
    UPDATE Usuarios
    SET Contrasena = u_contrasena,
        Nombre = u_nombre,
        Direccion = u_direccion,
        provincia = u_provincia,
        Telefono = u_telefono,
        fecNacimiento = u_fec_nacimiento,
        Rol = u_rol
    WHERE ID_Usuario = u_id_usuario;
    COMMIT;
END actualizar_usuario;
/

-- Eliminar un usuario
CREATE OR REPLACE PROCEDURE eliminar_usuario(
    u_id_usuario IN VARCHAR2
)
AS
BEGIN
    DELETE FROM Usuarios
    WHERE ID_Usuario = u_id_usuario;
    COMMIT;
END eliminar_usuario;
/

create or replace PROCEDURE cambiar_rol_usuario(
    u_id_usuario IN VARCHAR2,
    u_nuevo_rol IN CHAR
)
AS
BEGIN
    UPDATE Usuarios
    SET Rol = u_nuevo_rol
    WHERE ID_Usuario = u_id_usuario;
    COMMIT;
END cambiar_rol_usuario;

create or replace NONEDITIONABLE PROCEDURE obtener_usuarios
AS
BEGIN
    FOR usuario_row IN (SELECT * FROM Usuarios) LOOP
        DBMS_OUTPUT.PUT_LINE('ID Usuario: ' || usuario_row.ID_Usuario || ', Nombre: ' || usuario_row.Nombre);
    END LOOP;
END obtener_usuarios;

--Ver productos agotados
CREATE OR REPLACE VIEW productos_agotados AS
SELECT *
FROM productos
WHERE CANTIDAD_STOCK = 0;

--Usuarios con el rol de administrador
CREATE OR REPLACE VIEW usuarios_administrativos AS
SELECT *
FROM Usuarios
WHERE Rol = 'Admin';

--Productos con poco stock (menos de 5)
CREATE OR REPLACE VIEW productos_stock_bajo AS
SELECT *
FROM productos
WHERE CANTIDAD_STOCK < 5;

--Informacion de usuarios
CREATE OR REPLACE VIEW informacion_usuarios AS
SELECT ID_Usuario, Nombre, Direccion, Telefono, fecNacimiento, Rol
FROM Usuarios;

---TABLAS---

-- Crear la tabla de Categorias
CREATE TABLE Categorias (
    id_categoria NUMBER PRIMARY KEY,
    Nombre VARCHAR2(50),
    archivo blob
);

-- Crear la tabla de SubCategorias
CREATE TABLE SubCategorias (
    id_subcategoria NUMBER PRIMARY KEY,
    Nombre VARCHAR2(50),
    id_categoria Number,
    CONSTRAINT fk_categoria FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria)
);



-------------------------Categorias---------------------------------

--SP Categorias | CREAR --
CREATE OR REPLACE PROCEDURE CrearCategoria(
    c_nombre varchar2,
    c_archivo blob
)
AS
BEGIN
    INSERT INTO categorias (nombre, archivo)
    VALUES (c_nombre,c_archivo);
    COMMIT;
END;

--SP Categorias | OBTENER --

CREATE OR REPLACE PROCEDURE ObtenerCategorias (
    categorias_cursor OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN categorias_cursor FOR
    SELECT id_categoria,nombre, archivo
    FROM categorias;
END ObtenerCategorias;


--SP Categorias | ELIMINAR --
CREATE OR REPLACE PROCEDURE EliminarCategoria(id_cate IN NUMBER) AS
BEGIN
    DELETE FROM categorias WHERE id_categoria = id_cate;
END EliminarCategoria;

--SP Categorias | EDITAR --
CREATE OR REPLACE PROCEDURE editar_categoria(
    p_id IN number,
    p_nombreCategoria IN VARCHAR2,
    p_archivo IN BLOB
)
IS
BEGIN
    UPDATE categorias
    SET nombre = p_nombreCategoria,
        archivo = p_archivo
    WHERE id_categoria = p_id;
    
    COMMIT;
END editar_categoria;

--Triggers y secuencias--

CREATE SEQUENCE seq_categorias START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER trg_before_insert_categorias
BEFORE INSERT ON categorias
FOR EACH ROW
BEGIN
    SELECT seq_categorias.NEXTVAL INTO :NEW.id_categoria FROM DUAL;
END;

-- SUBCATEGORIAS --

--SP SubCategoria | Agregar
CREATE OR REPLACE PROCEDURE AgregarSubCategoria (
   nombre IN VARCHAR2,
   categoria_id IN NUMBER
) AS
   v_categoria_count NUMBER;
BEGIN
   -- Check if the selected category exists in the categorias table
   SELECT COUNT(1) INTO v_categoria_count FROM categorias WHERE id_categoria = categoria_id;

   IF v_categoria_count = 0 THEN
      -- Raise an exception if the categoria doesn't exist
      RAISE_APPLICATION_ERROR(-20001, 'Categoria no existe');
   END IF;

   -- The selected category exists, proceed with the subcategory insertion
   INSERT INTO subcategorias (nombre, id_categoria)
   VALUES (nombre, categoria_id);
END AgregarSubCategoria;

-- SP SubCategoria | Obtener 
CREATE OR REPLACE PROCEDURE ObtenerSubcategorias (
    subcategorias_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN subcategorias_cursor FOR
    SELECT id_subcategoria, nombre,id_categoria
    FROM subcategorias;
END ObtenerSubcategorias;

--SP SubCategoria | Eliminar
CREATE OR REPLACE PROCEDURE EliminarSubCategoria(id_subcate IN NUMBER) AS
BEGIN
    DELETE FROM subcategorias WHERE id_subcategoria = id_subcate;
END EliminarSubCategoria;

--SP SubCategoria | Editar
CREATE OR REPLACE PROCEDURE editar_subcategoria(
    p_id in number,
    p_nombreSubCategoria IN VARCHAR2,
    p_idcategoria in number
)
IS
BEGIN
    UPDATE subcategorias
    SET nombre = p_nombreSubCategoria,
        id_categoria = p_idcategoria
    WHERE id_subcategoria = p_id;
    
    COMMIT;
END editar_subcategoria;

-- Triggers y secuencias SubCategorias --
CREATE SEQUENCE seq_subcategorias START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER trg_before_insert_subcategorias
BEFORE INSERT ON subcategorias
FOR EACH ROW
BEGIN
    SELECT seq_subcategorias.NEXTVAL INTO :NEW.id_subcategoria FROM DUAL;
END;


------------------------RESENAS---------------------

CREATE TABLE Resenas (
    ID_Resena NUMBER PRIMARY KEY,
    Comentario VARCHAR2(1000),
    Calificacion NUMBER,
    Fecha_Resena DATE
);


-- CREATE
CREATE OR REPLACE PROCEDURE crear_resena (
    p_id_resena IN NUMBER,
    p_comentario IN VARCHAR2,
    p_calificacion IN NUMBER,
    p_fecha_resena IN DATE
) AS
BEGIN
    INSERT INTO Resenas (ID_Resena, Comentario, Calificacion, Fecha_Resena)
    VALUES (p_id_resena, p_comentario, p_calificacion, p_fecha_resena);
    COMMIT;
END;
/

-- READ
CREATE OR REPLACE FUNCTION obtener_resena(p_id_resena IN NUMBER) RETURN Resenas%ROWTYPE AS
    resena_row Resenas%ROWTYPE;
BEGIN
    SELECT * INTO resena_row FROM Resenas WHERE ID_Resena = p_id_resena;
    RETURN resena_row;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Reseña no encontrada');
        RETURN NULL;
END;
/



-- DELETE
CREATE OR REPLACE PROCEDURE borrar_resena (p_id_resena IN NUMBER) AS
BEGIN
    DELETE FROM Resenas WHERE ID_Resena = p_id_resena;
    COMMIT;
END;
/


------------------------ PEDIDOS ---------------------
CREATE TABLE Pedido (
    ID_Pedido NUMBER PRIMARY KEY,
    ID_Usuario VARCHAR2(100),
    Fecha_Pedido DATE,
    Metodo_Pago VARCHAR2(50),
    Envio VARCHAR2(50),
    Estado VARCHAR2(50),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario)
);


------------------------ DETALLE PEDIDOS ---------------------
CREATE TABLE Detalle_Pedido (
    ID_Detalle NUMBER PRIMARY KEY,
    ID_Pedido NUMBER,
    ID_PRODUCTO NUMBER,
    Cantidad NUMBER,
    Precio_Unidad NUMBER,
    Subtotal NUMBER,
    FOREIGN KEY (ID_Pedido) REFERENCES Pedido(ID_Pedido),
    FOREIGN KEY (ID_PRODUCTO) REFERENCES productos(ID_PRODUCTO)
);


-- Procedure to insert a new pedido
CREATE OR REPLACE PROCEDURE InsertarPedido(
    p_ID_Pedido IN NUMBER,
    p_ID_Usuario IN VARCHAR2,
    p_Fecha_Pedido IN DATE,
    p_Metodo_Pago IN VARCHAR2,
    p_Envio IN VARCHAR2,
    p_Estado IN VARCHAR2
) AS
BEGIN
    INSERT INTO Pedido (ID_Pedido, ID_Usuario, Fecha_Pedido, Metodo_Pago, Envio, Estado)
    VALUES (p_ID_Pedido, p_ID_Usuario, p_Fecha_Pedido, p_Metodo_Pago, p_Envio, p_Estado);
    COMMIT;
END InsertarPedido;

-- Function to obtain all pedidos
CREATE OR REPLACE FUNCTION ObtenerPedidos RETURN SYS_REFCURSOR AS
    pedidos_cursor SYS_REFCURSOR;
BEGIN
    OPEN pedidos_cursor FOR
    SELECT ID_Pedido, ID_Usuario, Fecha_Pedido, Metodo_Pago, Envio, Estado
    FROM Pedido;
    RETURN pedidos_cursor;
END ObtenerPedidos;

-- Procedure to update the estado of a pedido
CREATE OR REPLACE PROCEDURE ActualizarEstadoPedido(
    p_ID_Pedido IN NUMBER,
    p_NuevoEstado IN VARCHAR2
) AS
BEGIN
    UPDATE Pedido SET Estado = p_NuevoEstado WHERE ID_Pedido = p_ID_Pedido;
    COMMIT;
END ActualizarEstadoPedido;

-- Procedure to delete a pedido
CREATE OR REPLACE PROCEDURE EliminarPedido(
    p_ID_Pedido IN NUMBER
) AS
BEGIN
    DELETE FROM Pedido WHERE ID_Pedido = p_ID_Pedido;
    COMMIT;
END EliminarPedido;


-- DETALLE PEDIDOS

-- Procedure to insert a new detalle de pedido
CREATE OR REPLACE PROCEDURE InsertarDetallePedido(
    p_ID_Detalle IN NUMBER,
    p_ID_Pedido IN NUMBER,
    p_ID_Producto IN NUMBER,
    p_Cantidad IN NUMBER,
    p_Precio_Unidad IN NUMBER,
    p_Subtotal IN NUMBER
) AS
BEGIN
    INSERT INTO Detalle_Pedido (ID_Detalle, ID_Pedido, ID_Producto, Cantidad, Precio_Unidad, Subtotal)
    VALUES (p_ID_Detalle, p_ID_Pedido, p_ID_Producto, p_Cantidad, p_Precio_Unidad, p_Subtotal);
    COMMIT;
END InsertarDetallePedido;

-- Function to obtain all detalles de pedido of a specific pedido
CREATE OR REPLACE FUNCTION ObtenerDetallesPedido(
    p_ID_Pedido IN NUMBER
) RETURN SYS_REFCURSOR AS
    detalles_cursor SYS_REFCURSOR;
BEGIN
    OPEN detalles_cursor FOR
    SELECT ID_Detalle, ID_Pedido, ID_Producto, Cantidad, Precio_Unidad, Subtotal
    FROM Detalle_Pedido
    WHERE ID_Pedido = p_ID_Pedido;
    RETURN detalles_cursor;
END ObtenerDetallesPedido;

-- Procedure to update a detalle de pedido
CREATE OR REPLACE PROCEDURE ActualizarDetallePedido(
    p_ID_Detalle IN NUMBER,
    p_ID_Pedido IN NUMBER,
    p_ID_Producto IN NUMBER,
    p_Cantidad IN NUMBER,
    p_Precio_Unidad IN NUMBER,
    p_Subtotal IN NUMBER
) AS
BEGIN
    UPDATE Detalle_Pedido
    SET ID_Pedido = p_ID_Pedido,
        ID_Producto = p_ID_Producto,
        Cantidad = p_Cantidad,
        Precio_Unidad = p_Precio_Unidad,
        Subtotal = p_Subtotal
    WHERE ID_Detalle = p_ID_Detalle;
    COMMIT;
END ActualizarDetallePedido;

-- Procedure to delete a detalle de pedido
CREATE OR REPLACE PROCEDURE EliminarDetallePedido(
    p_ID_Detalle IN NUMBER
) AS
BEGIN
    DELETE FROM Detalle_Pedido WHERE ID_Detalle = p_ID_Detalle;
    COMMIT;
END EliminarDetallePedido;

