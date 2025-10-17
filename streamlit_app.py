import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.set_page_config(
    page_title='Wine Quality Dashboard',
    page_icon=':wine_glass:',
)

# -----------------------------------------------------------------------------
# Função para carregar dados

@st.cache_data
def get_wine_data():
    DATA_FILENAME = Path(__file__).parent / 'data/wine_dataset.csv'
    df = pd.read_csv(DATA_FILENAME)
    return df

wine_df = get_wine_data()

# -----------------------------------------------------------------------------
# Página principal

'''
# :wine_glass: Wine Quality Dashboard

Explore wine data (red and white) from Portugal and analyze which factors
most influence wine quality.
'''

''
''

# Filtros
wine_types = wine_df['type'].unique().tolist()

selected_types = st.multiselect(
    'Select wine types:',
    wine_types,
    default=wine_types
)

filtered_df = wine_df[wine_df['type'].isin(selected_types)]

''
st.header('Quality distribution', divider='gray')
''
st.bar_chart(
    filtered_df.groupby('quality')['quality'].count()
)

''
st.header('Average metrics by wine type', divider='gray')
''
numeric_cols = [c for c in wine_df.columns if wine_df[c].dtype != 'object' and c != 'quality']

agg_df = filtered_df.groupby('type')[numeric_cols + ['quality']].mean().reset_index()
st.dataframe(agg_df, use_container_width=True)

''
st.header('Compare chemical properties', divider='gray')
''
x_var = st.selectbox('X-axis variable:', numeric_cols, index=numeric_cols.index('alcohol') if 'alcohol' in numeric_cols else 0)
y_var = st.selectbox('Y-axis variable:', numeric_cols, index=numeric_cols.index('quality') if 'quality' in numeric_cols else 0)

st.scatter_chart(filtered_df, x=x_var, y=y_var, color='type')

''
st.header('Quality summary', divider='gray')
''
cols = st.columns(len(selected_types))

for i, t in enumerate(selected_types):
    col = cols[i % len(cols)]
    with col:
        avg_quality = filtered_df[filtered_df['type'] == t]['quality'].mean()
        st.metric(
            label=f'{t.title()} Wine Quality',
            value=f'{avg_quality:.2f}'
        )
