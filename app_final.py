import streamlit as st
import pandas as pd
import pickle
import random
import numpy as np
np.random.seed(42)


# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Quantum Insights Store",
    layout="wide"
)

st.markdown("""
<style>
/* 1. Importar Roboto Flex desde Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,100..1000&display=swap');

/* 2. Aplicarla a todo el cuerpo de la página */
html, body, [class*="css"] {
    font-family: 'Roboto Flex' !important;
}
.stApp {
    background-color: #f4f4f4 !important;
    font-family: 'Roboto Flex', sans-serif !important;
            
/* Opcional: Si quieres que los títulos (h1, h2, h3) se vean aún más modernos */
h1, h2, h3 {
    font-family: 'Roboto Flex', sans-serif !important;
    font-weight: 700 !important; /* Más negrita para encabezados */
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ============================================================
   PASO 1: APLICAR ESTILO A *TODOS* LOS DROPDOWNS (GLOBAL)
   (Esto afectará al de Cantidad, pero también a los del Sidebar... espera al paso 2)
   ============================================================ */
div[data-baseweb="select"] > div {
    background-color: #f4f4f4 !important;
    border: 2px solid #e2ddd9 !important;
    color: black !important;
    border-radius: 10px !important;
    height: 40px !important;       /* Altura pequeña para el de Cantidad */
    min-height: 40px !important;
    width: 5em !important;
    font-size: 14px !important;    /* Letra pequeña */
}

/* ============================================================
   PASO 2: RESTAURAR LOS DEL SIDEBAR (SOBREESCRIBIR)
   (Aquí le decimos: "Oye, pero si estás en el sidebar, vuelve a ser normal")
   ============================================================ */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;  /* Fondo blanco original */
    border: 1px solid #d6d6d6 !important; /* Borde gris sutil original */
    color: inherit !important;             /* Color texto original */
    height: auto !important;               /* Altura automática */
    min-height: 38px !important;           /* Altura estándar */
    border-radius: 4px !important;         /* Bordes normales */
    width: 100% !important;
}

/* Opcional: Arreglar la flechita también */
div[data-baseweb="select"] svg { fill: #a8a39d !important; } /* Todas rojas */
section[data-testid="stSidebar"] div[data-baseweb="select"] svg { fill: gray !important; } /* Sidebar gris */

</style>
""", unsafe_allow_html=True)




# ===============================
# CARGA DE DATOS Y MODELO
# ===============================
@st.cache_resource
def cargar_modelos():
    with open("modelos_entrenados/modelo_recomendacion_cc.pkl", "rb") as f:
        modelo_cc = pickle.load(f)

    with open("modelos_entrenados/modelo_recomendacion_nlp.pkl", "rb") as f:
        modelo_nlp = pickle.load(f)

    return modelo_cc, modelo_nlp
@st.cache_data
def cargar_productos():
    return pd.read_csv("databases/products.csv")

modelo_cc, modelo_nlp = cargar_modelos()
df_products = cargar_productos()
df_products["modelo"] = np.where(np.random.rand(len(df_products)) < 0.5, "CC", "NLP")



st.sidebar.title("Navegación")

# Opción A: Usar st.sidebar.radio para cambiar de "Página"
pagina = st.sidebar.radio("Ir a:", ["🛍️ Tienda", "📖 Introduccion - Guia"])

st.sidebar.markdown("---") # Separador


def vista_app():
    # ===============================
    # SIDEBAR
    # ===============================
    st.sidebar.title("🔍︎ Filtros")

    categoria = st.sidebar.selectbox(
        "Categoría",
        sorted(df_products["Category"].unique())
    )

    df_cat = df_products[df_products["Category"] == categoria]

    opciones_productos = (df_cat["ProductName"] + " - " + df_cat["product_id"].astype(str)).unique()
    producto_seleccionado = st.sidebar.selectbox(
        "Producto",
        opciones_productos
    )
    producto = df_cat[
        (df_cat["ProductName"] + " - " + df_cat["product_id"].astype(str)) == producto_seleccionado
    ].iloc[0]

    product_id = producto["product_id"]
    modelo = producto["modelo"]

    # ===============================
    # CONTENIDO PRINCIPAL
    # ===============================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

    .logo-tech {
        font-family: 'Orbitron', sans-serif;
        font-size: 45px;
        font-weight: 700;
        color: #80bc96; /* Rojo Streamlit, o ponle White */
        text-align: left;
        letter-spacing: 2px; /* Separar letras le da elegancia */
        padding-bottom: 2em;
    }
    </style>
    <div class="logo-tech">NexStore</div>
    """, unsafe_allow_html=True)
    col_img, col_info = st.columns([1, 2], gap="xlarge")

    with col_img:
        st.markdown(
            f"""
            <div style="
                display: block;
                margin: 0 auto; 
                width: fit-content; 
                box-shadow: 0 6px 6px rgba(0,0,0,0.2);
                border-radius: 10px;
                background-color: white; /* Importante para que la sombra resalte */
            ">
                <img src="{producto['Image_Url']}" width="500" style="border-radius: 10px; padding: 20px;">
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_info:
        if modelo == "NLP":
            st.markdown(f"""<button style="
                background-color: #F9EBEB; 
                border: none;
                color: #A66E6E;
                padding: 15px 15px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                Producto no disponible 😞
            </button>""", unsafe_allow_html=True)
        st.markdown(f"<h3> {producto['ProductName']}</h3>", unsafe_allow_html=True)
        st.markdown(f"**Marca:** {producto['Brand']}")
        st.markdown(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        )
        st.markdown(f"### 💲{producto['Price']} USD")

        cantidad = st.selectbox(
            "Cantidad",
            list(range(1, 11))
        )

        # st.button("🛒 Agregar al carrito")
        st.markdown(f"""<button style="
            background-color: #f4f4f4; 
            border: none;
            color: #000000;
            padding: 15px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 10px; /* <--- AQUÍ ESTÁN TUS BORDES REDONDOS */
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* Sombrita elegante */
        ">
            🛒 Agregar al carrito
        </button>""", unsafe_allow_html=True)

    # ===============================
    # RECOMENDACIONES
    # ===============================
    st.markdown("---")

    recs_cc = modelo_cc.recomendar(product_id, top_n=3)
    recs_nlp = modelo_nlp.recomendar(product_id, top_n=3)



    if modelo == "CC":
        st.markdown(f"<h1 style='font-size: 2em;'> Productos relacionados con {producto['ProductName']}</h1>", unsafe_allow_html=True)
        st.markdown("<div style = 'height: 4em'> </div>", unsafe_allow_html=True)
        if len(recs_cc) == 0:
            st.info("No se encontraron productos relacionados.")
        else:
            cols = st.columns(3, gap="small")
            for col, pid in zip(cols, recs_cc):
                prod = df_products[df_products["product_id"] == pid].iloc[0]
                with col:
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center;box-shadow: 0 6px 6px rgba(0,0,0,0.2);border-radius: 10px;">
                            <img src="{prod['Image_Url']}" width="300" style="border-radius: 10px;padding:20px;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(f"<div style ='text-align: center; padding:30px'>{prod['ProductName']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='font-size: 2em;'> Este producto no esta disponible actualmente, te sugerimos estos en cambio.</h1>", unsafe_allow_html=True)
        st.markdown("<div style = 'height: 4em'> </div>", unsafe_allow_html=True)
        if len(recs_nlp) == 0:
            st.info("No se encontraron productos relacionados.")
        else:
            cols = st.columns(3, gap="small")
            for col, pid in zip(cols, recs_nlp):
                prod = df_products[df_products["product_id"] == pid].iloc[0]
                with col:
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center;box-shadow: 0 6px 6px rgba(0,0,0,0.2);border-radius: 10px;">
                            <img src="{prod['Image_Url']}" width="300" style="border-radius: 10px;padding:20px;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(f"<div style ='text-align: center; padding:30px'>{prod['ProductName']}</div>", unsafe_allow_html=True)




def vista_guia_uso():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>Introduccion - Guia NexStore App</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; margin-bottom: 30px;'>
        <p style='font-size: 18px; color: #555;'>
            Bienvenido al módulo de introducción/guia de <b>NexStore</b>. 
            Nuestro sistema de recomendación detecta el estado del inventario para aplicar la estrategia de recomendación más efectiva en cada caso.
            No usamos un solo modelo al azar, sino que activamos el modelo correcto dependiendo de si podemos vender el producto o si necesitamos ofrecer una alternativa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🧠 Modelo NLP (Sustitutos)", "🔗 Modelo CC (Complementarios)", "⚙️ Lógica de la Simulación"])

    with tab1:
        st.markdown("### 🗣️ NLP: Procesamiento de Lenguaje Natural")
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown("<div style='font-size: 40px; text-align: center;'>📄🔍</div>", unsafe_allow_html=True)
        with col_b:
            st.info("**Rol:** El 'Salvavidas' de la venta.")
        
        st.markdown("""
        **¿Cómo se entrena?**
        El modelo utiliza algoritmos de **Vectorización (TF-IDF)** para transformar los nombres de los productos en coordenadas numéricas dentro de un espacio matemático. Luego, aplica la **Similitud del Coseno** para medir el ángulo entre estos vectores. Si dos productos comparten palabras clave importantes (como "Cebolla"), sus vectores estarán casi alineados, indicando que son matemáticamente "gemelos".
        
        **¿Cuál es su objetivo?**
        Evitar que el cliente se vaya con las manos vacías. Si el cliente busca una "Cebolla Roja" y no hay, este modelo analiza el texto y le ofrece una "Cebolla Blanca" o "Cebolla Larga". Busca similitud pura para ofrecer un **sustituto**.
        """)

    with tab2:
        st.markdown("### 🛒 CC: Modelo de Concurrencia")
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown("<div style='font-size: 40px; text-align: center;'>🤝🛍️</div>", unsafe_allow_html=True)
        with col_b:
            st.info("**Rol:** El 'Potenciador' del carrito.")
        
        st.markdown("""
                    
        **¿Cómo se entrena?**
        El sistema procesa miles de transacciones históricas para construir una **Matriz de Co-ocurrencia**. Matemáticamente, calcula la probabilidad condicional de que dos productos aparezcan juntos en el mismo ticket. Si el Producto A y el Producto B se compran juntos frecuentemente (más allá de la casualidad), el algoritmo crea un vínculo fuerte entre ellos.
        
        **¿Cuál es su objetivo?**
        Aprovechar la intención de compra para ofrecer productos **complementarios**. Si el cliente va a llevar "Pan", el modelo sabe por el historial de transacciones que debería ofrecerle "Leche" o "Huevos", aunque no se parezcan en nombre.
        """)

    with tab3:
        st.header("🔄 Simulación de Escenarios: Disponibilidad Inteligente")
        
        st.markdown("""
        Para efectos de esta demostración técnica, hemos configurado una simulación controlada que divide el catálogo en dos estados:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 1px solid #c8e6c9;'>
                <h4 style='color: #2e7d32; text-align: center;'>Escenario A: Producto Disponible</h4>
                <p style='text-align: center; font-size: 2em;'>✅</p>
                <p><b>Acción:</b> El sistema usa el <b>Modelo CC</b>.</p>
                <p><b>Lógica:</b> "Ya que vas a llevar esto, lleva también esto otro que combina bien".</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style='background-color: #ffebee; padding: 15px; border-radius: 10px; border: 1px solid #ffcdd2;'>
                <h4 style='color: #c62828; text-align: center;'>Escenario B: Producto Agotado</h4>
                <p style='text-align: center; font-size: 2em;'>❌</p>
                <p><b>Acción:</b> El sistema usa el <b>Modelo NLP</b>.</p>
                <p><b>Lógica:</b> "Lo sentimos, no tenemos X, pero este producto Y es casi idéntico".</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        **Nota Técnica:** En este prototipo, el 50% de los productos se marcan aleatoriamente como "Disponibles" y el otro 50% como "No Disponibles" para que puedas probar ambos comportamientos (Sustitución vs. Complementariedad) en tiempo real.
        """)

if pagina == "🛍️ Tienda":
    vista_app()
elif pagina == "📖 Introduccion - Guia":
    vista_guia_uso()