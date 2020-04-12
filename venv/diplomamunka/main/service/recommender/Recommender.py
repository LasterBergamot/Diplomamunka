from collections import defaultdict


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

    # computes the top 10 recommendations for the users
    def recommend(self, trainSet, antiTestSet):
        print("\nCreating recommendations...START!\n")
        recommendationsDictionary = {}
        
        for algorithmAndAccessor in self.algorithmsAndAccessors:
            algorithm = algorithmAndAccessor.getRecommenderAlgorithm()
            print("\nCreating recommendations with the algorithm called: {}...START!\n".format(algorithm.name))
            algorithm.getAlgorithm().fit(trainSet)
            predictions = algorithm.getAlgorithm().test(antiTestSet)
            recommendations = []

            for userID, movieID, actualRating, estimatedRating, _ in predictions:
                intMovieID = int(movieID)
                recommendations.append((intMovieID, estimatedRating))

            print("\nCreating recommendations with the algorithm called: {}...DONE!\n".format(algorithm.name))
            recommendations.sort(key=lambda x: x[1], reverse=True)

            recommendationsDictionary[algorithm.name] = recommendations

        print("\nCreating recommendations...DONE!\n")
        return recommendationsDictionary

    def getAlgorithmsAndAccessors(self):
        return self.algorithmsAndAccessors
