import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import plotly.graph_objects as go


#VERSION 3 - THIS VERSION LOADS UP ALL THE DATA INTO SEPARATE DATAFRAMES FOR EACH YEAR

#PAGE TITLE
st.set_page_config(
    page_title="US County Health Data",
        page_icon=":hospital",
        layout="wide"
)
st.title("County Comparisons by Year")

st.sidebar.success("")

if 'df2009' in st.session_state:
    

    df_list = [st.session_state.df2009, st.session_state.df2010, st.session_state.df2011, st.session_state.df2012, 
               st.session_state.df2013, st.session_state.df2014, st.session_state.df2015, st.session_state.df2016, 
               st.session_state.df2017, st.session_state.df2018, st.session_state.df2019, st.session_state.df2020, 
               st.session_state.df2021, st.session_state.df2022, st.session_state.df2023]

    #function to create bar chart for chosen counties within a state
    def bar_plot(year, state_choice, counties, topic):
         
        #get data from proper df, add year, and add to complete df for plotting
        bar_data = st.session_state[f'df{year}']
        if topic in bar_data.columns:
            #initialize a data frame
            chart_data = {
                    'name': ['county'],
                    f'{topic}': [7.0]
                    }
            chart_data_df = pd.DataFrame(chart_data)
            for county in counties:
                b_data_row = bar_data[(bar_data['state_abbreviation'] == state_choice) & (bar_data['name'] == county)][['name', topic]] 
                chart_data_df=pd.concat([chart_data_df,b_data_row])
            
            chart_data_df=chart_data_df.drop(0, axis=0) #get rid of the initiating row
    
        st.write(f'{year} data for {chosen_topic}')        
        st.bar_chart(chart_data_df, x='name', y=topic, 
                     x_label=topic, y_label='County', horizontal=True,  use_container_width=True)              

    def bar_table(year, state_choice, counties, topic):

     #get data from proper df, add year, and add to complete df for plotting
        bar_data = st.session_state[f'df{year}']
        if topic in bar_data.columns:
            #initialize a data frame
            chart_data = {
                    'name': ['county'],
                    f'{topic}': [7.0]
                    }
            chart_data_df = pd.DataFrame(chart_data)
            for county in counties:
                b_data_row = bar_data[(bar_data['state_abbreviation'] == state_choice) & (bar_data['name'] == county)][['state_abbreviation','name', topic]] 
                chart_data_df=pd.concat([chart_data_df,b_data_row])
            
            chart_data_df=chart_data_df.drop(0, axis=0) #get rid of the initiating row
    
        sorted_chart = chart_data_df.sort_values(by=f'{topic_title}', ascending=True)
        sorted_chart['Rank (lowest value)']=range(1,len(sorted_chart)+1)
        ranked_chart = sorted_chart.set_index('Rank (lowest value)')
        return ranked_chart



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
        abbr_state = st.session_state.df2009[(st.session_state.df2009['name'] == state)]['state_abbreviation'].values[0]

        available_counties = st.session_state.df2009[(st.session_state.df2009['state_abbreviation'] == abbr_state)]['name']
        return available_counties

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
            #paper_bgcolor="lightgrey",
            height=200,
            margin=dict(l=10, r=10, t=50, b=10, pad=8),
        )
        st.plotly_chart(fig, use_container_width=False)


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
                          'poor or fair health': 'Proportion of adults reporting fair or poor health (age-adjusted).',
                          'poor physical health days':'Average number of physically unhealthy days reported in past 30 days (age-adjusted).', 
                           "poor mental health days": 'Average number of mentally unhealthy days reported in past 30 days (age-adjusted).', 
                           "low birthweight":'Proportion of live births with low birthweight (< 2,500 grams)', 
                           "adult smoking":'Proportion of adults who are current smokers (age-adjusted)', 
                           "adult obesity":'Proportion of the adult population (age 18 and older) that reports a body mass index (BMI) greater than or equal to 30 kg/m2 (age-adjusted).', 
                           "excessive drinking":'Proportion of adults reporting binge or heavy drinking (age-adjusted). ', 
                           "motor vehicle crash deaths":'Number of motor vehicle crash deaths per 100,000 population.', 
                           "teen births":'Number of births per 1,000 female population ages 15-19', 
                           "uninsured adults":'Proportion of adults under age 65 without health insurance.' , 
                           "preventable hospital stays":'Rate of hospital stays for ambulatory-care sensitive conditions per 100,000 Medicare enrollees.', 
                           "diabetes monitoring":'Proportion of adults aged 20 and above with diagnosed diabetes (age-adjusted).', 
                           "high school graduation":'Proportion of ninth-grade cohort that graduates in four years. ', 
                           "college degrees":'Proportion of adults ages 25-44 with some post-secondary education.' , 
                           "unemployment":'Proportion of population ages 16 and older unemployed but seeking work.', 
                           "children in poverty":'Proportion of people under age 18 in poverty.',
                           "income inequality":'Ratio of household income at the 80th percentile to income at the 20th percentile. ', 
                           "single-parent households":'Proportion of children that live in a household headed by a single parent',
                           "homicides": 'Number of deaths due to homicide per 100,000 population.', 
                           "air pollution-particulate matter days" : 'Average daily density of fine particulate matter in micrograms per cubic meter (PM2.5). ', 
                           "access to healthy foods":'Proportion of population who are low-income and do not live close to a grocery store.',
                          }


    #click button to retrieve the trend chart
    year = st.slider('Select a year:',2009, 2023)

    x = chosen_topic.replace(' ','_')
    topic_title = x + '_raw_value'
    

    #find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
    abbr_state = st.session_state.df2009[(st.session_state.df2009['name'] == state_choice)]['state_abbreviation'].values[0]

    col1, col2 = st.columns([2,1], gap="small", vertical_alignment="top")

    with col1:    
    
         #include definition if exists
        if chosen_topic in category_explanation:
            st.markdown(f'About {chosen_topic}:  {category_explanation[chosen_topic]}')
    
        bar_plot(year, abbr_state, chosen_counties, topic_title)
    
    #SHOW MAP WITH CHOSEN COUNTIES HIGHLIGHTED WITH DOTS SIZED BY RANK
        if chosen_counties:    
    #create a dataframe that adds lat and long to the data
            county_loc_df = pd.DataFrame(pd.read_csv('./USA_county_seats.csv'))

            county_loc_df['County'] = county_loc_df['County'] + ' County'
            county_loc_df['County'] = county_loc_df['County'].str.strip()


            ranked_df = bar_table(year, abbr_state, chosen_counties, topic_title)
            ranked_df = ranked_df.rename(columns={'name': 'County', 'state_abbreviation': 'State'})
            # Merge DataFrames based on matching columns
            merged_df = pd.merge(
                ranked_df,
                county_loc_df,
                on=['County', 'State'],  # Match on these common columns
                how='left'              # Inner join to keep only matching rows
            )

 

        # Create the figure
            fig = go.Figure(go.Scattermapbox(
                lat=merged_df['Latitude'],
                lon=merged_df['Longitude'],
                mode='markers',
                marker=dict(size=ranked_df.index + 10),
                text=merged_df['County'],
            ))

            # Set the map layout
            fig.update_layout(
                mapbox=dict(
                    style="carto-positron",  # Use a map style from Mapbox
                    center=dict(lat=merged_df.at[0,'Latitude'], lon=merged_df.at[0,'Longitude']),  # Center the map
                    zoom=4  # Set the initial zoom level
                ),
                margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Remove margins
            )
             # Show the figure
            st.plotly_chart(fig)

        else:
            st.write('Please select some counties to generate map.')

    
   

    with col2:
    
        st.dataframe(bar_table(year, abbr_state, chosen_counties, topic_title), use_container_width=True)

        bar_data1 = st.session_state[f'df{year}']
        bar_data_state = bar_data1[(bar_data1['state_abbreviation'] == abbr_state)]
        sorted_bardata1=bar_data_state.sort_values(by=f'{topic_title}', ascending=True)
        sorted_bardata1['Rank (lowest value)']=range(1,len(sorted_bardata1)+1)
        sorted_bardata1 = sorted_bardata1.set_index('Rank (lowest value)')
        best = sorted_bardata1.at[1,'name']
        worst = sorted_bardata1.tail(1)['name'].values[0]
        plot_gauge(sorted_bardata1.at[1,topic_title], 'blue', '', f'Best in State: {best}', sorted_bardata1[topic_title].max())
        plot_gauge(sorted_bardata1.tail(1)[topic_title].values[0], 'blue', '', f'Worst in State: {worst}', sorted_bardata1[topic_title].max())
        st.markdown(category_explanation[chosen_topic])
else:
     st.write('Unfortunately, the data did not load correctly.  Please return to the main dashboard page before returning to create these charts.')
