from diplomamunka.main.service.recommender.algorithm.AlgorithmType import Algorithm

class Investigator:

    # returns with CF, CB or Hybrid algorithm (RecommenderAlgorithm object)
    def selectRecommenderAlgorithm(self, dataset):
        print("Will return with the most suitable algorithm...")
        return self.investigateChosenDataset(dataset)

    def investigateChosenDataset(self, dataset):
        print("Will investigate the sparsity of the chosen dataset...")
        return Algorithm.COLLABORATIVE_FILTERING.value
