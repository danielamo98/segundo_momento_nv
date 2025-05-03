import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Análisis Básico de Ventas")

# Cargar el dataset
@st.cache_data  # Para mejorar el rendimiento al cargar el archivo
def load_data():
    df = pd.read_csv("static/dataset/sales_data.csv")

    return df

df = load_data()

# Mostrar dataset completo
st.subheader("Datos Completos")
st.dataframe(df)

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Crea un selectbox para elegir una categoría
unique_categories = df['Category'].unique()
category = st.sidebar.selectbox("Seleccionar Categoría", ['Todas'] + list(unique_categories))

# Crea un slider para el rango de precios
min_price_all = int(df['Price'].min())
max_price_all = int(df['Price'].max())
price_range = st.sidebar.slider("Seleccionar Rango de Precios", min_value=min_price_all, max_value=max_price_all, value=(min_price_all, max_price_all))

# Aplicar filtros
filtered_df = df.copy()

if category != 'Todas':
    filtered_df = filtered_df[filtered_df['Category'] == category]

filtered_df = filtered_df[(filtered_df['Price'] >= price_range[0]) & (filtered_df['Price'] <= price_range[1])]

# Mostrar datos filtrados
st.subheader("Datos Filtrados")
if not filtered_df.empty:
    st.dataframe(filtered_df)
    st.write(f"Número de registros filtrados: {filtered_df.shape[0]}")
else:
    st.write("No hay datos para los filtros seleccionados.")

# Estadísticas
st.subheader("Estadísticas")
if not filtered_df.empty:
    # Calcula el total de ventas y el precio promedio
    total_sales = filtered_df['Total_Sales'].sum()
    avg_price = filtered_df['Price'].mean()

    # Muestra las estadísticas con st.metric
    st.metric("Total de Ventas", f"${total_sales:,.2f}")
    st.metric("Precio Promedio", f"${avg_price:.2f}")
else:
    st.write("No se pueden calcular estadísticas sin datos filtrados.")