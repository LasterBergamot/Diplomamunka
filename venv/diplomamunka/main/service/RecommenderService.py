from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor
from diplomamunka.main.service.recommender.Recommender import Recommender
from diplomamunka.main.service.recommender.algorithm.Algorithm import Algorithm
from diplomamunka.main.service.util.Metrics import Metrics
from diplomamunka.main.service.util.Investigator import Investigator
from diplomamunka.main.service.util.Plotter import Plotter
from diplomamunka.main.service.util.Stopwatch import Stopwatch


class RecommenderService:

    algorithms = []

    datasetAccessor: DatasetAccessor
    investigator: Investigator
    recommender: Recommender
    stopwatch: Stopwatch
    metrics: Metrics
    plotter: Plotter

    def __init__(self):
        self.datasetAccessor = DatasetAccessor()
        self.investigator = Investigator()
        self.recommender = Recommender()
        self.stopwatch = Stopwatch()
        self.metrics = Metrics()
        self.plotter = Plotter()

    def start(self):
        print(self.chooseDataset())
        print(self.investigateChosenDataset())
        self.evaluate()
        self.recommend()
        self.showMetrics()
        self.plot()

    def chooseDataset(self):
        return self.datasetAccessor.chooseDataset()

    def investigateChosenDataset(self):
        return self.investigator.investigateChosenDataset()

    # create train and validation sets here from the dataset
    def processChosenDataset(self):
        print("Will process the chosen dataset here...")

    def addAlgorithm(self, algorithm):
        self.algorithms.append(Algorithm(algorithm))

    # use stopwatch here
    def evaluate(self):
        self.recommender.evaluate()

    def recommend(self):
        self.recommender.recommend()

    def showMetrics(self):
        self.metrics.showMetrics()

    def plot(self):
        self.plotter.plot()
