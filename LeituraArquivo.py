import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilha", layout="wide")

arquivo = st.file_uploader("Selecione um arquivo .xls ou .xlsx", type=["xls", "xlsx"])

def ler_planilha(uploaded_file):
    nome = uploaded_file.name.lower()
    try:
        # Testa leitura direta com pandas (sem engine)
        return pd.read_excel(uploaded_file)
    except Exception as e1:
        try:
            # Se falhar, tenta com engine openpyxl (para .xlsx)
            if nome.endswith('.xlsx'):
                return pd.read_excel(uploaded_file, engine='openpyxl')
            # Se falhar, tenta com engine xlrd (para .xls)
            elif nome.endswith('.xls'):
                return pd.read_excel(uploaded_file, engine='xlrd')
        except Exception as e2:
            st.error(f"Erro ao ler o arquivo:\n{e1}\n{e2}")
            return None

if arquivo is not None:
    df = ler_planilha(arquivo)
    
    if df is not None:
        st.title("🔧 Limpeza de Planilha: Remoção de Colunas e SKUs")

        st.subheader("🗂️ Remover Colunas")
        colunas = st.multiselect("Selecione as colunas que deseja remover:", df.columns.tolist())
        df_filtrado = df.drop(columns=colunas, errors='ignore')

        coluna_sku = "Código (SKU)"
        st.subheader("📦 Remover SKUs (insira separados por vírgula)")
        skus_input = st.text_input("Digite os SKUs que deseja remover:")
        skus_para_remover = [sku.strip() for sku in skus_input.split(",") if sku.strip()]

        if skus_para_remover and coluna_sku in df_filtrado.columns:
            df_filtrado = df_filtrado[~df_filtrado[coluna_sku].astype(str).isin(skus_para_remover)]

        st.subheader("✅ Resultado Final")
        st.dataframe(df_filtrado)

        buffer = BytesIO()
        df_filtrado.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="📥 Baixar Excel com Dados Filtrados",
            data=buffer,
            file_name="dados_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
