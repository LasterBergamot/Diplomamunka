import itertools
import string
from collections import defaultdict

from surprise import accuracy

def calculateTopN(predictions, n=10, minimumRating=4.0):
    topN = defaultdict(list)

    for userID, itemID, actualRating, estimatedRating, _ in predictions:
        if estimatedRating >= minimumRating:
            topN[int(userID)].append((int(itemID), estimatedRating))

    for userID, ratings in topN.items():
        ratings.sort(key=lambda x: x[1], reverse=True)
        topN[int(userID)] = ratings[:n]

    return topN

class Metrics:

    algorithmName: string
    datasetName: string

    def __init__(self, algorithmName=None, datasetName=None):
        self.algorithmName = algorithmName
        self.datasetName = datasetName
        self.mae = 0.0
        self.rmse = 0.0
        self.coverage = 0.0
        self.diversity = 0.0
        self.novelty = 0.0
        self.scalability = 0.0

    def MAE(self, predictions):
        print("Calculating Mean Absolute Error...START!")
        self.mae = accuracy.mae(predictions, verbose=False)
        print("Calculating Mean Absolute Error...DONE!")

    def RMSE(self, predictions):
        print("Calculating Root Mean Squared Error...START!")
        self.rmse = accuracy.rmse(predictions, verbose=False)
        print("Calculating Root Mean Squared Error...DONE!")

    # What percentage of users have at least one "good" recommendation
    def Coverage(self, topNPredicted, numberOfUsers, ratingThreshold=0):
        print("Calculating Coverage...START!")
        hits = 0
        for userID in topNPredicted.keys():
            hit = False
            for itemID, predictedRating in topNPredicted[userID]:
                if predictedRating >= ratingThreshold:
                    hit = True
                    break
            if hit:
                hits += 1

        self.coverage = hits / numberOfUsers
        print("Calculating Coverage...DONE!")

    def Diversity(self, topNPredicted, similarityMatrix):
        print("Calculating Diversity...START!")

        n = 0
        total = 0
        simsMatrix = similarityMatrix.compute_similarities()
        for userID in topNPredicted.keys():
            pairs = itertools.combinations(topNPredicted[userID], 2)
            for pair in pairs:
                item1 = pair[0][0]
                item2 = pair[1][0]

                # need to skip this id, unless to_inner_iid() would throw an exception
                # because there's only one movie with this id
                # so, this one would be in either the train set or the test set, but not in both
                if item1 == 3280 or item2 == 3280:
                    continue

                innerID1 = similarityMatrix.trainset.to_inner_iid(str(item1))
                innerID2 = similarityMatrix.trainset.to_inner_iid(str(item2))
                similarity = simsMatrix[innerID1][innerID2]
                total += similarity
                n += 1

        S = total / n
        self.diversity = (1 - S)
        print("Calculating Diversity...DONE!")

    def Novelty(self, topNPredicted, popularityRankings):
        print("Calculating Novelty...START!")

        n = 0
        total = 0
        for userID in topNPredicted.keys():
            for rating in topNPredicted[userID]:
                movieID = rating[0]
                rank = popularityRankings[movieID]
                total += rank
                n += 1

        self.novelty = total / n
        print("Calculating Novelty...DONE!")

    # Scalability = time requirement of evaluation
    def setScalability(self, runTimeOfAlgorithm):
        self.scalability = runTimeOfAlgorithm

    def calculateMetrics(self, predictions, topNPredicted, numberOfUsers, similarityMatrix, popularityRankings, ratingThreshold=0):
        print("Calculating metrics...START!")
        self.MAE(predictions)
        self.RMSE(predictions)
        self.Coverage(topNPredicted, numberOfUsers, ratingThreshold)
        self.Diversity(topNPredicted, similarityMatrix)

        if popularityRankings is not None:
            self.Novelty(topNPredicted, popularityRankings)

        print("Calculating metrics...END!")

    def getMAE(self):
        return self.mae

    def getRMSE(self):
        return self.rmse

    def getCoverage(self):
        return self.coverage

    def getDiversity(self):
        return self.diversity

    def getNovelty(self):
        return self.novelty

    def getScalability(self):
        return self.scalability

    def getMetricsObject(self):
        return self

    def getAlgorithmName(self):
        return self.algorithmName

    def getDatasetName(self):
        return self.datasetName
