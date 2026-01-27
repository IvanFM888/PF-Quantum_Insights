import streamlit as st
import pandas as pd
import pickle
import os
from sqlalchemy import create_engine

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Quantum Insights - Híbrido", layout="wide")

# URL de Supabase
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
    
    # Rutas de archivos
    ruta_csv = os.path.join(base_dir, "databases", "lista_productos_completa.csv")
    ruta_nlp = os.path.join(base_dir, "modelos_entrenados", "modelo_recomendacion_npl.pkl")
    ruta_svd = os.path.join(base_dir, "modelos_entrenados", "modelo_svd_similitud.pkl")
    ruta_cc  = os.path.join(base_dir, "modelos_entrenados", "modelo_recomendacion_cc.pkl") # <--- NUEVA RUTA
    
    # Carga del catálogo base
    if not os.path.exists(ruta_csv):
        st.error(f"❌ No encuentro el CSV en: {ruta_csv}")
        st.stop()
    df = pd.read_csv(ruta_csv)
    
    # Estandarización de columnas clave para evitar errores
    # Aseguramos que existan 'product_id' y 'Category' con mayúsculas/minúsculas correctas
    if 'ProductId' in df.columns: df.rename(columns={'ProductId': 'product_id'}, inplace=True)
    if 'category' in df.columns: df.rename(columns={'category': 'Category'}, inplace=True)
    
    # Carga NLP
    matriz_nlp = None
    if os.path.exists(ruta_nlp):
        with open(ruta_nlp, 'rb') as f:
            matriz_nlp = pickle.load(f)
    
    # Carga SVD
    matriz_svd = None
    if os.path.exists(ruta_svd):
        with open(ruta_svd, 'rb') as f:
            matriz_svd = pickle.load(f)

    # Carga Co-ocurrencia (NUEVO)
    matriz_cc = None
    df_prods_cc = None # El pickle de CC guarda una tupla (matriz, df_productos)
    if os.path.exists(ruta_cc):
        with open(ruta_cc, 'rb') as f:
            try:
                # Intentamos desempaquetar la tupla
                datos_cc = pickle.load(f)
                if isinstance(datos_cc, tuple) and len(datos_cc) == 2:
                    matriz_cc, df_prods_cc = datos_cc
                else:
                    matriz_cc = datos_cc # Si por alguna razón solo guardó la matriz
            except Exception as e:
                st.warning(f"No se pudo cargar el modelo CC correctamente: {e}")
            
    return df, matriz_nlp, matriz_svd, matriz_cc

try:
    df_catalogo, modelo_nlp, modelo_svd, modelo_cc = load_models()
except Exception as e:
    st.error(f"Error crítico al cargar: {e}")
    st.stop()

# --- 3. LÓGICA DE RECOMENDACIÓN ---

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
        # Buscamos el ID del producto seleccionado
        filtro = df_catalogo[df_catalogo['ProductName'] == producto_nombre]
        if filtro.empty: return []
        prod_id = filtro['product_id'].values[0]
        
        # Lógica para DataFrame (matriz de similitud con índices de ID)
        if isinstance(modelo_svd, pd.DataFrame):
            if prod_id in modelo_svd.index:
                similares = modelo_svd.loc[prod_id].sort_values(ascending=False)
                top_ids = similares.index[1:top_n+1].tolist()
                return df_catalogo[df_catalogo['product_id'].isin(top_ids)]['ProductName'].tolist()
        
        # Lógica para Matriz Numpy (fallback si fuera matriz densa sin índices)
        else:
             idx = filtro.index[0]
             scores = list(enumerate(modelo_svd[idx]))
             scores = sorted(scores, key=lambda x: x[1], reverse=True)
             indices = [i[0] for i in scores[1:top_n+1]]
             return df_catalogo['ProductName'].iloc[indices].tolist()
    except:
        return []

def recomendar_cc(producto_nombre, top_n=3):
    """
    Lógica basada en Co-ocurrencia:
    1. Busca productos comprados juntos (product_id_x -> product_id_y).
    2. Filtra para recomendar solo productos de la misma Categoría (según notebook).
    """
    if modelo_cc is None: return []
    
    try:
        # 1. Obtener ID y Categoría del producto semilla
        filtro_seed = df_catalogo[df_catalogo['ProductName'] == producto_nombre]
        if filtro_seed.empty: return []
        
        seed_id = filtro_seed['product_id'].values[0]
        seed_cat = filtro_seed['Category'].values[0] # Importante para filtrar
        
        # 2. Buscar en la matriz de co-ocurrencia (DataFrame: product_id_x, product_id_y, frecuencia)
        # Filtramos donde el producto X es el seleccionado
        candidatos = modelo_cc[modelo_cc['product_id_x'] == seed_id].copy()
        
        if candidatos.empty: return []
        
        # 3. Unir con catálogo para saber la categoría de los candidatos (product_id_y)
        # Usamos df_catalogo que ya tenemos en memoria
        candidatos = candidatos.merge(
            df_catalogo[['product_id', 'Category', 'ProductName']], 
            left_on='product_id_y', 
            right_on='product_id', 
            how='left'
        )
        
        # 4. Aplicar filtros: Misma categoría y excluir el mismo producto
        candidatos = candidatos[
            (candidatos['Category'] == seed_cat) & 
            (candidatos['product_id_y'] != seed_id)
        ]
        
        # 5. Ordenar por frecuencia (mayor co-ocurrencia primero)
        candidatos = candidatos.sort_values('frecuencia', ascending=False)
        
        return candidatos['ProductName'].head(top_n).tolist()

    except Exception as e:
        # st.error(f"Error en CC: {e}") # Descomentar para debug
        return []

# --- 4. INTERFAZ GRÁFICA (LIMPIA) ---

st.title("🤖 Quantum Insights")
st.markdown("Sistema de Recomendación Inteligente")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    # AÑADIDA LA OPCIÓN DE CO-OCURRENCIA
    tipo_modelo = st.radio(
        "Estrategia:", 
        ["Contenido (NLP)", "Patrones (SVD)", "Estadístico (Co-ocurrencia)"]
    )
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
            
            # --- SELECCIÓN DEL MODELO ---
            if "NLP" in tipo_modelo:
                recomendados = recomendar_nlp(producto, top_k)
            elif "SVD" in tipo_modelo:
                recomendados = recomendar_svd(producto, top_k)
            elif "Co-ocurrencia" in tipo_modelo:
                recomendados = recomendar_cc(producto, top_k) # <--- LLAMADA NUEVA

            if recomendados:
                df_detalles = obtener_detalles_db(recomendados)
                
                if not df_detalles.empty:
                    items = df_detalles.to_dict(orient='records')
                    
                    # Grid de 2 columnas
                    grid_cols = st.columns(2)
                    
                    for i, item in enumerate(items):
                        with grid_cols[i % 2]:
                            # Robustez para nombres de columnas (mayúsculas/minúsculas)
                            cat = item.get('category') or item.get('Category') or "General"
                            nom = item.get('productname') or item.get('ProductName') or "Producto"
                            marca = item.get('brand') or item.get('Brand') or ""
                            
                            # --- TARJETA ---
                            with st.container(border=True):
                                st.markdown(f"## 📦") 
                                st.markdown(f"#### {nom}")
                                st.markdown(f"**Categoría:** {cat}")
                                if marca:
                                    st.caption(f"🏷️ Marca: {marca}")
                                st.success("Recomendado")
                else:
                    st.warning("Se encontraron recomendaciones, pero sin detalles en BD.")
                    for prod in recomendados:
                        st.info(f"🔹 {prod}")
            else:
                st.error("No hay recomendaciones disponibles para este producto con el modelo seleccionado.")
                st.caption("Prueba con otro producto o cambia de modelo.")