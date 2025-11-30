import numpy as np

class Agente:
    def __init__(self, x, y, estado):
        self.x = x
        self.y = y
        self.estado = estado  # 'S', 'I', 'R'

class ModeloAgentes:
    def __init__(self, num_agentes, tamaño, radio_contagio, beta, gamma):
        self.num_agentes = num_agentes
        self.tamaño = tamaño
        self.radio_contagio = radio_contagio
        self.beta = beta
        self.gamma = gamma
        self.agentes = []
        self._inicializar_agentes()
    
    def _inicializar_agentes(self):
        # Crear agentes en posiciones aleatorias
        for _ in range(self.num_agentes):
            x = np.random.uniform(0, self.tamaño)
            y = np.random.uniform(0, self.tamaño)
            # Estado inicial: la mayoría S, algunos I, pocos R
            if np.random.random() < 0.1:
                estado = 'I'
            elif np.random.random() < 0.05:
                estado = 'R'
            else:
                estado = 'S'
            self.agentes.append(Agente(x, y, estado))
    
    def mover_agentes(self):
        for agente in self.agentes:
            agente.x += np.random.uniform(-1, 1)
            agente.y += np.random.uniform(-1, 1)
            # Mantener dentro del área
            agente.x = np.clip(agente.x, 0, self.tamaño)
            agente.y = np.clip(agente.y, 0, self.tamaño)
    
    def contagiar(self):
        for i, agente in enumerate(self.agentes):
            if agente.estado == 'I':
                for j, otro in enumerate(self.agentes):
                    if i != j and otro.estado == 'S':
                        distancia = np.sqrt((agente.x - otro.x)**2 + (agente.y - otro.y)**2)
                        if distancia < self.radio_contagio:
                            if np.random.random() < self.beta:
                                otro.estado = 'I'
    
    def recuperar(self):
        for agente in self.agentes:
            if agente.estado == 'I' and np.random.random() < self.gamma:
                agente.estado = 'R'
    
    def obtener_estado(self):
        return [(agente.x, agente.y, agente.estado) for agente in self.agentes]
