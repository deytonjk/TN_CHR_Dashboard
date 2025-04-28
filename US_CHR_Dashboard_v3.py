import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st



#VERSION 3 - THIS VERSION LOADS UP ALL THE DATA INTO SEPARATE DATAFRAMES FOR EACH YEAR

#PAGE TITLE
st.set_page_config(
    page_title="US County Health Rankings Report",
        page_icon=":hospital",
        layout="wide"
)
st.title("National Health Rankings by State and County")

overview = '''This website offers interactive charts showcasing health indicators U.S. states and counties, using data from the County Health Rankings (CHR) project, managed by the University of Wisconsin's Population Health Institute. The CHR project compiles health metrics for over 3,000 U.S. counties and cities, with data available from 2009 onward.  
Users can explore health trends through customizable percentile and time series charts.  Thee platform allows users to select specific indicators, years, counties, and states to create personalized visualizations, with the option to download charts as PNG files for further use or analysis.'''

st.markdown("OVERVIEW")
st.markdown(overview)

st.markdown("Compare County Trends from 2009-2023:")


@st.cache_data
def load_data(data_year_start):
    df = pd.read_excel("./raw_data_file.xlsx", sheet_name=data_year_start)
    return(df)
    

df2009=load_data('2010_data')
df2010=load_data('2011_data')
df2011=load_data('2012_data')
df2012=load_data('2013_data')
df2013=load_data('2014_data')
df2014=load_data('2015_data')
df2015=load_data('2016_data')
df2016=load_data('2017_data')
df2017=load_data('2018_data')
df2018=load_data('2019_data')
df2019=load_data('2020_data')
df2020=load_data('2021_data')
df2021=load_data('2022_data')
df2022=load_data('2023_data')
df2023=load_data('2024_data')



df_list = [df2009, df2010, df2011, df2012, df2013, df2014, df2015, df2016, df2017, df2018, df2019, 
           df2020, df2021, df2022, df2023]

if 'df2009' not in st.session_state:
    st.session_state['df2009'] = df2009
if 'df2010' not in st.session_state:
    st.session_state['df2010'] = df2010
if 'df2011' not in st.session_state:
    st.session_state['df2011'] = df2011
if 'df2012' not in st.session_state:
    st.session_state['df2012'] = df2012
if 'df2013' not in st.session_state:
    st.session_state['df2013'] = df2013
if 'df2014' not in st.session_state:
    st.session_state['df2014'] = df2014
if 'df2015' not in st.session_state:    
    st.session_state['df2015'] = df2015
if 'df2016' not in st.session_state:
    st.session_state['df2016'] = df2016
if 'df2017' not in st.session_state:
    st.session_state['df2017'] = df2017
if 'df2018' not in st.session_state:
    st.session_state['df2018'] = df2018
if 'df2019' not in st.session_state:
    st.session_state['df2019'] = df2019
if 'df2020' not in st.session_state:
    st.session_state['df2020'] = df2020
if 'df2021' not in st.session_state:
    st.session_state['df2021'] = df2021
if 'df2022' not in st.session_state:
    st.session_state['df2022'] = df2022
if 'df2023' not in st.session_state:
    st.session_state['df2023'] = df2023

#function to create trend plot
def trend_plot(state_choice, counties, topic):
        
    YR = 2009
    #initialize the big data frame
    big_trend_data = {
                'year': [YR],
                'name': ['county'],
                f'{topic}': [7.0]
                }
    big_trend_df = pd.DataFrame(big_trend_data)
    
             
    #get data from proper df, add year, and add to complete df for plotting
    for df in df_list:
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

    
#function to view the dataset for the trend plot
def trend_plot_data(state_choice, counties, topic):
    YR = 2009
    #initialize the big data frame
    big_trend_data = {
                'year': [YR],
                'name': ['county'],
                f'{topic}': [7.0]
                }
    big_trend_df = pd.DataFrame(big_trend_data)
    
             
    #get data from proper df, add year, and add to complete df for plotting
    for df in df_list:
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
    
    st.dataframe(big_trend_df)


#user needs to pick a state to get the list of counties in that state
states_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
               "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
               "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
               "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
               "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
               "West Virginia", "Wisconsin", "Wyoming"]

#function to find the list of counties in the chosen state
def state_county_list(state):
    
    #find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
    abbr_state = df2009[(df2009['name'] == state)]['state_abbreviation'].values[0]

    available_counties = df2009[(df2009['state_abbreviation'] == abbr_state)]['name']
    return available_counties



#drop box for selecting the state - this will change the available county selections
state_choice = st.selectbox('To begin, please select a state:', states_list)



#dropbox to select either the state and / or chose counties to compare
chosen_counties = st.multiselect('Please select one or more counties.  Choosing the state will provide the average value for the entire state:', state_county_list(state_choice))

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

#dictionary containing explanations of (most) categories
category_explanation={'premature death': 'Years of potential life lost before age 75 per 100,000 population (age-adjusted).',
                      'poor or fair health': 'Percentage of adults reporting fair or poor health (age-adjusted).',
                      'poor physical health days':'Average number of physically unhealthy days reported in past 30 days (age-adjusted).', 
                       "poor mental health days": 'Average number of mentally unhealthy days reported in past 30 days (age-adjusted).', 
                       "low birthweight":'Percentage of live births with low birthweight (< 2,500 grams)', 
                       "adult smoking":'Percentage of adults who are current smokers (age-adjusted)', 
                       "adult obesity":'Percentage of the adult population (age 18 and older) that reports a body mass index (BMI) greater than or equal to 30 kg/m2 (age-adjusted).', 
                       "excessive drinking":'Percentage of adults reporting binge or heavy drinking (age-adjusted). ', 
                       "motor vehicle crash deaths":'Number of motor vehicle crash deaths per 100,000 population.', 
                       "teen births":'Number of births per 1,000 female population ages 15-19', 
                       "uninsured adults":'Percentage of adults under age 65 without health insurance.' , 
                       "preventable hospital stays":'Rate of hospital stays for ambulatory-care sensitive conditions per 100,000 Medicare enrollees.', 
                       "diabetes monitoring":'Percentage of adults aged 20 and above with diagnosed diabetes (age-adjusted).', 
                       "high school graduation":'Percentage of ninth-grade cohort that graduates in four years. ', 
                       "college degrees":'Percentage of adults ages 25-44 with some post-secondary education.' , 
                       "unemployment":'Percentage of population ages 16 and older unemployed but seeking work.', 
                       "children in poverty":'Percentage of people under age 18 in poverty.',
                       "income inequality":'Ratio of household income at the 80th percentile to income at the 20th percentile. ', 
                       "single-parent households":'Percentage of children that live in a household headed by a single parent',
                       "homicides": 'Number of deaths due to homicide per 100,000 population.', 
                       "air pollution-particulate matter days" : 'Average daily density of fine particulate matter in micrograms per cubic meter (PM2.5). ', 
                       "access to healthy foods":'Percentage of population who are low-income and do not live close to a grocery store.',
                      }


#click button to retrieve the trend chart

if st.button('Click to see chart'):
    #fix chosen topic to match column titles in the data set (put back in the _ and _raw_value)
    x = chosen_topic.replace(' ','_')
    topic_title = x + '_raw_value'
    
    #find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
    abbr_state = df2009[(df2009['name'] == state_choice)]['state_abbreviation'].values[0]
    
    #include definition if exists
    if chosen_topic in category_explanation:
        st.markdown(f'About {chosen_topic}:  {category_explanation[chosen_topic]}')

    trend_plot(abbr_state, chosen_counties, topic_title)
    
    

if st.button('Click to see the data in table form'):
    #fix chosen topic to match column titles in the data set (put back in the _ and _raw_value)
    x = chosen_topic.replace(' ','_')
    topic_title = x + '_raw_value'
    
    #find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
    abbr_state = df2009[(df2009['name'] == state_choice)]['state_abbreviation'].values[0]
    
    #include definition if exists
    if chosen_topic in category_explanation:
        st.markdown(f'About {chosen_topic}:  {category_explanation[chosen_topic]}')
       
    trend_plot_data(abbr_state, chosen_counties, topic_title)



