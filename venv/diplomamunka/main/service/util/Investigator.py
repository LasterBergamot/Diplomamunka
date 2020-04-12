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

class Investigator:

    # could return with several algorithm
    def investigateChosenDataset(self, datasetAccessor):
        print("Will investigate the sparsity of the chosen dataset...")
        datasetType = datasetAccessor.getDataset().getDatasetType()
        recommenderAlgorithm = None

        if datasetType == DatasetType.MOVIELENS_100K:
            recommenderAlgorithm = self.getRecommenderAlgorithmForML100k(datasetType.value)
        elif datasetType == DatasetType.MOVIELENS_1m:
            recommenderAlgorithm = self.getRecommenderAlgorithmForML1m(datasetType.value)
        elif datasetType == DatasetType.JESTER:
            recommenderAlgorithm = self.getRecommenderAlgorithmForJester(datasetType.value)
        else:
            print("The given dataset wasn't recognized!")

        return recommenderAlgorithm

    def getRecommenderAlgorithmForML100k(self, datasetName):
        recommenderAlgorithm = None

        if DatasetConstants.ML_100k_RATIO >= HYBRID_THRESHOLD:
            knn = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False}))
            cb = ContentBased()

            recommenderAlgorithm = RecommenderAlgorithm(Hybrid([knn, cb], [0.5, 0.5]), "Hybrid", datasetName)
        elif DatasetConstants.ML_100k_RATIO >= KNN_AND_CONTENT_BASED_THRESHOLD:
            recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline", datasetName)
        elif DatasetConstants.ML_100k_RATIO < KNN_AND_CONTENT_BASED_THRESHOLD:
            recommenderAlgorithm = RecommenderAlgorithm(ContentBased(), "ContentBased", datasetName)

        return recommenderAlgorithm

    def getRecommenderAlgorithmForML1m(self, datasetName):
        recommenderAlgorithm = None

        if DatasetConstants.ML_100k_RATIO >= HYBRID_THRESHOLD:
            knn = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False}))
            cb = ContentBased()

            recommenderAlgorithm = RecommenderAlgorithm(Hybrid([knn, cb], [0.5, 0.5]), "Hybrid", datasetName)
        elif DatasetConstants.ML_100k_RATIO >= KNN_AND_CONTENT_BASED_THRESHOLD:
            recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline", datasetName)
        elif DatasetConstants.ML_100k_RATIO < KNN_AND_CONTENT_BASED_THRESHOLD:
            recommenderAlgorithm = RecommenderAlgorithm(ContentBased(), "ContentBased", datasetName)

        return recommenderAlgorithm

    def getRecommenderAlgorithmForJester(self, datasetName):
        recommenderAlgorithm = None

        if DatasetConstants.ML_100k_RATIO >= HYBRID_THRESHOLD:
            knn = CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False}))
            cb = ContentBased()

            recommenderAlgorithm = RecommenderAlgorithm(Hybrid([knn, cb], [0.5, 0.5]), "Hybrid", datasetName)
        elif DatasetConstants.ML_100k_RATIO >= KNN_AND_CONTENT_BASED_THRESHOLD:
            recommenderAlgorithm = RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline", datasetName)
        elif DatasetConstants.ML_100k_RATIO < KNN_AND_CONTENT_BASED_THRESHOLD:
            recommenderAlgorithm = RecommenderAlgorithm(ContentBased(), "ContentBased", datasetName)

        return recommenderAlgorithm
