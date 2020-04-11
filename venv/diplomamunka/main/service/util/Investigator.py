from diplomamunka.main.service.recommender.algorithm.CollaborativeFiltering import CollaborativeFiltering
from diplomamunka.main.service.recommender.algorithm.RecommenderAlgorithm import RecommenderAlgorithm
from surprise import KNNBaseline


class Investigator:

    # could return with several algorithm
    def investigateChosenDataset(self, dataset):
        print("Will investigate the sparsity of the chosen dataset...")
        return RecommenderAlgorithm(CollaborativeFiltering(KNNBaseline(sim_options={'name': 'cosine', 'user_based': False})), "KNNBaseline")
