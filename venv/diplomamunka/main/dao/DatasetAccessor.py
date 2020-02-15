from collections import defaultdict

from diplomamunka.main.dao.DatasetType import DatasetType
from surprise.model_selection import train_test_split


class DatasetAccessor:

    def chooseDataset(self):
        print("The user will choose the dataset here...")
        return DatasetType.MOVIELENS_100K.value

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