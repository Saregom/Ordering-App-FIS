class Usuario:
    def __init__(self, cod_us, nombre_us):
        self.cod_us = cod_us
        self.nombre_us = nombre_us


class Cliente(Usuario):
    def __init__(self, cod_us, nombre_us, saldo, limite_credito, descuento):
        super().__init__(cod_us, nombre_us)
        self.saldo = saldo
        self.limite_credito = limite_credito
        self.descuento = descuento
        self.pedidos = []

    def realizar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def consultar_historial(self):
        return self.pedidos


class Proveedor(Usuario):
    def actualizar_stock(self, planta, articulo, cantidad):
        planta.cant_art_pm[articulo.codigo] = planta.cant_art_pm.get(articulo.codigo, 0) + cantidad


class DirectorVentas(Usuario):
    def consultar_inventario(self, inventario):
        return inventario.articulos