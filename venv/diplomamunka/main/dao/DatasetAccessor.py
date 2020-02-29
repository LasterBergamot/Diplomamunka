import csv
import os
from collections import namedtuple, defaultdict
from os.path import join

import pandas as pd

from diplomamunka.main.dao.Dataset import Dataset
from diplomamunka.main.dao.DatasetConstants import MOVIELENS_100k_SHORT, MOVIELENS_100k_LONG, MOVIELENS_1m_SHORT, \
    MOVIELENS_1m_LONG, JESTER_SHORT, JESTER_LONG, NETFLIX_SHORT, NETFLIX_LONG
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.algorithm.AlgorithmType import AlgorithmType


class DatasetAccessor:

    def __init__(self):
        self.dataset = Dataset()

    def chooseDataset(self):
        print("Hi! Please choose from the available datasets:")
        print("Movielens-100k: type in 100k or ml-100k")
        print("Movielens-1m: type in 1m or ml-1m")
        print("Jester (dataset 2): type in j or jester")
        print("Netflix Prize dataset: type in n or netflix")
        inputDatasetString = input()

        if inputDatasetString == MOVIELENS_100k_SHORT or inputDatasetString == MOVIELENS_100k_LONG:
            datasetType = DatasetType.MOVIELENS_100K
        elif MOVIELENS_1m_SHORT == inputDatasetString or inputDatasetString == MOVIELENS_1m_LONG:
            datasetType = DatasetType.MOVIELENS_1m
        elif inputDatasetString == JESTER_SHORT or inputDatasetString == JESTER_LONG:
            datasetType = DatasetType.JESTER
        elif inputDatasetString == NETFLIX_SHORT or inputDatasetString == NETFLIX_LONG:
            datasetType = DatasetType.NETFLIX_PRIZE_DATASET
        else:
            print("The given input didn't match any available dataset name! Returning...")
            return

        self.dataset.loadDataset(datasetType)

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        self.dataset.processChosenDataset(testSetSize)

    def getAdditionalData(self, algorithmType):

        genres = None
        years = None
        popularityRankings = self.getPopularityRanks()

        if (algorithmType == AlgorithmType.CONTENT_BASED):
            genres = self.getGenres()
            years = self.getYears()

        return {"genres": genres, "years": years, "popularityRankings": popularityRankings}

    # a builtin dataset has
    # - an url (where to download it)
    # - a path (where it is located on the filesystem)
    # - the parameters of the corresponding reader
    BuiltinDataset = namedtuple('BuiltinDataset', ['path', 'reader_params'])

    def loadMovies(self):
        movies = pd.read_csv(
            'D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/movies.csv',
            header=None,
            names=['movieId', 'title', 'genres'], usecols=[0, 1, 2])

        return movies

    def loadRatings(self):
        ratings = pd.read_csv(
            'D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/ratings.csv',
            header=None,
            names=['movieId', 'title', 'genres'], usecols=[0, 1, 2])

        return ratings

    def getYears(self):
        movies = self.loadMovies()
        years = defaultdict(int)

        return years

    def getGenres(self):
        movies = self.loadMovies()
        genres = defaultdict(int)

        return genres


    # BUILTIN_DATASETS = {
    #     'ml-100k-movies':
    #         BuiltinDataset(
    #             path='D:\Other\Programming\Workspaces\PyCharm_Workspace\Diplomamunka\venv\Datasets\MovieLens\100k\u.item',
    #             reader_params=dict(line_format='user item rating timestamp',
    #                                rating_scale=(1, 5),
    #                                sep='\t')
    #         ),
    #     'ml-1m':
    #         BuiltinDataset(
    #             path=join(get_dataset_dir(), 'ml-1m/ml-1m/ratings.dat'),
    #             reader_params=dict(line_format='user item rating timestamp',
    #                                rating_scale=(1, 5),
    #                                sep='::')
    #         ),
    #     'jester':
    #         BuiltinDataset(
    #             path=join(get_dataset_dir(), 'jester/jester_ratings.dat'),
    #             reader_params=dict(line_format='user item rating',
    #                                rating_scale=(-10, 10))
    #         )
    # }

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        #ratingsCsv = self.loadRatings()
        #with open(self.ratingsPath, newline='') as csvfile:
        with open('D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/ratings.csv', newline='') as csvfile:
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

    def getDataset(self):
        return self.dataset.getDataset()

    def getTrainSet(self):
        return self.dataset.getTrainSet()

    def getTestSet(self):
        return self.dataset.getTestSet()
