
import numpy as np
import pandas as pd
import glob
import sys
import dash
import warnings
warnings.filterwarnings('ignore')
import plotly
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import plotly.graph_objects as go
#from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import matplotlib.pyplot as plt
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.tools as tls
from plotly.tools import mpl_to_plotly
from sklearn.preprocessing import StandardScaler
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# link to the datasets hosted on github (Sangavi-123)

data= pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv")

fig = go.Figure(data=go.Scatter(x=data['Postal'],
                                y=data['Population'],
                                mode='markers',
                                marker_color=data['Population'],
                                text=data['State'])) # hover text goes here

fig.update_layout(title='Population of USA States')

# DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div(children =
                        [
                             dcc.Graph( id = 'g1', figure = fig),
                        ]
                     )
                         
if __name__ == '__main__':
    app.run_server()

