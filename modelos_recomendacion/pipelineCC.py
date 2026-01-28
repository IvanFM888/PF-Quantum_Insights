# Librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import mlflow
import os
import pickle
from modelos_recomendacion.modelocoocurrencia import ModeloCoocurrencia

ruta_actual = os.getcwd()
mlflow.set_tracking_uri(f"file:///{ruta_actual}/mlruns")
mlflow.set_experiment("Modelos de Recomendación - Comparativa")

# Cargamos cada archivo CSV en un DataFrame de pandas para poder manipularlos como tablas de datos
df_events = pd.read_csv("./databases/events.csv")
df_order_items = pd.read_csv("./databases/order_items.csv")
df_orders = pd.read_csv("./databases/orders.csv")
df_products = pd.read_csv("./databases/products.csv")
df_reviews = pd.read_csv("./databases/reviews.csv")
df_users = pd.read_csv("./databases/users.csv")

from sklearn.model_selection import train_test_split

# Se organiza los productos por ordenes
df_interacciones = df_order_items[['order_id', 'product_id']].copy()

# Se divide 80 train / 20 test
# Es mejor dividir por order_id para no separar una misma orden en dos
ordenes_unicas = df_interacciones['order_id'].unique()
train_ids, test_ids = train_test_split(ordenes_unicas, test_size=0.2, random_state=42)

train_data = df_interacciones[df_interacciones['order_id'].isin(train_ids)]
test_data = df_interacciones[df_interacciones['order_id'].isin(test_ids)]
# Unimos la tabla consigo misma usando order_id para encontrar parejas
df_pares = pd.merge(train_data, train_data, on='order_id')

# Filtramos para no contar un producto consigo mismo (ej: leche con leche)
df_pares = df_pares[df_pares['product_id_x'] != df_pares['product_id_y']]

# Contamos la frecuencia de cada pareja
matriz_cooc = df_pares.groupby(['product_id_x', 'product_id_y']).size().reset_index(name='frecuencia')

# Ordenamos por los más frecuentes para facilitar la búsqueda
matriz_cooc = matriz_cooc.sort_values(['product_id_x', 'frecuencia'], ascending=[True, False])







# 1. Definir la lógica de rutas (Idéntica a la que ya usas)
ruta_actual = os.getcwd()

if os.path.exists(os.path.join(ruta_actual, "modelos_entrenados")):
    ruta_modelos = os.path.join(ruta_actual, "modelos_entrenados")
else:
    ruta_modelos = os.path.join(os.path.dirname(ruta_actual), "modelos_entrenados")

if not os.path.exists(ruta_modelos):
    os.makedirs(ruta_modelos)

# 2. Nombre del archivo para el modelo CC
archivo_salida_cc = os.path.join(ruta_modelos, "modelo_recomendacion_cc.pkl")

# 3. Guardar AMBOS DataFrames en un solo archivo
# Los guardamos como una tupla: (matriz, productos)
modelo_cc = ModeloCoocurrencia(matriz_cooc, df_products)

with open(archivo_salida_cc, 'wb') as f:
    pickle.dump(modelo_cc, f)

## Para guardar el modelo ejecutar de esta forma ( python -m modelos_recomendacion.pipelineCC )
