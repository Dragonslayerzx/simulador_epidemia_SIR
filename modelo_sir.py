import numpy as np

def simulate_sir(N, I0, R0, beta, gamma, days):
    """
    Simula el modelo SIR determinista.
    
    Parámetros:
    N : int
        Población total.
    I0 : int
        Infectados iniciales.
    R0 : int
        Recuperados iniciales.
    beta : float
        Tasa de transmisión.
    gamma : float
        Tasa de recuperación.
    days : int
        Número de días a simular.
        
    Retorna:
    t : array
        Vector de tiempo.
    S : array
        Susceptibles por día.
    I : array
        Infectados por día.
    R : array
        Recuperados por día.
    """
    S0 = N - I0 - R0

    dt = 1.0  # paso de tiempo en días
    t = np.linspace(0, days, int(days/dt) + 1)
    S = np.zeros(len(t))
    I = np.zeros(len(t))
    R = np.zeros(len(t))
    
    S[0] = S0
    I[0] = I0
    R[0] = R0
    
    for i in range(1, len(t)):
        dS = -beta * S[i-1] * I[i-1] / N
        dI = beta * S[i-1] * I[i-1] / N - gamma * I[i-1]
        dR = gamma * I[i-1]
        S[i] = S[i-1] + dS * dt
        I[i] = I[i-1] + dI * dt
        R[i] = R[i-1] + dR * dt
    return t, S, I, R
