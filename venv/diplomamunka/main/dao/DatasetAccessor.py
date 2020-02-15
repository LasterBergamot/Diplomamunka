from diplomamunka.main.dao.Dataset import Dataset
from diplomamunka.main.dao.DatasetConstants import MOVIELENS_100k_SHORT, MOVIELENS_100k_LONG, MOVIELENS_1m_SHORT, \
    MOVIELENS_1m_LONG, JESTER_SHORT, JESTER_LONG, NETFLIX_SHORT, NETFLIX_LONG
from diplomamunka.main.dao.DatasetType import DatasetType

class DatasetAccessor:

    def __init__(self):
        self.dataset = Dataset()

    def chooseDataset(self):
        print("Hi! Please choose from the available datasets:")
        print("Movielens-100k: type in 100k or ml-100k")
        print("Movielens-1m: type in 1m or ml-1m")
        print("Jester (dataset 2): type in j or jester")
        print("Netflix Prize dataset: type in n or netflix")
        inputDatasetString = input()
        datasetType = None

        if inputDatasetString == MOVIELENS_100k_SHORT or inputDatasetString == MOVIELENS_100k_LONG:
            datasetType = DatasetType.MOVIELENS_100K
        elif MOVIELENS_1m_SHORT == inputDatasetString or inputDatasetString == MOVIELENS_1m_LONG:
            datasetType = DatasetType.MOVIELENS_1m
        elif inputDatasetString == JESTER_SHORT or inputDatasetString == JESTER_LONG:
            datasetType = DatasetType.JESTER
        elif inputDatasetString == NETFLIX_SHORT or inputDatasetString == NETFLIX_LONG:
            datasetType = DatasetType.NETFLIX_PRIZE_DATASET
        else:
            print("The given input didn't match any available dataset name! Returning...")
            return

        self.dataset.loadDataset(datasetType)

    # create train and validation sets here from the dataset
    def processChosenDataset(self):
        self.dataset.processChosenDataset()

    def getDataset(self):
        return self.dataset.getDataset()
