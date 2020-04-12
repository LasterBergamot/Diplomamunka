from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor, QUIT_LONG, QUIT_SHORT
from diplomamunka.main.dao.DatasetConstants import MOVIELENS_100k_SHORT, MOVIELENS_100k_LONG, MOVIELENS_1m_LONG, \
    MOVIELENS_1m_SHORT, JESTER_SHORT, JESTER_LONG, NETFLIX_SHORT, NETFLIX_LONG
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.Recommender import Recommender
from diplomamunka.main.service.util.Investigator import Investigator
from diplomamunka.main.service.util.Metrics import Metrics
from diplomamunka.main.service.util.Plotter import Plotter

def addDatasetAccessorToSet(datasetAccessors, datasetType):
    datasetAccessor = DatasetAccessor()
    datasetAccessor.loadDataset(datasetType)
    datasetAccessors.append(datasetAccessor)

def createDatasetAccessorsFromDatasets(choosenDatasets):
    datasetAccessors = []

    for dataset in choosenDatasets:
        addDatasetAccessorToSet(datasetAccessors, dataset)

    return datasetAccessors

def chooseDatasets():
    choosenDatasets = set()
    inputString = ""

    print("\nHi!")
    print("Please choose from the available datasets:")
    print("Note: no duplicates will be added!\n")
    while inputString != QUIT_SHORT and inputString != QUIT_LONG:
        print("Movielens-100k: type in 100k or ml-100k")
        print("Movielens-1m: type in 1m or ml-1m")
        print("Jester (dataset 2): type in j or jester")
        print("Netflix Prize dataset: type in n or netflix")
        # Instead of Netflix (??) the Book-Crossing Dataset will come here
        inputString = input()

        if inputString == MOVIELENS_100k_SHORT or inputString == MOVIELENS_100k_LONG:
            choosenDatasets.add(DatasetType.MOVIELENS_100K)
            print(DatasetType.MOVIELENS_100K.value + " added!\n")
        elif MOVIELENS_1m_SHORT == inputString or inputString == MOVIELENS_1m_LONG:
            choosenDatasets.add(DatasetType.MOVIELENS_1m)
            print(DatasetType.MOVIELENS_1m.value + " added!\n")
        elif inputString == JESTER_SHORT or inputString == JESTER_LONG:
            choosenDatasets.add(DatasetType.JESTER)
            print(DatasetType.JESTER.value + " added!\n")
        elif inputString == NETFLIX_SHORT or inputString == NETFLIX_LONG:
            choosenDatasets.add(DatasetType.NETFLIX_PRIZE_DATASET)
            print(DatasetType.NETFLIX_PRIZE_DATASET.value + " added!\n")
        elif inputString == QUIT_SHORT or inputString == QUIT_LONG:
            print("Quitting!")
        else:
            print("The given input didn't match any available dataset name!\n")

    return choosenDatasets

# prints out all of the metrics info
def showMetrics(metricsFromEvaluation):
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

class RecommenderService:

    metricsList: list

    def __init__(self):
        self.datasetAccessor = DatasetAccessor()
        self.investigator = Investigator()
        self.recommender = Recommender()
        self.metrics = Metrics()
        self.plotter = Plotter()

    def start(self):
        # create a list/set of dataset accessors - they have to be unique
        # be able to choose several datasets at the beginning, so put a for loop here and return an array of datasets
        choosenDatasets = chooseDatasets()
        datasetAccessors = createDatasetAccessorsFromDatasets(choosenDatasets)
        # ends here

        print("The selected datasets:")
        for dataset in choosenDatasets:
            print(dataset.value)

        # a foor loop: loop through all of the dataset accessors
        # process them
        # self.processChosenDataset(0.25)
        # dataset, trainSet, testSet = self.getDataset(), self.getTrainSet(), self.getTestSet()
        # # ends here
        #
        # # for loop: loop through the list/set created above
        # # select an algorithm for each through investigation
        # # popularity rankings (optional, for now)
        # # add each alg to the recommender
        # recommenderAlgorithm = self.investigateChosenDataset(dataset)
        #
        # # move this inside recommender
        # popularityRankings = self.getPopularityRankings(dataset.getDatasetType())
        #
        # # add algorithm and the dataset accessor as well
        # self.addAlgorithmToRecommender(recommenderAlgorithm)
        # # ends here
        #
        # # evaluate every alg
        # # since the dataset accessor is passed with the alg, no parameters are required
        # metricsFromEvaluation = self.evaluate(trainSet, testSet, popularityRankings)
        #
        # # recommendation is not required right now
        # # if dataset == DatasetType.MOVIELENS_100K or dataset == DatasetType.MOVIELENS_1m:
        # #     antiTestSet = self.datasetAccessor.getAntiTestSetForUser(trainSet)
        # #     self.recommendTopN(trainSet, antiTestSet)
        #
        # # print the metrics for each alg
        # self.showMetrics(metricsFromEvaluation)
        #
        # # plot the data for each alg
        # # self.plot()

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
        recommendationsFromEveryAlgorithm = self.recommender.recommend(trainSet, antiTestSet)

        print("\nWe recommend the followings:\n")
        for algorithmName in recommendationsFromEveryAlgorithm:
            print("The [{}] algorithm recommends:".format(algorithmName))
            recommendationsFromOneAlgorithm = recommendationsFromEveryAlgorithm[algorithmName]

            self.datasetAccessor.loadMovieIDsAndNames()
            for ratings in recommendationsFromOneAlgorithm[:n]:
                print(self.datasetAccessor.getMovieNameByID(ratings[0]), ratings[1])

        print()

    def plot(self):
        self.plotter.plot()
