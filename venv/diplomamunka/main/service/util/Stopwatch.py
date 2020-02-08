from surprise import AlgoBase


class Stopwatch:

    algorithm: AlgoBase

    def __init__(self, algorithm=None):
        self.algorithm = algorithm

    # Relevant only for algorithm using Pearson baseline similarity or the BaselineOnly algorithm
    def compute_baselines(self):
        return self.algorithm.compute_baselines()

    def compute_similarities(self):
        return self.algorithm.compute_similarities()

    def default_prediction(self):
        return self.algorithm.default_prediction()

    def fit(self, trainSet):
        return self.algorithm.fit(trainSet)

    def get_neighbors(self, numberOfNeighbors, innerId):
        return self.algorithm.get_neighbors(numberOfNeighbors, innerId)

    def predict(self, rawUserId, rawItemId, trueRating=None, clipEstimation=True, verbose=False):
        return self.algorithm.predict(rawUserId, rawItemId, trueRating, clipEstimation, verbose)

    def test(self, testSet, verbose=False):
        return self.algorithm.test(testSet, verbose)

    def getUserBaseline(self):
        return self.algorithm.bu

    def getItemBaseline(self):
        return self.algorithm.bi

    def getBaselineOptions(self):
        return self.algorithm.bsl_options

    def getSimilarityOptions(self):
        return self.algorithm.sim_options

    def getTrainSet(self):
        return self.algorithm.trainset
