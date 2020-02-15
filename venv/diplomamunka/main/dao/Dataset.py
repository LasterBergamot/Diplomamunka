from collections import defaultdict

from surprise import Dataset as surpriseDataset, Reader
from surprise.model_selection import train_test_split


class Dataset:

    def __init__(self):
        self.dataset = None
        self.datasetName = None
        self.trainSet = None
        self.testSet = None

    def loadDataset(self, datasetType):
        print("Loading dataset: [{}]".format(datasetType.value))
        # if datasetType == DatasetType.NETFLIX_PRIZE_DATASET:
        #     self.dataset = self.loadNetflixDataset()
        # else:
        self.dataset = surpriseDataset.load_builtin(datasetType.value)
        self.datasetName = datasetType.value

        print("Loading dataset: [{}] done!".format(datasetType.value))

    def loadNetflixDataset(self):
        netflixCSVPath = r"D:\Egyetem\Msc\Diplomamunka\Netflix_Prize_Dataset\Netflix_dataframe_to_csv_export.csv"
        reader = Reader(line_format="user rating item", sep=",")

        return surpriseDataset.load_from_file(netflixCSVPath, reader)

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        print("Spliting dataset [{}] into train- and testSets, with test_size [{}]!".format(self.datasetName, testSetSize))
        # Build a 75/25 train/test split for measuring accuracy
        self.trainSet, self.testSet = train_test_split(self.dataset, test_size=testSetSize, random_state=1)

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                movieID = int(row[1])
                ratings[movieID] += 1
        rank = 1
        for movieID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movieID] = rank
            rank += 1
        return rankings

    def getDataset(self):
        return self.dataset

    def getDatasetName(self):
        return self.datasetName

    def getTrainSet(self):
        return self.trainSet

    def getTestSet(self):
        return self.testSet
