import streamlit as st
import pandas as pd
import altair as alt

from urllib.error import URLError

@st.cache
def get_UN_data():
    df = pd.read_csv("Reporte Marzo.csv")
    return df.set_index("Modelo")

try:
    df = get_UN_data()
    modelo = st.multiselect(
        "Selecionna modelos", list(df.index), ["Real", "Hawkes H7"]
    )
    if not modelo:
        st.error("Por favor seleccione un modelo")
    else:
        data = df.loc[modelo]
        st.write("### Casos de covid diarios", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "Fecha", "value": "Casos de covid diarios"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="Fecha:T",
                y=alt.Y("Casos de covid diarios:Q", stack=None),
                color="Modelo:N",
            )
        )
        day_to_filter = st.slider('day', 1, 31, 15)  # min: 0h, max: 23h, default: 17h
        
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )