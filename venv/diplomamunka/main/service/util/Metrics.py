# Contains every metric data for the given algorithm
import string


class Metrics:

    algorithmName: string
    mae: float
    rmse: float
    coverage: float
    diversity: float
    novelty: float
    scalability: float

    def __init__(self, algorithmName=None):
        self.algorithmName = algorithmName

    def MAE(self):
        print("Will calculate Mean Absolute Error here...")

    def RMSE(self):
        print("Will calculate Root Mean Squared Error here...")

    def coverage(self):
        print("Will calculate coverage here...")

    def diversity(self):
        print("Will calculate diversity here...")

    def novelty(self):
        print("Will calculate novelty here...")

    # Scalability = time requirement of evaluation
    def scalability(self):
        print("Will calculate scalability here...")
