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
        self.addAlgorithmToRecommender(recommenderAlgorithm)
        metricsFromEvaluation = self.evaluate(trainSet, testSet, popularityRankings)
        antiTestSet = self.datasetAccessor.getAntiTestSetForUser(trainSet)
        self.recommendTopN(trainSet, antiTestSet)
        self.showMetrics(metricsFromEvaluation)
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

    def recommendTopN(self, trainSet, antiTestSet, n=10):
        recommendations = self.recommender.recommend(trainSet, antiTestSet)

        print("\nWe recommend:")
        for ratings in recommendations[:n]:
            # print(ml.getMovieName(ratings[0]), ratings[1])
            print(ratings)

        print()

    # prints out all of the metrics info
    def showMetrics(self, metricsFromEvaluation):
        for metrics in metricsFromEvaluation:
            print("\nPrinting metrics for the algorithm called: {}\n".format(metrics.getAlgorithmName()))
            print("RMSE:        {}".format(metrics.getRMSE()))
            print("MAE:         {}".format(metrics.getMAE()))
            print("Coverage:    {}".format(metrics.getCoverage()))
            print("Diversity:   {}".format(metrics.getDiversity()))
            print("Novelty:     {}".format(metrics.getNovelty()))
            print("Scalability: {} seconds".format(metrics.getScalability()))

        print("\nLegend:\n")
        print("RMSE:        Root Mean Squared Error. Lower values mean better accuracy.")
        print("MAE:         Mean Absolute Error. Lower values mean better accuracy.")
        print("Coverage:    Ratio of users for whom recommendations above a certain threshold exist. Higher is better.")
        print("Diversity:   1-S, where S is the average similarity score between every possible pair of recommendations for a given user. Higher means more diverse.")
        print("Novelty:     Average popularity rank of recommended items. Higher means more novel.")
        print("Scalability: The time required for the algorithm to evaluate the data.")

    def plot(self):
        self.plotter.plot()
