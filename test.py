import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Análisis de Excel", page_icon="📊", layout="wide")

# Título de la aplicación
st.title("Análisis de Excel y Generación de Gráficos")

# Cargar el archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)

    # Convertir las columnas de fecha a tipo datetime
    date_columns = ['Invoice Date', 'Entered On', 'Discount due date', 'Net Due date', 'PO Due Date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')  # 'coerce' para manejar errores en la conversión

    # Calcular días de atraso
    df['Days Overdue'] = (datetime.now() - df['Net Due date']).dt.days

    # Sidebar para diferentes filtros
    st.sidebar.header("Filtros")
    buyer = st.sidebar.multiselect("Selecciona uno o más Compradores", options=df['Buyer'].unique())
    vendor = st.sidebar.multiselect("Selecciona uno o más Proveedores", options=df['Vendor Name'].unique())
    days_exception = st.sidebar.slider("Selecciona el rango de Días en Excepción", min_value=int(df['Days in exception'].min()), max_value=int(df['Days in exception'].max()), value=(0, int(df['Days in exception'].max())))
    rule_id = st.sidebar.multiselect("Selecciona uno o más Rule ID", options=df['Rule ID'].unique())

    # Filtrar el DataFrame
    filtered_df = df
    if buyer:
        filtered_df = filtered_df[filtered_df['Buyer'].isin(buyer)]
    if vendor:
        filtered_df = filtered_df[filtered_df['Vendor Name'].isin(vendor)]
    if rule_id:
        filtered_df = filtered_df[filtered_df['Rule ID'].isin(rule_id)]
    filtered_df = filtered_df[(filtered_df['Days in exception'] >= days_exception[0]) & (filtered_df['Days in exception'] <= days_exception[1])]

    st.write("Facturas filtradas:")
    st.dataframe(filtered_df)

    # Gráficos
    st.subheader("Gráficos")

    # Histograma de días en excepción
    st.subheader("Distribución de Días en Excepción")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Days in exception'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # Gráfico de barras de días en excepción por proveedor
    st.subheader("Días en Excepción por Proveedor")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Vendor Name', y='Days in exception', data=filtered_df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Gráfico de dispersión de días de atraso vs días en excepción
    st.subheader("Días de Atraso vs Días en Excepción")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Days Overdue', y='Days in exception', data=filtered_df, ax=ax)
    st.pyplot(fig)

    # Gráfico de líneas de volumen de compras por mes
    st.subheader("Volumen de Compras por Mes")
    df.set_index('Invoice Date', inplace=True)
    fig, ax = plt.subplots()
    df.resample('M').size().plot(ax=ax)
    st.pyplot(fig)

    # Gráfico de torta de distribución de proveedores
    st.subheader("Distribución de Proveedores")
    fig, ax = plt.subplots()
    filtered_df['Vendor Name'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%', startangle=90, cmap='viridis')
    ax.set_ylabel('')
    st.pyplot(fig)

    # Gráfico de barras de monto total por comprador
    st.subheader("Monto Total por Comprador")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Buyer', y='Vchr Line Amount in USD', data=filtered_df, estimator=sum, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Gráfico de dispersión de monto de facturas vs días en excepción
    st.subheader("Monto de Facturas vs Días en Excepción")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Vchr Line Amount in USD', y='Days in exception', data=filtered_df, ax=ax)
    st.pyplot(fig)

else:
    st.write("Por favor, sube un archivo Excel para comenzar el análisis.")