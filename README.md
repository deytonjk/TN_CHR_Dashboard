# US County Health Rankings Dashboard

## Overview
This project is an interactive web application built with Python and Streamlit for visualizing and analyzing time-series public health data from the County Health Rankings & Roadmaps (CHR&R) program. It allows users to monitor health trends across US counties, identify anomalies, and apply statistical modeling for predictive insights. The dashboard supports data exploration, trend forecasting (e.g., using ARIMA models), and customizable visualizations to aid decision-making in public health.

Key achievements:
- Processes multi-year CSV data from CHR&R, handling inconsistencies like varying column names and structures.
- Delivers actionable insights, such as forecasting health trends and highlighting inefficiencies.
- Resulted in a shift to a more efficient dashboard structure for end-users.

This was developed as part of a graduate project in Data Analytics, integrating skills in data manipulation, visualization, and predictive modeling.

## Demo
The app is live and running at: [https://us-chr-dashboard-v3.streamlit.app/](https://us-chr-dashboard-v3.streamlit.app/)

## Features
- **Interactive Visualizations**: Explore health metrics like rankings, demographics, and outcomes with filters for counties, states, and years.
- **Time-Series Analysis**: View trends over time and detect anomalies using statistical methods.
- **Predictive Modeling**: Forecast future health trends based on historical data.
- **Data Integration**: Combines data from multiple CSV sources, with support for databases like MySQL or DuckDB for efficient querying.
- **Customizable Views**: Users can select specific metrics and generate reports.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Streamlit for the web interface
- **Libraries**: Pandas (data manipulation), NumPy (numerical computing), Matplotlib/Seaborn (visualizations), Scikit-learn/Statsmodels (modeling and forecasting), SQLAlchemy (database connections if used)
- **Data Sources**: CSV files from [countyhealthrankings.org](https://www.countyhealthrankings.org/)

## Installation
1. Clone the repository:
   git clone https://github.com/deytonjk/TN_CHR_Dashboard.git
2. Navigate to the project directory
   cd TN_CHR_Dashboard
3. Install dependencies
   pip install -r requirements.txt
(Note: If requirements.txt is missing, install core libraries: `pip install streamlit pandas numpy matplotlib scikit-learn statsmodels`)

4. Download original data CSVs from [countyhealthrankings.org](https://www.countyhealthrankings.org/) and place them in the project directory (or configure paths in the code). Data is year-specific with varying columns.

## Usage
Run the app locally:
streamlit run US_CHR_Dashboard_v3.py

- Open your browser to the provided local URL (e.g., http://localhost:8501).
- Use the sidebar to filter by state, county, year, or metrics.
- Explore tabs for visualizations, predictions, and raw data views.

For database integration (optional, if using MySQL/DuckDB):
- Set up a local database and import CSVs.
- Update connection strings in the code.

## Data Handling
- Raw data comes in separate CSVs per year which were combined into one Excel file with multiple sheets,          handling missing values, column changes, and time-series alignment.  Unfortunately, the process for this was not correctly saved, so the Excel file will need to be downloaded from this repository

## Contributing
Feel free to fork and submit pull requests for enhancements, such as adding more predictive models or improving UI.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For questions or collaboration, reach out via [LinkedIn](https://www.linkedin.com/in/joshuadeyton) or email: joshuakdeyton@gmail.com.
