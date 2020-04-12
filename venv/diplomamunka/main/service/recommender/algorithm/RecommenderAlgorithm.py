import time

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
        print("\nEvaluating dataset {} inside the algorithm called: {}...START!\n".format(self.datasetName, self.name))
        metrics = Metrics(self.name, self.datasetName)
        startTime = time.time()

        # do some stuff here
        # fit - Here the model learns from the trainSet
        self.algorithm.fit(trainSet)
        # test - Here the model tries to make predictions from a testSet,
        # depending on the knowledge it gathered while learning from the trainSet
        # Required for MAE, RMSE and topNPredicted
        predictions = self.algorithm.test(testSet)

        # Required for Coverage, Diversity and Novelty
        topNPredicted = calculateTopN(predictions)

        # Required for Diversity
        similarityMatrix = KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})
        similarityMatrix.fit(trainSet)

        metrics.calculateMetrics(predictions, topNPredicted, trainSet.n_users, similarityMatrix, popularityRankings, ratingThreshold=4)

        endTime = time.time()

        # Scalability - Runtime
        wholeProcessInSeconds = endTime - startTime

        # calculate metrics + add runtime to the Metrics object
        # return with the Metrics object
        metrics.setScalability(wholeProcessInSeconds)
        print("\nEvaluating the dataset inside the algorithm called: {}...DONE!\n".format(self.name))
        return metrics

    def getAlgorithm(self):
        return self.algorithm

    def getAlgorithmName(self):
        return self.name
