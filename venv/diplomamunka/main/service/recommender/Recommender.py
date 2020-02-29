from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise.model_selection import train_test_split


class Recommender:

    algorithms = []

    def __init__(self, dataset=None):
        self.dataset = dataset
        self.trainSet = None
        self.testSet = None

    def addAlgorithm(self, algorithm):
        self.algorithms.append(algorithm)

    # evaluates all of the algorithms, and returns with a list of Metrics objects
    def evaluate(self):
        print("Will evaluate some stuff...")
        metricsFromAlgorithms = []

        for algorithm in self.algorithms:
            metricsFromAlgorithms.append(algorithm.evaluate(self.trainSet, self.testSet))

        return metricsFromAlgorithms

    # computes the top 10 recommendations for the users
    def recommend(self):
        print("Will recommend some stuff...")
        return None
