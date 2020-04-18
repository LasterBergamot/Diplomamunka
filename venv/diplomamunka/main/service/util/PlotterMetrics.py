import string

class PlotterMetrics:

    algorithmName: string
    rmse: string
    mae: string
    coverage: string
    diversity: string
    novelty: string
    scalability: string

    def __init__(self, algorithmName, rmse, mae, coverage, diversity, novelty, scalability):
        self.algorithmName = algorithmName
        self.rmse = rmse
        self.mae = mae
        self.coverage = coverage
        self.diversity = diversity
        self.novelty = novelty
        self.scalability = scalability

    def getAlgorithmName(self):
        return self.algorithmName

    def getRMSE(self):
        return self.rmse

    def getMAE(self):
        return self.mae

    def getCoverage(self):
        return self.coverage

    def getDiversity(self):
        return self.diversity

    def getNovelty(self):
        return self.novelty

    def getScalability(self):
        return self.scalability
