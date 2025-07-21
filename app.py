import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pivot Explorer", layout="wide")

st.title("📊 Outil de Tableau & Diagramme Croisé")

# Upload du fichier
uploaded_file = st.file_uploader("📥 Upload un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")

        st.subheader("👁️ Aperçu des données")
        st.dataframe(df.head())

        cols = df.columns.tolist()

        st.subheader("🔧 Configuration du tableau croisé")
        index = st.multiselect("🧱 Index (lignes)", cols, default=cols[0] if cols else None, max_selections=2)
        columns = st.selectbox("📐 Colonnes", cols, index=1 if len(cols) > 1 else 0)
        values = st.selectbox("🔢 Valeur", cols, index=2 if len(cols) > 2 else 0)

        aggfunc = st.selectbox("🧮 Fonction d'agrégation", ["sum", "count", "mean", "max", "min"])

        if index and columns and values:
            try:
                pivot = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=0)
                st.subheader("📋 Tableau croisé")
                st.dataframe(pivot)

                st.subheader("📊 Diagramme croisé")
                chart_type = st.radio("📌 Type de graphique", ["Barres", "Heatmap"])

                pivot_reset = pivot.reset_index().melt(id_vars=index)

                if chart_type == "Barres":
                    fig = px.bar(pivot_reset, x=index[0], y="value", color=columns, barmode="group")
                else:
                    fig = px.density_heatmap(pivot_reset, x=index[0], y="variable", z="value", color_continuous_scale="Viridis")

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Erreur dans la création du pivot: {e}")

    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier: {e}")
