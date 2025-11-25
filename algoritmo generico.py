import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# --- 1. Cargar y preparar los datos (Dataset Iris) ---
# El dataset Iris es un estándar para clasificación en scikit-learn
iris = load_iris()
X, y = iris.data, iris.target
# Separar datos para entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- 2. Configuración del Algoritmo Genético (AG) ---
# Esto define nuestro "espacio de genes" o el rango de hiperparámetros a optimizar.
PARAM_SPACE = {
    # Hiperparámetro K: número de vecinos a considerar
    'n_neighbors': [3, 5, 7, 9, 11, 13, 15],
    # Hiperparámetro de peso: cómo ponderar los votos de los vecinos
    'weights': ['uniform', 'distance']
}
POPULATION_SIZE = 10  # Número de combinaciones de parámetros (individuos) en cada generación
GENERATIONS = 5       # Número de ciclos de evolución

def evaluate_fitness(n_neighbors, weights):
    """
    Función de Aptitud (Fitness).
    Evalúa el rendimiento de un individuo (combinación de hiperparámetros) 
    midiendo la precisión (accuracy) del modelo K-NN en el conjunto de prueba.
    
    Args:
        n_neighbors (int): El valor del hiperparámetro K.
        weights (str): La estrategia de ponderación.
        
    Returns:
        float: El score de precisión del modelo (el fitness).
    """
    model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)

def initialize_population():
    """Crea una población inicial de individuos (combinaciones de hiperparámetros) aleatorios."""
    population = []
    neighbors = PARAM_SPACE['n_neighbors']
    weights = PARAM_SPACE['weights']
    
    for _ in range(POPULATION_SIZE):
        # Selección aleatoria de los "genes" para el individuo inicial
        n = np.random.choice(neighbors)
        w = np.random.choice(weights)
        population.append({'n_neighbors': n, 'weights': w, 'fitness': 0.0})
    return population

def genetic_algorithm_search():
    """
    Simula el proceso de búsqueda de hiperparámetros mediante un Algoritmo Genético.
    Implementa los pasos de: Evaluación, Selección, Cruce y Mutación.
    """
    population = initialize_population()
    best_params = None
    best_fitness = -1

    print("--- Inicio del Algoritmo Genético Simulado ---")

    for gen in range(GENERATIONS):
        # 3. Evaluación (Fitness)
        for individual in population:
            # Calcular la aptitud del individuo
            individual['fitness'] = evaluate_fitness(individual['n_neighbors'], individual['weights'])

        # Ordenar por fitness (los mejores individuos primero)
        population.sort(key=lambda x: x['fitness'], reverse=True)
        
        current_best = population[0]
        if current_best['fitness'] > best_fitness:
            best_fitness = current_best['fitness']
            best_params = current_best

        print(f"Generación {gen+1}: Mejor Fitness = {best_fitness:.4f}, Parámetros = {best_params['n_neighbors'], best_params['weights']}")
        
        if gen < GENERATIONS - 1:
            # 4. Selección (Tomamos los 5 mejores como padres para la siguiente generación)
            parents = population[:5]
            new_population = []

            # 5. Cruce (Crossover) y 6. Mutación (Generación de nuevos hijos)
            for i in range(POPULATION_SIZE):
                # Selección aleatoria de un padre (el más apto tiene más probabilidad de ser elegido)
                p1 = np.random.choice(parents)
                
                # Simulación de Cruce: Heredamos n_neighbors del mejor padre
                n_neighbor_new = p1['n_neighbors'] 
                
                # Mutación del parámetro 'weights': 
                # Simplemente elegimos un nuevo weight al azar de todo el espacio
                weight_new = np.random.choice(PARAM_SPACE['weights'])
                
                # Mutación de n_neighbors: Pequeña probabilidad de cambiar el valor K
                if np.random.rand() < 0.2: # 20% de probabilidad de mutación
                    n_neighbor_new = np.random.choice(PARAM_SPACE['n_neighbors'])

                # Nuevo individuo (hijo)
                new_population.append({'n_neighbors': n_neighbor_new, 
                                       'weights': weight_new, 
                                       'fitness': 0.0}) # Su fitness se evaluará en la siguiente generación
            population = new_population

    print("--- Búsqueda Finalizada ---")
    print(f"Mejores parámetros encontrados: K={best_params['n_neighbors']} con weights='{best_params['weights']}'")
    print(f"Máximo Accuracy (Fitness) alcanzado: {best_fitness:.4f}")

if __name__ == '__main__':
    genetic_algorithm_search()