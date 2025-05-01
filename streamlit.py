import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import streamlit as st
from pathlib import Path
import os

# Set current working directory
BASE_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()

# Load datasets (relative paths)
file_path_2021 = BASE_DIR / '2021_dataset-Table 1.xlsx'
file_path_2023 = BASE_DIR / '2023_dataset-Table 1.xlsx'

# Read Excel files
data_2021 = pd.read_excel(file_path_2021, engine='openpyxl')
data_2023 = pd.read_excel(file_path_2023, engine='openpyxl')

# Streamlit interface
st.title("Criminal Market Analysis")

# Year selection
year = st.selectbox("Select Year", [2021, 2023])
data = data_2021 if year == 2021 else data_2023

# Country selection
countries = st.multiselect("Select Countries", options=data['Country'].unique().tolist())

# Plot: Horizontal stacked bar chart
def plot_stacked_bar(data, countries, categories):
    selected_data = data[data['Country'].isin(countries)].set_index('Country')[categories]
    selected_data.plot(
        kind='barh', stacked=True, figsize=(10, 6), colormap='cividis'
    )
    plt.title("Criminal Market Breakdown")
    plt.xlabel("Score")
    plt.ylabel("Country")
    plt.legend(title="Criminal Market")
    st.pyplot(plt)

# Plot: Radar chart
def plot_radar_chart(data, countries, categories):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]

    for country in countries:
        values = data[data['Country'] == country][categories].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=country)
        ax.fill(angles, values, alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title("Radar Chart: Criminal Market Breakdown")
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    st.pyplot(plt)

# Render UI
if not countries:
    st.write("Please select at least one country to view the analysis.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.write("Criminal Market Breakdown (Stacked Bar Chart)")
        plot_stacked_bar(data, countries, ["Human trafficking", "Arms trafficking", "Heroin trade", "Cannabis trade"])

    with col2:
        st.write("Criminal Market Profile (Radar Chart)")
        plot_radar_chart(data, countries, ["Human trafficking", "Arms trafficking", "Heroin trade", "Cannabis trade"])
