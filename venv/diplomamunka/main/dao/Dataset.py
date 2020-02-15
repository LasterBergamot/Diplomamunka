from collections import defaultdict

from diplomamunka.main.dao.DatasetType import DatasetType
from surprise.model_selection import train_test_split


from surprise import Dataset as surpriseDataset, Reader


class Dataset:

    def __init__(self):
        self.dataset = None
        self.trainSet = None
        self.testSet = None

    def loadDataset(self, datasetType):
        print("Loading dataset: ", datasetType.value)
        # if datasetType == DatasetType.NETFLIX_PRIZE_DATASET:
        #     self.dataset = self.loadNetflixDataset()
        # else:
        self.dataset = surpriseDataset.load_builtin(datasetType.value)

        print(self.dataset.has_been_split)

    def loadNetflixDataset(self):
        netflixCSVPath = r"D:\Egyetem\Msc\Diplomamunka\Netflix_Prize_Dataset\Netflix_dataframe_to_csv_export.csv"
        reader = Reader(line_format="user rating item", sep=",")

        return surpriseDataset.load_from_file(netflixCSVPath, reader)

    # create train and validation sets here from the dataset
    def processChosenDataset(self):
        print("Will process the chosen dataset here...")
        # Build a 75/25 train/test split for measuring accuracy
        self.trainSet, self.testSet = train_test_split(self.dataset, test_size=.25, random_state=1)

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
