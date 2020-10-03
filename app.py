
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
import os

# working directory
os.chdir('C:\\Users\\sangavi\\Desktop\\DraupZinnov\\Dell_Taxonomy\\app\\Datasets')
path =r'C:\Users\sangavi\Desktop\DraupZinnov\Dell_Taxonomy\app\Datasets'


# ### Reading the datasets



# link to the datasets hosted on github (Sangavi-123)

url_eng ='https://github.com/Sangavi-123/flying-dog-beers/raw/master/Dell_Eng_Talent_byLocations.xlsx'
url_pdt = 'https://github.com/Sangavi-123/flying-dog-beers/raw/main/Dell_Pdt_Ser_Talent_byLocations.xlsx'
url_prof = 'https://github.com/Sangavi-123/flying-dog-beers/raw/main/Dell_Prof_Ser_Talent_byLocations.xlsx'

eng = pd.read_excel(url_eng)
pdt = pd.read_excel(url_pdt)
profs = pd.read_excel(url_prof)



# ## Outline of workflow
#     * there are three business functions available
#     * For each function, six clustering tasks
#     * Create a function that 
#         - Performs elbow method and picks the right number of clusters
#         - clusters them taking transformed variables
#         - Stores clusters back to unscaled data with only the respective two features  
#         - plots the clusters in dash app
#         
#         

# ### Preprocessing




# converting two columns to absolute percentage in all the three dataframes 
# creating new column ease of hiring by dividing job postings by Normalized value
dfList = [eng, pdt, profs] # list of original dataframes

for i in range(len(dfList)):
    dfList[i]['Gender Diversity'] = dfList[i]['Gender Diversity']*100
    dfList[i]['8 + years'] = dfList[i]['8 + years']*100
    dfList[i]['Employed Talent Growth Rate'] = dfList[i]['Employed Talent Growth Rate'] * 100  
    
    # creating ease of hiring column 
    dfList[i]['ease_hiring'] = dfList[i][' Job Postings ']/dfList[i]['Normalized Value']
  


# ### Standardising the features
#     *  standardize the features iteratively for each dataset



# features to be scaled in each dataset 
toScale = ['Normalized Value', ' Job Postings ', ' Base Pay (Median) ','Gender Diversity', '8 + years', 'Employed Talent Growth Rate','ease_hiring']
transformed = []  # will contain the list of dataframes post transdformation

# Setting up standard Scaler
scaler = StandardScaler()

# Iteratively standardize features in each dataset
for i in range(len(dfList)):
    sliced = dfList[i][toScale]    
    
    # fitting the scaler to the data
    scaler = scaler.fit(sliced)
    
    #transforming the data using the fit and converting it into a dataframe 
    #with column names from the list 'toScale'
    scaled = scaler.fit_transform(sliced)
    scaled = pd.DataFrame(scaled, columns = toScale)
    transformed.append(scaled)
#     transformed[i]['locations'] = dfList[i]['locations']
    


# ## Clustering Function 
#     * take the data in and iteratively pick each column against the default column
#     * perform elbow method
#     * pick the suggested clusters and if greater than 4, set it back to 4
#     * cluster each couple of features 
#     * store the clustered results in an object
#     



# set the columns to be picked iteratively
columns = [' Job Postings ', ' Base Pay (Median) ','Gender Diversity', '8 + years', 'Employed Talent Growth Rate','ease_hiring']
elbowScores = []
figures = []

def preprocessing(scaled,unscaled,column): 
    """
    1. Perform elbow method
    2.store the results in a list
    3.iteratively pick the column couple and perform clustering with 'n' from the list above
    """

    for i in range(len(columns)):
        # Set the data for X
        X = scaled[['Normalized Value', column]]


        # set up the kmeans clustering object and elbow plot object
        model = KMeans()
        visualizer = KElbowVisualizer(model, k=(2,12))

        # fit and visualise the elbow plot
        visualizer.fit(X)
    #     elbowScores.append(visualizer.elbow_value_) # stores the elbow scores of each cluster
      
        # perform clustering
        kmeans = KMeans(n_clusters = visualizer.elbow_value_, init ='k-means++', max_iter=300, n_init=10,random_state=0 )


        # Seggregating Clusters
        y_kmeans = kmeans.fit_predict(X)

        # Add the column Clusters  and locations to the subset of unscaled data
        df = X
        df['locations'] = unscaled['locations']
        df['Clusters'] = y_kmeans
        df['Clusters'] = df['Clusters'].astype(str)


        figure = px.scatter(df, x = 'Normalized Value', y = column, color="Clusters", hover_name = 'locations')
        figure.update_traces(marker=dict(size=15))
        return figure


# DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#     server = app.server
app.layout = html.Div(children =
                        [
                             html.Div(
                                     dcc.Dropdown(id = 'dropmenu',
                                     options = [{'label': 'Engineering', 'value':0},
                                                {'label': 'Product Services', 'value':1},
                                                {'label': 'Professional Services', 'value':2}
                                               ],value = 2
                                     )
                             ),
                            dbc.Row(
                                     [               
                                     dbc.Col(
                                    html.Div([
                                             dcc.Graph(
                                                     id = 'g1',
#                                                  figure = fig
                                                     )
                                    ])),
                                     dbc.Col(
                                             dcc.Graph(
                                                     id = 'g2',
#                                                      figure = figures[1]
                                                     )
                                               ),
                                    
                                        
                                     ]),

                          dbc.Row([                                          
                                      dbc.Col(
                                                 dcc.Graph(
                                                         id = 'g3',
#                                                          figure = figures[2]
                                                         )
                                                 ),

                                      dbc.Col(
                                                 dcc.Graph(
                                                         id = 'g4',
#                                                          figure = figures[3]
                                                     )
                                          ),
                                      ]
                              ),

                            dbc.Row([ 
                                    dbc.Col(
                                                 dcc.Graph(
                                                         id = 'g5',
#                                                          figure = figures[4]
                                                                 )
                                                 ),
                                     dbc.Col(
                                                 dcc.Graph(
                                                         id = 'g6',
#                                                          figure = figures[5]
                                                     )
                                                 ),   
                                             ]
                                          ),                 
                                    ]
                                 )


@app.callback(Output('g1', 'figure'),            
[Input('dropmenu', 'value')])
def changedata1(value):
    scaled = transformed[value]
    unscaled = dfList[value]
    figure = preprocessing(scaled, unscaled, columns[0])
    return figure

@app.callback(Output('g2', 'figure'),
[Input('dropmenu', 'value')])
def changedata2(value):
    scaled = transformed[value]
    unscaled = dfList[value]
    figure = preprocessing(scaled, unscaled, columns[1])
    return figure

@app.callback(Output('g3', 'figure'),
[Input('dropmenu', 'value')])
def changedata3(value):
    scaled = transformed[value]
    unscaled = dfList[value]
    figure = preprocessing(scaled, unscaled, columns[2])
    return figure

@app.callback(Output('g4', 'figure'),
[Input('dropmenu', 'value')])
def changedata4(value):
    scaled = transformed[value]
    unscaled = dfList[value]
    figure = preprocessing(scaled, unscaled, columns[3])
    return figure

@app.callback(Output('g5', 'figure'),
[Input('dropmenu', 'value')])
def changedata5(value):
    scaled = transformed[value]
    unscaled = dfList[value]
    figure = preprocessing(scaled, unscaled, columns[4])
    return figure

@app.callback(Output('g6', 'figure'),
[Input('dropmenu', 'value')])
def changedata6(value):
    scaled = transformed[value]
    unscaled = dfList[value]
    figure = preprocessing(scaled, unscaled, columns[5])
    return figure

if __name__ == '__main__':
    app.run_server()



