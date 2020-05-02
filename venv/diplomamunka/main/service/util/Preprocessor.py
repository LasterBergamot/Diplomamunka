import csv
import os
import time

import numpy as np
import pandas as pd

PATH_EXPORT_CSV = r'D:\Netflix_dataframe_to_csv_export.csv'

PATH_COMBINED_DATA_4 = 'D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/combined_data_4.txt'
PATH_COMBINED_DATA_3 = 'D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/combined_data_3.txt'
PATH_COMBINED_DATA_2 = 'D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/combined_data_2.txt'
PATH_COMBINED_DATA_1 = 'D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/combined_data_1.txt'


def reorderCsvColumns():
    csvPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings.csv"
    reorderedCsvPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/removedHeader_Netflix_dataframe_to_csv_export.csv"

    with open(csvPath, 'r') as infile, open(reorderedCsvPath, 'a') as outfile:
        # output dict needs a list for new column ordering
        fieldnames = ['user', 'item', 'rating', 'timestamp']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)


def removeHeader():
    csvPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings.csv"
    removedHeaderCsv = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/removedHeader_Netflix_dataframe_to_csv_export.csv"

    with open(csvPath, 'r') as infile, open(removedHeaderCsv, 'a') as outfile:
        next(infile)
        for line in infile:
            outfile.write(line)


def removeEmptyRowsFromCsvPd():
    csvPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings_1.csv"
    noBlankRowsCsv = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings_1asd.csv"

    df = pd.read_csv(csvPath)
    df.to_csv(noBlankRowsCsv, index=False)


# source: https://gist.github.com/jrivero/1085501
def split(filehandler, delimiter=',', row_limit=10000, output_name_template='output_%s.csv', output_path='.',
          keep_headers=True):
    """
    Splits a CSV file into multiple pieces.

    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:

        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));

    """
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


def removeEmptyRows():
    csvPath = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/Netflix_Prize_Dataset_ratings.csv"
    noBlankRowsCsv = "D:/Egyetem/Msc/Diplomamunka/Netflix_Prize_Dataset/noBlankRows_Netflix_dataframe_to_csv_export.csv"

    reader = csv.DictReader(open(csvPath))
    writer = csv.DictWriter(open(noBlankRowsCsv, 'w'), fieldnames=reader.fieldnames)

    for row in reader:
        if all(col != '' for col in row.values()):
            continue

        writer.writerow(row)


def readFromCsv(csvPath):
    return pd.read_csv(csvPath, header=None, names=['user', 'rating', 'timestamp'], usecols=[0, 1, 2])

# Source: https://www.kaggle.com/laowingkin/netflix-movie-recommendation
def makeNetflixDatasetUsable():
    start = time.time()

    print("Reading combined_data_1")
    df1 = readFromCsv(PATH_COMBINED_DATA_1)
    df1['rating'] = df1['rating'].astype(float)

    print("Reading combined_data_2")
    df2 = readFromCsv(PATH_COMBINED_DATA_2)
    df2['rating'] = df2['rating'].astype(float)

    print("Reading combined_data_3")
    df3 = readFromCsv(PATH_COMBINED_DATA_3)
    df3['rating'] = df3['rating'].astype(float)

    print("Reading combined_data_4")
    df4 = readFromCsv(PATH_COMBINED_DATA_4)
    df4['rating'] = df4['rating'].astype(float)

    print("Reading the data took: {}".format(time.time() - start))

    # Combining the data
    print("Combining the data...")
    df = df1
    df = df.append(df2)
    df = df.append(df3)
    df = df.append(df4)

    df.index = np.arange(0, len(df))
    print('Full dataset shape: {}'.format(df.shape))
    print('-Dataset examples-')
    print(df.iloc[::5000000, :])

    print("Combining the data took: {}".format(time.time() - start))

    print("Data Cleaning...")
    # Data Cleaning
    # Getting the Movie_Id field
    df_nan = pd.DataFrame(pd.isnull(df.rating))
    df_nan = df_nan[df_nan['rating'] == True]
    df_nan = df_nan.reset_index()

    movie_np = []
    movie_id = 1

    for i, j in zip(df_nan['index'][1:], df_nan['index'][:-1]):
        # numpy approach
        temp = np.full((1, i - j - 1), movie_id)
        movie_np = np.append(movie_np, temp)
        movie_id += 1

    # Account for last record and corresponding length
    # numpy approach
    last_record = np.full((1, len(df) - df_nan.iloc[-1, 0] - 1), movie_id)
    movie_np = np.append(movie_np, last_record)

    print('Movie numpy: {}'.format(movie_np))
    print('Length: {}'.format(len(movie_np)))

    # remove those Movie ID rows
    df = df[pd.notnull(df['rating'])]

    df['item'] = movie_np.astype(int)
    df['user'] = df['user'].astype(int)
    print('-Dataset examples-')
    print(df.iloc[::5000000, :])

    timeToFormatTheData = time.time()
    print("Time to format the data: " + str(timeToFormatTheData - start) + " seconds")

    df.to_csv(PATH_EXPORT_CSV, index=None, header=True)

    end = time.time()
    print("Whole process: " + str(end - start) + " seconds")


class Preprocessor:
    pass
