from diplomamunka.main.service.RecommenderService import RecommenderService
from diplomamunka.main.service.util.Preprocessor import Preprocessor
from surprise import Dataset


def main():
    # could create a while loop, so the user could go through all of the datasets
    # could create a version without the investigator, so the user could choose the algorithm manually

    recommenderService = RecommenderService()
    recommenderService.start()

    # preprocessor = Preprocessor()
    # preprocessor.makeNetflixDatasetUsable()

if __name__ == "__main__":
    main()
