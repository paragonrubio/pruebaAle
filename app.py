import streamlit as st
import pandas as pd
from collections import defaultdict

st.title("Consolidar CSVs por Nombre")

uploaded_files = st.file_uploader("Carga tus archivos CSV", type="csv", accept_multiple_files=True)

if uploaded_files:
    data_dict = defaultdict(dict)

    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file, header=None, names=['Nombre', 'Ventas'])
        file_name = uploaded_file.name.split('.')[0]  # Use the file name without extension
        for index, row in df.iterrows():
            name = row['Nombre']
            data_dict[name][file_name] = row['Ventas']

    consolidated_df = pd.DataFrame(data_dict).T.fillna(0)  # Transpose and fill missing values with 0
    consolidated_df.reset_index(inplace=True)
    consolidated_df.rename(columns={'index': 'Nombre'}, inplace=True)

    st.write("Datos Consolidados")
    st.dataframe(consolidated_df)

    # Option to download the consolidated data as CSV
    csv = consolidated_df.to_csv(index=False).encode()
    st.download_button(label="Descargar CSV consolidado", data=csv, file_name='datos_consolidados.csv', mime='text/csv')
