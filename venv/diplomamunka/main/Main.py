from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
import os
import pandas as pd
import numpy as np
import time
from surprise.model_selection import train_test_split

def main():

    start = time.time()
    print("Reading combined_data_1")
    # Reading combined_data_1
    # Relative path doesn't work for some reason
    df1 = pd.read_csv('D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Netflix/combined_data_1.txt', header = None,
                      names = ['Cust_Id', 'Rating'], usecols = [0, 1])
    df1['Rating'] = df1['Rating'].astype(float)

    print("Reading combined_data_2")
    # Reading combined_data_2
    # Relative path doesn't work for some reason
    df2 = pd.read_csv('D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Netflix/combined_data_2.txt',
                      header=None,
                      names=['Cust_Id', 'Rating'], usecols=[0, 1])
    df2['Rating'] = df2['Rating'].astype(float)

    print("Reading combined_data_3")
    # # Reading combined_data_3
    # # Relative path doesn't work for some reason
    df3 = pd.read_csv('D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Netflix/combined_data_3.txt',
                      header=None,
                      names=['Cust_Id', 'Rating'], usecols=[0, 1])
    df3['Rating'] = df3['Rating'].astype(float)

    print("Reading combined_data_4")
    # # Reading combined_data_4
    # # Relative path doesn't work for some reason
    df4 = pd.read_csv('D:/Other/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Netflix/combined_data_4.txt',
                      header=None,
                      names=['Cust_Id', 'Rating'], usecols=[0, 1])
    df4['Rating'] = df4['Rating'].astype(float)

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

    # get movie count
    movie_count = df.isnull().sum()[1]

    # get customer count
    cust_count = df['Cust_Id'].nunique() - movie_count

    # get rating count
    rating_count = df['Cust_Id'].count() - movie_count

    print("Data Cleaning...")
    # Data Cleaning
    # Getting the Movie_Id field
    df_nan = pd.DataFrame(pd.isnull(df.Rating))
    df_nan = df_nan[df_nan['Rating'] == True]
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
    df = df[pd.notnull(df['Rating'])]

    df['Movie_Id'] = movie_np.astype(int)
    df['Cust_Id'] = df['Cust_Id'].astype(int)
    print('-Dataset examples-')
    print(df.iloc[::5000000, :])

    timeToFormatTheData = time.time()
    print("Time to format the data: " + str(timeToFormatTheData - start) + " seconds")

    export_csv = df.to_csv(r'D:\Netflix_dataframe_to_csv_export.csv', index=None, header=True)

    end = time.time()
    print("Whole process: " + str(end - start) + " seconds")
    # reader = Reader(rating_scale=(1, 5))
    # data = Dataset.load_from_df(df[['Cust_Id', 'Rating']], reader)
    # print("len: " + str(len(data.raw_ratings)))
    # Load the movielens-100k dataset (download it if needed),
    # data = Dataset.load_builtin('jester')
    # rawRatings = data.raw_ratings
    # users = set()
    # items = set()
    #
    # # for rating in rawRatings:
    # #     users.add(rating.__getitem__(0))
    # #     items.add(rating.__getitem__(1))
    # #
    # # print("Size of users: " + str(len(users)))
    # # print("Size of items: " + str(len(items)))
    #
    # # number_of_users = 943
    # # number_of_items = 1682
    # # size_of_matrix = number_of_users * number_of_items
    # # print("size of matrix: " + str(size_of_matrix))
    # print("size of raw_ratings: " + str(len(data.raw_ratings)))
    # print("ratio: " + str(len(data.raw_ratings) / size_of_matrix))

    # sample random trainset and testset
    # test set is made of 25% of the ratings.
    # trainset, testset = train_test_split(data, test_size=.25)
    #
    # # We'll use the famous SVD algorithm.
    # algo = SVD()
    #
    # # Train the algorithm on the trainset, and predict ratings for the testset
    # algo.fit(trainset)
    # predictions = algo.test(testset)
    #
    # # Then compute RMSE
    # accuracy.rmse(predictions)

if __name__ == "__main__":
    main()
