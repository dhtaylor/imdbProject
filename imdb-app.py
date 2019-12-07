import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from flask import Flask
import numpy as np

server = Flask(__name__)
app = dash.Dash(__name__, server = server)

np.random.seed(101)
random_x = np.random.randint(1,21,20)
random_y = np.random.randint(1,21,20)

app.layout = html.Div(
    children = [
        html.H1('Hello World'),
        dcc.Graph(
            id = 'scatter',
            figure = {
                'data': [
                    go.Scatter(
                        x = random_x,
                        y = random_y,
                        mode = 'markers'
                    )
                ],
                'layout':
                    go.Layout(
                        title = 'Scatter Plot!',
                        xaxis = {'title':'X-Axis!'},
                        yaxis = {'title':'Y-Axis!'}
                    )
            }
        )
    ]
)

if __name__ == '__main__':
    app.run_server()