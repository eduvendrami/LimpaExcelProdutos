import pandas as pd
import streamlit as st
from io import BytesIO

arquivo = st.file_uploader("Selecione um arquivo .xls ou .xlsx", type=["xls", "xlsx"])

if arquivo is not None:
    df = pd.read_excel(arquivo)

    st.title("🔧 Limpeza de Planilha: Remoção de Colunas e SKUs")

    # Seletor de colunas para remoção
    st.subheader("🗂️ Remover Colunas")
    colunas = st.multiselect("Selecione as colunas que deseja remover:", df.columns.tolist())

    # Remove as colunas selecionadas
    df_filtrado = df.drop(columns=colunas, errors='ignore')

    # Nome fixo da coluna SKU
    coluna_sku = "Código (SKU)"

    # Campo para inserir SKUs para remover
    st.subheader("📦 Remover SKUs (insira separados por vírgula)")
    skus_input = st.text_input("Digite os SKUs que deseja remover:")

    # Processa o input para lista
    skus_para_remover = [sku.strip() for sku in skus_input.split(",") if sku.strip()]

    # Remove os SKUs indicados
    if skus_para_remover:
        df_filtrado = df_filtrado[~df_filtrado[coluna_sku].isin(skus_para_remover)]

    # Exibe resultado
    st.subheader("✅ Resultado Final")
    st.dataframe(df_filtrado)

    # Exportação para Excel
    # Exportação para Excel
    buffer = BytesIO()
    df_filtrado.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    st.download_button(
        label="📥 Baixar Excel com Dados Filtrados",
        data=buffer,
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
