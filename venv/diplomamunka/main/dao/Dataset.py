from diplomamunka.main.dao.DatasetType import DatasetType
from surprise import Dataset as surpriseDataset, Reader
from surprise.model_selection import train_test_split


class Dataset:

    def __init__(self):
        self.dataset = None
        self.datasetType = None
        self.trainSet = None
        self.testSet = None

    def loadDataset(self, datasetType):
        print("Loading dataset: [{}]...START!".format(datasetType.value))
        self.datasetType = datasetType

        if datasetType == DatasetType.NETFLIX_PRIZE_DATASET:
            self.dataset = self.loadNetflixDataset()
        else:
            self.dataset = surpriseDataset.load_builtin(datasetType.value)

        print("Loading dataset: [{}]...DONE!".format(datasetType.value))

    def loadNetflixDataset(self):
        # netflixCSVPath = r"D:\Egyetem\Msc\Diplomamunka\Netflix_Prize_Dataset\Netflix_dataframe_to_csv_export.csv"
        netflixCSVPath = r"D:\Netflix_dataframe_to_csv_export.csv"
        reader = Reader(line_format="user rating timestamp item", sep=",")

        return surpriseDataset.load_from_file(netflixCSVPath, reader)

    # create train and validation sets here from the dataset
    def processChosenDataset(self, testSetSize):
        print("Splitting dataset [{}] into train- and testSets, with test_size [{}]!".format(self.getDatasetName(), testSetSize))
        # Build a 75/25 train/test split for measuring accuracy
        self.trainSet, self.testSet = train_test_split(self.dataset, test_size=testSetSize, random_state=1)

    def getDataset(self):
        return self.dataset

    def getDatasetName(self):
        return self.datasetType.value

    def getDatasetType(self):
        return self.datasetType

    def getTrainSet(self):
        return self.trainSet

    def getTestSet(self):
        return self.testSet
