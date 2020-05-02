from diplomamunka.main.dao import DatasetConstants
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.ContentBased import ContentBased
from diplomamunka.main.service.recommender.algorithm.Hybrid import Hybrid
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise import KNNBasic, KNNWithMeans
from surprise.prediction_algorithms.matrix_factorization import SVD

KNN_BASIC_ITEM_BASED_CF = "KNNBasic: Item-based CF"

SIM_OPTIONS = {'name': 'pearson', 'user_based': False}

RATINGS_THRESHOLD = 1500000
RATIO_THRESHOLD = 0.5

def getRecommenderAlgorithmForML100k(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options=SIM_OPTIONS)), KNN_BASIC_ITEM_BASED_CF, datasetName)

def getRecommenderAlgorithmForML1m(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options=SIM_OPTIONS)), KNN_BASIC_ITEM_BASED_CF, datasetName)

def getRecommenderAlgorithmForJester(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options=SIM_OPTIONS)), KNN_BASIC_ITEM_BASED_CF, datasetName)

def getRecommenderAlgorithmForNetflix(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(ContentBased(datasetAccessor), "Content-Based KNN", datasetName)

def getRecommenderAlgorithm(datasetNumberOfRatings, datasetRatio, datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    # if there are too many ratings/data matrix factorization can be used
    if datasetNumberOfRatings >= RATINGS_THRESHOLD and datasetRatio >= RATIO_THRESHOLD:
        svd = SVD()
        knnItemPearson = CollaborativeFiltering(KNNWithMeans(sim_options=SIM_OPTIONS))

        recommenderAlgorithm = RecommenderAlgorithm(Hybrid([svd, knnItemPearson], [0.5, 0.5]), "Hybrid: SVD and CF: Item-based KNNWithMeans", datasetName)

    # if most of the matrix is filled with data CF can be used
    elif datasetRatio >= RATIO_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNWithMeans(sim_options=SIM_OPTIONS)), "CF: Item-based KNNWithMeans", datasetName)

    # if the matrix is sparse: content-based + KNN CF
    else:
        cb = ContentBased(datasetAccessor)
        knnItemPearson = CollaborativeFiltering(KNNWithMeans(sim_options=SIM_OPTIONS))

        recommenderAlgorithm = RecommenderAlgorithm(Hybrid([cb, knnItemPearson], [0.5, 0.5]), "Hybrid: Content-Based KNN and CF: Item-based KNNWithMeans", datasetName)

    return recommenderAlgorithm

# could return with several algorithm
def investigateChosenDataset(datasetAccessor):
    datasetType = datasetAccessor.getDataset().getDatasetType()
    numberOfRatings = 0
    ratio = 0

    if datasetType == DatasetType.MOVIELENS_100K:
        numberOfRatings = DatasetConstants.ML_100k_NUMBER_OF_RATINGS
        ratio = DatasetConstants.ML_100k_RATIO
    elif datasetType == DatasetType.MOVIELENS_1m:
        numberOfRatings = DatasetConstants.ML_1M_NUMBER_OF_RATINGS
        ratio = DatasetConstants.ML_1M_RATIO
    elif datasetType == DatasetType.JESTER:
        numberOfRatings = DatasetConstants.JESTER_NUMBER_OF_RATINGS
        ratio = DatasetConstants.JESTER_RATIO
    elif datasetType == DatasetType.NETFLIX_PRIZE_DATASET:
        numberOfRatings = DatasetConstants.NETFLIX_NUMBER_OF_RATINGS
        ratio = DatasetConstants.NETFLIX_RATIO

    return getRecommenderAlgorithm(numberOfRatings, ratio, datasetAccessor)

class Investigator:
    pass
