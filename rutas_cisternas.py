import heapq
from collections import defaultdict
import matplotlib.pyplot as plt

class GrafoRutasCisternas:
    """
    Clase para modelar la red vial como un grafo dirigido y ponderado
    para optimizar rutas de distribución de agua en cisternas
    """
    
    def __init__(self):
        self.grafo = defaultdict(list)
        self.vertices = set()
        self.pesos = {}
    
    def agregar_arista(self, u, v, peso):
        """Agrega una arista dirigida de u a v con peso especificado"""
        self.grafo[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)
        self.pesos[(u, v)] = peso
    
    def dijkstra(self, origen, destino):
        """
        Implementa algoritmo de Dijkstra para encontrar camino más corto
        Retorna: (costo_total, camino, longitud_ruta)
        """
        distancias = {v: float('inf') for v in self.vertices}
        distancias[origen] = 0
        padre = {v: None for v in self.vertices}
        visitados = set()
        
        cola_prioridad = [(0, origen)]
        
        while cola_prioridad:
            distancia_actual, vertice_actual = heapq.heappop(cola_prioridad)
            
            if vertice_actual in visitados:
                continue
            
            visitados.add(vertice_actual)
            
            if vertice_actual == destino:
                break
            
            for vecino in self.grafo[vertice_actual]:
                peso_arista = self.pesos[(vertice_actual, vecino)]
                nueva_distancia = distancia_actual + peso_arista
                
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padre[vecino] = vertice_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
        
        # Reconstruir camino
        if distancias[destino] == float('inf'):
            return None, [], 0
        
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = padre[actual]
        camino.reverse()
        
        return distancias[destino], camino, len(camino)

# Crear grafo 5x5 (red vial de Lima simulada)
print("="*70)
print("ENTREGA DE AGUA EN CISTERNAS - OPTIMIZACIÓN DE RUTAS")
print("Teoría de Grafos - Red Vial 5x5 - ESCENARIO BASE")
print("="*70)

grafo = GrafoRutasCisternas()

# Modelar red vial 5x5 (nodos: 0-24)
# Estructura: matriz de posiciones
#     0   1   2   3   4
#     5   6   7   8   9
#    10  11  12  13  14
#    15  16  17  18  19
#    20  21  22  23  24

# Aristas horizontales
aristas_red = [
    # Fila 0
    (0, 1, 15), (1, 2, 12), (2, 3, 18), (3, 4, 14),
    # Fila 1
    (5, 6, 16), (6, 7, 13), (7, 8, 17), (8, 9, 15),
    # Fila 2
    (10, 11, 14), (11, 12, 19), (12, 13, 13), (13, 14, 16),
    # Fila 3
    (15, 16, 17), (16, 17, 12), (17, 18, 15), (18, 19, 18),
    # Fila 4
    (20, 21, 13), (21, 22, 16), (22, 23, 14), (23, 24, 17),
    
    # Aristas verticales
    (0, 5, 20), (5, 10, 18), (10, 15, 22), (15, 20, 19),
    (1, 6, 18), (6, 11, 16), (11, 16, 20), (16, 21, 17),
    (2, 7, 19), (7, 12, 17), (12, 17, 18), (17, 22, 21),
    (3, 8, 16), (8, 13, 19), (13, 18, 17), (18, 23, 19),
    (4, 9, 17), (9, 14, 18), (14, 19, 20), (19, 24, 18),
    
    # Aristas diagonales/alternativas
    (1, 5, 22), (6, 2, 21), (7, 3, 20), (8, 4, 23),
    (11, 7, 19), (12, 8, 18), (13, 9, 21),
    (16, 12, 20), (17, 13, 19), (18, 14, 22),
]

for u, v, peso in aristas_red:
    grafo.agregar_arista(u, v, peso)

# Parámetros
DEPOSITO = 0          # Depósito de agua (esquina superior izquierda)
PUNTO_ENTREGA = 24    # Punto de entrega (esquina inferior derecha)

# Escenario Base
print("\n[ESCENARIO BASE]")
costo_base, camino_base, longitud_base = grafo.dijkstra(DEPOSITO, PUNTO_ENTREGA)

print(f"\n✓ Costo Total: {costo_base:.0f} unidades")
print(f"✓ Longitud de Ruta: {longitud_base} nodos")
print(f"✓ Camino Óptimo: {' → '.join(map(str, camino_base))}")
print(f"✓ Estado: Alcanzable / Óptima")

print("\n" + "="*70)
print("TABLA RESUMEN")
print("="*70)
print(f"{'Parámetro':<30} {'Valor':<20}")
print("-"*70)
print(f"{'Nodo de Origen (Depósito)':<30} {DEPOSITO:<20}")
print(f"{'Nodo de Destino (Entrega)':<30} {PUNTO_ENTREGA:<20}")
print(f"{'Costo Total':<30} {costo_base:.0f} unidades")
print(f"{'Longitud de Ruta':<30} {longitud_base} nodos")
print(f"{'Estado de la Ruta':<30} Óptima")
print("="*70)

# Visualización del escenario base
fig, ax = plt.subplots(figsize=(8, 8))

# Dibujar todos los nodos
for i in range(5):
    for j in range(5):
        nodo = i * 5 + j
        ax.plot(j, -i, 'o', color='lightblue', markersize=12, zorder=2)
        ax.text(j, -i, str(nodo), ha='center', va='center', fontsize=9, 
                fontweight='bold', zorder=3)

# Dibujar todas las aristas (muy tenues)
for u, v, peso in aristas_red:
    u_x, u_y = u % 5, -(u // 5)
    v_x, v_y = v % 5, -(v // 5)
    ax.plot([u_x, v_x], [u_y, v_y], 'gray', alpha=0.2, linewidth=0.5, zorder=1)

# Dibujar camino óptimo en rojo
for i in range(len(camino_base) - 1):
    u, v = camino_base[i], camino_base[i+1]
    u_x, u_y = u % 5, -(u // 5)
    v_x, v_y = v % 5, -(v // 5)
    ax.arrow(u_x, u_y, (v_x-u_x)*0.8, (v_y-u_y)*0.8, 
            head_width=0.2, head_length=0.15, fc='red', ec='red', 
            alpha=0.8, linewidth=2, zorder=4)
    
    # Añadir peso de la arista
    mid_x, mid_y = (u_x + v_x) / 2, (u_y + v_y) / 2
    peso_arista = grafo.pesos.get((u, v), 0)
    ax.text(mid_x+0.15, mid_y+0.15, f'{peso_arista}', fontsize=7, 
            color='darkred', fontweight='bold', zorder=5)

# Marcar inicio y fin
ax.plot(DEPOSITO % 5, -(DEPOSITO // 5), '*', color='green', markersize=30, 
       label='Depósito (Inicio)', zorder=5)
ax.plot(PUNTO_ENTREGA % 5, -(PUNTO_ENTREGA // 5), '*', color='orange', 
       markersize=30, label='Punto de Entrega (Final)', zorder=5)

ax.set_xlim(-0.8, 4.8)
ax.set_ylim(-4.8, 0.8)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_title(f'RUTA ÓPTIMA - ESCENARIO BASE\nCosto: {costo_base:.0f} u. | Longitud: {longitud_base} nodos', 
            fontsize=12, fontweight='bold', pad=20)
ax.set_xlabel('Columna', fontsize=10, fontweight='bold')
ax.set_ylabel('Fila', fontsize=10, fontweight='bold')
ax.legend(loc='upper right', fontsize=10, framealpha=0.95)

plt.tight_layout()
plt.savefig('ruta_optima_base.png', dpi=100, bbox_inches='tight')
print("\n✓ Gráfico guardado como 'ruta_optima_base.png'")
plt.show()

print("\n" + "="*70)
print("EJECUCIÓN COMPLETADA EXITOSAMENTE")
print("="*70)