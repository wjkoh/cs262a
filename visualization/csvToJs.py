import calendar
from collections import namedtuple
import csv
import glob
import time

def rowToKey(row):
    return row[0] + row[1];

# Indices of CSV
LogData = namedtuple("LogData", "messageId nodeId filename lineNumber date unixtime values logMessage")

# TODO: Gather list of all files
fileList = glob.glob("../parsedData/*.csv");
# fileList = ["train.csv"];

flatData = []
uniqueIds = []
node_i = 0;
for currFile in fileList:
    # Read the CSV file
    filename = currFile
    filecontent = file(filename, 'rb')
    filecontent.next() # ignore header
    lines = csv.reader(filecontent, skipinitialspace=True)

    # Convert CSV object into LogData struct
    for l in lines:
        # Get unique ID for this message
        key = rowToKey(l)
        if key not in uniqueIds:
            uniqueIds.append(key)

        # Get timestamp in seconds since 1970
        try:
            timefmt = time.strptime(l[2], '%Y-%m-%d %H:%M:%S.%f')
        except:
            timefmt = time.strptime(l[2], '%Y-%m-%d %H:%M:%S')
        if timefmt.tm_year == 1900:
            timeWriteable = list(timefmt)
            timeWriteable[0] = 2013
            timefmt = time.struct_time(timeWriteable)
        timefmt = calendar.timegm(timefmt)

        # Create the struct
        numel = len(l)
        curr = LogData(nodeId = node_i,
                       messageId = uniqueIds.index(key),
                       filename = l[0],
                       lineNumber = l[1],
                       date = l[2],
                       unixtime = timefmt,
                       values = l[3:numel-1],
                       logMessage = l[numel-1])

        # Validate time TODO
        minTime = 1381274510
        maxTime = 1381274515
        if curr.unixtime > maxTime or curr.unixtime < minTime:
            continue;

        # Append to one-dimensional
        flatData.append(curr);

    node_i = node_i + 1;

# Create the 2-dimensional data. Structs at [nodeId][messageId]
numMessages = len(uniqueIds);
numNodes = len(fileList);
data = [ [[] for _ in range(numMessages) ] for _ in range(numNodes) ]; 
for d in flatData:
    data[d.nodeId][d.messageId].append(d);

# Print all that out
print '['
for node_i in range(numNodes):
    print '['
    for msg_i in range(numMessages):
        print '   ['
        for d in data[node_i][msg_i]:
            i = 0;
            for val in d.values:
                if not val:
                    val = "0"
                print '      ' + \
                      'new Data(' + str(d.unixtime) + ', ' +  \
                                    str(val) + ', ' +      \
                                    str(i) + ', \"' +      \
                                    d.logMessage +         \
                            '\"),';
                i = i + 1;
        print '   ],'
    print '],'
print '];'
