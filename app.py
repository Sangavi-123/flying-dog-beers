import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

########### Define your variables
url ='https://github.com/Sangavi-123/Dash_App_Cluster/raw/main/Dell_Eng_Talent_byLocations.xlsx'

df = pd.read_excel(url)

fig = px.scatter(df, x = 'Normalized Value', y = column, color="Clusters", hover_name = 'locations')
        figure.update_traces(marker=dict(size=15))


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
