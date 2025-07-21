import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tableau Croisé Classique", layout="wide")
st.title("📊 Tableau & Diagramme Croisé - Version Classique Excel")

uploaded_file = st.file_uploader("📥 Upload un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")
        st.dataframe(df.head())

        cols = df.columns.tolist()

        st.subheader("🎛️ Sélection du tableau croisé")
        index_vars = st.multiselect("📌 Lignes (jusqu'à 3)", cols, max_selections=3)
        column_var = st.selectbox("📍 Colonnes", [c for c in cols if c not in index_vars])

        aggfunc = st.selectbox("🧮 Fonction d'agrégation", ["count", "sum", "mean", "max", "min"])

        if aggfunc != "count":
            value_vars = df.select_dtypes(include="number").columns.tolist()
            value_var = st.selectbox("🔢 Colonne à agréger", value_vars)
        else:
            value_var = None

        if index_vars and column_var:
            st.subheader("📋 Tableau croisé")

            try:
                if aggfunc == "count":
                    pivot = pd.pivot_table(df, index=index_vars, columns=column_var, aggfunc="size", fill_value=0)
                else:
                    pivot = pd.pivot_table(df, index=index_vars, columns=column_var, values=value_var, aggfunc=aggfunc, fill_value=0)

                st.dataframe(pivot)

                # Diagramme simple basé sur la 1re variable d'index
                st.subheader("📊 Diagramme croisé")

                pivot_reset = pivot.reset_index()
                pivot_melted = pivot_reset.melt(id_vars=index_vars, var_name=column_var, value_name="Valeur")

                fig = px.bar(
                    pivot_melted,
                    x=index_vars[0],
                    y="Valeur",
                    color=column_var,
                    barmode="group",
                    facet_row=index_vars[1] if len(index_vars) > 1 else None,
                    facet_col=index_vars[2] if len(index_vars) > 2 else None,
                    title="Diagramme croisé",
                )

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Erreur dans le pivot : {e}")

    except Exception as e:
        st.error(f"Erreur de lecture du fichier : {e}")
