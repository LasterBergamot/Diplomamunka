from diplomamunka.main.dao.DatasetAccessor import DatasetAccessor
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm


class AlgorithmAndAccessor:

    recommenderAlgorithm: RecommenderAlgorithm
    datasetAccessor: DatasetAccessor

    def __init__(self, recommenderAlgorithm, datasetAccessor):
        self.recommenderAlgorithm = recommenderAlgorithm
        self.datasetAccessor = datasetAccessor

    def getRecommenderAlgorithm(self):
        return self.recommenderAlgorithm

    def getDatasetAccessor(self):
        return self.datasetAccessor