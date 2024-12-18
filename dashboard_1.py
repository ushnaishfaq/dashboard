#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

# ---------- Helper: Generate Dummy Data ----------
def generate_dummy_excel(file_path, num_rows=120):
    """
    Generates dummy pollutant data for variables and saves it as an Excel file.
    """
    np.random.seed(42)
    time_index = [datetime.now() - timedelta(minutes=i) for i in range(num_rows)][::-1]
    data = {
        "Time": time_index,
        "TVOC": np.random.randint(50, 500, num_rows),
        "NH3": np.random.randint(0, 50, num_rows),
        "NO": np.random.randint(10, 100, num_rows),
        "H2": np.random.randint(0, 10, num_rows),
        "PM25": np.random.randint(5, 200, num_rows),
        "H2S": np.random.randint(0, 20, num_rows),
        "CO": np.random.randint(0, 200, num_rows),
        "HCL": np.random.randint(0, 20, num_rows),
        "NO2": np.random.randint(10, 150, num_rows),
        "CO2": np.random.randint(300, 2000, num_rows),
        "O3": np.random.randint(0, 120, num_rows),
        "HCHO": np.random.randint(0, 50, num_rows),
        "SO2": np.random.randint(0, 100, num_rows),
        "CH4": np.random.randint(0, 10, num_rows),
        "AQI": np.random.randint(0, 300, num_rows),
        "UV_Index": np.random.randint(0, 11, num_rows),
        "WS": np.random.randint(0, 20, num_rows),
        "WD": np.random.randint(0, 360, num_rows)
    }
    pd.DataFrame(data).to_excel(file_path, index=False)
    print(f"Dummy data generated: {file_path}")

# ---------- Setup Global Variables ----------
EXCEL_FILE = "combined_air_quality.xlsx"
if not os.path.exists(EXCEL_FILE):
    generate_dummy_excel(EXCEL_FILE)

DATA = pd.read_excel(EXCEL_FILE)
POLLUTANTS = ["TVOC", "NH3", "NO", "H2", "PM25", "H2S", "CO", "HCL",
              "NO2", "CO2", "O3", "HCHO", "SO2", "CH4"]

# ---------- Initialize Dash App ----------
app = Dash(__name__)
app.title = "Unified Air Quality Monitoring Dashboard"

# ---------- Layout ----------
app.layout = html.Div([
    html.H1("Unified Air Quality Monitoring Dashboard", style={'textAlign': 'center'}),
    html.Div([

    # Top Row - Gauges
    html.Div([
        html.Div([dcc.Graph(id='gauge-aqi', style={'width': '100%',  'margin': '1%', 'display': 'inline-block'})
                 ], style={}),
        html.Div([dcc.Graph(id='gauge-uv', style={'width': '100%',  'margin': '1%', 'display': 'inline-block'})
                 ], style={}),
        html.Div([dcc.Graph(id='speedometer-wind', style={'width': '100%',  'margin': '1%', 'display': 'inline-block'})
                 ], style={}),
        html.Div([dcc.Graph(id='wind-direction', style={'width': '100%',  'margin': '1%', 'display': 'inline-block'})
                 ], style={}),
    ],style={
    'display': 'flex',
    'flex-direction': 'column',  # Horizontal layout for the entire row
    'align-items': 'left',
    'justify-content': 'space-around',
    'gap': '1px',
    'padding': '',
    'background-color': '',
    'border': '1px solid #ccc',
    'border-radius': '',
    'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
    'width': '30%',  # Full width for the container
    'margin': '1px 1px 1px 1px'
    }),

    # Middle Row - Individual Pollutant Gauges
    # Top Row - Gauge Charts
    html.Div([
        html.Div([
            html.H2("Current Data", style={'textAlign': 'LEFT', 'margin-bottom': '5px'}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width':'50%','height':'50%', 'display': 'inline-block'})
                for var in POLLUTANTS[:2]
            ], style={}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width': '50%','height':'50%', 'display': 'inline-block'})
                for var in POLLUTANTS[2:4]
            ], style={}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width': '50%','height':'50%', 'display': 'inline-block'})
                for var in POLLUTANTS[4:6]
            ], style={}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width': '50%','height':'50%', 'display': 'inline-block'})
                for var in POLLUTANTS[6:8]
            ], style={}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width': '50%','height':'50%', 'display': 'inline-block'})
                for var in POLLUTANTS[8:10]
            ], style={}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width': '50%', 'height':'50%','display': 'inline-block'})
                for var in POLLUTANTS[10:12]
            ], style={}),
            html.Div([
                html.Div([dcc.Graph(id=f'gauge-{var}')], style={'width': '50%','height':'50%', 'display': 'inline-block'})
                for var in POLLUTANTS[12:14]
            ], style={}),
        ])
    ],style={
            'display': 'flex',
            'flex-direction': 'column',  # Vertical layout
            'align-items': 'LEFT',
            'justify-content': 'space-around',
            'gap': '1px',
            'padding': '',
            'background-color': '',
            'border': '1px solid #ccc',
            'border-radius': '',
            'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
            'width': '25%',  # Adjust width for container
            'margin': '1px 1px 1px 1px',
    }),

    # Bottom Row - Line and Bar Charts
     html.Div([
        html.Div([
        html.Div([dcc.Graph(id='line-chart')], style={'width': '100%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bar-chart')], style={'width': '100%', 'display': 'inline-block'}),
            
    ], style={}),
         
    ],style={
            'display': 'flex',
            'flex-direction': 'column',  # Vertical layout
            'align-items': 'center',
            'justify-content': 'space-around',
            'gap': '1px',
            'padding': '',
            'background-color': '#f9f9f9',
            'border': '1px solid #ccc',
            'border-radius': '10px',
            'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
            'width': '30%',  # Adjust width for container
            'margin': '1px 1px 1px 1px',
        }),
],style={
        'display': 'flex',          # Horizontal alignment for all 3 containers
        'justify-content': 'space-around',
        'flex-wrap': 'wrap',        # Wrap containers if screen is too small
        'width': '100%',
        'margin': '1px 1px 10px 1px auto',
        'padding': '1px',
        'box-sizing': 'border-box'
    }),

    # Interval for live updates
    dcc.Interval(id='update-interval', interval=5000, n_intervals=0)
])

# ---------- Callbacks ----------
@app.callback(
    [Output('gauge-aqi', 'figure'), Output('gauge-uv', 'figure'),
     Output('speedometer-wind', 'figure'), Output('wind-direction', 'figure')] +
    [Output(f'gauge-{var}', 'figure') for var in POLLUTANTS] +
    [Output('line-chart', 'figure'), Output('bar-chart', 'figure')],
    Input('update-interval', 'n_intervals')
)
def update_dashboard(n_intervals):
    # Load data
    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return [go.Figure()] * (4 + len(POLLUTANTS) + 2)

    latest_data = df.iloc[-1]

    # AQI Gauge
    aqi_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=latest_data['AQI'],
        title={'text': "AQI"}, gauge={'axis': {'range': [0, 300]},'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "green"},
                    {'range': [51, 100], 'color': "yellow"},
                    {'range': [101, 150], 'color': "orange"},
                    {'range': [151, 200], 'color': "red"},
                    {'range': [201, 300], 'color': "Purple"},
                    {'range': [301, 500],'color': "brown" }
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 175  # Threshold marker
                }}
    ))

    # UV Index Gauge
    uv_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=latest_data['UV_Index'],
        title={'text': "UV Index"}, gauge={'axis': {'range': [0, 11]}, 'steps': [
            {'range': [0, 2], 'color': "green"},
            {'range': [3, 5], 'color': "yellow"},
            {'range': [6, 7], 'color': "orange"},
            {'range': [8, 10], 'color': "red"},
        ]}
    ))

    # Wind Speed Gauge
    wind_speed = go.Figure(go.Indicator(
        mode="gauge+number", value=latest_data['WS'],
        title={'text': "Wind Speed (km/h)"}, gauge={'axis': {'range': [0, 20]}}
    ))

    # Wind Direction Polar Plot
    wind_direction = px.scatter_polar(df, r='WS', theta='WD', title="Wind Direction")

    # Individual Pollutant Gauges
    gauges = []
    for var in POLLUTANTS:
        max_val = df[var].max() * 1.2
        gauges.append(go.Figure(go.Indicator(
            mode="gauge+number", value=latest_data[var],
            title={'text': var}, gauge={'axis': {'range': [0, max_val]},
                                        'steps': [
                                            {'range': [0, max_val * 0.25], 'color': "green"},
                                            {'range': [max_val * 0.25, max_val * 0.5], 'color': "yellow"},
                                            {'range': [max_val * 0.5, max_val * 0.75], 'color': "orange"},
                                            {'range': [max_val * 0.75, max_val], 'color': "red"}]}
        )))

    # Line Chart
    line_chart = px.line(df, x='Time', y=POLLUTANTS, title="Pollutant Trends Over Time", )

    # Bar Chart
    bar_chart = px.bar(x=POLLUTANTS, y=[latest_data[var] for var in POLLUTANTS],
                       title="Latest Pollutant Levels", labels={'x': 'Pollutants', 'y': 'Levels'})

    return [aqi_gauge, uv_gauge, wind_speed, wind_direction] + gauges + [line_chart, bar_chart]

# ---------- Main ----------
if __name__ == '__main__':
    app.run_server(debug=True, port=8192)


# In[ ]:





# In[ ]:




