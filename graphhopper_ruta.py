import requests
import os

API_KEY = os.getenv("GRAPHHOPPER_API_KEY")

if not API_KEY:
    print("Error: No se encontró la API Key de GraphHopper.")
    exit()

def obtener_coordenadas(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "hits" not in data or len(data["hits"]) == 0:
        return None

    lat = data["hits"][0]["point"]["lat"]
    lon = data["hits"][0]["point"]["lng"]
    return lat, lon


print("=== Calculador de Rutas Chile - Argentina (GraphHopper) ===")
print("Escriba 'v' para salir\n")

while True:
    origen = input("Ciudad de Origen: ")
    if origen.lower() == "v":
        break

    destino = input("Ciudad de Destino: ")
    if destino.lower() == "v":
        break

    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)

    if not coord_origen or not coord_destino:
        print("No se pudieron obtener coordenadas de alguna ciudad\n")
        continue

    print("\nMedio de transporte:")
    print("1 - Auto")
    print("2 - Bicicleta")
    print("3 - A pie")

    opcion = input("Seleccione una opción: ")

    if opcion.lower() == "v":
        break

    if opcion == "1":
        vehiculo = "car"
    elif opcion == "2":
        vehiculo = "bike"
    elif opcion == "3":
        vehiculo = "foot"
    else:
        print("Opción inválida\n")
        continue

    url = "https://graphhopper.com/api/1/route"
    params = {
        "key": API_KEY,
        "vehicle": vehiculo,
        "locale": "es",
        "points_encoded": "false",
        "instructions": "true",
        "point": [
            f"{coord_origen[0]},{coord_origen[1]}",
            f"{coord_destino[0]},{coord_destino[1]}"
        ]
    }

    print("\nCalculando ruta...\n")

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error al obtener la ruta\n")
        continue

    data = response.json()
    ruta = data["paths"][0]

    distancia_km = ruta["distance"] / 1000
    distancia_millas = distancia_km * 0.621371

    tiempo_seg = ruta["time"] / 1000
    horas = int(tiempo_seg // 3600)
    minutos = int((tiempo_seg % 3600) // 60)

    print("=== RESULTADOS ===")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Distancia: {distancia_millas:.2f} millas")
    print(f"Duración: {horas} h {minutos} min\n")

    print("=== NARRATIVA DEL VIAJE ===")
    for paso in ruta["instructions"]:
        print(f"- {paso['text']}")

    print("\n----------------------------\n")
