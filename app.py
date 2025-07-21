import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pivot Explorer", layout="wide")
st.title("📊 Outil de Tableau & Diagramme Croisé")

# Upload du fichier Excel
uploaded_file = st.file_uploader("📥 Upload un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")

        st.subheader("👁️ Aperçu des données")
        st.dataframe(df.head())

        cols = df.columns.tolist()

        st.subheader("🔧 Configuration du tableau croisé")

        # Choix du nombre de variables pour l'index
        num_index_vars = st.selectbox("🔢 Nombre de variables pour les lignes (index)", [1, 2, 3, 4])

        # Sélection dynamique des index
        index = st.multiselect(f"🧱 Choisis {num_index_vars} variable(s) pour les lignes", cols, max_selections=num_index_vars)
        if len(index) != num_index_vars:
            st.warning(f"⚠️ Tu dois choisir exactement {num_index_vars} variable(s).")
            st.stop()

        # Sélection des colonnes
        column = st.selectbox("📐 Colonne", [col for col in cols if col not in index])
        value = st.selectbox("🔢 Valeur", [col for col in cols if col not in index and col != column])

        # Fonction d'agrégation
        aggfunc = st.selectbox("🧮 Fonction d'agrégation", ["sum", "count", "mean", "max", "min"])

        # Calcul et affichage du tableau croisé
        if index and column and value:
            try:
                pivot = pd.pivot_table(df, index=index, columns=column, values=value, aggfunc=aggfunc, fill_value=0)
                st.subheader("📋 Tableau croisé")
                st.dataframe(pivot)

                # Affichage du graphique
                st.subheader("📊 Diagramme croisé")
                chart_type = st.radio("📌 Type de graphique", ["Barres", "Heatmap"])

                pivot_reset = pivot.reset_index().melt(id_vars=index)

                if chart_type == "Barres":
                    fig = px.bar(pivot_reset, x=index[0], y="value", color="variable", barmode="group")
                else:
                    fig = px.density_heatmap(pivot_reset, x=index[0], y="variable", z="value", color_continuous_scale="Viridis")

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Erreur dans la création du tableau croisé : {e}")

    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
