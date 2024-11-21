import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import duckdb


#VERSION 2 - THIS VERSION LOADS UP ALL THE DATA INTO A DATAFRAME ON INITIAL PAGE LOADING
#THIS SPEEDS UP THE PROCESSING TIME FOR THE CHARTS

#PAGE TITLE
st.set_page_config(
    page_title="US County Health Rankings Report",
        page_icon=":hospital",
        layout="wide"
)
st.title("National Health Rankings by State and County")
st.markdown("Selected Data and Charts")



@st.cache_data
def load_data(data_year_start):
    df3 = pd.read_excel("./raw_data_file.xlsx", sheet_name=data_year_start)
    #insert a year column so the graph can know from which year the data is retrieved
    df3.insert(0, 'year', 2010)
    YR = 2011
    while YR < 2025:
        df2 = pd.read_excel("./raw_data_file.xlsx", sheet_name=f'{YR}_data')
        df2.insert(0,'year', YR)
        df3 = pd.concat([df3, df2])
        YR+=1
    return df3

df1=load_data('2010_data')

#function to create trend plot
def trend_plot(state_choice, counties, topic):
        
    #initialize a data frame
    trend_data = {
        'year': [2010],
        'name': ['county'],
        f'{topic}': [7.0]
        }
    trend_data_df = pd.DataFrame(trend_data)
    #find the for each county and add to a separate dataframe for visualization
    for county in counties:
        county_data = df1[(df1['state_abbreviation'] == state_choice) & (df1['name'] == county)][['year','name', topic]] 
        trend_data_df=pd.concat([trend_data_df,county_data])
            
    #drop the initializing data
    trend_data_df=trend_data_df.drop(0, axis=0) #get rid of the initializing row
    
    #use the dataframe to create trend line chart
    fig = px.line(
        trend_data_df,
        x= 'year',
        y= topic,
        color= 'name',
        markers=True,
        title= chosen_topic,

        )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)


#convert state name to abbreviation for table purposes
def state_abbr(state_name):
    #GET INITIAL DATA FROM CSV/EXCEL FILE
    df5 = pd.read_excel("./raw_data_file.xlsx", sheet_name='2010_data')
    state_info = duckdb.sql(
        f'''
        SELECT state_abbreviation
        FROM df5
            WHERE name = '{state_name}'
                    ''')
    return state_info.fetchone()[0]


#user needs to pick a state to get the list of counties in that state
states_list = ["United States", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
               "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
               "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
               "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
               "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
               "West Virginia", "Wisconsin", "Wyoming"]

#function to find the list of counties in the chosen state
def state_county_list(state):
    
    state_info = df1[(df1['state_abbreviation'] == state) & (df1['year'] == 2010)]['name']
    return state_info



#drop box for selecting the state - this will change the available county selections
state_choice = st.selectbox('To begin, please select a state:', states_list)


#find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
abbr_state = state_abbr(state_choice)


#dropbox to select either the state and / or chose counties to compare
chosen_counties = st.multiselect('Please select one or more counties.  Choosing the state will provide the average value for the entire state:', state_county_list(abbr_state))

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


#click button to retrieve the trend chart
if st.button('Click to see chart'):
   trend_plot(abbr_state, chosen_counties, topic_title)

