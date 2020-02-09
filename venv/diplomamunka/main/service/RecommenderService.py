from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor
from diplomamunka.main.service.recommender.Recommender import Recommender
from diplomamunka.main.service.util.Investigator import Investigator
from diplomamunka.main.service.util.Metrics import Metrics
from diplomamunka.main.service.util.Plotter import Plotter


class RecommenderService:

    metricsList: list

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
        algorithm = self.selectRecommenderAlgorithm(dataset)
        self.addAlgorithm(algorithm)
        metricsFromEvaluation = self.evaluate()
        self.recommend()
        self.showMetrics(metricsFromEvaluation)
        self.plot()

    def chooseDataset(self):
        return self.datasetAccessor.chooseDataset()

    def selectRecommenderAlgorithm(self, dataset):
        return self.investigator.selectRecommenderAlgorithm(dataset)

    def processChosenDataset(self):
        self.recommender.processChosenDataset()

    def addAlgorithm(self, algorithm):
        self.recommender.addAlgorithm(algorithm)

    def evaluate(self):
        return self.recommender.evaluate()

    def recommend(self):
        topN = self.recommender.recommend()
        print("Will print TopN recommendations here...")

    # prints out all of the metrics info
    def showMetrics(self, metricsFromEvaluation):
        print("Will show metrics here...")

    def plot(self):
        self.plotter.plot()

    def addMetricsFromArrayToMetricsList(self, otherMetricsList):
        self.metricsList.extend(otherMetricsList)
