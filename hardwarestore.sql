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