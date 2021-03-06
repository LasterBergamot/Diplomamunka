import csv
import re
from collections import defaultdict

import pandas as pd
from diplomamunka.main.dao.Dataset import Dataset
from diplomamunka.main.dao.DatasetType import DatasetType

JESTER_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/Jester/jester_ratings.csv'

NETFLIX_RATINGS_CSV = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings.csv"

NETFLIX_MOVIES_CSV = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/movie_titles.csv"

ML_1M_MOVIES_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/1m/csv/movies_1m.csv'
ML_1M_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/1m/csv/ratings_1m.csv'

ML_100K_MOVIES_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/movies.csv'
ML_100K_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/ratings.csv'

QUIT_LONG = "quit"
QUIT_SHORT = "q"

def createPopularityRankingsForJester():
    print("Calculating popularity rankings for Jester...START!")
    ratings = defaultdict(int)
    rankings = defaultdict(int)
    rank = 1

    with open(JESTER_RATINGS_CSV, newline='') as csvfile:
        ratingReader = csv.reader(csvfile)
        next(ratingReader)
        for row in ratingReader:
            if len(row) is not 0:
                jokeID = int(row[2])
                ratings[jokeID] += 1

    for jokeID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
        rankings[jokeID] = rank
        rank += 1

    print("Calculating popularity rankings for Jester...END!")
    return rankings


class DatasetAccessor:

    def __init__(self):
        self.dataset = Dataset()

    def loadDataset(self, datasetType):
        self.dataset.loadDataset(datasetType)

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        self.dataset.processChosenDataset(testSetSize)

    # Only in the case of MovieLens dataset
    def getPopularityRankings(self):
        return createPopularityRankingsForJester() if self.dataset.getDatasetType() == DatasetType.JESTER else self.createPopularityRanks()

    def createPopularityRanks(self):
        print("Calculating popularity rankings...START!")
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        rank = 1

        with open(self.getCsvPathForRatings(), newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)

            if self.dataset.getDatasetType() == DatasetType.NETFLIX_PRIZE_DATASET:
                next(ratingReader)

            for row in ratingReader:
                movieID = int(row[1])
                ratings[movieID] += 1

        for movieID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movieID] = rank
            rank += 1

        print("Calculating popularity rankings...END!")
        return rankings

    def loadRatings(self):
        return pd.read_csv(self.getCsvPathForRatings(), header=None, names=['movieId', 'title', 'genres'], usecols=[0, 1, 2])

    def getCsvPathForRatings(self):
        csvPath = ML_100K_RATINGS_CSV

        if self.dataset.getDatasetType() == DatasetType.MOVIELENS_1m:
            csvPath = ML_1M_RATINGS_CSV
        elif self.dataset.getDatasetType() == DatasetType.NETFLIX_PRIZE_DATASET:
            csvPath = NETFLIX_RATINGS_CSV

        return csvPath

    def getYears(self):
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)
        with open(self.getCsvPathForMovies(), newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)
            for row in movieReader:
                movieID = int(row[0])
                title = row[1] if self.dataset.getDatasetName() == DatasetType.MOVIELENS_100K.value or self.dataset.getDatasetName() == DatasetType.MOVIELENS_1m.value else row[2]
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
        csvPath = ML_100K_MOVIES_CSV

        if self.dataset.getDatasetType() == DatasetType.MOVIELENS_1m:
            csvPath = ML_1M_MOVIES_CSV
        elif self.dataset.getDatasetType() == DatasetType.NETFLIX_PRIZE_DATASET:
            csvPath = NETFLIX_MOVIES_CSV

        return csvPath

    def getDataset(self):
        return self.dataset

    def getTrainSet(self):
        return self.dataset.getTrainSet()

    def getTestSet(self):
        return self.dataset.getTestSet()
