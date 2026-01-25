---
---

# Proyecto Final Data Science - Quantum Insights 🚀 

### **Equipo 2**

### **Cohorte DSFT01**


---
---

## 1. Requerimientos del Proyecto
Proyecto final de la carrera de Data Science de la academia Henry.

El objetivo es simular el rol de un equipo de consultoría de datos para resolver un problema de negocio real mediante la implementación de soluciones de Machine Learning de punta a punta (End-to-End).

---

## 2. Descripción del Proyecto

### Contexto y Problema
En el E-commerce actual, la sobreoferta de productos genera una "parálisis por análisis" en los clientes. Las tiendas pierden ventas por no sugerir lo que el usuario realmente desea.

**Quantum Insights** nace con la misión de **eliminar la fricción** en la experiencia de compra mediante un sistema de recomendación inteligente.

### Solución Propuesta

Desarrollamos un **Sistema de Recomendación Híbrido** que ataca el problema desde dos frentes:

1.  **Filtrado Basado en Contenido (NLP):** Analiza descripciones y metadatos de productos para encontrar similitudes semánticas (Ideal para *Cold Start*).

2.  **Filtrado Colaborativo (SVD):** Utiliza la factorización de matrices para encontrar patrones latentes en el historial de compras de los usuarios.

### KPIs del Proyecto
Para medir el éxito de nuestra solución, hemos definido los siguientes indicadores:
* **Precisión de la Recomendación (Qualitative Accuracy):** Evaluación de coherencia en las sugerencias.
* **Variedad del Catálogo (Catalog Coverage):** Porcentaje del inventario que el sistema es capaz de recomendar.

---

## 3. Desarrollo del Proyecto

El proyecto se estructura en 2 sprints semanales siguiendo la metodología SCRUM:

* **1° Etapa: Puesta en marcha y MVP** 👉 *Sprint Actual*
    * Limpieza de datos (ETL) y Análisis Exploratorio (EDA).
    * Desarrollo de pipelines de Machine Learning (SVD y NLP).
    * Generación de recomendaciones preliminares.
* **2° Etapa: Evaluación y Despliegue** 👉 *Próximos pasos*
    * Optimización de hiperparámetros.
    * Creación de interfaz de usuario (Streamlit).
    * Presentación de Demo Funcional.

---

## 4. Datasets y Stack Tecnológico

Los datos provienen de una base de datos relacional de E-commerce, procesada con el siguiente stack:

| Área | Herramientas |
| :--- | :--- |
| **Lenguaje** | 🐍 Python 3.10+ |
| **Data Eng.** | `pandas`, `numpy` |
| **Visualización** | `matplotlib`, `seaborn` |
| **Machine Learning** | `scikit-learn` (TruncatedSVD, TfidfVectorizer, Cosine Similarity) |
| **Control de Versiones** | `git`, `github` |

---

## 5. Insights Preliminares (EDA)

Del análisis de nuestros datos (`EDA.ipynb` y Pipelines), destacamos:

* **Comportamiento del Usuario:** La base cuenta con ~10,000 usuarios con una distribución de género balanceada (~33% por categoría), lo que reduce el sesgo demográfico en las recomendaciones.

* **Dispersión de Datos:** Nuestro modelo SVD inicial explica el **2.38% de la varianza** con 20 componentes, lo que indica una matriz de preferencias altamente compleja y dispersa ("Long Tail").

* **Relaciones Semánticas:** El modelo NLP logra conectar productos no solo por nombre, sino por jerarquía (`Category` -> `SubCategory`), mejorando la relevancia frente a búsquedas simples.

---

## 6. Integrantes - Quantum Insights

**Product Owner**
* **Felipe Varela** | [LinkedIn](#) | [GitHub](#)

**Data Scientists**
* **Freddy Yaquive** | [LinkedIn](#) | [GitHub](#)
* **Ivan Martinez** | [LinkedIn](#) | [GitHub](#)
* **Sebastian Moya** | [LinkedIn](#) | [GitHub](#)

**Scrum Master**
* **Nicolás Lazarte** | [LinkedIn](#) | [GitHub](#)

---

## 7. Disclaimer

De parte del equipo de Henry se quiere aclarar y remarcar que los fines de los proyectos propuestos son exclusivamente pedagógicos, con el objetivo de realizar proyectos que simulen un entorno laboral, en el cual se trabajen diversas temáticas ajustadas a la realidad. No reflejan necesariamente la filosofía y valores de la organización.

---
---