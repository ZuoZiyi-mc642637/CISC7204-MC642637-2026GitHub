"""CISC3015 Assignment 02 - Module 05 Practice Project - Part 2
Dashboard to display charts based on the selected Region and Year.

Run locally:
    python Dash_wildfire.py
then open http://127.0.0.1:8050 in a browser.
(In Theia: Terminal -> New Terminal -> python Dash_wildfire.py, note the port,
then Launch Application -> 8050.)
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
import os

# ----------------------------------------------------------------------------
# Create app
# ----------------------------------------------------------------------------
app = dash.Dash(__name__)

# Clear the layout and do not display exceptions till the callback gets executed
app.config.suppress_callback_exceptions = True

# ----------------------------------------------------------------------------
# Read the wildfire data into a pandas dataframe
# (local copy first, so the dashboard also works offline; falls back to the URL)
# ----------------------------------------------------------------------------
URL = ('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
       'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Look for the local copy first: next to this script, or inside the data/ folder
# used by the Part 1 notebook. Falls back to the cloud URL if neither exists.
for _path in ('data/Historical_Wildfires.csv', 'Historical_Wildfires.csv'):
    if os.path.exists(_path):
        df = pd.read_csv(_path)
        print(f'Loaded local data: {_path}')
        break
else:
    df = pd.read_csv(URL)
    print('Loaded data from IBM cloud storage')

# Extract year and month from the date column
# NOTE: month_name() returns names in ALPHABETICAL order when plotted, which matches
#       the reference layout of this lab (April, August, December, ...).
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df['Month'] = df['Date'].dt.month_name()   # used for the names of the months
df['Year'] = df['Date'].dt.year

YEARS = sorted(df['Year'].unique().tolist())   # .tolist() keeps the options JSON-serialisable

# ----------------------------------------------------------------------------
# Layout Section of Dash
# ----------------------------------------------------------------------------

# TASK 2.1: Add the Title to the Dashboard
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),

    # outer division starts
    html.Div([

        # ------------------------------------------------------------------
        # First inner division: the INPUT components (radio items + dropdown)
        # ------------------------------------------------------------------
        html.Div([

            # TASK 2.2 (a): Radio items to choose the Region
            html.Div([
                html.H2('Select Region:', style={'margin-right': '2em'}),
                dcc.RadioItems(
                    [{"label": "New South Wales",    "value": "NSW"},
                     {"label": "Northern Territory", "value": "NT"},
                     {"label": "Queensland",         "value": "QL"},
                     {"label": "South Australia",    "value": "SA"},
                     {"label": "Tasmania",           "value": "TA"},
                     {"label": "Victoria",           "value": "VI"},
                     {"label": "Western Australia",  "value": "WA"}],
                    value='NSW',
                    id='region',
                    inline=True
                )
            ]),

            # TASK 2.2 (b): Dropdown to choose the Year, right below the radio items
            html.Div([
                html.H2('Select Year:', style={'margin-right': '2em'}),
                dcc.Dropdown(YEARS, value=2005, id='year', clearable=False)
            ]),

        ], style={'padding': '10px'}),

        # ------------------------------------------------------------------
        # Second inner division: the two OUTPUT containers for the graphs
        # TASK 2.3: Add two empty divisions for output inside the next inner division
        # ------------------------------------------------------------------
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2')
        ], style={'display': 'flex', 'gap': '20px', 'padding': '10px'}),

    ])
    # outer division ends
])
# layout ends


# ----------------------------------------------------------------------------
# TASK 2.4: Add the Output and Input components inside the app.callback decorator
# ----------------------------------------------------------------------------
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
              [Input(component_id='region', component_property='value'),
               Input(component_id='year', component_property='value')])
# ----------------------------------------------------------------------------
# TASK 2.5: Add the callback function
# ----------------------------------------------------------------------------
def reg_year_display(input_region, input_year):
    """Filter the dataframe by region and year, then build the two charts."""

    # data
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Plot one - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data,
                  values='Estimated_fire_area',
                  names='Month',
                  title="{} : Monthly Average Estimated Fire Area in year {}".format(
                      input_region, input_year))

    # Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data,
                  x='Month',
                  y='Count',
                  title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(
                      input_region, input_year))

    return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]


if __name__ == '__main__':
    # dash >= 2.16 supports app.run(); on dash 2.x < 2.16 use app.run_server()
    try:
        app.run(debug=False, port=8050)
    except AttributeError:
        app.run_server(debug=False, port=8050)
