#!/usr/bin/python
import csv
import calendar
import datetime
import glob
import os
import sys

dirName = sys.argv[1]
multiplier = float(sys.argv[2]);
fnames = []
dates = []
rows = []
headers = [];
for index,fname in enumerate(glob.glob(dirName + "/*.csv")):
    fnames.append(fname)
    rows.append([])
    dates.append([])
    with open(fname, 'rb') as f:
        reader = csv.DictReader(f)
        headers.append(reader.fieldnames)
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['date'],
                        '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                date = datetime.datetime.strptime(row['date'],
                        '%Y-%m-%d %H:%M:%S')
            rows[index].append(row)
            dates[index].append(date)

minDate = dates[0][0]
for datesInFile in dates:
    minDate = min(min(datesInFile),minDate)

# Clear the monkey directory
outdir = 'parsedData/monkey/'
for f in glob.glob(outdir + '/*'):
    os.remove(f)

for file_i,fname in enumerate(fnames):
    currDates = dates[file_i];
    currRows = rows[file_i];
    for row_i,row in enumerate(currRows):
        date = currDates[row_i]
        td = (date-minDate);
        tdNew = datetime.timedelta(seconds = multiplier * td.total_seconds()*2.5);
        newDate = minDate + tdNew;
        rows[file_i][row_i]['date'] = newDate;

    # Print out curr file
    (path,fn) = os.path.split(fname)
    outfn = outdir + fn;
    print outfn
    with open(outfn, 'wb') as f:
        writer = csv.DictWriter(f, delimiter = ',', fieldnames = headers[file_i])
        writer.writeheader()
        for row in currRows:
            writer.writerow(row)
