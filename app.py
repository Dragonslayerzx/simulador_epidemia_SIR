import streamlit as st
from modelo_sir import simulate_sir
from modelo_agentes import ModeloAgentes
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
    
    /* KPI CARDS - MEJORADO: gap mínimo solo para métricas */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) {
        gap: 0.75rem !important;
    }
    
    /* Tarjetas KPI estilo dashboard - OPTIMIZADO */
    div[data-testid="stMetric"] {
        background-color: #0f172a;
        padding: 1.2rem 1rem !important;
        border-radius: 0.75rem;
        border: 1px solid #1e293b;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        height: 120px !important;        /* altura fija uniforme */
        width: 100% !important;          /* ocupa todo su contenedor */
        max-width: none !important;      /* elimina restricción anterior */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
    }
    
    div[data-testid="stMetric"] > label {
        color: #e5e7eb !important;
        font-weight: 600;
        font-size: 0.9rem !important;
        margin-bottom: 0.25rem;
        text-align: center;
    }
    
    div[data-testid="stMetric"] span[data-testid="stMetricValue"] {
        color: #f9fafb !important;
        font-weight: 700;
        font-size: 1.5rem !important;
        margin-top: 0.25rem;
        text-align: center;
    }
    
    /* Elimina regla conflictiva anterior */
    div[data-testid="column"] > div:has(div[data-testid="stMetric"]) {
        display: flex !important;
        flex-direction: column !important;
    }
    
    /* Responsive: en pantallas pequeñas, stack vertical */
    @media (max-width: 1200px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex-basis: 100% !important;
        }
        div[data-testid="stMetric"] {
            height: 100px !important;  /* más compacto en móvil */
        }
    }
    
    /* Colores específicos para cada métrica - CORREGIDO con nth-of-type */
    div[data-testid="stMetric"]:nth-of-type(1) span[data-testid="stMetricValue"] {
        color: #f97316 !important; /* Naranja para día pico */
    }
    div[data-testid="stMetric"]:nth-of-type(2) span[data-testid="stMetricValue"] {
        color: #f59e0b !important; /* Amarillo para máximo infectados */
    }
    div[data-testid="stMetric"]:nth-of-type(3) span[data-testid="stMetricValue"] {
        color: #22c55e !important; /* Verde para % recuperados */
    }
    div[data-testid="stMetric"]:nth-of-type(4) span[data-testid="stMetricValue"] {
        color: #38bdf8 !important; /* Azul para % susceptibles */
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
    if st.button("Modelo de agentes", use_container_width=True):
        st.session_state.page = "Modelo de agentes"

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

                # Fila de KPIs tipo dashboard
                kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

                with kpi_col1:
                    st.metric(
                        label="Día pico de infección",
                        value=f"{peak_day:.1f}",
                        help="Momento en el que se alcanza el número máximo de infectados simultáneos."
                    )

                with kpi_col2:
                    st.metric(
                        label="Máximo infectados",
                        value=f"{int(max_infectados):,}".replace(",", " "),
                        help="Cantidad máxima de personas infectadas al mismo tiempo."
                    )

                with kpi_col3:
                    st.metric(
                        label="% Recuperados al final",
                        value=f"{porc_recuperados:.2f} %",
                        help="Porcentaje de la población que acaba en el compartimento Recuperados."
                    )

                with kpi_col4:
                    st.metric(
                        label="% Susceptibles al final",
                        value=f"{porc_susceptibles:.2f} %",
                        help="Porcentaje de la población que nunca se infectó."
                    )

                # Card para la gráfica
                with st.container(border=True):
                    st.markdown("**Evolución temporal S, I, R**")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(t, S, label="Susceptibles", color="#38bdf8", linewidth=3)
                    ax.plot(t, I, label="Infectados", color="#f97316", linewidth=3)
                    ax.plot(t, R, label="Recuperados", color="#22c55e", linewidth=3)
                    ax.set_facecolor("#020617")
                    fig.patch.set_facecolor("#020617")
                    ax.tick_params(colors="#e5e7eb")
                    ax.spines["bottom"].set_color("#475569")
                    ax.spines["left"].set_color("#475569")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.set_xlabel("Días", color="#e5e7eb", fontsize=12)
                    ax.set_ylabel("Número de personas", color="#e5e7eb", fontsize=12)
                    ax.grid(alpha=0.2, color="#64748b")
                    legend = ax.legend(frameon=True, fancybox=True, shadow=True)
                    legend.get_frame().set_facecolor("#1e293b")
                    for text in legend.get_texts():
                        text.set_color("#e5e7eb")
                    plt.tight_layout()
                    st.pyplot(fig)

                
            else:  # Tiempo real
                st.subheader("Simulación en tiempo real")
                
                # Placeholder para KPIs arriba de la gráfica
                kpis_placeholder = st.empty()
                
                # Animación
                chart_placeholder = st.empty()
                
                # Placeholder para información visual debajo de la gráfica
                info_placeholder = st.empty()
                
                for i in range(len(t)):
                    fig, ax = plt.subplots(figsize=(10, 4))

                    # Estilo de la gráfica (colores y diseño idéntico)
                    ax.plot(t[:i+1], S[:i+1], label="Susceptibles", color="#38bdf8", linewidth=3)
                    ax.plot(t[:i+1], I[:i+1], label="Infectados", color="#f97316", linewidth=3)
                    ax.plot(t[:i+1], R[:i+1], label="Recuperados", color="#22c55e", linewidth=3)

                    # Fondo oscuro
                    ax.set_facecolor("#020617")
                    fig.patch.set_facecolor("#020617")

                    # Color de los ejes, ticks y texto
                    ax.tick_params(colors="#e5e7eb")
                    ax.spines["bottom"].set_color("#475569")
                    ax.spines["left"].set_color("#475569")
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)
                    ax.set_xlabel("Días", color="#e5e7eb")
                    ax.set_ylabel("Número de personas", color="#e5e7eb")

                    # Grid suave
                    ax.grid(alpha=0.2, color="#64748b")

                    # Leyenda estilizada
                    legend = ax.legend(frameon=True, fancybox=True, shadow=True)
                    legend.get_frame().set_facecolor("#1e293b")
                    for text in legend.get_texts():
                        text.set_color("#e5e7eb")

                    # Rango de ejes
                    ax.set_xlim(0, days)
                    ax.set_ylim(0, N)

                    chart_placeholder.pyplot(fig)
                    plt.close(fig)

                    
                    # Tarjeta visual debajo de la gráfica, más compacta
                    with info_placeholder.container():
                        st.markdown(
                            f"""
                            <div style="background-color:#0f172a; border-radius:0.75rem; border:1px solid #1e293b; padding:1rem; margin-top:0.5rem; display:flex; justify-content:center; align-items:center; gap:1rem; font-size:1.1rem;">
                                <span style="color:#e5e7eb;">Día actual: <span style="color:#22c55e; font-weight:700;">{int(t[i])}</span></span>
                                <span style="color:#e5e7eb;">| Infectados: <span style="color:#f59e0b; font-weight:700;">{int(I[i])}</span></span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    time.sleep(0.05)
                    
                    if i == len(t) - 1:
                        with kpis_placeholder.container():
                            st.subheader("Resultados finales")
                            
                            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
                            
                            with kpi_col1:
                                st.metric(
                                    label="Día pico de infección",
                                    value=f"{peak_day:.1f}",
                                    help="Momento en el que se alcanza el número máximo de infectados simultáneos."
                                )
                            
                            with kpi_col2:
                                st.metric(
                                    label="Máximo infectados",
                                    value=f"{int(max_infectados):,}".replace(",", "."),
                                    help="Cantidad máxima de personas infectadas al mismo tiempo."
                                )
                            
                            with kpi_col3:
                                st.metric(
                                    label="% Recuperados al final",
                                    value=f"{porc_recuperados:.1f}%",
                                    help="Porcentaje de la población que acaba en el compartimento Recuperados."
                                )
                            
                            with kpi_col4:
                                st.metric(
                                    label="% Susceptibles al final",
                                    value=f"{porc_susceptibles:.1f}%",
                                    help="Porcentaje de la población que nunca se infectó."
                                )

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

    elif st.session_state.page == "Modelo de agentes":
        st.header("Simulador de Agentes - Modelo Individualizado")

        # Parámetros (comparables con SIR y específicos de agentes)
        num_agentes = st.slider("Número de agentes", 10, 1000, 100)
        tamaño = st.slider("Tamaño del área", 10, 100, 50)
        radio_contagio = st.slider("Radio de contagio", 0.1, 5.0, 1.0)
        beta = st.slider("Probabilidad de contagio (β)", 0.0, 1.0, 0.3)
        gamma = st.slider("Probabilidad de recuperación (γ)", 0.0, 1.0, 0.1)
        dias = st.number_input("Días de simulación", min_value=1, value=100, step=1, help="Número de pasos (días) para la simulación")

        if st.button("Iniciar simulación"):
            # Inicializar modelo de agentes
            modelo_agentes = ModeloAgentes(num_agentes, tamaño, radio_contagio, beta, gamma)

            # Placeholder para gráfica y métricas
            chart_placeholder = st.empty()

            # Listas para registrar métricas por día
            infectados_por_dia = []

            # Simulación iterativa
            for paso in range(dias):
                modelo_agentes.mover_agentes()
                modelo_agentes.contagiar()
                modelo_agentes.recuperar()

                # Registrar número de infectados en el paso actual
                estados = modelo_agentes.obtener_estado()
                infecc = sum(1 for s in estados if s[2] == 'I')
                infectados_por_dia.append(infecc)

                # Mostrar gráfica con estilo oscuro
                x = [e[0] for e in estados]
                y = [e[1] for e in estados]
                c = [e[2] for e in estados]

                # Colores alineados con SIR puro
                colores = []
                for estado in c:
                    if estado == 'S':
                        colores.append('#38bdf8')  # Azul claro
                    elif estado == 'I':
                        colores.append('#f97316')  # Naranja
                    else:
                        colores.append('#22c55e')  # Verde

                fig, ax = plt.subplots(figsize=(10, 4))
                ax.set_facecolor("#020617")
                fig.patch.set_facecolor("#020617")
                ax.scatter(x, y, c=colores, s=100)
                ax.tick_params(colors="#e5e7eb")
                ax.spines["bottom"].set_color("#475569")
                ax.spines["left"].set_color("#475569")
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.set_xlabel("X", color="#e5e7eb")
                ax.set_ylabel("Y", color="#e5e7eb")
                ax.set_xlim(0, tamaño)
                ax.set_ylim(0, tamaño)
                ax.set_title(f"Paso de simulación: {paso + 1}", color="#e5e7eb")
                ax.grid(alpha=0.2, color="#64748b")
                chart_placeholder.pyplot(fig)
                plt.close(fig)

                time.sleep(0.1)

            # Calcular métricas finales y avanzadas
            states_final = modelo_agentes.obtener_estado()
            num_s = sum(1 for s in states_final if s[2] == 'S')
            num_i = sum(1 for s in states_final if s[2] == 'I')
            num_r = sum(1 for s in states_final if s[2] == 'R')
            total = len(states_final)
            max_infectados = max(infectados_por_dia)
            dia_pico = infectados_por_dia.index(max_infectados) + 1
            porcentaje_max_infectados = 100 * max_infectados / total
            porcentaje_final_s = 100 * num_s / total
            porcentaje_final_i = 100 * num_i / total
            porcentaje_final_r = 100 * num_r / total

            # Mostrar resultados finales y avanzados
            st.markdown("---")
            st.markdown("<h3 style='color:#f9fafb; text-align:center;'>Resultados finales</h3>", unsafe_allow_html=True)

            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            with kpi_col1:
                st.markdown(f"""
                    <div style="background-color:#0f172a; border-radius:0.75rem; border:1px solid #1e293b; padding:1rem; margin:0.5rem; text-align:center; box-shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                        <p style="margin:0; font-size:1rem; font-weight:600; color:#e5e7eb;">Susceptibles</p>
                        <p style="margin:0; font-size:1.8rem; font-weight:700; color:#38bdf8;">{num_s}<br><span style="font-size:1rem;">({porcentaje_final_s:.1f}%)</span></p>
                    </div>
                    """, unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"""
                    <div style="background-color:#0f172a; border-radius:0.75rem; border:1px solid #1e293b; padding:1rem; margin:0.5rem; text-align:center; box-shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                        <p style="margin:0; font-size:1rem; font-weight:600; color:#e5e7eb;">Infectados</p>
                        <p style="margin:0; font-size:1.8rem; font-weight:700; color:#f97316;">{num_i}<br><span style="font-size:1rem;">({porcentaje_final_i:.1f}%)</span></p>
                    </div>
                    """, unsafe_allow_html=True)
            with kpi_col3:
                st.markdown(f"""
                    <div style="background-color:#0f172a; border-radius:0.75rem; border:1px solid #1e293b; padding:1rem; margin:0.5rem; text-align:center; box-shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                        <p style="margin:0; font-size:1rem; font-weight:600; color:#e5e7eb;">Recuperados</p>
                        <p style="margin:0; font-size:1.8rem; font-weight:700; color:#22c55e;">{num_r}<br><span style="font-size:1rem;">({porcentaje_final_r:.1f}%)</span></p>
                    </div>
                    """, unsafe_allow_html=True)

            # Métricas avanzadas
            st.markdown("### Métricas avanzadas")
            st.metric("Número máximo de infectados", max_infectados, f"{porcentaje_max_infectados:.1f}%")
            st.metric("Día del pico de infección", dia_pico)
            st.markdown("---")
            kpi_col4, kpi_col5 = st.columns(2)
            with kpi_col4:
                st.metric("Días simulados", dias)
            with kpi_col5:
                st.metric("Agentes totales", total)




