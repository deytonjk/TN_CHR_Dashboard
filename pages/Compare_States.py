import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st



#PAGE TITLE
st.set_page_config(
    page_title="US County Health Data",
        page_icon=":hospital",
        layout="wide"
)
st.title("Compare State Trends (2009-2023)")


if 'df2009' in st.session_state:


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
    df_list = [st.session_state.df2009, st.session_state.df2010, st.session_state.df2011, st.session_state.df2012, 
               st.session_state.df2013, st.session_state.df2014, st.session_state.df2015, st.session_state.df2016, 
               st.session_state.df2017, st.session_state.df2018, st.session_state.df2019, st.session_state.df2020, 
               st.session_state.df2021, st.session_state.df2022, st.session_state.df2023]


    #function to create a trend plot for state comparison
    def state_trend_plot(states, topic2):
        YR2 = 2009
        #initialize the big data frame
        big_trend_data2 = {
                    'year': [YR2],
                    'name': ['state'],
                    f'{topic2}': [7.0]
                    }
        big_trend_df2 = pd.DataFrame(big_trend_data2)
    
             
        #get data from proper df, add year, and add to complete df for plotting
        for df in df_list:
            if topic2 in df.columns:
                #initialize a data frame
                trend_data2 = {
                    'year': [YR2],
                    'name': ['state'],
                    f'{topic2}': [7.0]
                    }
                trend_data_df2 = pd.DataFrame(trend_data2)
                for state in states:
                    t_data_row2 = df[(df['name'] == state)][['name', topic2]] 
                    #insert a year column so the graph can know from which year the data is retrieved
                    t_data_row2.insert(0, 'year', YR2)
                    trend_data_df2=pd.concat([trend_data_df2,t_data_row2])
            
                trend_data_df2=trend_data_df2.drop(0, axis=0) #get rid of the initiating row
         
            #add the year data to the bigger dataframe
            big_trend_df2=pd.concat([big_trend_df2, trend_data_df2])
            YR2+=1
        big_trend_df2=big_trend_df2.drop(0, axis=0) #get rid of the initiating row


            

        fig = px.line(
            big_trend_df2,
            x= 'year',
            y= topic2,
            color= 'name',
            markers=True,
            title= states_chosen_topic,

            )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)



    #user needs to pick a state to get the list of counties in that state
    states_list2 = [ "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", 
                   "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
                   "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
                   "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
                   "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                   "West Virginia", "Wisconsin", "Wyoming"]


    #drop box for selecting the states
    state_choices = st.multiselect('To begin, please select some states:', states_list2)

    #get choices for column titles
    states_chosen_topic = st.selectbox('Please choose a topic:', ["premature death", "poor or fair health", "poor physical health days", 
                                "poor mental health days", "low birthweight", "adult smoking", "adult obesity", "excessive drinking", 
                                "motor vehicle crash deaths", "chlamydia rate", "teen births", "uninsured adults", 
                                "preventable hospital stays", "diabetes monitoring", "hospice use", "high school graduation", 
                                "college degrees", "unemployment", "children in poverty", "income inequality", "inadequate social support", 
                                "single-parent households", "violent crime", "homicides", "air pollution-particulate matter days", 
                                "air pollution-ozone days", "access to healthy foods", "liquor store density", "smoking during pregnancy", 
                                "motor vehicle crash occupancy rate", "on-road motor vehicle crash-related er visits", 
                                "off-road motor vehicle crash-related er visits", "no recent dental visit", "did not get needed health care", 
                                "lead poisoned children (wi)", "municipal water (wi)", "contaminants in municipal water (wi)"])

    #click button to retrieve the trend chart

    if st.button('Click here to create the chart'):
        #fix chosen topic to match column titles in the data set (put back in the _ and _raw_value)
        y = states_chosen_topic.replace(' ','_')
        states_topic_title = y + '_raw_value'
    
    
        state_trend_plot(state_choices, states_topic_title)
    
        #include definition if exists
        if states_chosen_topic in category_explanation:
            st.markdown(f'About {states_chosen_topic}:  {category_explanation[states_chosen_topic]}')

else: 
    st.write('Unfortunately, the data did not load correctly.  Please return to the main dashboard page before returning to create these charts.')
