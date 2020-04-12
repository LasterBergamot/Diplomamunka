import csv
from collections import namedtuple, defaultdict

import pandas as pd
from diplomamunka.main.dao.Dataset import Dataset
from diplomamunka.main.dao.DatasetConstants import MOVIELENS_100k_SHORT, MOVIELENS_100k_LONG, MOVIELENS_1m_SHORT, \
    MOVIELENS_1m_LONG, JESTER_SHORT, JESTER_LONG, NETFLIX_SHORT, NETFLIX_LONG
from diplomamunka.main.dao.DatasetType import DatasetType

QUIT_LONG = "quit"
QUIT_SHORT = "q"


class DatasetAccessor:

    movieID_to_name = {}
    name_to_movieID = {}

    def __init__(self):
        self.dataset = Dataset()

    def chooseDataset(self):
        choosenDatasets = set()
        inputString = ""

        print("\nHi!")

        while inputString != QUIT_SHORT and inputString != QUIT_LONG:
            print("Please choose from the available datasets:")
            print("Note: no duplicates will be added!\n")
            print("Movielens-100k: type in 100k or ml-100k")
            print("Movielens-1m: type in 1m or ml-1m")
            print("Jester (dataset 2): type in j or jester")
            print("Netflix Prize dataset: type in n or netflix")
            # Instead of Netflix (??) the Book-Crossing Dataset will come here
            inputString = input()

            if inputString == MOVIELENS_100k_SHORT or inputString == MOVIELENS_100k_LONG:
                choosenDatasets.add(DatasetType.MOVIELENS_100K)
                print(DatasetType.MOVIELENS_100K.value + " added!\n")
            elif MOVIELENS_1m_SHORT == inputString or inputString == MOVIELENS_1m_LONG:
                choosenDatasets.add(DatasetType.MOVIELENS_1m)
                print(DatasetType.MOVIELENS_1m.value + " added!\n")
            elif inputString == JESTER_SHORT or inputString == JESTER_LONG:
                choosenDatasets.add(DatasetType.JESTER)
                print(DatasetType.JESTER.value + " added!\n")
            elif inputString == NETFLIX_SHORT or inputString == NETFLIX_LONG:
                choosenDatasets.add(DatasetType.NETFLIX_PRIZE_DATASET)
                print(DatasetType.NETFLIX_PRIZE_DATASET.value + " added!\n")
            elif inputString == QUIT_SHORT or inputString == QUIT_LONG:
                print("Quitting!")
            else:
                print("The given input didn't match any available dataset name!\n")

        # self.dataset.loadDataset(datasetType)
        return choosenDatasets

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        self.dataset.processChosenDataset(testSetSize)

    # Only in the case of MovieLens dataset
    def getPopularityRankings(self, datasetType):
        popularityRankings = None

        if (datasetType == DatasetType.MOVIELENS_1m or datasetType == DatasetType.MOVIELENS_100K):
            popularityRankings = self.getPopularityRanks()

        return popularityRankings

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

    def getAntiTestSetForUser(self, trainSet, testSubject=85):
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

    def loadMovieIDsAndNames(self):
        with open('D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/MovieLens/100k/csv/movies.csv', newline='', encoding='ISO-8859-1') as csvfile:
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
