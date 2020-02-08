from surprise import AlgoBase


class Stopwatch:

    algorithm: AlgoBase

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def asd(self):
        self.algorithm.bi
        self.algorithm.bsl_options
        self.algorithm.bu
        self.algorithm.sim_options
        self.algorithm.trainset

    def compute_baselines(self):
        self.algorithm.compute_baselines()

    def compute_similarities(self):
        self.algorithm.compute_similarities()

    def default_prediction(self):
        self.algorithm.default_prediction()

    def fit(self):
        self.algorithm.fit()

    def get_neighbors(self):
        self.algorithm.get_neighbors()

    def predict(self):
        self.algorithm.predict()

    def test(self):
        self.algorithm.test()
