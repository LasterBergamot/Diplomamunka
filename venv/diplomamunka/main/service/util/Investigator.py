from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise import KNNBaseline


class Investigator:

    # Dataset infos:
    # ml-100k: u.info file
    # users: 943
    # items (movies): 1682
    # ratings: 100000
    # size of matrix: 943 * 1682 = 1 586 126
    # ratio: 0.063
    ML_100k_NUMBER_OF_USERS = 943
    ML_100k_NUMBER_OF_ITEMS = 1682
    ML_100k_NUMBER_OF_RATINGS = 100000
    ML_100k_SIZE_OF_MATRIX = ML_100k_NUMBER_OF_RATINGS * ML_100k_NUMBER_OF_ITEMS
    ML_100k_RATIO = ML_100k_NUMBER_OF_RATINGS / ML_100k_SIZE_OF_MATRIX

    # ml-1m: README
    # users: 6040
    # items (movies): 3900
    # ratings: 1000209
    # size of matrix: 6040 * 3900 = 23 556 000
    # ratio: 0.0424
    ML_1M_NUMBER_OF_USERS = 6040
    ML_1M_NUMBER_OF_ITEMS = 3900
    ML_1M_NUMBER_OF_RATINGS = 1000209
    ML_1M_SIZE_OF_MATRIX = ML_1M_NUMBER_OF_USERS * ML_1M_NUMBER_OF_ITEMS
    ML_1M_RATIO = ML_1M_NUMBER_OF_RATINGS / ML_1M_SIZE_OF_MATRIX

    # jester: https://goldberg.berkeley.edu/jester-data/ - dataset 2 - counted the number of 99s => 641 007
    # users: 23 500
    # items (jokes): 101
    # ratings: 1 761 439
    # size of matrix: 23 500 * 101 = 2 373 500
    # ratio: 0.742
    JESTER_NUMBER_OF_USERS = 23500
    JESTER_NUMBER_OF_ITEMS = 101
    JESTER_NUMBER_OF_RATINGS = 1761439
    JESTER_SIZE_OF_MATRIX = JESTER_NUMBER_OF_USERS * JESTER_NUMBER_OF_ITEMS
    JESTER_RATIO = JESTER_NUMBER_OF_RATINGS / JESTER_SIZE_OF_MATRIX

    # 5% baseline?
    # KNN: ratio >= 5%
    # Content-Based: ratio < 5%
    # Hybrid: ratio >= 50%

    # could return with several algorithm
    def investigateChosenDataset(self, datasetAccessor):
        print("Will investigate the sparsity of the chosen dataset...")
        return RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline", datasetAccessor.getDataset().getDatasetType().value)
