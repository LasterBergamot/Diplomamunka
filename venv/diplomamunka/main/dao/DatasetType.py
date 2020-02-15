from enum import Enum

class DatasetType(Enum):
    MOVIELENS_100K = "ml-100k"
    MOVIELENS_1m = "ml-1m"
    JESTER = "jester"
    NETFLIX_PRIZE_DATASET = "Netflix Prize Dataset"
