import time


class RecommenderAlgorithm:

    def __init__(self, algorithm, name):
        self.algorithm = algorithm
        self.name = name

    # use stopwatch here
    # will return metrics here
    def evaluate(self):
        print("Will evaluate the given data with the given algorithm here...")
        startTime = time.time()

        # do some stuff here
        # fit
        # test etc.

        endTime = time.time()
        wholeProcessInSeconds = endTime - startTime

        # calculate metrics + add runtime to the Metrics object
        # return with the Metrics object
