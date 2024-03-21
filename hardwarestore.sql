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
    Nombre VARCHAR2(100),
    Direccion VARCHAR2(200),
    provincia VARCHAR2(50),
    Telefono NUMBER,
    fecNacimiento DATE,
    Rol CHAR(1) CHECK (Rol IN ('Admin', 'Usuario'))
);