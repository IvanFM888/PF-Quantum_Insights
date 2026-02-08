# ⚛️ Proyecto Final Henry - Data Science - Quantum Insights

### **Cohorte DSFT01** | **Equipo 2**

<p align="left">
  <img src="https://assets.soyhenry.com/LOGO-REDES-01_og.jpg" alt="Henry Logo" width="100">
</p>

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg?style=flat&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg?style=flat&logo=scikit-learn)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blueviolet.svg?style=flat&logo=mlflow)
![Licencia](https://img.shields.io/badge/License-MIT-green.svg)

---

## 👥 Nuestro Equipo

Somos un equipo de consultoría de datos enfocado en resolver problemas de negocio reales mediante soluciones End-to-End.

| Integrante | Rol | Links |
| :--- | :--- | :--- |
| **Felipe Varela** | 🎯 **Product Owner** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/felipe-varela-miranda/) [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github)](#) |
| **Freddy Yaquive** | 🧪 **Data Scientist** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/freddy-esteban-b352a7309/) [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github)](#) |
| **Ivan Martinez** | 🧪 **Data Scientist** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ivanmf888/) [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github)](#) |
| **Sebastian Moya** | 🧪 **Data Scientist** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sebastian-moya-670584196/) [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github)](#) |
| **Nicolás Lazarte** | 🚀 **Scrum Master** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nicolas-angel-lazarte/) [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github)](#) |

---

## 📖 Descripción del Proyecto

### 🎯 Contexto y Problema
En el E-commerce actual, la sobreoferta de productos genera una "parálisis por análisis" en los clientes. Las tiendas pierden ventas y fidelidad por no sugerir lo que el usuario realmente desea en el momento adecuado.

### 💡 Solución Propuesta
Nuestra misión es **eliminar la fricción** en la experiencia de compra. Desarrollamos un **Sistema de Recomendación Híbrido** que ataca el problema mediante:
1.  **Market Basket Analysis:** Para compras impulsivas y complementarias.
2.  **NLP (Content-Based):** Para resolver el "Cold Start" de productos nuevos.
3.  **SVD (Collaborative Filtering):** Para personalización profunda basada en historial.

---

## 📋 Índice

* [📂 Estructura del Proyecto](#estructura-del-proyecto)
* [⚙️ Pipeline del Proyecto](#pipeline-del-proyecto)
* [🤖 Modelos Evaluados](#modelos-evaluados)
* [📊 Resultados y Métricas](#resultados-y-métricas)
* [💻 Instalación y Requisitos](#instalación-y-requisitos)
* [🚀 Uso y Ejecución](#uso-y-ejecución)
* [📝 Conclusiones del Proyecto](#conclusiones-del-proyecto)
* [⚖️ Licencia](#licencia)

---

## 📂 Estructura del Proyecto

Organización de directorios y archivos principales del repositorio:

```text
📂 PF-Quantum_Insights
│
├── 📂 databases/               # Archivos CSV crudos (Source)
├── 📂 mlruns/                  # Logs de experimentos y métricas (MLflow)
├── 📂 modelos_recomendación/   # Notebooks de entrenamiento y lógica
│   ├── 📓 pipelineSVD.ipynb    # Entrenamiento Modelo SVD (Filtrado Colaborativo)
│   ├── 📓 pipelineCC.ipynb     # Entrenamiento Modelo Co-ocurrencia (Market Basket)
│   └── 📓 pipelineNLP.ipynb    # Procesamiento NLP y matriz de similitud (Content-Based)
│
├── 📓 ETL.ipynb                # Pipeline de Extracción, Transformación y Carga (Supabase)
├── 📓 EDA.ipynb                # Análisis Exploratorio de Datos
│
├── 🚀 app_final.py             # Aplicación principal (Interfaz en Streamlit)
├── 📄 requirements.txt         # Dependencias del proyecto
└── 📄 README.md                # Documentación

```

---

## ⚙️ Pipeline del Proyecto

El flujo de datos sigue una arquitectura **End-to-End** diseñada para escalabilidad:

1. **Ingesta:** Lectura de archivos planos (`Events`, `Orders`, `Products`).
2. **ETL (Extract-Transform-Load):** Limpieza de datos, estandarización de IDs y carga a base de datos en la nube (**Supabase/PostgreSQL**).
3. **EDA (Exploratory Data Analysis):** Detección de patrones, análisis de "Long Tail" y tratamiento de dispersión (Sparsity).
4. **Modelado:** Entrenamiento de tres motores distintos (SVD, NLP, Co-ocurrencia).
5. **Evaluación:** Rastreo de métricas (`Recall`, `Precision`, `NDCG`) usando **MLflow**.
6. **Despliegue:** Interfaz de usuario interactiva construida con **Streamlit**, capaz de servir recomendaciones en tiempo real.

---

## 🤖 Modelos Evaluados

Para cubrir diferentes necesidades del negocio, implementamos un enfoque híbrido:

| Modelo | Tipo | Caso de Uso | Descripción Técnica |
| --- | --- | --- | --- |
| **Co-ocurrencia** | Reglas de Asociación | **Cross-Selling** (Carrito) | Calcula la probabilidad condicional (Si compras A, ¿qué tan probable es que compres B?). Ideal para compras impulsivas. |
| **NLP (Contenido)** | Content-Based | **Cold Start** (Nuevos) | Utiliza `TF-IDF` y Similitud del Coseno para recomendar productos semánticamente similares a partir de la descripción. |
| **SVD** | Filt. Colaborativo | **Personalización** (Home) | Factorización de matrices (`TruncatedSVD`) para hallar gustos latentes en usuarios recurrentes con historial extenso. |

---

## 📊 Resultados y Métricas

Evaluación realizada sobre el set de prueba (Test Set) con un corte de **K=5** recomendaciones.

| Modelo | Recall@5 | Precision@5 | NDCG@5 | Observación |
| --- | --- | --- | --- | --- |
| **Co-ocurrencia** | **21.76%** 🏆 | **8.73%** | **0.199** | Modelo "ganador" con mayor impacto en conversión inmediata (Siguiente item). |
| **SVD** | 5.46% | 1.20% | 0.044 | Afectado por la alta dispersión de la matriz usuario-item (Sparsity > 99%). |
| **NLP** | 1.71% | 0.69% | 0.011 | Baja predicción de venta directa, pero garantiza **74% de cobertura de catálogo**. |

> **Nota:** Aunque SVD tiene métricas de ranking más bajas, explica el **29.53% de la varianza** de los datos, siendo útil para capturar tendencias generales de categorías.

---

## 💻 Instalación y Requisitos

### Requisitos previos

* Python 3.10 o superior.
* Git.

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone [https://github.com/IvanFM888/PF-Quantum_Insights.git](https://github.com/IvanFM888/PF-Quantum_Insights.git)
cd PF-Quantum_Insights

```


2. **Crear un entorno virtual (Recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

```


3. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```



---

## 🚀 Uso y Ejecución

Puedes probar el proyecto de dos maneras: accediendo a la versión online (recomendado) o ejecutándolo en tu máquina.

### 🌐 Opción 1: Demo Online (Deploy)

La aplicación se encuentra disponible públicamente en el siguiente enlace:

👉 **[https://pf-quantuminsights.streamlit.app/](https://pf-quantuminsights.streamlit.app/)**

### 💻 Opción 2: Ejecución Local

Si prefieres correr la aplicación en tu propio entorno:

1. Asegúrate de tener las dependencias instaladas.
2. Ejecuta el siguiente comando en la terminal:
```bash
streamlit run app_final.py

```


3. *La aplicación se abrirá automáticamente en tu navegador (usualmente http://localhost:8501).*

### Re-entrenar modelos

Si deseas actualizar los modelos con nuevos datos, ejecuta los notebooks en el siguiente orden:

1. `ETL.ipynb` (Limpieza y carga)
2. `modelos_recomendación/pipelineCC.ipynb` (Matriz de co-ocurrencia)
3. `modelos_recomendación/pipelineNLP.ipynb` (Matriz NLP)
4. `modelos_recomendación/pipelineSVD.ipynb` (Modelo SVD)

---

## 📝 Conclusiones del Proyecto

### 🛠️ Sobre el ETL y Datos

* **Integridad:** Se detectaron inconsistencias críticas entre `Events` y `Order_Items` que requerían estandarización de IDs.
* **Escalabilidad:** La migración de CSV local a **Supabase** permitió centralizar la verdad de los datos y preparar el proyecto para un entorno productivo.

### 📊 Sobre el EDA (Análisis Exploratorio)

* **Sparsity (Dispersión):** Confirmamos que la matriz de interacción es extremadamente dispersa. Los usuarios interactúan con una fracción mínima del catálogo.
* **Comportamiento:** Existe una fuerte tendencia a la compra complementaria (Items que se compran juntos en la misma sesión) más que a la compra repetitiva del mismo item.

### 🤖 Sobre los Modelos

* **El Hallazgo:** El modelo de **Co-ocurrencia** demostró ser superior para este dataset específico, sugiriendo que las reglas de asociación (Market Basket) son más efectivas aquí que la factorización de matrices compleja.
* **Estrategia Híbrida:** Ningún modelo es perfecto por sí solo. La combinación de NLP (para visibilidad de catálogo nuevo) y Co-ocurrencia (para conversión de carrito) crea el sistema más robusto.

---

## ⚖️ Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

```text
MIT License
Copyright (c) 2025 Quantum Insights Team

```

---

*Disclaimer: Proyecto realizado con fines educativos para la academia Henry.*

```

```