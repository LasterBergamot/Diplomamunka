class Recommender:

    algorithmsAndAccessors = []

    def addAlgorithmAndAccessor(self, algorithmAndAccessor):
        self.algorithmsAndAccessors.append(algorithmAndAccessor)

    # evaluates all of the algorithms, and returns with a list of Metrics objects
    def evaluate(self):
        print("\nEvaluating every algorithm...START!\n")
        metricsFromAlgorithms = []

        for algorithmAndAccessor in self.algorithmsAndAccessors:
            algorithm = algorithmAndAccessor.getRecommenderAlgorithm()
            accessor = algorithmAndAccessor.getDatasetAccessor()
            trainSet = accessor.getTrainSet()
            testSet = accessor.getTestSet()
            popularityRankings = accessor.getPopularityRankings()

            metricsFromAlgorithms.append(algorithm.evaluate(trainSet, testSet, popularityRankings))

        print("\nEvaluating every algorithm...DONE!\n")
        return metricsFromAlgorithms

    def getAlgorithmsAndAccessors(self):
        return self.algorithmsAndAccessors
