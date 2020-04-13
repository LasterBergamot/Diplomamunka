import csv

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
from diplomamunka.main.service.util.PlotMetrics import PlotMetrics


def convertJesterDatToCsv():
    datPath = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/Jester/jester_ratings.dat'
    csvPath = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/Jester/jester_ratings.csv'

    with open(datPath, "r") as dat_file, open(csvPath, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for line in dat_file:
            row = [field.strip() for field in line.split('\t')]
            # rowForCsv = row[0] + "," + row[2] + "," + row[4]
            csv_writer.writerow(row)


def readJesterCsv():
    jesterCsvPath = 'D:/Other/Hobby/Programming/Workspaces/PyCharm_Workspace/Diplomamunka/venv/Datasets/Jester/jester_ratings.csv'

    with open(jesterCsvPath, newline='') as csvfile:
        ratingReader = csv.reader(csvfile)
        next(ratingReader)
        for row in ratingReader:
            if len(row) is not 0:
                asd = row[0] + " " + row[2] + " " + row[4]
                print(asd)


def readMetricsFromCSV(csvPath):
    df = pd.read_csv(csvPath, header=None)
    return df.to_numpy()


def convertXlsxToCsv(xlsxPath, csvPath, sheetName):
    wb = xlrd.open_workbook(xlsxPath)
    sh = wb.sheet_by_name(sheetName)
    your_csv_file = open(csvPath, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def getMetricsListFromNumpyArray(numpyArray):
    plotMetricsList = []

    for index in range(len(numpyArray)):
        if index is not 0:
            currentArray = numpyArray[index]
            algName = currentArray[0]
            rmse = currentArray[1]
            mae = currentArray[2]
            coverage = currentArray[3]
            diversity = currentArray[4]
            novelty = currentArray[5]
            scalability = currentArray[6]

            plotMetricsList.append(PlotMetrics(algName, rmse, mae, coverage, diversity, novelty, scalability))

    return plotMetricsList

def plotMetrics(algNameList, metricsList, yLabel, datasetName):
    font = {
        'size': 10
    }

    matplotlib.rc('font', **font)
    plt.plot(algNameList, metricsList, 'ro')
    plt.xticks(rotation=90)
    plt.xlabel("Datasets")
    plt.ylabel(yLabel)
    plt.title(datasetName)
    plt.grid(True)
    plt.show()

class Plotter:

    # creates graphs from the metrics data
    def plot(self):
        print("Will plot here...")
        xlsxPath = "D:/Egyetem/Msc/Diplomamunka/Metrics_for_algorithms.xlsx"
        csvPath = "D:/Egyetem/Msc/Diplomamunka/Metrics_for_algorithms_100k.csv"
        sheetName = "ml-100k"
        convertXlsxToCsv(xlsxPath, csvPath, sheetName)

        numpyArray = readMetricsFromCSV(csvPath)

        metricsList = getMetricsListFromNumpyArray(numpyArray)

        algNameList = []
        rmseList = []
        maeList = []
        coverageList = []
        diversityList = []
        noveltyList = []
        scalabilityList = []
        for metrics in metricsList:
            algNameList.append(metrics.getAlgorithmName())
            rmseList.append(float(metrics.getRMSE()))
            maeList.append(float(metrics.getMAE()))
            coverageList.append(float(metrics.getCoverage()))
            diversityList.append(float(metrics.getDiversity()))
            noveltyList.append(float(metrics.getNovelty()))
            scalabilityList.append(float(metrics.getScalability()))

        plotMetrics(algNameList, rmseList, "RMSE values: lower is better", "ml-100k")
        plotMetrics(algNameList, maeList, "MAE values: lower is better", "ml-100k")
        plotMetrics(algNameList, coverageList, "Coverage values: higher is better", "ml-100k")
        plotMetrics(algNameList, diversityList, "Diversity values: higher is better", "ml-100k")
        plotMetrics(algNameList, noveltyList, "Novelty values: higher is better", "ml-100k")
        plotMetrics(algNameList, scalabilityList, "Runtimes: lower the better", "ml-100k")

        # plotMetrics(algNameList, rmseList, "RMSE values: lower is better", "ml-1m")
        # plotMetrics(algNameList, maeList, "MAE values: lower is better", "ml-1m")
        # plotMetrics(algNameList, coverageList, "Coverage values: higher is better", "ml-1m")
        # plotMetrics(algNameList, diversityList, "Diversity values: higher is better", "ml-1m")
        # plotMetrics(algNameList, noveltyList, "Novelty values: higher is better", "ml-1m")
        # plotMetrics(algNameList, scalabilityList, "Runtimes: lower the better", "ml-1m")

        # plotMetrics(algNameList, rmseList, "RMSE values: lower is better", "ml-1m")
        # plotMetrics(algNameList, maeList, "MAE values: lower is better", "ml-1m")
        # plotMetrics(algNameList, coverageList, "Coverage values: higher is better", "ml-1m")
        # plotMetrics(algNameList, diversityList, "Diversity values: higher is better", "ml-1m")
        # plotMetrics(algNameList, noveltyList, "Novelty values: higher is better", "ml-1m")
        # plotMetrics(algNameList, scalabilityList, "Runtimes: lower the better", "ml-1m")
