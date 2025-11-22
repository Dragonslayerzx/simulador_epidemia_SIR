import streamlit as st
from modelo_sir import simulate_sir
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuración de página
st.set_page_config(layout="wide")

# CSS para ajustar botones y espaciado
st.markdown("""
    <style>
    /* Ajustar botones: texto a la izquierda */
    button[kind="secondary"] {
        text-align: left !important;
        justify-content: flex-start !important;
    }
    
    /* Ajustar el contenedor principal de columnas */
    div[data-testid="stHorizontalBlock"] {
        gap: 3rem !important;
    }
    
    /* Ajustar padding interno de cada columna */
    div[data-testid="column"] {
        padding: 0 2rem !important;
    }
    
    /* Ajustar el container general */
    .block-container {
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Estado de sesión
if "page" not in st.session_state:
    st.session_state.page = "Inicio"

# Crear columnas: sidebar y contenido principal
col_sidebar, col_main = st.columns([1, 4], gap="large")

with col_sidebar:
    st.markdown("### Navegación")
    if st.button("Inicio", use_container_width=True):
        st.session_state.page = "Inicio"
    if st.button("Simulador", use_container_width=True):
        st.session_state.page = "Simulador"
    if st.button("Información del Modelo", use_container_width=True):
        st.session_state.page = "Información"

with col_main:
    st.title("Simulador Epidemiológico SIR")
    
    # Contenido según página
    if st.session_state.page == "Inicio":
        st.header("Bienvenido al Simulador Epidemiológico SIR")
        
        st.markdown("""
        Esta aplicación permite simular y visualizar la propagación de enfermedades infecciosas 
        utilizando el modelo matemático SIR (Susceptibles-Infectados-Recuperados).
        """)
        
        st.subheader("Características principales")
        
        # Crear columnas con proporción que minimiza espacio vertical
        feature_col1, feature_col2, feature_col3 = st.columns([4, 4, 1], gap="small")
        
        with feature_col1:
            st.markdown("**Simulación interactiva**")
            st.markdown("""
            - Ajusta parámetros epidemiológicos en tiempo real
            - Visualiza resultados instantáneos o animados
            - Calcula indicadores clave automáticamente
            """)
            st.write("")
            
            st.markdown("**Modelo determinista**")
            st.markdown("""
            - Basado en ecuaciones diferenciales
            - Predice la evolución temporal de la epidemia
            - Calcula el número reproductivo básico (R₀)
            """)
        
        with feature_col2:
            st.markdown("**Validaciones integradas**")
            st.markdown("""
            - Verifica la consistencia de los parámetros
            - Proporciona alertas y advertencias
            - Ayuda contextual en cada parámetro
            """)
            st.write("")
            
            st.markdown("**Información educativa**")
            st.markdown("""
            - Explicación detallada del modelo SIR
            - Interpretación de parámetros y resultados
            - Referencias a conceptos epidemiológicos
            """)
        
        st.subheader("Cómo usar el simulador")
        
        st.markdown("""
        1. **Navega al Simulador** usando el menú lateral
        2. **Configura los parámetros**: población total, condiciones iniciales, tasas de infección y recuperación
        3. **Elige el modo de visualización**: instantáneo o tiempo real
        4. **Ejecuta la simulación** y analiza los resultados
        5. **Consulta la sección Información** para entender mejor el modelo
        """)
        
        st.subheader("Casos de uso")
        
        # Columnas para casos de uso con proporción ajustada
        use_col1, use_col2, use_col3 = st.columns([4, 4, 1], gap="small")
        
        with use_col1:
            st.markdown("**Educación**")
            st.write("Comprender conceptos básicos de epidemiología")
            st.write("")
            st.markdown("**Investigación**")
            st.write("Explorar escenarios hipotéticos de propagación")
        
        with use_col2:
            st.markdown("**Planificación**")
            st.write("Estimar recursos necesarios en sistemas de salud")
            st.write("")
            st.markdown("**Análisis de sensibilidad**")
            st.write("Evaluar el impacto de diferentes parámetros")
        
        st.write("")
        st.info("Usa el menú lateral para comenzar a explorar el simulador o conocer más sobre el modelo SIR.")




    elif st.session_state.page == "Simulador":
        st.header("Simulador SIR - Modelo Determinista")
        
        # Inicializar estado de simulación si no existe
        if "simulation_results" not in st.session_state:
            st.session_state.simulation_results = None
        
        # Parámetros de entrada con tooltips
        N = st.number_input(
            "Población total", 
            min_value=1, 
            value=1000,
            help="Número total de individuos en la población (S + I + R = N)"
        )
        
        I0 = st.number_input(
            "Infectados iniciales", 
            min_value=0, 
            value=1,
            help="Número de individuos infectados al inicio de la simulación"
        )
        
        R0 = st.number_input(
            "Recuperados iniciales", 
            min_value=0, 
            value=0,
            help="Número de individuos que ya se recuperaron al inicio (con inmunidad)"
        )
        
        beta = st.number_input(
            "Tasa de infección (beta)", 
            min_value=0.0, 
            value=0.3, 
            format="%.3f",
            help="Probabilidad de transmisión por contacto entre susceptible e infectado. Valores típicos: 0.1 - 0.5"
        )
        
        gamma = st.number_input(
            "Tasa de recuperación (gamma)", 
            min_value=0.0, 
            value=0.1, 
            format="%.3f",
            help="Tasa a la que los infectados se recuperan. Si gamma=0.1, el período infeccioso es de 10 días"
        )
        
        days = st.number_input(
            "Días de duración", 
            min_value=1, 
            value=160,
            help="Número de días que durará la simulación"
        )
        
        # Validaciones
        errores = []
        
        if I0 + R0 > N:
            errores.append("ERROR: La suma de infectados iniciales y recuperados iniciales no puede ser mayor que la población total.")
        
        if I0 == 0:
            errores.append("ADVERTENCIA: No hay infectados iniciales. La simulación no mostrará propagación de la enfermedad.")
        
        if beta == 0:
            errores.append("ADVERTENCIA: Con tasa de infección igual a cero no habrá transmisión de la enfermedad.")
        
        if gamma == 0:
            errores.append("ADVERTENCIA: Con tasa de recuperación igual a cero los infectados nunca se recuperarán.")
        
        # Mostrar errores si existen
        if errores:
            for error in errores:
                if "ERROR" in error:
                    st.error(error)
                else:
                    st.warning(error)
        
        # Calcular y mostrar R0
        if gamma > 0:
            R0_valor = beta / gamma
            st.info(f"Número reproductivo básico (R₀): {R0_valor:.2f}")
            if R0_valor < 1:
                st.write("La enfermedad se extinguirá (R₀ < 1)")
            elif R0_valor == 1:
                st.write("La enfermedad se mantendrá endémica (R₀ = 1)")
            else:
                st.write("Habrá propagación epidémica (R₀ > 1)")
        
        # Selector de modo de visualización
        modo_visualizacion = st.radio(
            "Modo de visualización:",
            ["Resultado instantáneo", "Tiempo real"],
            horizontal=True,
            help="Instantáneo muestra el resultado final. Tiempo real anima la evolución día a día."
        )
        
        # Deshabilitar botón si hay errores críticos
        tiene_errores_criticos = any("ERROR" in e for e in errores)
        
        # Limpiar resultados ANTES de mostrar botones
        if "clear_clicked" in st.session_state and st.session_state.clear_clicked:
            st.session_state.simulation_results = None
            st.session_state.clear_clicked = False
            st.rerun()
        
        # Ejecutar simulación ANTES de mostrar botones
        if "run_clicked" in st.session_state and st.session_state.run_clicked:
            st.session_state.run_clicked = False
            t, S, I, R = simulate_sir(N, I0, R0, beta, gamma, days)
            st.session_state.simulation_results = {
                't': t, 'S': S, 'I': I, 'R': R,
                'N': N, 'days': days, 'modo': modo_visualizacion
            }
            st.rerun()
        
        # Botones de control con proporción ajustada
        btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 3])
        
        with btn_col1:
            if st.button("Iniciar simulación", use_container_width=True, disabled=tiene_errores_criticos):
                st.session_state.run_clicked = True
                st.rerun()
        
        with btn_col2:
            if st.button("Limpiar resultados", use_container_width=True, disabled=(st.session_state.simulation_results is None)):
                st.session_state.clear_clicked = True
                st.rerun()
        
        # Mostrar resultados si existen
        if st.session_state.simulation_results is not None:
            results = st.session_state.simulation_results
            t = results['t']
            S = results['S']
            I = results['I']
            R = results['R']
            N = results['N']
            days = results['days']
            
            # Calcular indicadores
            peak_day = t[np.argmax(I)]
            max_infectados = np.max(I)
            porc_recuperados = (R[-1] / N) * 100
            porc_susceptibles = (S[-1] / N) * 100
            
            if modo_visualizacion == "Resultado instantáneo":
                st.subheader("Resultados de la simulación")
                st.write(f"Día del pico de infección: {peak_day:.1f}")
                st.write(f"Máximo infectados: {int(max_infectados)}")
                st.write(f"% Recuperados: {porc_recuperados:.2f}%")
                st.write(f"% Susceptibles: {porc_susceptibles:.2f}%")
                
                fig, ax = plt.subplots(figsize=(10, 5))    # ancho, alto en pulgadas
                ax.plot(t, S, label="Susceptibles")
                ax.plot(t, I, label="Infectados")
                ax.plot(t, R, label="Recuperados")
                ax.set_xlabel("Días")
                ax.set_ylabel("Número de personas")
                ax.legend()
                st.pyplot(fig)
                
            else:  # Tiempo real
                st.subheader("Simulación en tiempo real")
                chart_placeholder = st.empty()
                indicators_placeholder = st.empty()
                
                for i in range(len(t)):
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(t[:i+1], S[:i+1], label="Susceptibles")
                    ax.plot(t[:i+1], I[:i+1], label="Infectados")
                    ax.plot(t[:i+1], R[:i+1], label="Recuperados")
                    ax.set_xlim(0, days)
                    ax.set_ylim(0, N)
                    ax.legend()
                    ax.set_xlabel("Días")
                    ax.set_ylabel("Número de personas")
                    chart_placeholder.pyplot(fig)
                    plt.close(fig)
                    
                    indicators_placeholder.write(f"Día actual: {t[i]:.0f} | Infectados: {int(I[i])}")
                    
                    time.sleep(0.05)
                
                st.subheader("Resultados finales")
                st.write(f"Día del pico de infección: {peak_day:.1f}")
                st.write(f"Máximo infectados: {int(max_infectados)}")
                st.write(f"% Recuperados: {porc_recuperados:.2f}%")
                st.write(f"% Susceptibles: {porc_susceptibles:.2f}%")




    elif st.session_state.page == "Información":
        st.header("Información del modelo SIR")
        
        st.subheader("¿Qué es el modelo SIR?")
        st.markdown("""
        El modelo SIR es un modelo matemático compartimentado utilizado en epidemiología para predecir 
        la propagación de enfermedades infecciosas en una población. Fue desarrollado por Kermack y McKendrick en 1927.
        
        La población se divide en tres compartimentos:
        - **S (Susceptibles):** individuos que pueden contraer la enfermedad.
        - **I (Infectados):** individuos que han contraído la enfermedad y pueden transmitirla.
        - **R (Recuperados):** individuos que se han recuperado y adquirido inmunidad permanente.
        """)
        
        st.subheader("Ecuaciones del modelo")
        st.markdown("""
        El modelo está gobernado por un sistema de ecuaciones diferenciales ordinarias:
        """)
        
        st.latex(r"\frac{dS}{dt} = -\beta \frac{SI}{N}")
        st.latex(r"\frac{dI}{dt} = \beta \frac{SI}{N} - \gamma I")
        st.latex(r"\frac{dR}{dt} = \gamma I")
        
        st.subheader("Parámetros del modelo")
        st.markdown("""
        - **N:** Población total (constante). Es la suma de S + I + R.
        - **β (beta):** Tasa de transmisión o contacto efectivo. Representa la probabilidad de transmisión 
        por contacto entre un susceptible y un infectado por unidad de tiempo.
        - **γ (gamma):** Tasa de recuperación. Es el inverso del período infeccioso promedio. 
        Por ejemplo, si γ = 0.1, el período infeccioso es de 10 días.
        """)
        
        st.subheader("Número Reproductivo Básico (R₀)")
        st.markdown("""
        El número reproductivo básico R₀ es un concepto fundamental en epidemiología:
        """)
        
        st.latex(r"R_0 = \frac{\beta}{\gamma}")
        
        st.markdown("""
        - **R₀ < 1:** La enfermedad se extingue. Cada infectado contagia en promedio a menos de una persona.
        - **R₀ = 1:** La enfermedad se mantiene endémica (equilibrio).
        - **R₀ > 1:** La enfermedad se propaga (epidemia). Cada infectado contagia a más de una persona.
        """)
        
        st.subheader("Interpretación de resultados")
        st.markdown("""
        Al ejecutar una simulación, observe:
        - **Pico de infección:** momento de máxima carga en el sistema de salud.
        - **Porcentaje final de recuperados:** indica qué proporción de la población fue afectada.
        - **Porcentaje final de susceptibles:** población que nunca se infectó.
        - **Curva de infectados:** su forma y duración determinan la presión sobre recursos sanitarios.
        """)
        
        st.subheader("Limitaciones del modelo")
        st.markdown("""
        - Asume población homogénea y completamente mezclada.
        - No considera demografía (nacimientos, muertes naturales).
        - Inmunidad permanente (no aplica a todas las enfermedades).
        - No incluye medidas de intervención como vacunación o cuarentenas.
        - Parámetros constantes en el tiempo.
        """)
