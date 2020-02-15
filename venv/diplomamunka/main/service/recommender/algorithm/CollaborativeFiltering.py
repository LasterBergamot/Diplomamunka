from surprise import AlgoBase


class CollaborativeFiltering(AlgoBase):

    def __init__(self, model):
        AlgoBase.__init__(self)
        self.model = model

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        return self.model.fit(self, trainset)

    def estimate(self, u, i):
        return self.model.estimate(u, i)

