from diplomamunka.main.service.recommender.algorithm.AlgorithmType import Algorithm

class Investigator:

    def investigateChosenDataset(self):
        print("Will investigate the sparsity of the chosen dataset...")
        return Algorithm.COLLABORATIVE_FILTERING.value
