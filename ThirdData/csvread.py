import csv

with open('G.csv') as csvfile:
    #reader = csv.DictReader(csvfile)
    reader = csv.reader(csvfile, delimiter = ',', quotechar='|')
    for row in reader:
        print ', '.join(row)
    print csvreader.fieldnames
