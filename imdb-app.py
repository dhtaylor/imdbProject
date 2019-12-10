import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from flask import Flask
import numpy as np
import MovieRepo as mr

movies = mr.MovieRepo()

server = Flask(__name__)
app = dash.Dash(__name__, server = server)

np.random.seed(101)
random_x = np.random.randint(1,21,20)
random_y = np.random.randint(1,21,20)

app.layout = html.Div(
    children = [
        html.H1('Pandas for Data Science (CPSC-442)'),
        dcc.Graph(
            id = 'rating_by_actor',
            figure = movies.getRatingByActor(10)
        ),
        dcc.Graph(
            id = 'rating_by_director',
            figure = movies.getRatingByDirector(15)
        ),
        dcc.Graph(
            id = 'rating_by_genre',
            figure = movies.getRatingByGenre(5)
        ),
        dcc.Graph(
            id = 'rating_by_revenue',
            figure = movies.getRatingByRevenue()
        ),
        dcc.Graph(
            id = 'rating_by_year',
            figure = movies.getRatingByYear()
        ),
        dcc.Graph(
            id = 'revenue_by_actor',
            figure = movies.getRevenueByActor(10)
        ),
        dcc.Graph(
            id = 'revenue_by_director',
            figure = movies.getRevenueByDirector(15)
        ),
        dcc.Graph(
            id = 'revenue_by_genre',
            figure = movies.getRevenueByGenre(5)
        ),
        dcc.Graph(
            id = 'revenue_by_rating',
            figure = movies.getRevenueByRating()
        ),
        dcc.Graph(
            id = 'revenue_by_year',
            figure = movies.getRevenueByYear()
        )
    ]
)

if __name__ == '__main__':
    app.run_server()