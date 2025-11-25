import matplotlib.pyplot as plt

class Region:
    """Clase para representar una región con su nombre y población."""
    def __init__(self, nombre, poblacion):
        """
        Constructor de la clase Region.
        
        Args:
            nombre (str): El nombre de la región.
            poblacion (int/float): El número de habitantes (en millones) de la región.
        """
        self.nombre = nombre
        self.poblacion = poblacion

class Pais:
    """
    Clase para representar un país y sus regiones.
    Permite generar un gráfico de barras de población por región.
    """
    def __init__(self, nombre, regiones):
        """
        Constructor de la clase País.
        
        Args:
            nombre (str): Nombre del país (ej: "Alemania").
            regiones (list): Lista de objetos Region.
        """
        self.nombre = nombre  # Nombre del país
        self.regiones = regiones  # Lista de objetos Region

    def graficar(self):
        """
        Genera y muestra un gráfico de barras de población por región.
        Utiliza Matplotlib para la visualización.
        """
        # Extraer nombres y poblaciones de la lista de objetos Region
        nombres = [r.nombre for r in self.regiones]
        poblaciones = [r.poblacion for r in self.regiones]

        plt.figure(figsize=(8,5))
        plt.bar(nombres, poblaciones)
        plt.title(f"Población por región en {self.nombre}")
        plt.xlabel("Regiones")
        plt.ylabel("Población (millones)")
        plt.show()

# --- Ejecución y uso de las clases ---
regiones_alemania = [
    Region("Norte", 13),
    Region("Centro", 26),
    Region("Sur", 23)
]

alemania = Pais("Alemania", regiones_alemania)
alemania.graficar()