def recomendar_cc_eval(product_id, df_matriz, df_products, top_n=3):
    # Producto semilla
    row = df_products[df_products['product_id'] == product_id]
    if row.empty:
        return []
    cat_seed = row.iloc[0]['Category']
    subcat_seed = row.iloc[0]['SubCategory']
    candidatos = df_matriz[df_matriz['product_id_x'] == product_id]
    if candidatos.empty:
        return []
    recs = candidatos.merge(
        df_products[['product_id', 'Category', 'SubCategory']],
        left_on='product_id_y',
        right_on='product_id',
        how='left'
    )
    recs = recs[recs['product_id_y'] != product_id]
    recs = recs.sort_values('frecuencia', ascending=False)
    recomendaciones = []
    nivel_1 = (
        recs[
            (recs['Category'] == cat_seed) &
            (recs['SubCategory'] == subcat_seed)
        ]
        .drop_duplicates(subset='product_id_y')
    )
    recomendaciones.extend(nivel_1['product_id_y'].tolist())

    if len(recomendaciones) < top_n:
        nivel_2 = (
            recs[
                (recs['Category'] == cat_seed) &
                (recs['SubCategory'] != subcat_seed)
            ]
            .drop_duplicates(subset='product_id_y')
        )
        nivel_2 = nivel_2[
            ~nivel_2['product_id_y'].isin(recomendaciones)
        ]
        faltantes = top_n - len(recomendaciones)
        recomendaciones.extend(
            nivel_2['product_id_y'].head(faltantes).tolist()
        )
    if len(recomendaciones) < top_n:
        nivel_3 = (
            recs[
                recs['Category'] != cat_seed
            ]
            .drop_duplicates(subset='product_id_y')
        )
        nivel_3 = nivel_3[
            ~nivel_3['product_id_y'].isin(recomendaciones)
        ]
        faltantes = top_n - len(recomendaciones)
        recomendaciones.extend(
            nivel_3['product_id_y'].head(faltantes).tolist()
        )
    return recomendaciones[:top_n]



class ModeloCoocurrencia:
    def __init__(self, df_matriz, df_products):
        self.df_matriz = df_matriz
        self.df_products = df_products

    def recomendar(self, product_id, top_n=3):
        return recomendar_cc_eval(
            product_id,
            self.df_matriz,
            self.df_products,
            top_n
        )