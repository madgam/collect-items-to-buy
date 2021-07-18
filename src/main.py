import csv
import glob

from modules.scrape import Scrape

scrape = Scrape()
csv_files = glob.glob('csv/in/*.csv')
for csv_file in csv_files:
    with open(csv_file, newline='', encoding="utf-8-sig") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        scrape.getData(spamreader)
