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

-- Crear un nuevo usuario
CREATE OR REPLACE PROCEDURE crear_usuario(
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
    INSERT INTO Usuarios (ID_Usuario, Contrasena, Nombre, Direccion, provincia, Telefono, fecNacimiento, Rol)
    VALUES (u_id_usuario, u_contrasena, u_nombre, u_direccion, u_provincia, u_telefono, u_fec_nacimiento, u_rol);
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

--SP Categorias--
CREATE OR REPLACE PROCEDURE CrearCategoria(
    c_nombre varchar2,
    c_archivo blob,
)
AS
BEGIN
    INSERT INTO categorias (nombre, archivo)
    VALUES (c_nombre,c_archivo);
    COMMIT;
END;


--Triggers y secuencias--

CREATE SEQUENCE seq_categorias START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER trg_before_insert_categorias
BEFORE INSERT ON categorias
FOR EACH ROW
BEGIN
    SELECT seq_categorias.NEXTVAL INTO :NEW.id FROM DUAL;
END;