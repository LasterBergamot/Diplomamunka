from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor, QUIT_LONG, QUIT_SHORT
from diplomamunka.main.dao.DatasetConstants import MOVIELENS_100k_SHORT, MOVIELENS_100k_LONG, MOVIELENS_1m_LONG, \
    MOVIELENS_1m_SHORT, JESTER_SHORT, JESTER_LONG, NETFLIX_SHORT, NETFLIX_LONG
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.Recommender import Recommender
from diplomamunka.main.service.recommender.algorithm.AlgorithmAndAccessor import AlgorithmAndAccessor
from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from diplomamunka.main.service.util.Investigator import Investigator, investigateChosenDataset
from surprise import KNNBasic, KNNWithMeans

TESTSET_SIZE = 0.25

CF_MEANS_ITEM_PEARSON = RecommenderAlgorithm(CollaborativeFiltering(KNNWithMeans(sim_options={'name': 'pearson', 'user_based': False})), "KNNWithMeans: Item-based CF - Pearson", "")
CF_BASIC_ITEM_PEARSON = RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options={'name': 'pearson', 'user_based': False})), "KNNBasic: Item-based CF - Pearson", "")

def addDatasetAccessorToSet(datasetAccessors, datasetType):
    datasetAccessor = DatasetAccessor()
    datasetAccessor.loadDataset(datasetType)
    datasetAccessors.append(datasetAccessor)

def createDatasetAccessorsFromDatasets(selectedDatasets):
    datasetAccessors = []

    for dataset in selectedDatasets:
        addDatasetAccessorToSet(datasetAccessors, dataset)

    return datasetAccessors

def chooseDatasets():
    choosenDatasets = set()
    inputString = ""

    print("\nHi!")
    print("Please choose from the available datasets:")
    print("Note: no duplicates will be added!\n")
    while inputString != QUIT_SHORT and inputString != QUIT_LONG:
        print("To quit: type in q or quit")
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
        print("\nPrinting metrics for dataset [{}] with the algorithm called: [{}]\n".format(metrics.getDatasetName(), metrics.getAlgorithmName()))
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

def printSelectedDatasets(selectedDatasets):
    print("The selected datasets:")
    for dataset in selectedDatasets:
        print(dataset.value)

def createTrainAndTestSetsForTheSelectedDatasets(datasetAccessors, testSetSize):
    for datasetAccessor in datasetAccessors:
        datasetAccessor.processChosenDataset(testSetSize)

class RecommenderService:

    metricsList: list

    def __init__(self):
        self.datasetAccessor = DatasetAccessor()
        self.investigator = Investigator()
        self.recommender = Recommender()

    def start(self):
        # create a set of datasets - they have to be unique
        # create a list of dataset accessors
        # be able to choose several datasets at the beginning, so put a for loop here and return a set of datasets
        selectedDatasets = chooseDatasets()
        datasetAccessors = createDatasetAccessorsFromDatasets(selectedDatasets)
        # ends here

        printSelectedDatasets(selectedDatasets)

        # a for loop: loop through all of the dataset accessors
        # create train and test sets
        createTrainAndTestSetsForTheSelectedDatasets(datasetAccessors, testSetSize=TESTSET_SIZE)
        # ends here

        # for loop: loop through the list/set created above
        # select an algorithm for each through investigation
        self.addAlgorithmsAndDatasetAccessorsToRecommenderAfterInvestigation(datasetAccessors)
        # ends here

        self.printSelectedAlgorithmsWithDatasets()

        # evaluate every alg
        # since the dataset accessor is passed with the alg, no parameters are required
        metricsFromEvaluation = self.recommender.evaluate()

        # print the metrics for each alg
        showMetrics(metricsFromEvaluation)

    def printSelectedAlgorithmsWithDatasets(self):
        print("Selected algorithms with datasets:")
        algorithmsAndAccessors = self.recommender.getAlgorithmsAndAccessors()
        for algorithmAndAccessor in algorithmsAndAccessors:
            algorithm = algorithmAndAccessor.getRecommenderAlgorithm()
            accessor = algorithmAndAccessor.getDatasetAccessor()

            print("Algorithm selected for dataset [{}]: [{}]".format(accessor.getDataset().getDatasetType().value, algorithm.getAlgorithmName()))

    def addAlgorithmsAndDatasetAccessorsToRecommenderAfterInvestigation(self, datasetAccessors):
        for datasetAccessor in datasetAccessors:
            recommenderAlgorithm = investigateChosenDataset(datasetAccessor)

            # add algorithm and the dataset accessor as well
            self.recommender.addAlgorithmAndAccessor(AlgorithmAndAccessor(recommenderAlgorithm, datasetAccessor))

    def tester(self):
        print("Testing...START!")
        selectedDatasets = chooseDatasets()
        datasetAccessors = createDatasetAccessorsFromDatasets(selectedDatasets)

        printSelectedDatasets(selectedDatasets)

        createTrainAndTestSetsForTheSelectedDatasets(datasetAccessors, TESTSET_SIZE)

        self.testerAddDatasetAccessorAndAlgorithmToRecommender(datasetAccessors)

        self.printSelectedAlgorithmsWithDatasets()

        metricsFromEvaluation = self.recommender.evaluate()

        showMetrics(metricsFromEvaluation)

        print("Testing...DONE!")

    def testerAddDatasetAccessorAndAlgorithmToRecommender(self, datasetAccessors):
        algorithms = [CF_BASIC_ITEM_PEARSON, CF_MEANS_ITEM_PEARSON]

        for datasetAccessor in datasetAccessors:
            datasetName = datasetAccessor.getDataset().getDatasetType().value

            for algorithm in algorithms:
                recommenderAlgorithm = algorithm
                recommenderAlgorithm.setDatasetName(datasetName)

                self.recommender.addAlgorithmAndAccessor(AlgorithmAndAccessor(recommenderAlgorithm, datasetAccessor))
