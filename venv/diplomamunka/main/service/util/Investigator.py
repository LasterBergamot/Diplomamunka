from diplomamunka.main.service.recommender.algorithm.AlgorithmType import AlgorithmType
from surprise import KNNBaseline


class Investigator:

    # returns with CF, CB or Hybrid algorithm (AlgorithmType enum object)
    def selectRecommenderAlgorithm(self, dataset):
        print("Will return with the most suitable algorithm...")
        return self.investigateChosenDataset(dataset)

    def investigateChosenDataset(self, dataset):
        print("Will investigate the sparsity of the chosen dataset...")
        return KNNBaseline(sim_options={'name': 'cosine', 'user_based': False}), "KNNBaseline", AlgorithmType.COLLABORATIVE_FILTERING
