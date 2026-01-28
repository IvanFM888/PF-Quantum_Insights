import streamlit as st
import pandas as pd
import pickle
import random

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
def cargar_modelo_cc():
    with open("modelos_entrenados/modelo_recomendacion_cc.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def cargar_productos():
    return pd.read_csv("databases/products.csv")

modelo_cc = cargar_modelo_cc()
df_products = cargar_productos()


# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("🛍️ Filtros")

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
st.markdown(f"<h1 style='font-size: 2em;'> Productos relacionados con {producto['ProductName']}</h1>", unsafe_allow_html=True)

st.markdown("<div style = 'height: 4em'> </div>", unsafe_allow_html=True)

recs = modelo_cc.recomendar(producto["product_id"], top_n=3)

if len(recs) == 0:
    st.info("No se encontraron productos relacionados.")
else:
    cols = st.columns(3, gap="small")
    for col, pid in zip(cols, recs):
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
