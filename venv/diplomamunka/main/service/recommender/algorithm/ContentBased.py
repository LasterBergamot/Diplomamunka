import heapq
import math
from collections import defaultdict

import numpy as np
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.algorithm.AlgorithmType import AlgorithmType
from surprise import AlgoBase, PredictionImpossible

# based on the cosine similarity where the coordinates are the genres given by the movies
def computeGenreSimilarity(movie1, movie2, genres):
    genres1 = genres[movie1]
    genres2 = genres[movie2]
    similarity = 0.0

    if len(genres1) != 0 and len(genres2) != 0:
        sumxx, sumxy, sumyy = 0, 0, 0

        for i in range(len(genres1)):
            x = genres1[i]
            y = genres2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y

        similarity = sumxy / math.sqrt(sumxx * sumyy)

    return similarity

# based on the year difference of the given movies
# if the difference is at least 10 years, the similarity will be close to 0
# if the difference is close to 0, the similarity will be close to 1
def computeYearSimilarity(movie1, movie2, years):
    diff = abs(years[movie1] - years[movie2])
    sim = math.exp(-diff / 10.0)
    return sim

class ContentBased(AlgoBase):

    algorithmType = AlgorithmType.CONTENT_BASED

    def __init__(self, datasetAccessor, k=40):
        AlgoBase.__init__(self)
        self.k = k
        self.datasetAccessor = datasetAccessor

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        genres = defaultdict(list)
        genreSimilarity = 1
        datasetName = self.datasetAccessor.getDataset().getDatasetType().value
        datasetType = self.datasetAccessor.getDataset().getDatasetType()
        datasetTypeIsMovieLens = datasetType == DatasetType.MOVIELENS_100K or datasetType == DatasetType.MOVIELENS_1m

        # Compute item similarity matrix based on content attributes
        years = self.datasetAccessor.getYears()

        if datasetTypeIsMovieLens:
            genres = self.datasetAccessor.getGenres()

        print("Computing content-based similarity matrix for {}...START!".format(datasetName))

        # Compute genre distance for every movie combination as a 2x2 matrix
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))

        for thisRating in range(self.trainset.n_items):
            if thisRating % 100 == 0:
                print(thisRating, " of ", self.trainset.n_items)
            for otherRating in range(thisRating + 1, self.trainset.n_items):
                thisMovieID = int(self.trainset.to_raw_iid(thisRating))
                otherMovieID = int(self.trainset.to_raw_iid(otherRating))

                if datasetTypeIsMovieLens:
                    genreSimilarity = computeGenreSimilarity(thisMovieID, otherMovieID, genres)

                yearSimilarity = computeYearSimilarity(thisMovieID, otherMovieID, years)
                self.similarities[thisRating, otherRating] = genreSimilarity * yearSimilarity if datasetTypeIsMovieLens else yearSimilarity
                self.similarities[otherRating, thisRating] = self.similarities[thisRating, otherRating]

        print("Computing content-based similarity matrix for {}...END!".format(datasetName))

    def estimate(self, u, i):
        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')

        # Build up similarity scores between this item and everything the user rated
        neighbors = []
        for rating in self.trainset.ur[u]:
            genreSimilarity = self.similarities[i, rating[0]]
            neighbors.append((genreSimilarity, rating[1]))

        # Extract the top-K most-similar ratings
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[0])

        # Compute average sim score of K neighbors weighted by user ratings
        simTotal = weightedSum = 0
        for (simScore, rating) in k_neighbors:
            if simScore > 0:
                simTotal += simScore
                weightedSum += simScore * rating

        if simTotal == 0:
            raise PredictionImpossible('No neighbors')

        predictedRating = weightedSum / simTotal

        return predictedRating
