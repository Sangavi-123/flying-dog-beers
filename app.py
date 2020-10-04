
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

url_eng ='https://github.com/Sangavi-123/flying-dog-beers/raw/master/Dell_Eng_Talent_byLocations.xlsx'
#url_pdt = 'https://github.com/Sangavi-123/flying-dog-beers/raw/main/Dell_Pdt_Ser_Talent_byLocations.xlsx'
#url_prof = 'https://github.com/Sangavi-123/flying-dog-beers/raw/main/Dell_Prof_Ser_Talent_byLocations.xlsx'

eng = pd.read_excel(url_eng)
#pdt = pd.read_excel(url_pdt)
#profs = pd.read_excel(url_prof)

df = eng

figure = px.scatter(df, x = 'Normalized Value', y = '8 + years', hover_name = 'locations')
figure.update_traces(marker=dict(size=15))



# DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div(children =
                        [
                             dcc.Graph( id = 'g1', figure = figure),
                        ]
                     )
                         
if __name__ == '__main__':
    app.run_server()

