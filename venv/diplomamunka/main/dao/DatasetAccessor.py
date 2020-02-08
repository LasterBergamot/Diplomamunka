from diplomamunka.main.dao.Dataset import Dataset

class DatasetAccessor:

    def chooseDataset(self):
        print("The user will choose the dataset here...")
        return Dataset.MOVIELENS_100K.value