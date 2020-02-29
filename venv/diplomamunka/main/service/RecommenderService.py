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
        dataset, trainSet, testSet = self.getDataset(), self.getTrainSet(), self.getTestSet()
        recommenderAlgorithm = self.investigateChosenDataset(dataset)
        popularityRankings = self.getPopularityRankings(dataset.getDatasetType())

        # print(popularityRankings)

        self.addAlgorithmToRecommender(recommenderAlgorithm)
        metricsFromEvaluation = self.evaluate(trainSet, testSet, popularityRankings)

        print("MAE: {}".format(metricsFromEvaluation.__getitem__(0).getMAE()))
        print("Novelty: {}".format(metricsFromEvaluation.__getitem__(0).getNovelty()))

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

    def getPopularityRankings(self, datasetType):
        return self.datasetAccessor.getPopularityRankings(datasetType)

    def addAlgorithmToRecommender(self, algorithm):
        self.recommender.addAlgorithm(algorithm)

    def evaluate(self, trainSet, testSet, popularityRankings):
        return self.recommender.evaluate(trainSet, testSet, popularityRankings)

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
