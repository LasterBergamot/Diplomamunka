from collections import defaultdict


class Recommender:

    algorithms = []

    def addAlgorithm(self, algorithm):
        self.algorithms.append(algorithm)

    # evaluates all of the algorithms, and returns with a list of Metrics objects
    def evaluate(self, trainSet, testSet, popularityRankings):
        print("\nEvaluating every algorithm...START!\n")
        metricsFromAlgorithms = []

        for algorithm in self.algorithms:
            metricsFromAlgorithms.append(algorithm.evaluate(trainSet, testSet, popularityRankings))

        print("\nEvaluating every algorithm...DONE!\n")
        return metricsFromAlgorithms

    # computes the top 10 recommendations for the users
    def recommend(self, trainSet, antiTestSet):
        print("\nCreating recommendations...START!\n")
        recommendationsDictionary = {}
        
        for algorithm in self.algorithms:
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
