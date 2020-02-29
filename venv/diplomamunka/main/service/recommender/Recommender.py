from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise.model_selection import train_test_split


class Recommender:

    algorithms = []

    def addAlgorithm(self, algorithm):
        self.algorithms.append(algorithm)

    # evaluates all of the algorithms, and returns with a list of Metrics objects
    def evaluate(self, trainSet, testSet, popularityRankings):
        print("Will evaluate some stuff...")
        metricsFromAlgorithms = []

        for algorithm in self.algorithms:
            metricsFromAlgorithms.append(algorithm.evaluate(trainSet, testSet, popularityRankings))

        return metricsFromAlgorithms

    # computes the top 10 recommendations for the users
    def recommend(self):
        print("Will recommend some stuff...")
        return None
