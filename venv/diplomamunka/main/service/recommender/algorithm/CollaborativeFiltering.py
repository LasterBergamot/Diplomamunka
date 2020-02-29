from diplomamunka.main.service.recommender.algorithm.AlgorithmType import AlgorithmType
from surprise import AlgoBase


class CollaborativeFiltering(AlgoBase):

    algorithmType = AlgorithmType.COLLABORATIVE_FILTERING

    def __init__(self, model):
        AlgoBase.__init__(self)
        self.model = model

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        return self.model.fit(trainset)

    def estimate(self, u, i):
        return self.model.estimate(u, i)

