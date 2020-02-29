from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor
from diplomamunka.main.service.recommender.Recommender import Recommender
from diplomamunka.main.service.util.Investigator import Investigator
from diplomamunka.main.service.util.Metrics import Metrics
from diplomamunka.main.service.util.Plotter import Plotter


class RecommenderService:

    metricsList: list

    def __init__(self):
        self.datasetAccessor = DatasetAccessor()
        self.investigator = Investigator()
        self.recommender = Recommender()
        self.metrics = Metrics()
        self.plotter = Plotter()

    def start(self):
        self.chooseDataset()
        self.processChosenDataset(0.25)
        dataset = self.getDataset()
        trainSet = self.getTrainSet()
        testSet = self.getTestSet()
        recommenderAlgorithm = self.investigateChosenDataset(dataset)
        additionalDataDict = self.getAdditionalData(recommenderAlgorithm.algorithm.algorithmType)

        print(additionalDataDict)

        self.addAlgorithmToRecommender(recommenderAlgorithm)
        # metricsFromEvaluation = self.evaluate()
        # self.recommend()
        # self.showMetrics(metricsFromEvaluation)
        # self.plot()

    def chooseDataset(self):
        return self.datasetAccessor.chooseDataset()

    def processChosenDataset(self, testSetSize):
        self.datasetAccessor.processChosenDataset(testSetSize)

    def getDataset(self):
        return self.datasetAccessor.getDataset()

    def getTrainSet(self):
        return self.datasetAccessor.getTrainSet()

    def getTestSet(self):
        return self.datasetAccessor.getTestSet()

    def investigateChosenDataset(self, dataset):
        return self.investigator.investigateChosenDataset(dataset)

    def getAdditionalData(self, algorithmType):
        return self.datasetAccessor.getAdditionalData(algorithmType)

    def addAlgorithmToRecommender(self, algorithm):
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
