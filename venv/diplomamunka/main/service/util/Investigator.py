from diplomamunka.main.dao import DatasetConstants
from diplomamunka.main.dao.DatasetType import DatasetType
from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.ContentBased import ContentBased
from diplomamunka.main.service.recommender.algorithm.Hybrid import Hybrid
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise import KNNBaseline

# 5% threshold?
# KNN: ratio >= 5%
# Content-Based: ratio < 5%
# Hybrid: ratio >= 50%
KNN_AND_CONTENT_BASED_THRESHOLD = 0.05
HYBRID_THRESHOLD = 0.5


def getRecommenderAlgorithmForML100k(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value
    # recommenderAlgorithm = None
    #
    # if DatasetConstants.ML_100k_RATIO >= HYBRID_THRESHOLD:
    #     knn = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False}))
    #     cb = ContentBased(datasetAccessor)
    #
    #     recommenderAlgorithm = RecommenderAlgorithm(Hybrid([knn, cb], [0.5, 0.5]), "Hybrid: Item-based KNN CF and Content-Based KNN", datasetName)
    # elif DatasetConstants.ML_100k_RATIO >= KNN_AND_CONTENT_BASED_THRESHOLD:
    #     recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline: Item-based KNN CF", datasetName)
    # elif DatasetConstants.ML_100k_RATIO < KNN_AND_CONTENT_BASED_THRESHOLD:
    #     recommenderAlgorithm = RecommenderAlgorithm(ContentBased(datasetAccessor), "ContentBased", datasetName)
    #
    # return recommenderAlgorithm
    return RecommenderAlgorithm(ContentBased(datasetAccessor), "ContentBased", datasetName)


def getRecommenderAlgorithmForML1m(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value
    recommenderAlgorithm = None

    if DatasetConstants.ML_1M_RATIO >= HYBRID_THRESHOLD:
        knn = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': True}))
        cb = ContentBased(datasetAccessor)

        recommenderAlgorithm = RecommenderAlgorithm(Hybrid([knn, cb], [0.5, 0.5]), "Hybrid: User-based KNN CF and Content-Based KNN", datasetName)
    elif DatasetConstants.ML_1M_RATIO >= KNN_AND_CONTENT_BASED_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': True})), "KNNBaseline: User-based KNN CF", datasetName)
    elif DatasetConstants.ML_1M_RATIO < KNN_AND_CONTENT_BASED_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(ContentBased(datasetAccessor), "ContentBased", datasetName)

    return recommenderAlgorithm

# Hybrid with two KNNs: user and item
# OR
# One KNN: user or item
def getRecommenderAlgorithmForJester(datasetAccessor):
    datasetName = datasetAccessor.getDataset().getDatasetType().value
    recommenderAlgorithm = None

    if DatasetConstants.JESTER_RATIO >= HYBRID_THRESHOLD:
        knnItem = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False}))
        knnUser = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': True}))

        recommenderAlgorithm = RecommenderAlgorithm(Hybrid([knnItem, knnUser], [0.5, 0.5]), "Hybrid: Item- and User-based KNN CF", datasetName)
    elif DatasetConstants.JESTER_RATIO >= KNN_AND_CONTENT_BASED_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline: Item-based KNN CF", datasetName)
    elif DatasetConstants.JESTER_RATIO < KNN_AND_CONTENT_BASED_THRESHOLD:
        recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': True})), "KNNBaseline: User-based KNN CF", datasetName)

    return recommenderAlgorithm

# could return with several algorithm
def investigateChosenDataset(datasetAccessor):
    print("Will investigate the sparsity of the chosen dataset...")
    datasetType = datasetAccessor.getDataset().getDatasetType()
    recommenderAlgorithm = None

    if datasetType == DatasetType.MOVIELENS_100K:
        recommenderAlgorithm = getRecommenderAlgorithmForML100k(datasetAccessor)
    elif datasetType == DatasetType.MOVIELENS_1m:
        recommenderAlgorithm = getRecommenderAlgorithmForML1m(datasetAccessor)
    elif datasetType == DatasetType.JESTER:
        recommenderAlgorithm = getRecommenderAlgorithmForJester(datasetAccessor)
    else:
        print("The given dataset wasn't recognized!")

    return recommenderAlgorithm


class Investigator:
    pass
