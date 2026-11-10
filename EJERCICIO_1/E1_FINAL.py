
def limpiar_registro_sensor(registro_raw):

    # Limpiar el identificador.
    sensor_id = registro_raw["sensor_id"].strip()

    # Limpiar temperatura y eliminar la unidad.
    temperatura = registro_raw["temperatura"]
    temperatura = temperatura.replace("C", "").strip()                 
    # Lo casteamos a float.
    temperatura = float(temperatura)                                   

    # Obtener ubicación o asignar valor por defecto.
    ubicacion = registro_raw.get("ubicacion", "Ubicación desconocida")

    if not ubicacion or not ubicacion.strip():
        ubicacion = "Ubicación desconocida"

    # Crear un nuevo diccionario normalizado.
    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion.strip()
    }

    return registro_limpio


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):

    lista_sensores_alerta = []
    suma_temperaturas = 0

    # Recorrer los sensores.
    for sensor in lista_sensores_limpios:

        temperatura = sensor["temperatura"]

        # Comprobar si supera el umbral.
        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

        suma_temperaturas += temperatura

    # Calcula el promedio.
    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)

    return lista_sensores_alerta, promedio_temperatura


# ----------------------------------
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ----------------------------------

# Registros originales, los datos sin limpiar.
sensores_raw = [
    {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
    {"sensor_id": " SENSOR-002 ", "temperatura": "32.8C", "ubicacion": "Planta Sur"},
    {"sensor_id": " SENSOR-003 ", "temperatura": "28.2C", "ubicacion": "Planta Este"},
    {"sensor_id": " SENSOR-004 ", "temperatura": "35.1C"}
]

# Limpiar los registros.
sensores_limpios = []

for registro in sensores_raw:
    sensor_limpio = limpiar_registro_sensor(registro)
    sensores_limpios.append(sensor_limpio)

# Generar el reporte.
alertas, promedio = generar_resumen_sensores(
    sensores_limpios, 30
)

# Mostrar resultados
print("===== REPORTE DE SENSORES =====")

print("\nRegistros normalizados:")

for sensor in sensores_limpios:
    print(sensor)

print("\nSensores que superan los 30°C:")

for sensor_id in alertas:
    print(f"ALERTA: {sensor_id}")

print(f"\nTemperatura promedio: {promedio:.2f} °C")
