import csv
from collections import namedtuple, defaultdict

import pandas as pd
from diplomamunka.main.dao.Dataset import Dataset
from diplomamunka.main.dao.DatasetType import DatasetType

ML_1M_MOVIES_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/1m/csv/movies_1m.csv'
ML_1M_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/1m/csv/ratings_1m.csv'

ML_100K_MOVIES_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/movies.csv'
ML_100K_RATINGS_CSV = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/ratings.csv'

QUIT_LONG = "quit"
QUIT_SHORT = "q"

class DatasetAccessor:
    movieID_to_name = {}
    name_to_movieID = {}

    datasetType: DatasetType

    def __init__(self):
        self.dataset = Dataset()

    def loadDataset(self, datasetType):
        self.datasetType = datasetType
        self.dataset.loadDataset(datasetType)

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        self.dataset.processChosenDataset(testSetSize)

    # Only in the case of MovieLens dataset
    def getPopularityRankings(self):
        popularityRankings = None

        if self.datasetType == DatasetType.MOVIELENS_1m or self.datasetType == DatasetType.MOVIELENS_100K:
            popularityRankings = self.createPopularityRanks()

        return popularityRankings

    def createPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        # ratingsCsv = self.loadRatings()
        # with open(self.ratingsPath, newline='') as csvfile:
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

    # a builtin dataset has
    # - an url (where to download it)
    # - a path (where it is located on the filesystem)
    # - the parameters of the corresponding reader
    BuiltinDataset = namedtuple('BuiltinDataset', ['path', 'reader_params'])

    def loadRatings(self):
        return pd.read_csv(self.getCsvPathForRatings(), header=None, names=['movieId', 'title', 'genres'], usecols=[0, 1, 2])

    def getCsvPathForRatings(self):
        return ML_100K_RATINGS_CSV if self.datasetType == DatasetType.MOVIELENS_100K else ML_1M_RATINGS_CSV

    def loadMovies(self):
        return pd.read_csv(self.getCsvPathForMovies(), header=None, names=['movieId', 'title', 'genres'], usecols=[0, 1, 2])

    def getCsvPathForMovies(self):
        return ML_100K_MOVIES_CSV if self.datasetType == DatasetType.MOVIELENS_100K else ML_1M_MOVIES_CSV

    def getAntiTestSetForUser(self, testSubject=85):
        trainSet = self.getTrainSet()
        fill = trainSet.global_mean
        anti_testset = []
        u = trainSet.to_inner_uid(str(testSubject))
        user_items = set([j for (j, _) in trainSet.ur[u]])
        # anti_testset += [
        #     (trainSet.to_raw_uid(u), trainSet.to_raw_iid(i), fill)
        #     for i in trainSet.all_items()
        #     if i not in user_items
        # ]

        anti_testset += [(trainSet.to_raw_uid(u), trainSet.to_raw_iid(i), fill) for
                         i in trainSet.all_items() if
                         i not in user_items]

        return anti_testset

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

    def loadMovieIDsAndNames(self):
        with open(self.getCsvPathForMovies(), newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)  # Skip header line
            for row in movieReader:
                movieID = int(row[0])
                movieName = row[1]
                self.movieID_to_name[movieID] = movieName
                self.name_to_movieID[movieName] = movieID

    def getDatasetType(self):
        return self.datasetType

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
