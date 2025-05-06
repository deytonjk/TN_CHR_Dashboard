
#This page will let the user choose features to run through some ml models

import pandas as pd
import numpy as np
from numpy import array
import streamlit as st
import altair as alt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")  # Suppress convergence warnings
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from scipy.stats import norm
import pmdarima as pm



#VERSION 3 - THIS VERSION LOADS UP ALL THE DATA INTO SEPARATE DATAFRAMES FOR EACH YEAR

#PAGE TITLE
st.set_page_config(
    page_title="US County Health Data",
        page_icon=":hospital",
        layout="wide"
)
st.title("Forecasting")


   

# verify that data is available
if 'df2009' in st.session_state:
    df_list = [st.session_state.df2009, st.session_state.df2010, st.session_state.df2011, st.session_state.df2012, 
               st.session_state.df2013, st.session_state.df2014, st.session_state.df2015, st.session_state.df2016, 
               st.session_state.df2017, st.session_state.df2018, st.session_state.df2019, st.session_state.df2020, 
               st.session_state.df2021, st.session_state.df2022, st.session_state.df2023]

    
    def trend_plot_data(state_choice, county, topic):
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
                t_data_row = df[(df['state_abbreviation'] == state_choice) & (df['name'] == county)][['name', topic]] 
                #insert a year column so the graph can know from which year the data is retrieved
                t_data_row.insert(0, 'year', YR)
                trend_data_df=pd.concat([trend_data_df,t_data_row])
            
                trend_data_df=trend_data_df.drop(0, axis=0) #get rid of the initiating row
         
            #add the year data to the bigger dataframe
            big_trend_df=pd.concat([big_trend_df, trend_data_df])
            YR+=1
        big_trend_df=big_trend_df.drop(0, axis=0) #get rid of the initiating row
        big_trend_df['year']= pd.to_datetime(big_trend_df['year'], format='%Y') #change the number to an actual year in datetime
        
        return big_trend_df


    
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



    #drop box for selecting the state - this will change the available county selections
    state_choice = st.selectbox('To begin, please select a state:', states_list)



    #dropbox to select either the state and / or chose counties to compare
    chosen_county = st.selectbox('Please select one county for forecasting.  Choosing the state will provide the average value for the entire state:', state_county_list(state_choice))

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


            

    


    if st.button('Click here to for the 5 - year forecast (ARIMA Model).'):
        
        #fix chosen topic to match column titles in the data set (put back in the _ and _raw_value)
        x = chosen_topic.replace(' ','_')
        topic_title = x + '_raw_value'
    
        #find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
        abbr_state = st.session_state.df2009[(st.session_state.df2009['name'] == state_choice)]['state_abbreviation'].values[0]
        
        
        
        data = trend_plot_data(abbr_state, chosen_county, topic_title)

        

        # pull out the data for the county and topic and begin the ARIMA process
        county_df = data[(data['name']== chosen_county)][['year', topic_title]]

        county_df[chosen_topic]=county_df[topic_title]*100

        # TURN THE YEAR TO DATE-TIME OBJECT
        county_df['year']=pd.to_datetime(county_df['year'], format='%Y')

        # make the date the index
        county_df.index = county_df['year']


        # Sort the DataFrame by the Date index in ascending order
        county_df.sort_index(inplace=True)





        # determine stationary - repeat differences until reaching p-value < .05.  Limit degree (d) <= 3.    
        def find_stationary(df, topic):
            d = 0
            st_value = ''
            ADF_statistic = 0
            p_value = 0
    
    
            # Perform the Augmented Dickey-Fuller test on the original series
            result_original = adfuller(df[topic])        

            if result_original[1] < 0.05:   # p -value
                st_value = 'Stationary'
                ADF_statistic = result_original[0]
                p_value = result_original[1]
            else:     
        
                while d < 4 and st_value != 'Stationary':

                    # Apply differencing
                    d += 1
                    df[f'{topic}_diff'] = df[topic].diff()
            
                    # Perform the Augmented Dickey-Fuller test on the differenced series
                    result_diff = adfuller(df[f'{topic}_diff'].dropna())
            
                    if result_diff[1]<0.05:
                        st_value = 'Stationary'
                        ADF_statistic = result_diff[0]
                        p_value = result_diff[1]
    
            stationary_results = [ d, p_value, ADF_statistic ]
    
            return stationary_results



        topic_results = find_stationary(county_df, topic_title )

        if topic_results[0] == 4:
            
            
            model = pm.auto_arima(county_df[topic_title], 
                      start_p=0, start_q=0, 
                      max_p=3, max_q=3, 
                      max_d=3, 
                      stepwise=True, 
                      trace=True, 
                      error_action="ignore", 
                      suppress_warnings=True)
            #st.markdown(model.summary())
            
            forecasts, conf_int = model.predict(n_periods=5, return_conf_int=True)
            forecast_df = pd.DataFrame(forecasts, columns=['forecast']) 
            conf_df = pd.DataFrame(conf_int, columns=['lower_ci', 'upper_ci'])
            conf_df.index = forecast_df.index
            forecast_df['lower_ci'] = conf_df['lower_ci']
            forecast_df['upper_ci'] = conf_df['upper_ci']
            forecast_df['year'] = forecast_df.index
            
            # small df to connect the end of historical data to futue data (just for appearance)
            gap_df = pd.DataFrame({'year': [county_df.index[-1], forecast_df.year[0]], topic_title: [county_df[topic_title][-1], forecast_df['forecast'][0]]})

            # Create the chart with a dotted line
            connection = alt.Chart(gap_df).mark_line().encode(
                x='year',
                y=topic_title,
                strokeDash=alt.value( [4, 4]), #  Alternating dash and space lengths
                color = alt.value('green')
            )
    


            # display chart in streamlit
            # Create two columns: one for the chart, one for the legend
            col1, col2 = st.columns([3, 1])

            

            with col1:
                historical_line = alt.Chart(county_df).mark_line(point=True).encode(
                    alt.Y(topic_title).title(chosen_topic),
                    alt.X('year:T')
    
    
    
                    )

                forecast_band = alt.Chart(forecast_df).mark_errorband().encode(
                    alt.Y(
                        "upper_ci:Q",
                        scale=alt.Scale(zero=False),
        
                    ).title(chosen_topic),
                    alt.Y2("lower_ci:Q").title(chosen_topic),
                    alt.X("year:T"),
                    color = alt.value("red")
                )

                forecast_line = alt.Chart(forecast_df).mark_line(point=True).encode(
                    alt.Y("forecast").title(chosen_topic),
                    alt.X("year:T"),
                    color=alt.value("red")
                )


                chart = (historical_line + forecast_line + forecast_band + connection).properties(
                    width=600,
                    height=400,
                    title=f'{chosen_topic} with Auto-ARIMA Forecast and 95% Confidence Interval',
    
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
                
                   
            # Create standalone HTML legend
            legend_html = """
            <div style="font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ccc; width: 200px; margin-top: 10px;">
                <h4 style="margin: 0 0 10px 0;">Legend</h4>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 2px; background-color: #1f77b4; margin-right: 5px;"></div>
                    <span>Historical Data</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 2px; background-color: #FF0000; margin-right: 5px;"></div>
                    <span>Forecast</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 10px; background-color: #FF0000; opacity: 0.2; margin-right: 5px;"></div>
                    <span>Confidence Interval</span>
                </div>
            </div>
            """
            with col2:
                st.markdown(legend_html, unsafe_allow_html=True)

                if chosen_topic in category_explanation:
                    st.write('Definition:')
                    st.markdown(f'{chosen_topic}:  {category_explanation[chosen_topic]}')
                
            col3, col4 = st.columns([1, 1])
            
            with col3:
               st.markdown('Original Data Table')
               st.dataframe(county_df[['year', topic_title]], hide_index = True)
                
            
            with col4:
               st.markdown('Forecast Table')
               st.dataframe(forecast_df[['forecast','lower_ci', 'upper_ci']])
                    








        # THE DIFFERENCING METHOD FOUND d =< 3 so use it in the regular ARIMA process


        else:
            # find the best p and q values to go with d for the ARIMA model
            p_values = range(0, 3)
            q_values = range(0, 3)
    

            # Grid search
            best_aic = float("inf")
            best_params = None

            for p in p_values:
                for q in q_values:
                    try:
                        model = ARIMA(county_df[topic_title], order=(p, topic_results[0], q))
                        results = model.fit()
                        aic = results.aic
                        if aic < best_aic:
                            best_aic = aic
                            best_params = (p, topic_results[0], q)
            
                    except:
                        continue



            # Define and fit ARIMA model (order can be tuned)
            order = (p, topic_results[0], q)  # Example: ARIMA(1,1,1)
            model = ARIMA(county_df[topic_title], order=order)
            model_fit = model.fit()

            
            # Forecast 5 years 
            forecast_steps = 5
            forecast = model_fit.get_forecast(steps=forecast_steps)
            forecast_mean = forecast.predicted_mean
            forecast_ci = forecast.conf_int()

            # Create dates for forecast
            forecast_dates = pd.date_range(start=county_df.index[-1] + pd.offsets.YearBegin(1), 
                                          periods=forecast_steps, freq='YS')

            # Create forecast DataFrame
            forecast_df = pd.DataFrame({
                'year': forecast_dates,
                'forecast': forecast_mean,
                'lower_ci': forecast_ci.iloc[:, 0],
                'upper_ci': forecast_ci.iloc[:, 1]
            })

	
            # small df to connect the end of historical data to futue data (just for appearance)
            gap_df = pd.DataFrame({'year': [county_df.index[-1], forecast_df.year[0]], topic_title: [county_df[topic_title][-1], forecast_df['forecast'][0]]})

            # Create the chart with a dotted line
            connection = alt.Chart(gap_df).mark_line().encode(
                x='year',
                y=topic_title,
                strokeDash=alt.value( [4, 4]), #  Alternating dash and space lengths
                color = alt.value('green')
            )
    


            # display chart in streamlit
            # Create two columns: one for the chart, one for the legend
            col1, col2 = st.columns([3, 1])

            
            with col1:
                historical_line = alt.Chart(county_df).mark_line(point=True).encode(
                    alt.Y(topic_title).title(chosen_topic),
                    alt.X('year:T')
    
    
    
                    )

                forecast_band = alt.Chart(forecast_df).mark_errorband().encode(
                    alt.Y(
                        "upper_ci:Q",
                        scale=alt.Scale(zero=False),
        
                    ).title(chosen_topic),
                    alt.Y2("lower_ci:Q").title(chosen_topic),
                    alt.X("year:T"),
                    color = alt.value("red")
                )

                forecast_line = alt.Chart(forecast_df).mark_line(point=True).encode(
                    alt.Y("forecast").title(chosen_topic),
                    alt.X("year:T"),
                    color=alt.value("red")
                )


                chart = (historical_line + forecast_line + forecast_band + connection).properties(
                    width=600,
                    height=400,
                    title=f'{chosen_topic} with ARIMA({p}, {topic_results[0]}, {q}) Forecast and 95% Confidence Interval',
    
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
             

            # Create standalone HTML legend
            legend_html = """
            <div style="font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ccc; width: 200px; margin-top: 10px;">
                <h4 style="margin: 0 0 10px 0;">Legend</h4>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 2px; background-color: #1f77b4; margin-right: 5px;"></div>
                    <span>Historical Data</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 2px; background-color: #FF0000; margin-right: 5px;"></div>
                    <span>Forecast</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 10px; background-color: #FF0000; opacity: 0.2; margin-right: 5px;"></div>
                    <span>Confidence Interval</span>
                </div>
            </div>
            """
            with col2:
                st.markdown(legend_html, unsafe_allow_html=True)

                if chosen_topic in category_explanation:
                    st.write('Definition:')
                    st.markdown(f'{chosen_topic}:  {category_explanation[chosen_topic]}')

            col3, col4 = st.columns([1, 1])
            
            with col3:
               st.markdown('Original Data Table')
               st.dataframe(county_df[['year', topic_title]], hide_index = True)
                
            
            with col4:
               st.markdown('Forecast Table')
               st.dataframe(forecast_df[['forecast','lower_ci', 'upper_ci']])



    if st.button('Click here to for the 5 - year forecast (LSTM Model).'):
        
        #fix chosen topic to match column titles in the data set (put back in the _ and _raw_value)
        x = chosen_topic.replace(' ','_')
        topic_title = x + '_raw_value'
    
        #find the abbreviation for the state - this will match the abbreviation linked to the county in the dataframe
        abbr_state = st.session_state.df2009[(st.session_state.df2009['name'] == state_choice)]['state_abbreviation'].values[0]
        
        
        
        data = trend_plot_data(abbr_state, chosen_county, topic_title)

        

        # pull out the data for the county and topic and begin the ARIMA process
        county_df = data[(data['name']== chosen_county)][['year', topic_title]]

        
        # TURN THE YEAR TO DATE-TIME OBJECT
        county_df['year']=pd.to_datetime(county_df['year'], format='%Y')

        # make the date the index
        county_df.index = county_df['year']


        # Sort the DataFrame by the Date index in ascending order
        county_df.sort_index(inplace=True)


        # univariate data preparation
        

        
        # split the univariate sequence into samples
        def split_sequence(sequence, n_steps):
            X, y = list(), list()
            for i in range(len(sequence)):
		        # find the end of this pattern
                end_ix = i + n_steps
		        # check if we are beyond the sequence
                if end_ix > len(sequence)-1:
                    break
		        # gather input and output parts of the pattern
                seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
                X.append(seq_x)
                y.append(seq_y)
            return array(X), array(y)

        # Prepare data for LSTM
        raw_seq = county_df[topic_title].values
        n_steps = 3
        n_features = 1
        X, y = split_sequence(raw_seq, n_steps)
	
	# Define LSTM model
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(n_steps, n_features), return_sequences=True),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
	
	# Reshape data
        X = X.reshape((X.shape[0], X.shape[1], n_features))
	
	# Fit model
        model.fit(X, y, epochs=200, verbose=0)
	
	# Monte Carlo Dropout Prediction Function
        def mc_predict(model, x_input, n_mc=100):
            predictions = []
            for _ in range(n_mc):
                # Enable dropout during inference by setting training=True
                pred = model(x_input, training=True)
                predictions.append(pred.numpy()[0, 0])
            return np.array(predictions)
	
	# Forecast with confidence intervals
        n_mc = 100  # Number of Monte Carlo samples
        confidence_level = 0.95  # 95% confidence interval
        z_score = norm.ppf((1 + confidence_level) / 2)  # Z-score for 95% CI (~1.96)
	
        mean_forecasts = []
        lower_ci = []
        upper_ci = []
	
	# Initial input
        x_input = raw_seq[-n_steps:].reshape((1, n_steps, n_features))
	
	# Generate 5 forecasts
        for _ in range(5):
            # Get Monte Carlo predictions
            mc_predictions = mc_predict(model, x_input, n_mc=n_mc)
	    
	    # Compute mean and standard deviation
            mean_pred = np.mean(mc_predictions)
            std_pred = np.std(mc_predictions)
	    
	    # Compute 95% confidence interval
            margin_error = z_score * std_pred
            lower_bound = mean_pred - margin_error
            upper_bound = mean_pred + margin_error
	    
	    # Store results
            mean_forecasts.append(mean_pred)
            lower_ci.append(lower_bound)
            upper_ci.append(upper_bound)
	    
	    # Update input for next prediction
            if len(mean_forecasts) < n_steps:
                x_input = np.append(raw_seq[-(n_steps-len(mean_forecasts)):], mean_forecasts)
            else:
                x_input = np.array(mean_forecasts[-n_steps:])
	    
            x_input = x_input.reshape((1, n_steps, n_features))


        
        #  create the df for display and graphing
        forecast_dates = pd.date_range(start=county_df.index[-1] + pd.offsets.YearBegin(1), 
                                      periods=5, freq='YS')

        # Create forecast DataFrame
        forecast_df = pd.DataFrame({
            'year': forecast_dates,
	    'forecast': mean_forecasts,
            'lower_ci': lower_ci,
            'upper_ci': upper_ci
        })


        # small df to connect the end of historical data to futue data (just for appearance)
        gap_df = pd.DataFrame({'year': [county_df.index[-1], forecast_df.year[0]], topic_title: [county_df[topic_title][-1], forecast_df['forecast'][0]]})

            # Create the chart with a dotted line
        connection = alt.Chart(gap_df).mark_line().encode(
                x='year',
                y=topic_title,
                strokeDash=alt.value( [4, 4]), #  Alternating dash and space lengths
                color = alt.value('green')
            )
    


            # display chart in streamlit
            # Create two columns: one for the chart, one for the legend
        col1, col2 = st.columns([3, 1])

        

        with col1:
                historical_line = alt.Chart(county_df).mark_line(point=True).encode(
                    alt.Y(topic_title).title(chosen_topic),
                    alt.X('year:T')
    
    
    
                    )

                forecast_band = alt.Chart(forecast_df).mark_errorband(opacity=0.3).encode(
                    alt.Y(
                        "upper_ci:Q",
                        scale=alt.Scale(zero=False),
        
                    ).title(chosen_topic),
                    alt.Y2("lower_ci:Q").title(chosen_topic),
                    alt.X("year:T"),
                    color = alt.value("red")
                )

                forecast_line = alt.Chart(forecast_df).mark_line(point=True).encode(
                    alt.Y("forecast").title(chosen_topic),
                    alt.X("year:T"),
                    color=alt.value("red")
                )


                chart = (historical_line + forecast_line + forecast_band + connection).properties(
                    width=600,
                    height=400,
                    title=f'{chosen_topic} LSTM Forecast and 95% Confidence Interval',
    
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
                

        # Create standalone HTML legend
        legend_html = """
            <div style="font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ccc; width: 200px; margin-top: 10px;">
                <h4 style="margin: 0 0 10px 0;">Legend</h4>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 2px; background-color: #1f77b4; margin-right: 5px;"></div>
                    <span>Historical Data</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                    <div style="width: 20px; height: 2px; background-color: #FF0000; margin-right: 5px;"></div>
                    <span>Forecast</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 10px; background-color: #FF0000; opacity: 0.2; margin-right: 5px;"></div>
                    <span>Confidence Interval</span>
                </div>
            </div>
            """
        with col2:
                st.markdown(legend_html, unsafe_allow_html=True)

                if chosen_topic in category_explanation:
                    st.write('Definition:')
                    st.markdown(f'{chosen_topic}:  {category_explanation[chosen_topic]}')

        col3, col4 = st.columns([1, 1])
            
        with col3:
               st.markdown('Original Data Table')
               st.dataframe(county_df[['year', topic_title]], hide_index = True)
                
            
        with col4:
               st.markdown('Forecast Table')
               st.dataframe(forecast_df[['year','forecast','lower_ci', 'upper_ci']], hide_index = True)

else:
     st.write('Unfortunately, the data did not load correctly.  Please return to the main dashboard page before returning to create these charts.')
