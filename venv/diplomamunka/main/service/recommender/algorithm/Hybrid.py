from diplomamunka.main.service.recommender.algorithm.AlgorithmType import AlgorithmType
from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.ContentBased import ContentBased
from surprise import AlgoBase, KNNBaseline


class Hybrid(AlgoBase):

    algorithmType = AlgorithmType.HYBRID

    def __init__(self, algorithms, weights, sim_options={}):
        AlgoBase.__init__(self)
        self.algorithms = algorithms
        self.weights = weights

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        for algorithm in self.algorithms:
            algorithm.fit(trainset)

        return self

    def estimate(self, u, i):

        sumScores = 0
        sumWeights = 0

        for idx in range(len(self.algorithms)):
            if isinstance(self.algorithms[idx], CollaborativeFiltering):
                est = self.algorithms[idx].estimate(u, i) if isinstance(self.algorithms[idx].estimate(u, i), float) else self.algorithms[idx].estimate(u, i)[0]

                sumScores += est * self.weights[idx]
                sumWeights += self.weights[idx]
            elif isinstance(self.algorithms[idx], ContentBased):
                sumScores += self.algorithms[idx].estimate(u, i) * self.weights[idx]
                sumWeights += self.weights[idx]

        return sumScores / sumWeights
