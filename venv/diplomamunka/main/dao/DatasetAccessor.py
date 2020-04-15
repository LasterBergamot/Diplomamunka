import csv
import re
from collections import defaultdict

import pandas as pd
from diplomamunka.main.dao.Dataset import Dataset
from diplomamunka.main.dao.DatasetType import DatasetType

ML_1M_MOVIES_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/1m/csv/movies_1m.csv'
ML_1M_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/1m/csv/ratings_1m.csv'

ML_100K_MOVIES_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/movies.csv'
ML_100K_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/ratings.csv'

QUIT_LONG = "quit"
QUIT_SHORT = "q"

def createPopularityRankingsForJester():
    ratings = defaultdict(int)
    rankings = defaultdict(int)
    jesterCsvPath = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/Jester/jester_ratings.csv'
    rank = 1

    with open(jesterCsvPath, newline='') as csvfile:
        ratingReader = csv.reader(csvfile)
        next(ratingReader)
        for row in ratingReader:
            if len(row) is not 0:
                jokeID = int(row[2])
                ratings[jokeID] += 1

    for jokeID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
        rankings[jokeID] = rank
        rank += 1

    return rankings


class DatasetAccessor:
    movieID_to_name = {}
    name_to_movieID = {}

    def __init__(self):
        self.dataset = Dataset()

    def loadDataset(self, datasetType):
        self.dataset.loadDataset(datasetType)

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        self.dataset.processChosenDataset(testSetSize)

    # Only in the case of MovieLens dataset
    def getPopularityRankings(self):
        popularityRankings = None

        if self.dataset.getDatasetType() == DatasetType.MOVIELENS_1m or self.dataset.getDatasetType() == DatasetType.MOVIELENS_100K:
            popularityRankings = self.createPopularityRanks()
        elif self.dataset.getDatasetType() == DatasetType.JESTER:
            popularityRankings = createPopularityRankingsForJester()

        return popularityRankings

    def createPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)

        with open(self.getCsvPathForRatings(), newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                movieID = int(row[1])
                ratings[movieID] += 1
        rank = 1
        for movieID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movieID] = rank
            rank += 1
        return rankings

    def loadRatings(self):
        return pd.read_csv(self.getCsvPathForRatings(), header=None, names=['movieId', 'title', 'genres'], usecols=[0, 1, 2])

    def getCsvPathForRatings(self):
        return ML_100K_RATINGS_CSV if self.dataset.getDatasetType() == DatasetType.MOVIELENS_100K else ML_1M_RATINGS_CSV

    def getYears(self):
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)
        with open(self.getCsvPathForMovies(), newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)
            for row in movieReader:
                movieID = int(row[0])
                title = row[1]
                m = p.search(title)
                year = m.group(1)
                if year:
                    years[movieID] = int(year)
        return years

    def getGenres(self):
        genres = defaultdict(list)
        genreIDs = {}
        maxGenreID = 0
        with open(self.getCsvPathForMovies(), newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)  # Skip header line
            for row in movieReader:
                movieID = int(row[0])
                genreList = row[2].split('|')
                genreIDList = []
                for genre in genreList:
                    if genre in genreIDs:
                        genreID = genreIDs[genre]
                    else:
                        genreID = maxGenreID
                        genreIDs[genre] = genreID
                        maxGenreID += 1
                    genreIDList.append(genreID)
                genres[movieID] = genreIDList
        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (movieID, genreIDList) in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[movieID] = bitfield

        return genres

    def getCsvPathForMovies(self):
        return ML_100K_MOVIES_CSV if self.dataset.getDatasetType() == DatasetType.MOVIELENS_100K else ML_1M_MOVIES_CSV

    def loadMovieIDsAndNames(self):
        with open(self.getCsvPathForMovies(), newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)  # Skip header line
            for row in movieReader:
                movieID = int(row[0])
                movieName = row[1]
                self.movieID_to_name[movieID] = movieName
                self.name_to_movieID[movieName] = movieID

    def getDataset(self):
        return self.dataset

    def getTrainSet(self):
        return self.dataset.getTrainSet()

    def getTestSet(self):
        return self.dataset.getTestSet()

    def getMovieNameByID(self, movieID):
        return self.movieID_to_name[movieID] if movieID in self.movieID_to_name else ""

    def getMovieIDByName(self, movieName):
        return self.name_to_movieID[movieName] if movieName in self.name_to_movieID else ""
