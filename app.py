import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explorateur Croisé", layout="wide")
st.title("📊 Tableau et Diagramme Croisé Générique")

uploaded_file = st.file_uploader("📥 Upload un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")
        st.dataframe(df.head())

        cols = df.columns.tolist()

        st.subheader("🎛️ Sélection des dimensions")
        selected_vars = st.multiselect("Choisis 1 à 3 variables pour explorer les données", cols, max_selections=3)

        if len(selected_vars) < 1:
            st.warning("🟡 Choisis au moins une variable.")
            st.stop()

        # Choix de la fonction d'agrégation
        aggfunc = st.selectbox("🧮 Fonction d'agrégation", ["count", "sum", "mean"])

        # Si count, on ne choisit pas de variable à agréger
        if aggfunc != "count":
            num_cols = df.select_dtypes(include='number').columns.tolist()
            value_col = st.selectbox("🔢 Colonne à agréger", num_cols)
        else:
            value_col = None

        # Préparation du dataframe à afficher
        st.subheader("📋 Résumé croisé")

        # GROUP BY dynamique
        group = df.groupby(selected_vars)
        if aggfunc == "count":
            result = group.size().reset_index(name="Total")
        else:
            result = group[value_col].agg(aggfunc).reset_index(name=f"{aggfunc}_{value_col}")

        st.dataframe(result)

        # Affichage graphique
        st.subheader("📊 Visualisation")

        # Mapping des dimensions
        x = selected_vars[0]
        color = selected_vars[1] if len(selected_vars) >= 2 else None
        facet = selected_vars[2] if len(selected_vars) == 3 else None

        value_name = "Total" if aggfunc == "count" else f"{aggfunc}_{value_col}"

        fig = px.bar(
            result,
            x=x,
            y=value_name,
            color=color,
            facet_col=facet,
            barmode="group" if color else "relative",
            title="Diagramme croisé",
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")
