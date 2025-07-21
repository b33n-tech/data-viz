import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Tableau croisé imbriqué", layout="wide")

st.title("📊 Tableau croisé imbriqué")

uploaded_file = st.file_uploader("📥 Uploade ton fichier Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Fichier chargé avec succès")

        st.subheader("🧩 Choix des variables")
        st.markdown("Choisis :")
        row_var = st.selectbox("🧱 Variable des **lignes** (ex: Année)", df.columns)
        col_var_1 = st.selectbox("🏷️ Variable principale des **colonnes** (ex: Région)", df.columns)
        col_var_2 = st.selectbox("📍 Variable secondaire imbriquée (ex: Succès/Échec)", df.columns)

        if row_var and col_var_1 and col_var_2:
            try:
                # Création du tableau croisé avec MultiIndex colonnes
                pivot = pd.crosstab(index=df[row_var],
                                    columns=[df[col_var_1], df[col_var_2]])

                # Tri des colonnes pour plus de lisibilité
                pivot = pivot.sort_index(axis=1, level=[0, 1])

                st.subheader("📋 Résultat du tableau croisé imbriqué")
                st.dataframe(pivot, use_container_width=True)

                # Export Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    pivot.to_excel(writer, sheet_name='Tableau Croisé')
                    writer.close()
                st.download_button(
                    label="📥 Télécharger le tableau croisé (.xlsx)",
                    data=output.getvalue(),
                    file_name="tableau_croise.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except Exception as e:
                st.error(f"❌ Erreur dans le pivot : {e}")
    except Exception as e:
        st.error(f"❌ Impossible de lire le fichier : {e}")
else:
    st.info("🕓 En attente d'un fichier Excel.")
