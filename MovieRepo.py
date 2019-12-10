import pandas as pd
import plotly.express as px

class MovieRepo():
    __filename = ""
    __movies = pd.DataFrame()
    __actors = pd.DataFrame()
    __genres = pd.DataFrame()
    __revenue = pd.DataFrame()
    __ratings = pd.DataFrame()
    __directors = pd.DataFrame()
    __years = pd.DataFrame()

    def __init__(self):
        self.__filename = './IMDB-Movie-Data.csv'
        self.__movies = pd.read_csv(self.__filename)
        self.__movies = self.cleanMovies()
        self.__actors = self.loadActors()
        self.__genres = self.loadGenres()
        self.__revenue = self.loadRevenue()
        self.__ratings = self.loadRatings()
        self.__directors = self.loadDirectors()
        self.__years = self.loadYears()
    
# Load Repository Data Structures
    def cleanMovies(self):
        # Clean Data for Analysis
        # Change some Column Names
        movies = self.__movies.rename(
            columns={
                'Revenue (Millions)':'Revenue_Millions',
                'Runtime (Minutes)':'Runtime_Minutes'
            }
        )

        # Remove Metascore since it has null values and we aren't doing analysis on that data
        del movies['Metascore']
        movies = movies.dropna()
        return movies
    
    def loadActors(self):
        actors = pd.DataFrame(
            self.__movies.Actors.str.split(pat = ',').tolist(),
            index = self.__movies.Rank
        ).stack()

        actors = actors.reset_index([0, 'Rank'])
        actors.columns = ['Rank','Actor']
        return actors

    def loadGenres(self):
        genres = pd.DataFrame(
            self.__movies.Genre.str.split(pat = ',').tolist(),
            index = self.__movies.Rank
        ).stack()

        genres = genres.reset_index([0, 'Rank'])
        genres.columns = ['Rank','Genre']
        return genres

    def loadRevenue(self):
        revenue = self.__movies[['Rank','Revenue_Millions']]
        return revenue

    def loadRatings(self):
        ratings = self.__movies[['Rank','Rating']]
        return ratings

    def loadDirectors(self):
        directors = self.__movies[['Rank','Director']]
        return directors

    def loadYears(self):
        years = self.__movies[['Rank','Year']]
        return years

# Public Methods
# Ratings Metrics
    def getRatingByActor(self, limit):
        # Merge Ratings to Actors on Rank
        actor_ratings = self.__actors.merge(self.__ratings)
        actor_ratings = actor_ratings.groupby('Actor')['Rating'].mean().reset_index()

        # Generate Graph
        fig = px.bar(
            actor_ratings.sort_values('Rating', ascending = False).head(limit),
            x = 'Actor',
            y = 'Rating',
            labels = {
                'Rating':'Average Rating'
            }
        )

        fig.update_layout(title_text = 'Average Ratings by Top ' + str(limit) + ' Actor(s)')
        return fig

    def getRatingByDirector(self, limit):
        # Merge Ratings to Directors on Rank
        director_ratings = self.__directors.merge(self.__ratings)
        director_ratings = director_ratings.groupby('Director')['Rating'].mean().reset_index()

        # Generate Graph
        fig = px.bar(
            director_ratings.sort_values('Rating', ascending = False).head(limit),
            x = 'Director',
            y = 'Rating',
            labels = {
                'Rating':'Average Rating'
            }
        )

        fig.update_layout(title_text = 'Average Ratings by Top ' + str(limit) + ' Director(s)')
        return fig

    def getRatingByGenre(self, limit):
        # Merge Ratings to Directors on Rank
        genre_ratings = self.__genres.merge(self.__ratings)
        genre_ratings = genre_ratings.groupby('Genre')['Rating'].mean().reset_index()

        # Generate Graph
        fig = px.bar(
            genre_ratings.sort_values('Rating', ascending = False).head(limit),
            x = 'Genre',
            y = 'Rating',
            labels = {
                'Rating':'Average Rating'
            }
        )

        fig.update_layout(title_text = 'Average Ratings by Top ' + str(limit) + ' Genre(s)')
        return fig

    def getRatingByRevenue(self):
        # Merge Ratings to Directors on Rank
        revenue_ratings = self.__revenue.merge(self.__ratings)
        revenue_ratings = revenue_ratings.groupby('Revenue_Millions')['Rating'].mean().reset_index()

        # Generate Graph
        fig = px.scatter(
            revenue_ratings.sort_values(['Rating', 'Revenue_Millions'], ascending = False),
            x = 'Revenue_Millions',
            y = 'Rating',
            labels = {
                'Revenue_Millions': 'Revenue (Millions)',
                'Rating':'Average Rating'
            }
        )

        fig.update_layout(title_text = 'Average Ratings by Revenue (Millions)')
        return fig

    def getRatingByYear(self):
        # Merge Ratings to Directors on Rank
        years_ratings = self.__years.merge(self.__ratings)
        years_ratings = years_ratings.groupby('Year')['Rating'].mean().reset_index()

        # Generate Graph
        fig = px.scatter(
            years_ratings.sort_values(['Rating', 'Year'], ascending = False),
            x = 'Year',
            y = 'Rating',
            labels = {
                'Year': 'Production Year',
                'Rating':'Average Rating'
            }
        )

        fig.update_layout(title_text = 'Average Ratings by Production Year(s)')
        return fig

# Revenue Metrics
    def getRevenueByActor(self, limit):
        # Get Revenue divided by Actor Count per Rank
        actor_count = self.__actors.groupby('Rank').count().reset_index([0,'Rank'])
        actor_count.columns = ['Rank','ActorCount']

        temp = actor_count.merge(self.__revenue)

        rel_revenue = pd.DataFrame({
            'Rank': temp.Rank,
            'Relative_Revenue': temp.Revenue_Millions / temp.ActorCount
        })

        # Merge Revenue to Actors on Rank
        actor_revenue = self.__actors.merge(rel_revenue)
        actor_revenue = actor_revenue.groupby('Actor')['Relative_Revenue'].sum().reset_index()
        
        # Generate Graph
        fig = px.bar(
            actor_revenue.sort_values('Relative_Revenue', ascending = False).head(limit),
            x = 'Actor',
            y = 'Relative_Revenue',
            labels = {
                'Relative_Revenue': 'Relative Revenue (Millions)'
            }
        )

        fig.update_layout(title_text = 'Relative Revenue (Millions) by Top ' + str(limit) + ' Actor(s)')
        return fig

    def getRevenueByDirector(self, limit):
        # Merge Revenue to Actors on Rank
        director_revenue = self.__directors.merge(self.__revenue)
        director_revenue = director_revenue.groupby('Director')['Revenue_Millions'].sum().reset_index()
        
        # Generate Graph
        fig = px.bar(
            director_revenue.sort_values('Revenue_Millions', ascending = False).head(limit),
            x = 'Director',
            y = 'Revenue_Millions',
            labels = {
                'Revenue_Millions': 'Revenue (Millions)'
            }
        )

        fig.update_layout(title_text = 'Revenue (Millions) by Top ' + str(limit) + ' Director(s)')
        return fig

    def getRevenueByGenre(self, limit):
        # Get Revenue divided by Actor Count per Rank
        genre_count = self.__genres.groupby('Rank').count().reset_index([0,'Rank'])
        genre_count.columns = ['Rank','GenreCount']

        temp = genre_count.merge(self.__revenue)

        rel_revenue = pd.DataFrame({
            'Rank': temp.Rank,
            'Relative_Revenue': temp.Revenue_Millions / temp.GenreCount
        })

        # Merge Revenue to Actors on Rank
        genre_revenue = self.__genres.merge(rel_revenue)
        genre_revenue = genre_revenue.groupby('Genre')['Relative_Revenue'].sum().reset_index()
        
        # Generate Graph
        fig = px.bar(
            genre_revenue.sort_values('Relative_Revenue', ascending = False).head(limit),
            x = 'Genre',
            y = 'Relative_Revenue',
            labels = {
                'Relative_Revenue': 'Relative Revenue (Millions)'
            }
        )

        fig.update_layout(title_text = 'Relative Revenue (Millions) by Top ' + str(limit) + ' Genre(s)')
        return fig

    def getRevenueByRating(self):
        # Merge Revenue to Actors on Rank
        rating_revenue = self.__ratings.merge(self.__revenue)
        rating_revenue = rating_revenue.groupby('Rating')['Revenue_Millions'].sum().reset_index()
        
        # Generate Graph
        fig = px.scatter(
            rating_revenue.sort_values('Revenue_Millions', ascending = False),
            x = 'Rating',
            y = 'Revenue_Millions',
            labels = {
                'Revenue_Millions': 'Revenue (Millions)'
            }
        )

        fig.update_layout(title_text = 'Revenue (Millions) by Rating(s)')
        return fig

    def getRevenueByYear(self):
        # Merge Revenue to Years on Rank
        year_revenue = self.__years.merge(self.__revenue)
        year_revenue = year_revenue.groupby('Year')['Revenue_Millions'].sum().reset_index()
        
        # Generate Graph
        fig = px.scatter(
            year_revenue.sort_values('Revenue_Millions', ascending = False),
            x = 'Year',
            y = 'Revenue_Millions',
            labels = {
                'Year': 'Production Year',
                'Revenue_Millions': 'Revenue (Millions)'
            }
        )

        fig.update_layout(title_text = 'Revenue (Millions) by Production Year(s)')
        return fig
