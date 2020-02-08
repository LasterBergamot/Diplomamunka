class Recommender:

    dataset: object

    def __init__(self, dataset=None):
        self.dataset = dataset

    def evaluate(self):
        print("Will evaluate some stuff...")

    def recommend(self):
        print("Will recommend some stuff...")
