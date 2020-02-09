from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm


class Recommender:

    algorithms = []

    dataset: object

    def __init__(self, dataset=None):
        self.dataset = dataset

    def addAlgorithm(self, algorithm, name):
        self.algorithms.append(RecommenderAlgorithm(algorithm, name))

    # evaluates all of the algorithm, and returns with an array of Metrics objects
    def evaluate(self):
        print("Will evaluate some stuff...")

    # create train and validation sets here from the dataset
    def processChosenDataset(self):
        print("Will process the chosen dataset here...")

    # computes the top 10 recommendations for the users
    def recommend(self):
        print("Will recommend some stuff...")
        return None
