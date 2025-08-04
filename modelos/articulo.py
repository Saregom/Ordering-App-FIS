class Articulo:
    def __init__(self, codigo, nombre, descripcion, precio, cantidad=0, stock_minimo=5, unidad_medida="unidades"):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.stock_minimo = stock_minimo
        self.unidad_medida = unidad_medida