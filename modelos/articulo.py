class Articulo:
    def __init__(self, codigo, nombre, descripcion, precio, cantidad=0):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad