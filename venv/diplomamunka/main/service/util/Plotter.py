import csv

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import xlrd

from diplomamunka.main.service.util.PlotterMetrics import PlotterMetrics

def convertXlsxToCsv(xlsxPath, csvPath, sheetName):
    wb = xlrd.open_workbook(xlsxPath)
    sh = wb.sheet_by_name(sheetName)
    your_csv_file = open(csvPath, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

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
    return pd.read_csv(csvPath, header=None).to_numpy()

def plotMetrics(algNameList, metricsList, yLabel, title):
    font = {
        'size': 14
    }

    matplotlib.rc('font', **font)
    plt.plot(algNameList, metricsList)
    plt.xticks(rotation=90)
    plt.xlabel("Algoritmusok")
    plt.ylabel(yLabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def getMetricsListFromNumpyArray(numpyArray):
    plotterMetricsList = []

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

            plotterMetricsList.append(PlotterMetrics(algName, rmse, mae, coverage, diversity, novelty, scalability))

    return plotterMetricsList

def plot():
    xlsxPath = "D:/Egyetem/Msc/Diplomamunka/Metrics_for_algorithms.xlsx"
    csvPath = "D:/Egyetem/Msc/Diplomamunka/Metrics_for_algorithms_allInOne.csv"
    sheetName = "All_In_One"
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

    plotMetrics(algNameList, rmseList, "RMSE értékek: a kisebb jobb", "RMSE értékek minden adathalmaz esetén")
    plotMetrics(algNameList, maeList, "MAE értékek: a kisebb jobb", "MAE értékek minden adathalmaz esetén")
    plotMetrics(algNameList, coverageList, "Lefedettségi értékek: a nagyobb jobb", "Lefedettségi értékek minden adathalmaz esetén")
    plotMetrics(algNameList, diversityList, "Különbözőségi értékek: a nagyobb jobb", "Különbözőségi értékek minden adathalmaz esetén")
    plotMetrics(algNameList, noveltyList, "Újszerűségi értékek: a nagyobb jobb", "Újszerűségi értékek minden adathalmaz esetén")
    plotMetrics(algNameList, scalabilityList, "Futási idők: a kisebb jobb", "Futási idők minden adathalmaz esetén")

class Plotter:
    pass
