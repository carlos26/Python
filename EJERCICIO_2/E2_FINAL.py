
import json


# ==========================================
# EXCEPCIÓN PERSONALIZADA
# ==========================================

class StockInvalidoError(Exception):
    pass


# ==========================================
# CLASE BASE
# ==========================================

class DispositivoEcológico:

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.__stock = stock

    # Getter: permite consultar el stock
    def obtener_stock(self):
        return self.__stock

    # Setter: permite modificar el stock con validación
    def establecer_stock(self, nuevo_stock):

        if nuevo_stock < 0:
            raise StockInvalidoError(
                "El stock no puede ser negativo."
            )

        self.__stock = nuevo_stock

    # Método genérico
    def ficha_tecnica(self):
        return (
            f"Producto: {self.nombre}\n"
            f"Precio: ${self.precio}\n"
            f"Stock: {self.__stock}"
        )

    # Convertir el objeto en diccionario
    def convertir_diccionario(self):
        return {
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.__stock
        }


# ==========================================
# CLASE HIJA
# ==========================================

class PanelSolar(DispositivoEcológico):

    def __init__(self, nombre, precio, stock, potencia, eficiencia):
        super().__init__(nombre, precio, stock)

        self.potencia = potencia
        self.eficiencia = eficiencia

    # Sobrescritura del método (polimorfismo)
    def ficha_tecnica(self):
        ficha = super().ficha_tecnica()

        return (
            f"{ficha}\n"
            f"Potencia: {self.potencia} W\n"
            f"Eficiencia: {self.eficiencia}%"
        )

    # Ampliar la información para el archivo JSON
    def convertir_diccionario(self):
        datos = super().convertir_diccionario()

        datos["potencia"] = self.potencia
        datos["eficiencia"] = self.eficiencia

        return datos


# ==========================================
# GESTOR DE INVENTARIO
# ==========================================

class GestorInventario:

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):

        catalogo = []

        for dispositivo in lista_dispositivos:
            catalogo.append(dispositivo.convertir_diccionario())

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:

            json.dump(
                catalogo,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        print(f"\nCatálogo guardado correctamente en: {ruta_archivo}")


# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================

# Crear productos
panel1 = PanelSolar(
    "Panel Solar EcoMax",
    250000,
    15,
    450,
    22.5
)

panel2 = PanelSolar(
    "Panel Solar GreenPower",
    180000,
    10,
    350,
    20.8
)

# Verificar excepción personalizada
try:
    panel1.establecer_stock(-5)

except StockInvalidoError as error:
    print(f"ERROR CONTROLADO: {error}")


# Crear catálogo con productos válidos
catalogo = [panel1, panel2]

# Mostrar fichas técnicas
for producto in catalogo:
    print("\n" + producto.ficha_tecnica())


# Guardar catálogo en JSON
gestor = GestorInventario()

gestor.guardar_catalogo_json(
    catalogo,
    "catalogo_ecotech.json"
)
