from diplomamunka.main.service.recommender.algorithm.AlgorithmType import AlgorithmType
from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.ContentBased import ContentBased
from surprise import AlgoBase


class Hybrid(AlgoBase):

    algorithmType = AlgorithmType.HYBRID

    def __init__(self, algorithms, weights):
        AlgoBase.__init__(self)
        self.algorithms = algorithms
        self.weights = weights

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        print("Fitting with Hybrid algorithm...START!")
        for algorithm in self.algorithms:
            algorithm.fit(trainset)

        print("Fitting with Hybrid algorithm...END!")

        return self

    def estimate(self, u, i):
        sumScores = 0
        sumWeights = 0

        for idx in range(len(self.algorithms)):
            currentAlgorithm = self.algorithms[idx]
            estimate = currentAlgorithm.estimate(u, i)
            currentWeight = self.weights[idx]

            if isinstance(currentAlgorithm, CollaborativeFiltering) and not isinstance(estimate, float):
                estimate = estimate[0]

            sumScores += estimate * currentWeight
            sumWeights += currentWeight

        return sumScores / sumWeights
