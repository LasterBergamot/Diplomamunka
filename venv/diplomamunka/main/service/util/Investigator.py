from diplomamunka.main.service.recommender.algorithm.AlgorithmType import Algorithm

class Investigator:

    # returns with CF, CB or Hybrid algorithm (RecommenderAlgorithm object)
    def investigateChosenDataset(self, dataset):
        print("Will investigate the sparsity of the chosen dataset...")
        return Algorithm.COLLABORATIVE_FILTERING.value
