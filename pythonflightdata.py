import streamlit as st
from dbconnector1 import dbconn
import plotly.graph_objects as go 
import plotly.express as px 
db=dbconn()
st.sidebar.title('Flight analytics')
user_option=st.sidebar.selectbox('Menu',['Select One','Check Flights','Analytics'])
if user_option=='Check Flights':
    st.title('Check Flights')
    col1,col2=st.columns(2) 
    city=db.fetch_all_cities()
    with col1:
        source=st.selectbox('Source',sorted(city))
    with col2:
        destination=st.selectbox('Destination',sorted(city))
    if st.button('Search'):
        results=db.fetch_all_flights(source,destination) 
        st.dataframe(results)
elif user_option=='Analytics':
    airline,frequency=db.fetch_flight_frequency()
    fig=go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="percent+label"
        )
    )
    st.header("Piechart")
    st.plotly_chart(fig)
    city,frequency=db.busiest_cities()
    fig=px.bar(
        x=city,
        y=frequency
    )
    st.plotly_chart(fig,theme='streamlit',use_container_width=True)
    date,frequency=db.daily_frequency()
    fig=px.line(
        x=date,
        y=frequency
    )
    st.plotly_chart(fig,theme='streamlit',use_container_width=True)