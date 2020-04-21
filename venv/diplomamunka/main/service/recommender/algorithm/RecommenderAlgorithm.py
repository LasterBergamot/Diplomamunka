import time

from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.util.Metrics import Metrics, calculateTopN
from surprise import KNNBaseline

class RecommenderAlgorithm:

    def __init__(self, algorithm, name, datasetName):
        self.algorithm = algorithm
        self.name = name
        self.datasetName = datasetName

    # use stopwatch here
    # will return metrics here
    def evaluate(self, trainSet, testSet, popularityRankings):
        print("\nEvaluating dataset [{}] using algorithm [{}]...START!\n".format(self.datasetName, self.name))
        metrics = Metrics(self.name, self.datasetName)
        ratingThreshold = 4
        startTime = time.time()

        # do some stuff here
        # fit - Here the model learns from the trainSet
        print("Fitting...START!")
        self.algorithm.fit(trainSet)
        print("Fitting ...END!")

        # test - Here the model tries to make predictions from a testSet,
        # depending on the knowledge it gathered while learning from the trainSet
        # Required for MAE, RMSE and topNPredicted
        print("Testing...START!")
        predictions = self.algorithm.test(testSet)
        print("Testing...END!")

        # Required for Coverage, Diversity and Novelty
        print("Calculating top-N predictions...START!")
        topNPredicted = calculateTopN(predictions)
        print("Calculating top-N predictions...END!")

        # Required for Diversity
        print("Calculating similarity matrix...START!")
        similarityMatrix = KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})
        similarityMatrix.fit(trainSet)
        print("Calculating similarity matrix...END!")

        if self.datasetName == DatasetType.JESTER.value:
            ratingThreshold = 8

        metrics.calculateMetrics(predictions, topNPredicted, trainSet.n_users, similarityMatrix, popularityRankings, ratingThreshold=ratingThreshold)

        endTime = time.time()

        # Scalability - Runtime
        wholeProcessInSeconds = endTime - startTime

        # calculate metrics + add runtime to the Metrics object
        # return with the Metrics object
        metrics.setScalability(wholeProcessInSeconds)
        print("\nEvaluating dataset [{}] using algorithm [{}]...DONE!\n".format(self.datasetName, self.name))
        return metrics

    def getAlgorithm(self):
        return self.algorithm

    def getAlgorithmName(self):
        return self.name

    def setDatasetName(self, datasetName):
        self.datasetName = datasetName
