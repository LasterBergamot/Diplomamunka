from diplomamunka.main.dao import DatasetConstants
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.ContentBased import ContentBased
from diplomamunka.main.service.recommender.algorithm.Hybrid import Hybrid
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise import KNNBasic, KNNWithMeans
from surprise.prediction_algorithms.matrix_factorization import SVD

RATINGS_THRESHOLD = 1500000
RATIO_THRESHOLD = 0.5

def getRecommenderAlgorithmForML100k(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options={'name': 'pearson', 'user_based': False})), "KNNBasic: Item-based CF", datasetName)

def getRecommenderAlgorithmForML1m(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options={'name': 'pearson', 'user_based': False})), "KNNBasic: Item-based CF", datasetName)

def getRecommenderAlgorithmForJester(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    return RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options={'name': 'pearson', 'user_based': False})), "KNNBasic: Item-based CF", datasetName)

def getRecommenderAlgorithm(datasetNumberOfRatings, datasetRatio, datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value

    # if there are too many ratings/data matrix factorization can be used
    if datasetNumberOfRatings >= RATINGS_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(SVD(), "SVD", datasetName)

    # if most of the matrix is filled with data CF can be used
    elif datasetRatio >= RATIO_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNWithMeans(sim_options={'name': 'pearson', 'user_based': False})), "CF: Item-based KNNWithMeans", datasetName)

    # if the matrix is sparse: content-based + KNN CF
    else:
        cb = ContentBased(datasetAccessor)
        knnItem = CollaborativeFiltering(KNNWithMeans(sim_options={'name': 'pearson', 'user_based': True}))

        recommenderAlgorithm = RecommenderAlgorithm(Hybrid([cb, knnItem], [0.5, 0.5]), "Hybrid: Content-Based KNN and CF: User-based KNNWithMeans", datasetName)

    return recommenderAlgorithm

# could return with several algorithm
def investigateChosenDataset(datasetAccessor):
    print("Will investigate the sparsity of the chosen dataset...")
    datasetType = datasetAccessor.getDataset().getDatasetType()

    if datasetType == DatasetType.MOVIELENS_100K:
        recommenderAlgorithm = getRecommenderAlgorithm(DatasetConstants.ML_100k_NUMBER_OF_RATINGS, DatasetConstants.ML_100k_RATIO, datasetAccessor)
    elif datasetType == DatasetType.MOVIELENS_1m:
        recommenderAlgorithm = getRecommenderAlgorithm(DatasetConstants.ML_1M_NUMBER_OF_RATINGS, DatasetConstants.ML_1M_RATIO, datasetAccessor)
    elif datasetType == DatasetType.JESTER:
        recommenderAlgorithm = getRecommenderAlgorithm(DatasetConstants.JESTER_NUMBER_OF_RATINGS, DatasetConstants.JESTER_RATIO, datasetAccessor)

    # worst case scenario: use KNNBasic
    else:
        print("The given dataset wasn't recognized! Returning with KNNBaseline")
        recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBasic(sim_options={'name': 'cosine', 'user_based': False})), "CF: Item-based KNNBasic", datasetType.value)

    return recommenderAlgorithm

class Investigator:
    pass
