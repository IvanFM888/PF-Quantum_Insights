class ModeloNLP:
    def __init__(self, df_sim):
        self.df_sim = df_sim

    def recomendar(self, product_id, top_n=3):
        if product_id not in self.df_sim.index:
            return []

        similares = (
            self.df_sim[product_id]
            .sort_values(ascending=False)
            .drop(product_id, errors="ignore")
        )

        return similares.head(top_n).index.tolist()