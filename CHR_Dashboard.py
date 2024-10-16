import random
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#PAGE TITLE
st.set_page_config(
    page_title="County Health Rankings Report",
        page_icon=":hospital",
        layout="wide"
)
st.title("Tennessee County Health Rankings")
st.markdown("Selected Data and Charts")


#GET DATA FROM CSV/EXCEL FILE
@st.cache_data
def load_data(path: str):
    data = pd.read_excel(path)
    return data

df=load_data("./TN_CHR_data2024.xlsx")

#display the uploaded file in dropdown
with st.expander("2024 Data Preview"):
    st.dataframe(
        df,
    )


# GAUGE METHOD
def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 18,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 18},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=False)


#Metric Method
def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 20,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=False)


#Life Expectancy Chart Method
def plot_LIFE_exp():
    fig = px.bar(df, x='County', y='Life Expectancy raw value',
             hover_data=['Population raw value', '% Rural raw value'], color='Population raw value',
             labels={'County':'County'}, height=400,
             title= "Life Expectancy by County",
             color_continuous_scale=px.colors.sequential.Sunsetdark_r
)
    st.plotly_chart(fig, use_container_width=True)
        





st.header(":orange[Tennessee State Averages and Totals - 2024]", divider="orange")

#PAGE LAYOUT - UNDER DATA PREVIEW AND BAR GRAPH
top_left_column, top_right_column = st.columns((2, 1))
bottom_left_column, bottom_right_column = st.columns(2)

with top_left_column:
    column_1, column_2, column_3, column_4 = st.columns(4)

    with column_1:
        
        plot_gauge(361, "#FF8700", " days", "Good Physical Health Days/Year", 365)

        plot_metric("Preventable Hospital Stays", 2896, prefix="", suffix="", show_graph=True, color_graph="rgba(0, 104, 201, 0.2)", )

    with column_2:
        
        plot_gauge(359.2, "#708090", " days", "Good Mental Health Days/Year", 365)

        plot_metric("Uninsured", 11.8, prefix="", suffix="%", show_graph=False,)

        
    with column_3:
        plot_gauge(35.5, "#ffff00", "%", "Adult Obesity", 100)
        
        plot_metric("Population per Mental Health Professional", 532, prefix="", suffix="", show_graph=True, color_graph="rgba(246, 150, 200, 0.8)", )


    with column_4:
        plot_gauge(67.4, "#66ff33", "%", "Access to Exercise Opportunities", 100)

        plot_metric("Unemployment", 3.4, prefix="", suffix="%", show_graph=False,)


with top_right_column:
    
    plot_LIFE_exp()


#Choose which metrics to compare
st.header(":orange[Statewide County Metric Comparison]")
option = st.selectbox(
    "Choose which metric to compare between counties:",
    ("Poor or Fair Health raw value", 
     "Poor Physical Health Days raw value", 
     "Poor Mental Health Days raw value",
     "Low Birthweight raw value",
     "Adult Smoking raw value",
     "Adult Obesity raw value",
     "Food Environment Index raw value",
     "Physical Inactivity raw value",
     "Access to Exercise Opportunities raw value",
     "Excessive Drinking raw value",
     "Alcohol-Impaired Driving Deaths raw value",
     "Sexually Transmitted Infections raw value",
     "Teen Births raw value",
     "Uninsured raw value",
     "Primary Care Physicians raw value",
     "Ratio of population to primary care physicians.",
     "Dentists raw value",
     "Ratio of population to dentists.",
     "Mental Health Providers raw value",
     "Ratio of population to mental health providers."
    
     ),
)

#click button to activate chart
if st.button('Click to show your choice'):
    fig = px.bar(df, y=option, x='County', text_auto='.2s',
            title=option,
)
    st.plotly_chart(fig) 
else: "Waiting for your selection..."



st.header(":orange[County Seat Locations]")
st.map(df, latitude="LAT", longitude="LON", color="#ff9900", use_container_width=True)


st.header(":orange[Five-Year Premature Death Data for Select Counties]")
df=load_data("./TN_County_Premature_D_5_Year.xlsx")
all_years = ['2019','2020','2021','2022','2023']
def plot_bottom_left():
        trend_data=duckdb.sql(
            f"""
            WITH trend_data AS (
                SELECT *
                FROM df
                WHERE Name ='Shelby County'
                    OR Name = 'Williamson County'
                    OR Name = 'Sullivan County'
                    OR Name = 'Washington County'
                    OR Name = 'Knox County'                
                )
                UNPIVOT trend_data
                ON {',' .join(all_years)}
                INTO
                    NAME year
                    VALUE deaths
           
        """
        ).df()

        fig = px.line(
            trend_data,
            x= 'year',
            y='deaths',
            color='Name',
            markers=True,
            title="Five-Year Premature Death Raw Numbers",

        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

        
        st.dataframe(trend_data)

       

        

plot_bottom_left()

