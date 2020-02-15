# Contains every metric data for the given algorithm
import itertools
import string

from surprise import accuracy


class Metrics:

    algorithmName: string

    def __init__(self, algorithmName=None):
        self.algorithmName = algorithmName
        self.mae = 0
        self.rmse = 0
        self.coverage = 0
        self.diversity = 0
        self.novelty = 0
        self.scalability = 0

    def MAE(self, predictions):
        print("Calculating Mean Absolute Error...")
        self.mae = accuracy.mae(predictions, verbose=False)
        print("Calculating Mean Absolute Error...Done")

        return self.mae

    def RMSE(self, predictions):
        print("Calculating Root Mean Squared Error...")
        self.rmse = accuracy.rmse(predictions, verbose=False)
        print("Calculating Root Mean Squared Error...Done")

        return self.rmse

    # What percentage of users have at least one "good" recommendation
    def coverage(self, topNPredicted, numUsers, ratingThreshold=0):
        print("Calculating Coverage...")
        hits = 0
        for userID in topNPredicted.keys():
            hit = False
            for movieID, predictedRating in topNPredicted[userID]:
                if (predictedRating >= ratingThreshold):
                    hit = True
                    break
            if (hit):
                hits += 1

        self.coverage = hits / numUsers
        print("Calculating Coverage...Done")

        return self.coverage

    def diversity(self, topNPredicted, simsAlgo):
        print("Calculating Diversity...")

        n = 0
        total = 0
        simsMatrix = simsAlgo.compute_similarities()
        for userID in topNPredicted.keys():
            pairs = itertools.combinations(topNPredicted[userID], 2)
            for pair in pairs:
                movie1 = pair[0][0]
                movie2 = pair[1][0]
                innerID1 = simsAlgo.trainset.to_inner_iid(str(movie1))
                innerID2 = simsAlgo.trainset.to_inner_iid(str(movie2))
                similarity = simsMatrix[innerID1][innerID2]
                total += similarity
                n += 1

        S = total / n
        self.diversity = (1 - S)
        print("Calculating Diversity...Done")

        return self.diversity

    def novelty(self, topNPredicted, rankings):
        print("Calculating Novelty...")

        n = 0
        total = 0
        for userID in topNPredicted.keys():
            for rating in topNPredicted[userID]:
                movieID = rating[0]
                rank = rankings[movieID]
                total += rank
                n += 1
        self.novelty = total / n
        print("Calculating Novelty...Done")

        return self.novelty

    # Scalability = time requirement of evaluation
    def setScalability(self, runTimeOfAlgorithm):
        self.scalability = runTimeOfAlgorithm

    def getScalability(self):
        return self.scalability
