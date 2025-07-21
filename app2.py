import streamlit as st
import pandas as pd
import io
import plotly.express as px

st.set_page_config(page_title="Tableau croisé dynamique", layout="wide")

st.title("📊 Outil Tableau Croisé + Diagramme")
st.markdown("Charge un fichier `.xlsx`, choisis tes colonnes, et obtiens un tableau croisé et un graphique visuel !")

uploaded_file = st.file_uploader("📁 Upload ton fichier Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # Nettoyage des noms de colonnes
        st.success("✅ Fichier chargé avec succès")
        st.write("🔍 Colonnes détectées :", list(df.columns))

        # Sélections des colonnes
        row_var = st.selectbox("🧱 Axe des lignes (ex: année)", df.columns, key="row")
        col_var_1 = st.selectbox("🏷️ Colonne principale (ex: région)", df.columns, key="col1")
        col_var_2 = st.selectbox("🏷️ Colonne emboîtée (ex: succès/échec)", df.columns, key="col2")

        aggfunc_choice = st.selectbox("📐 Méthode d’agrégation", ["count", "sum"])
        diagram_mode = st.radio("📊 Mode du diagramme", ["Barres empilées", "Barres côte-à-côte"])

        if st.button("🧮 Générer le tableau croisé"):
            try:
                # Construction du tableau croisé
                pivot_table = pd.pivot_table(
                    df,
                    index=row_var,
                    columns=[col_var_1, col_var_2],
                    aggfunc="size" if aggfunc_choice == "count" else "sum",
                    fill_value=0
                )

                st.subheader("📑 Tableau croisé")
                st.dataframe(pivot_table)

                # Téléchargement
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    pivot_table.to_excel(writer, sheet_name='Pivot')
                    writer.close()
                    st.download_button(
                        label="📥 Télécharger le tableau en .xlsx",
                        data=buffer.getvalue(),
                        file_name="tableau_croise.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                # Diagramme
                st.subheader("📊 Diagramme croisé")

                pivot_reset = pivot_table.reset_index()
                melted = pivot_reset.melt(id_vars=row_var, var_name=["Groupe1", "Groupe2"], value_name="Valeur")

                barmode = "stack" if diagram_mode == "Barres empilées" else "group"
                fig = px.bar(
                    melted,
                    x=row_var,
                    y="Valeur",
                    color="Groupe2",
                    facet_col="Groupe1",
                    barmode=barmode,
                    title="Diagramme croisé"
                )
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Erreur dans le pivot : {e}")

    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
