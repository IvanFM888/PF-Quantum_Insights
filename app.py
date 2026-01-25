import streamlit as st
import pandas as pd
import pickle
import os
from sqlalchemy import create_engine

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Quantum Insights - Híbrido", layout="wide")

# URL de Supabase (Modo Túnel - Puerto 6543)
URI_SUPABASE = "postgresql://postgres.yolftbsmdognqlwfeaon:ProyectoFinal2025@aws-0-us-west-2.pooler.supabase.com:6543/postgres"

@st.cache_resource
def init_connection():
    try:
        return create_engine(URI_SUPABASE, pool_pre_ping=True)
    except Exception as e:
        st.error(f"Error conectando a la nube: {e}")
        st.stop()

engine = init_connection()

# --- 2. CARGA DE MODELOS ---
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    ruta_csv = os.path.join(base_dir, "databases", "lista_productos_completa.csv")
    ruta_nlp = os.path.join(base_dir, "modelos_entrenados", "modelo_recomendacion_npl.pkl")
    ruta_svd = os.path.join(base_dir, "modelos_entrenados", "modelo_svd_similitud.pkl")
    
    if not os.path.exists(ruta_csv):
        st.error(f"❌ No encuentro el CSV en: {ruta_csv}")
        st.stop()
    df = pd.read_csv(ruta_csv)
    
    matriz_nlp = None
    if os.path.exists(ruta_nlp):
        with open(ruta_nlp, 'rb') as f:
            matriz_nlp = pickle.load(f)
    
    matriz_svd = None
    if os.path.exists(ruta_svd):
        with open(ruta_svd, 'rb') as f:
            matriz_svd = pickle.load(f)
            
    return df, matriz_nlp, matriz_svd

try:
    df_catalogo, modelo_nlp, modelo_svd = load_models()
except Exception as e:
    st.error(f"Error crítico al cargar: {e}")
    st.stop()

# --- 3. LÓGICA ---

def obtener_detalles_db(lista_nombres):
    if not lista_nombres: return pd.DataFrame()
    nombres_limpios = [str(n).replace("'", "''") for n in lista_nombres]
    texto_sql = "'" + "','".join(nombres_limpios) + "'"
    query = f"SELECT * FROM productos WHERE productname IN ({texto_sql})"
    try:
        return pd.read_sql(query, engine)
    except:
        return pd.DataFrame()

def recomendar_nlp(producto_nombre, top_n=3):
    if modelo_nlp is None: return []
    try:
        idx = df_catalogo[df_catalogo['ProductName'] == producto_nombre].index[0]
        scores = list(enumerate(modelo_nlp[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        indices = [i[0] for i in scores[1:top_n+1]]
        return df_catalogo['ProductName'].iloc[indices].tolist()
    except:
        return []

def recomendar_svd(producto_nombre, top_n=3):
    if modelo_svd is None: return []
    try:
        col_id = 'product_id'
        if col_id not in df_catalogo.columns:
             if 'ProductId' in df_catalogo.columns: col_id = 'ProductId'
        
        filtro = df_catalogo[df_catalogo['ProductName'] == producto_nombre]
        if filtro.empty: return []
        
        prod_id = filtro[col_id].values[0]
        
        if isinstance(modelo_svd, pd.DataFrame):
            if prod_id in modelo_svd.index:
                similares = modelo_svd.loc[prod_id].sort_values(ascending=False)
                top_ids = similares.index[1:top_n+1].tolist()
                nombres = df_catalogo[df_catalogo[col_id].isin(top_ids)]['ProductName'].tolist()
                return nombres
        else:
             idx = df_catalogo[df_catalogo['ProductName'] == producto_nombre].index[0]
             scores = list(enumerate(modelo_svd[idx]))
             scores = sorted(scores, key=lambda x: x[1], reverse=True)
             indices = [i[0] for i in scores[1:top_n+1]]
             return df_catalogo['ProductName'].iloc[indices].tolist()
    except:
        return []

# --- 4. INTERFAZ GRÁFICA (LIMPIA) ---

st.title("🤖 Quantum Insights")
st.markdown("Sistema de Recomendación Inteligente")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    tipo_modelo = st.radio("Estrategia:", ["Contenido (NLP)", "Patrones (SVD)"])
    top_k = st.slider("Resultados:", 1, 6, 3)

col1, col2 = st.columns([1, 2])

with col1:
    st.info("🔎 **Buscador**")
    opciones = df_catalogo['ProductName'].unique()
    producto = st.selectbox("Selecciona un producto:", opciones)
    
    if st.button("Buscar Similares", type="primary"):
        st.session_state['buscar'] = True

with col2:
    if st.session_state.get('buscar'):
        st.subheader(f"Resultados usando: {tipo_modelo}")
        
        with st.spinner('Analizando datos...'):
            recomendados = []
            
            if "NLP" in tipo_modelo:
                recomendados = recomendar_nlp(producto, top_k)
            else:
                recomendados = recomendar_svd(producto, top_k)

            if recomendados:
                df_detalles = obtener_detalles_db(recomendados)
                
                if not df_detalles.empty:
                    items = df_detalles.to_dict(orient='records')
                    
                    # Grid de 2 columnas
                    grid_cols = st.columns(2)
                    
                    for i, item in enumerate(items):
                        with grid_cols[i % 2]:
                            cat = item.get('category') or item.get('Category') or "General"
                            nom = item.get('productname') or item.get('ProductName') or "Producto"
                            marca = item.get('brand') or item.get('Brand') or ""
                            
                            # --- TARJETA SOLO TEXTO (Sin st.image) ---
                            with st.container(border=True):
                                # Usamos un Emoji grande como "Logo" del producto
                                st.markdown(f"## 📦") 
                                st.markdown(f"#### {nom}")
                                st.markdown(f"**Categoría:** {cat}")
                                if marca:
                                    st.caption(f"🏷️ Marca: {marca}")
                                st.success("Recomendado 100%")
                else:
                    st.warning("Se encontraron recomendaciones, pero sin detalles en BD.")
                    for prod in recomendados:
                        st.info(f"🔹 {prod}")
            else:
                st.error("No hay recomendaciones disponibles para este producto/modelo.")