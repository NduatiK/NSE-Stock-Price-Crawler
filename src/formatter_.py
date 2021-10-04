import os
import csv
from src.crawler_ import Crawler


class FormatData:
    def __init__(self):
        self.yearsFolder = list()
        self.crawler = Crawler()

    # returns the years,months, days and csv in the folder.
    # It depends on when its being referenced.
    def getDataInFolder(self, path):
        dataFolder = list()
        for data in os.listdir(path):
            dataFolder.append(data)
        sortedDataFolder = sorted(dataFolder)
        return sortedDataFolder

    # extract from daily csv
    def getMonthlyData(self, inputPath, outputPath):
        # return years in folder
        years = self.getDataInFolder(inputPath)
        for year in years:
            self.crawler.createFolder(outputPath + str(year))
            yearlyPath = inputPath + str(year) + '/'
            # returns months in a folder
            months = self.getDataInFolder(yearlyPath)
            for month in months:
                self.crawler.createFolder(outputPath + str(year) + '/' + str(month))
                monthlyPath = yearlyPath + str(month) + '/'
                # returns days in a folder
                days = self.getDataInFolder(monthlyPath)
                for day in days:
                    dailyCsvPath = monthlyPath + str(day)
                    self.monthlyCSV(dailyCsvPath, day, outputPath + str(year) + '/' + str(month) + '/')

    # saves the data in the monthly csv file
    def monthlyCSV(self, dailyPath, fileName, finalPath):
        with open(dailyPath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(spamreader, None)
            for row in spamreader:
                date = fileName.strip('.csv')
                # append date to be the first element
                row.insert(0, date)
                file = finalPath + str(row[1]) + '.csv'
                # if files does exist add header
                self.add_header(file)
                file_append_data = open(file, 'a')
                writeFile = csv.writer(file_append_data, delimiter=';')
                # removes the code
                del row[1]
                # removes the company name
                del row[1]
                writeFile.writerows([row])
                file_append_data.close()

    # extract from monthly csv
    def getYearlyData(self, inputPath, outputPath):
        years = self.getDataInFolder(inputPath)
        for year in years:
            self.crawler.createFolder(outputPath + str(year))
            yearlyPath = inputPath + str(year) + '/'
            months = self.getDataInFolder(yearlyPath)
            for month in months:
                monthlyPath = yearlyPath + str(month) + '/'
                months = self.getDataInFolder(monthlyPath)
                for monthlyCSV in months:
                    csvPath = monthlyPath + str(monthlyCSV)
                    self.YearlyCSV(csvPath, monthlyCSV, outputPath + str(year) + '/')

    # saves the data in the yearly csv file
    def YearlyCSV(self, monthlyCSVPath, csvName, outputPath):
        with open(monthlyCSVPath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(spamreader, None)
            for row in spamreader:
                file = outputPath + str(csvName)
                # if files does exist add header
                self.add_header(file)
                file_append_data = open(file, 'a')
                writeFile = csv.writer(file_append_data, delimiter=',')
                writeFile.writerows([row])
                file_append_data.close()

    # extract from yearly csv
    def getCompanyData(self, inputPath, outputPath):
        years = self.getDataInFolder(inputPath)
        for year in years:
            yearlyPath = inputPath + str(year) + '/'
            year = self.getDataInFolder(yearlyPath)
            for yearlyCSV in year:
                csvPath = yearlyPath + str(yearlyCSV)
                self.companyCSV(csvPath, yearlyCSV, outputPath + '/')

    # saves the data in the company csv file
    def companyCSV(self, yearlyCSVPath, csvName, outputPath):
        with open(yearlyCSVPath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(spamreader, None)
            for row in spamreader:
                file = outputPath + str(csvName)
                # if files does exist add header
                self.add_header(file)
                file_append_data = open(file, 'a')
                writeFile = csv.writer(file_append_data, delimiter=';')
                writeFile.writerows([row])
                file_append_data.close()

    def add_header(self, file):
        # if files does exist add header
        if not os.path.isfile(file):
            file_header = open(file, 'a')
            writeFile = csv.writer(file_header, delimiter=';')
            writeFile.writerow(['Date', 'Lowest Price of the Day', 'Highest Price of the Day',
                                'Closing Price', 'Previous Day Closing Price', 'Volume Traded'])
            file_header.close()
