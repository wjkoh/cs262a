#!/usr/bin/python
import calendar
from collections import namedtuple
import csv
import glob
import json
import sys
import time

sys.path.append('../')
import clusterer

if len(sys.argv) == 1:
    args = json.load(sys.stdin)
    numNodes = int(args[0])
    minTime =  int(args[1])
    maxTime =  int(args[2])
    grepMsg = args[3]
elif len(sys.argv) == 4:
    numNodes = 2;
    minTime = 0;
    maxTime = calendar.timegm(time.gmtime());
    grepMsg = "";
else:
    numNodes = int(sys.argv[1])
    minTime =  int(sys.argv[2])
    maxTime =  int(sys.argv[3])
    grepMsg = sys.argv[4]

if(maxTime==minTime):
    maxTime = calendar.timegm(time.gmtime());
clusterOutput = clusterer.run_clustering('../parsedData', \
                                         numNodes, minTime, maxTime, grepMsg);

# TODO: Gather list of all files
# fileList = glob.glob("../parsedData/*.csv");
print clusterOutput;
nodeList = clusterOutput['closest_nodes'];
msgList = clusterOutput['matched_log_types'];

def rowToKey(row):
    return row[0] + row[1];

# Indices of CSV
LogData = namedtuple("LogData", "messageId nodeId filename lineNumber date unixtime values logMessage")

flatData = []
uniqueIds = []
node_i = 0;
for currNode in nodeList:
    for currMsg in msgList:
        currFile = currNode + "/" + currMsg + ".csv";

        # Read the CSV file if it exists
        try:
            filename = currFile
            filecontent = file(filename, 'rb')
            filecontent.next() # ignore header
            lines = csv.reader(filecontent, skipinitialspace=True)
        except:
            continue;

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
                           logMessage = l[3],
                           unixtime = timefmt,
                           values = l[4:numel])

            # Append to one-dimensional
            flatData.append(curr);

    node_i = node_i + 1;

# Create the 2-dimensional data. Structs at [nodeId][messageId]
numMessages = len(uniqueIds);
numNodes = len(nodeList);
data = [ [[] for _ in range(numMessages) ] for _ in range(numNodes) ]; 
for d in flatData:
    data[d.nodeId][d.messageId].append(d);

# Print all that out
print "Content-Type: text/html\n"
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
