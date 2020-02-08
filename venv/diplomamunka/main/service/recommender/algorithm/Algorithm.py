from surprise import AlgoBase


class Algorithm:

    algorithm: AlgoBase

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def evaluate(self):
        print("Will evaluate the given data with the given algorithm here...")
