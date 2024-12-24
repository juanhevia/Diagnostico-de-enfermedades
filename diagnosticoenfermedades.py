import json
import matplotlib.pyplot as plt

# Cargar la base de datos de enfermedades desde un archivo JSON
def cargar_enfermedades():
    try:
        with open("enfermedades.json", "r") as file:
            enfermedades = json.load(file)
        return enfermedades
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'enfermedades.json'.")
        return []

def diagnosticar_sintomas(enfermedades):
    print("Introduce los síntomas que tienes uno por uno. Escribe 'listo' cuando termines:")
    sintomas_usuario = {}
    while True:
        sintoma = input("Síntoma: ").strip().lower()  
        if sintoma == "listo":
            break
        
        # Validar entrada 
        if not sintoma:
            print("Por favor, ingresa un síntoma válido.")
            continue
        
        # Preguntar la gravedad del síntoma
        while True:
            try:
                gravedad = int(input(f"Del 1 al 10, ¿cuál es la gravedad de {sintoma}? "))
                if 1 <= gravedad <= 10:
                    sintomas_usuario[sintoma] = gravedad
                    break  # Salir del ciclo interno si la gravedad es válida
                else:
                    print("Por favor, introduce un valor entre 1 y 10.")
            except ValueError:
                print("Por favor, introduce un número válido para la gravedad.")
    
    # Calcular coincidencia ponderada
    diagnostico = {}
    for enfermedad in enfermedades:
        nombre = enfermedad["nombre"]
        sintomas = enfermedad["sintomas"]
        puntuacion = 0
        for sintoma, peso in sintomas.items():
            if sintoma in sintomas_usuario:
                puntuacion += peso * sintomas_usuario[sintoma]  # Peso del síntoma por gravedad indicada
        if puntuacion > 0:
            diagnostico[nombre] = puntuacion
    
    # Mostrar diagnóstico ordenado por relevancia
    diagnostico = dict(sorted(diagnostico.items(), key=lambda x: x[1], reverse=True))
    print("\nPosibles enfermedades y su relevancia:")
    for enfermedad, puntuacion in diagnostico.items():
        print(f"{enfermedad}: {puntuacion}")
    
    return diagnostico, sintomas_usuario

def graficar_diagnostico(diagnostico, sintomas_usuario):
    if not diagnostico:
        print("No se encontraron enfermedades relacionadas con los síntomas proporcionados.")
        return
    
    enfermedades = list(diagnostico.keys())
    relevancias = list(diagnostico.values())
    
    # Graficar relevancia de las enfermedades
    plt.figure(figsize=(10, 6))
    plt.bar(enfermedades, relevancias, color='skyblue')
    plt.title("Posibles enfermedades según los síntomas reportados")
    plt.xlabel("Enfermedades")
    plt.ylabel("Relevancia (ponderación por gravedad)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    # Graficar gravedad de los síntomas reportados
    sintomas = list(sintomas_usuario.keys())
    gravedades = list(sintomas_usuario.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(sintomas, gravedades, color='salmon')
    plt.title("Gravedad de los síntomas reportados")
    plt.xlabel("Síntomas")
    plt.ylabel("Gravedad (escala 1-10)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Flujo principal del programa
if __name__ == "__main__":
    enfermedades = cargar_enfermedades()
    if enfermedades:
        diagnostico, sintomas_usuario = diagnosticar_sintomas(enfermedades)
        graficar_diagnostico(diagnostico, sintomas_usuario)
