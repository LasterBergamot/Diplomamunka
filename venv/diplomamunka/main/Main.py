from diplomamunka.main.service.RecommenderService import RecommenderService
from diplomamunka.main.service.util.Preprocessor import reorderCsvColumns, removeHeader, removeEmptyRows, \
    removeEmptyRowsFromCsvPd, split


def main():
    RecommenderService().start()

    # csvPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings.csv"
    # outputPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset"
    # split(open(csvPath, 'r'), row_limit=5000000, output_path=outputPath, keep_headers=False)
    # removeEmptyRowsFromCsvPd()


if __name__ == "__main__":
    main()
