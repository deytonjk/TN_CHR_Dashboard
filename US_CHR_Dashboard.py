import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import duckdb

#PAGE TITLE
st.set_page_config(
    page_title="US County Health Rankings Report",
        page_icon=":hospital",
        layout="wide"
)
st.title("National Health Rankings by State and County")
st.markdown("Selected Data and Charts")

#GET INITIAL DATA FROM CSV/EXCEL FILE
df1 = pd.read_excel("./raw_data_file.xlsx", sheet_name='2010_data')


#convert state name to abbreviation for table purposes
def state_abbr(state_name):
    state_info = duckdb.sql(
        f'''
        SELECT state_abbreviation
        FROM df1
            WHERE name = '{state_name}'
                    ''')
    return state_info.fetchone()[0]

#user needs to pick a state to get the list of counties in that state
states_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
               "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
               "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
               "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
               "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
               "West Virginia", "Wisconsin", "Wyoming"]

state_choice = st.selectbox('To begin, please select a state:', states_list)

abbr_state = state_abbr(state_choice)

#function to find the list of counties in the chosen state
def state_county_list(state):
    state_info=duckdb.sql(
        f'''
        SELECT name
        FROM df1
            WHERE state_abbreviation = '{state}'
            ''')
    return state_info
chosen_counties = st.multiselect('Please select one or more counties:', state_county_list(abbr_state))

#get choices for column titles
chosen_topic = st.selectbox('Please select a health indicator:', ["premature death", "poor or fair health", "poor physical health days", 
                            "poor mental health days", "low birthweight", "adult smoking", "adult obesity", "excessive drinking", 
                            "motor vehicle crash deaths", "chlamydia rate", "teen births", "uninsured adults", 
                            "preventable hospital stays", "diabetes monitoring", "hospice use", "high school graduation", 
                            "college degrees", "unemployment", "children in poverty", "income inequality", "inadequate social support", 
                            "single-parent households", "violent crime", "homicides", "air pollution-particulate matter days", 
                            "air pollution-ozone days", "access to healthy foods", "liquor store density", "smoking during pregnancy", 
                            "motor vehicle crash occupancy rate", "on-road motor vehicle crash-related er visits", 
                            "off-road motor vehicle crash-related er visits", "no recent dental visit", "did not get needed health care", 
                            "lead poisoned children (wi)", "municipal water (wi)", "contaminants in municipal water (wi)"])
#fix chosen topic to match column titles in the data set (put back in the _ and _raw_value)
x = chosen_topic.replace(' ','_')
topic_title = x + '_raw_value'


def trend_plot(state_choice, counties, topic):
        
    YR = 2010
    #initialize the big data frame
    big_trend_data = {
                'year': [YR],
                'name': ['county'],
                f'{topic}': [7.0]
                }
    big_trend_df = pd.DataFrame(big_trend_data)
    while YR < 2025:
             
        #get data from spreadsheet
        df = pd.read_excel("./raw_data_file.xlsx", sheet_name=f'{YR}_data')
        if topic in df.columns:
            #initialize a data frame
            trend_data = {
                'year': [YR],
                'name': ['county'],
                f'{topic}': [7.0]
                }
            trend_data_df = pd.DataFrame(trend_data)
            for county in counties:
                t_data_row = df[(df['state_abbreviation'] == state_choice) & (df['name'] == county)][['name', topic]] 
                #insert a year column so the graph can know from which year the data is retrieved
                t_data_row.insert(0, 'year', YR)
                trend_data_df=pd.concat([trend_data_df,t_data_row])
            
            trend_data_df=trend_data_df.drop(0, axis=0) #get rid of the initiating row
         
        #add the year data to the bigger dataframe
        big_trend_df=pd.concat([big_trend_df, trend_data_df])
        YR+=1
    big_trend_df=big_trend_df.drop(0, axis=0) #get rid of the initiating row


            

    fig = px.line(
        big_trend_df,
        x= 'year',
        y= topic,
        color= 'name',
        markers=True,
        title= chosen_topic,

        )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)


#click button to retrieve the trend chart
if st.button('Click to see chart'):
   st.markdown(f'Here is your trend chart for {topic_title}. Please wait while we comb through 15 years of data.')
   trend_plot(abbr_state, chosen_counties, topic_title)
