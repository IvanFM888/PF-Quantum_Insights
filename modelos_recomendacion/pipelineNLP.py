import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mlflow
import os
from modelos_recomendacion.modelonlp import ModeloNLP
import pickle
from sklearn.model_selection import train_test_split



def preparar_nlp(df):
    # Solo nos interesa limpiar la columna del nombre
    # No concatenamos ni marca ni categoría para evitar sesgos
    df['perfil_texto'] = df['ProductName'].fillna('').astype(str).str.lower().str.strip()
    
    return df

# def preparar_nlp(df):
#     columnas_clave = ['ProductName', 'Brand', 'Category', 'SubCategory']
#     for col in columnas_clave:
#         df[col] = df[col].fillna('')
    
#     # Creamos el perfil de texto de forma eficiente
#     df['perfil_texto'] = (df['Brand'] + " " + df['Category'] + " " + 
#                           df['SubCategory'] + " " + df['ProductName']).str.lower().str.strip()
#     return df

# df_productos = preparar_nlp(pd.read_csv("./databases/products.csv"))

# # Vectorización: Convertimos texto a números
# tfidf = TfidfVectorizer(stop_words='english') 
# tfidf_matrix = tfidf.fit_transform(df_productos['perfil_texto'])

# # Matriz de similitud de Coseno
# cos_sim = cosine_similarity(tfidf_matrix)
# df_sim_nlp = pd.DataFrame(cos_sim, index=df_productos['product_id'], columns=df_productos['product_id'])


# # 1. Identificamos todas las órdenes únicas
# ordenes_unicas = df_order_items['order_id'].unique()

# # 2. Dividimos las órdenes: 80% para entrenamiento y 20% para prueba
# # Usamos random_state=42 para que siempre obtengas los mismos resultados
# train_ids, test_ids = train_test_split(ordenes_unicas, test_size=0.2, random_state=42)

# # 3. Creamos los DataFrames filtrando por esos IDs
# # 'train_data' lo usarías si quisieras hacer un modelo híbrido más adelante
# # 'test_data' es el que usaremos en la función 'evaluar_nlp_baskets'
# train_data = df_order_items[df_order_items['order_id'].isin(train_ids)]
# test_data = df_order_items[df_order_items['order_id'].isin(test_ids)]


df_productos = preparar_nlp(pd.read_csv("./databases/products.csv"))

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_productos['perfil_texto'])

cos_sim = cosine_similarity(tfidf_matrix)
df_sim_nlp = pd.DataFrame(cos_sim, index=df_productos['product_id'], columns=df_productos['product_id'])

modelo_nlp = ModeloNLP(df_sim_nlp)

ruta_actual = os.getcwd()

# Identificar la carpeta correcta donde se guardarán los modelos
if os.path.exists(os.path.join(ruta_actual, "modelos_entrenados")):
    ruta_modelos = os.path.join(ruta_actual, "modelos_entrenados")
else:
    # Buscar la carpeta subiendo un nivel si no está en el actual
    ruta_modelos = os.path.join(os.path.dirname(ruta_actual), "modelos_entrenados")

# Crear la carpeta automáticamente si no existe
if not os.path.exists(ruta_modelos):
    os.makedirs(ruta_modelos)

# Construir la ruta completa con el nombre del archivo final
archivo_salida = os.path.join(ruta_modelos, "modelo_recomendacion_nlp.pkl")

modelo_nlp = ModeloNLP(df_sim_nlp)

archivo_salida = os.path.join(ruta_modelos, "modelo_recomendacion_nlp.pkl")

with open(archivo_salida, "wb") as f:
    pickle.dump(modelo_nlp, f)

## Ejecutar con este comando ( python -m modelos_recomendacion.pipelineNLP )