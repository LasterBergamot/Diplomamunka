from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor
from diplomamunka.main.service.recommender.Recommender import Recommender
from diplomamunka.main.service.util.Investigator import Investigator
from diplomamunka.main.service.util.Metrics import Metrics
from diplomamunka.main.service.util.Plotter import Plotter


class RecommenderService:

    datasetAccessor: DatasetAccessor
    investigator: Investigator
    recommender: Recommender
    metrics: Metrics
    plotter: Plotter

    def __init__(self):
        self.datasetAccessor = DatasetAccessor()
        self.investigator = Investigator()
        self.recommender = Recommender()
        self.metrics = Metrics()
        self.plotter = Plotter()

    def start(self):
        dataset = self.chooseDataset()
        algorithm = self.investigateChosenDataset(dataset)
        self.addAlgorithm(algorithm)
        metricsArray = self.evaluate()
        topN = self.recommend()
        self.showMetrics()
        self.plot()

    def chooseDataset(self):
        return self.datasetAccessor.chooseDataset()

    def investigateChosenDataset(self, dataset):
        return self.investigator.investigateChosenDataset(dataset)

    def processChosenDataset(self):
        self.recommender.processChosenDataset()

    def addAlgorithm(self, algorithm):
        self.recommender.addAlgorithm(algorithm)

    def evaluate(self):
        return self.recommender.evaluate()

    def recommend(self):
        return self.recommender.recommend()

    def showMetrics(self):
        self.metrics.showMetrics()

    def plot(self):
        self.plotter.plot()
