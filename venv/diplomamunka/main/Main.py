from diplomamunka.main.service.RecommenderService import RecommenderService


def main():
    recommenderService = RecommenderService()

    # could create a while loop, so the user could go through all of the datasets
    # could create a version without the investigator, so the user could choose the algorithm manually

    recommenderService.start()


if __name__ == "__main__":
    main()
