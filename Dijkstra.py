import heapq
import sys


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, edges):
        self.vertices[name] = edges

    def shortest_path(self, start, finish):
        distances = {}  # Distanza dallo start al nodo considerato
        previous = {}  # Nodo precedente nel percorso ottimale dalla sorgente
        nodes = []  # Coda di priorità per tutti i nodi del Grafo

        for vertex in self.vertices:
            if vertex == start:  # Mette il nodo sorgente alla distanza 0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]  # Vertice in "nodes" con la distanza minore in "distances"
            if smallest == finish:  # Se il nodo più vicino è il target allora fine
                path = []
                while previous[smallest]:  # Torna indietro fino a che non torna alla radice
                    path.append(smallest)
                    smallest = previous[smallest]
                path.reverse()
                return path
            if distances[smallest] == sys.maxsize:  # Tutti i vertici rimanenti sono inaccessibili dalla sorgente
                break

            for neighbor in self.vertices[smallest]:  # Guarda tutti i vicini del nodo considerato
                alt = distances[smallest] + self.vertices[smallest][neighbor]
                if alt < distances[neighbor]:  # Se c'è un nuovo percorso più breve aggiorna la coda di priorità
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)
        return distances

    def __str__(self):
        return str(self.vertices)


if __name__ == '__main__':
    g = Graph()

    vertex = {}
    for i in range(2, 8):
        tmp = str(i)
        vertex[tmp] = i*2
    g.add_vertex('1', {'2': 7, '3': 8})
    g.add_vertex('2', {'1': 7, '6': 2})
    g.add_vertex('3', {'1': 8, '6': 6, '7': 4})
    g.add_vertex('4', {'6': 8})
    g.add_vertex('5', {'8': 1})
    g.add_vertex('6', {'2': 2, '3': 6, '4': 8, '7': 9, '8': 3})
    g.add_vertex('7', {'3': 4, '6': 9})
    g.add_vertex('8', {'5': 1, '6': 3})
    print(g.shortest_path('1', '8'))
