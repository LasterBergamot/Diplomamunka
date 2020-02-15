from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise.model_selection import train_test_split


class Recommender:

    algorithms = []

    def __init__(self, dataset=None):
        self.dataset = dataset
        self.trainSet = None
        self.testSet = None

    def addAlgorithm(self, algorithm, name):
        self.algorithms.append(RecommenderAlgorithm(algorithm, name))

    # create train and validation sets here from the dataset
    def processChosenDataset(self):
        print("Will process the chosen dataset here...")
        # Build a 75/25 train/test split for measuring accuracy
        self.trainSet, self.testSet = train_test_split(self.dataset, test_size=.25, random_state=1)

    # evaluates all of the algorithms, and returns with a list of Metrics objects
    def evaluate(self):
        print("Will evaluate some stuff...")
        metricsFromAlgorithms = []

        for algorithm in self.algorithms:
            metricsFromAlgorithms.append(algorithm.evaluate())

        return metricsFromAlgorithms

    # computes the top 10 recommendations for the users
    def recommend(self):
        print("Will recommend some stuff...")
        return None
