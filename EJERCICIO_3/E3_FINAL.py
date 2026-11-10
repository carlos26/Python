
import json
import unittest


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

        # Validamos el stock inicial
        self.__stock = 0
        self.establecer_stock(stock)

    # Getter
    def obtener_stock(self):
        return self.__stock

    # Setter
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

    # Convertir objeto en diccionario
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

    # Ampliar información para JSON
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
# PUNTO B: CÁLCULO DE EMISIONES
# ==========================================

def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):

    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo.")

    emisiones = consumo_kwh * factor_emision

    return emisiones


# ==========================================
# PUNTO B: OBTENER MÉTRICAS DE CONSUMO
# ==========================================

def obtener_metricas_consumo(registros):

    total_emisiones = 0
    consumo_por_planta = {}

    for registro in registros:

        planta = registro["planta"]
        consumo = registro["consumo_kwh"]

        # Calcular emisiones del registro
        emisiones = calcular_emisiones_carbono(consumo)

        total_emisiones += emisiones

        # Acumular consumo por planta
        if planta in consumo_por_planta:
            consumo_por_planta[planta] += consumo
        else:
            consumo_por_planta[planta] = consumo

    # Determinar planta con mayor consumo
    if consumo_por_planta:

        planta_mayor_consumo = max(
            consumo_por_planta,
            key=consumo_por_planta.get
        )

        mayor_consumo_kwh = consumo_por_planta[planta_mayor_consumo]

    else:
        planta_mayor_consumo = None
        mayor_consumo_kwh = 0

    return {
        "total_emisiones": total_emisiones,
        "consumo_por_planta": consumo_por_planta,
        "planta_mayor_consumo": planta_mayor_consumo,
        "mayor_consumo_kwh": mayor_consumo_kwh
    }


# ==========================================
# PUNTO B: PRUEBAS UNITARIAS
# ==========================================

class TestCalculoEmisiones(unittest.TestCase):

    def test_calculo_normal(self):

        resultado = calcular_emisiones_carbono(100)

        self.assertAlmostEqual(resultado, 40.0)

    def test_factor_personalizado(self):

        resultado = calcular_emisiones_carbono(100, 0.5)

        self.assertAlmostEqual(resultado, 50.0)

    def test_consumo_cero(self):

        resultado = calcular_emisiones_carbono(0)

        self.assertEqual(resultado, 0)

    def test_consumo_negativo(self):

        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)


class TestMetricasConsumo(unittest.TestCase):

    def test_metricas_consumo(self):

        registros = [
            {"planta": "Planta A", "consumo_kwh": 100},
            {"planta": "Planta B", "consumo_kwh": 200},
            {"planta": "Planta A", "consumo_kwh": 50}
        ]

        resultado = obtener_metricas_consumo(registros)

        self.assertAlmostEqual(
            resultado["total_emisiones"], 140.0
        )

        self.assertEqual(
            resultado["planta_mayor_consumo"], "Planta B"
        )

        self.assertEqual(
            resultado["mayor_consumo_kwh"], 200
        )


# ==========================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================

def main():

    # --------------------------------------
    # CREAR PRODUCTOS
    # --------------------------------------

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

    # --------------------------------------
    # VERIFICAR EXCEPCIÓN PERSONALIZADA
    # --------------------------------------

    try:
        panel1.establecer_stock(-5)

    except StockInvalidoError as error:
        print(f"ERROR CONTROLADO: {error}")

    # --------------------------------------
    # MOSTRAR EL CATÁLOGO
    # --------------------------------------

    catalogo = [panel1, panel2]

    for producto in catalogo:
        print("\n" + producto.ficha_tecnica())

    # --------------------------------------
    # GUARDAR CATÁLOGO EN JSON
    # --------------------------------------

    gestor = GestorInventario()

    gestor.guardar_catalogo_json(
        catalogo,
        "catalogo_ecotech.json"
    )

    # --------------------------------------
    # PROCESAR REGISTROS DE CONSUMO
    # --------------------------------------

    registros = [
        {"planta": "Planta A", "consumo_kwh": 100},
        {"planta": "Planta B", "consumo_kwh": 200},
        {"planta": "Planta A", "consumo_kwh": 50},
        {"planta": "Planta C", "consumo_kwh": 80}
    ]

    metricas = obtener_metricas_consumo(registros)

    print("\n========== MÉTRICAS DE CONSUMO ==========")

    print(
        f"Emisiones totales: "
        f"{metricas['total_emisiones']} kg CO2"
    )

    print("\nConsumo por planta:")

    for planta, consumo in metricas["consumo_por_planta"].items():
        print(f"{planta}: {consumo} kWh")

    print(
        f"\nPlanta con mayor consumo: "
        f"{metricas['planta_mayor_consumo']}"
    )

    print(
        f"Mayor consumo: "
        f"{metricas['mayor_consumo_kwh']} kWh"
    )


# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    main()
