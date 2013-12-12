#!/usr/bin/python
import calendar
from collections import namedtuple
import csv
import glob
import json
import os.path
import sys
import time

sys.path.append('../')
import clusterer

def parse_num(num):
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            pass
    return num

if len(sys.argv) == 1:
    args = json.load(sys.stdin)
    numClusters = int(args[0])
    minTime =  int(args[1])
    maxTime =  int(args[2])
    grepMsg = args[3]
elif len(sys.argv) != 5:
    numClusters = 2;
    minTime = 0;
    maxTime = 1923228265; # Year 2020
    grepMsg = "";
else:
    numClusters = int(sys.argv[1])
    minTime =  int(sys.argv[2])
    maxTime =  int(sys.argv[3])
    grepMsg = sys.argv[4]

if(maxTime==minTime):
    maxTime = 1923228265;

# Reload from cache if possible
keepcharacters = (' ','.','_')
grepMsgSafe = "".join(c for c in grepMsg if c.isalnum() or c in keepcharacters).rstrip()
cacheFilename = 'cache/' + str(numClusters) + "_" +\
                           str(minTime) + "_" +    \
                           str(maxTime) + "_" +    \
                           str(grepMsgSafe) + ".txt";
if(os.path.exists(cacheFilename)):
    f = open(cacheFilename, "r")
    data = f.read()
    f.close()
    print data;
    quit()

clusterOutput = clusterer.run_clustering('../parsedData', \
                                         numClusters, minTime, maxTime, grepMsg);

# TODO: Gather list of all files
# fileList = glob.glob("../parsedData/*.csv");
nodeList = clusterOutput['closest_nodes'];
msgList = clusterOutput['matched_log_types'];
totalNumNodes = clusterOutput['num_nodes'];
totalNumMessages = clusterOutput['num_messages'];
totalMinTime = clusterOutput['min_time'];
totalMaxTime = clusterOutput['max_time'];
nodesPerCluster = clusterOutput['nodes_per_cluster'];

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

        with open(filename) as fin:
                nl = sum(1 for line in fin)

        # Convert CSV object into LogData struct
        import math
        truncation = 1
        if nl > 5000:
            truncation = math.floor(nl / 5000);
        for line_i,l in enumerate(lines):
            if line_i % truncation != 0:
                continue
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

            if curr.unixtime > maxTime or curr.unixtime < minTime:
                continue;

            # Append to one-dimensional
            flatData.append(curr);

    node_i = node_i + 1;

# Create the 2-dimensional data. Structs at [nodeId][messageId]
numMessages = len(uniqueIds);
numClusters = len(nodeList);
data = [ [[] for _ in range(numMessages) ] for _ in range(numClusters) ]; 
for d in flatData:
    data[d.nodeId][d.messageId].append(d);

# Set up printing to go to file and stdout
class Cacher(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

sys.stdout = Cacher(cacheFilename)

# Print all that out
print "Content-Type: text/html\n"
print 'data = ['
uniqueVals = []
for node_i in range(numClusters):
    print '['
    for msg_i in range(numMessages):
        print '   ['
        for d in data[node_i][msg_i]:
            i = 0;
            for val in d.values:
                if not val:
                    val = 0
                val = parse_num(val)
                if isinstance(val, str):
                    if val not in uniqueVals:
                        uniqueVals.append(val)
                    val = uniqueVals.index(val)
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
print 'totalNumNodes = ' + str(totalNumNodes) + ';'
print 'totalNumMessages = ' + str(totalNumMessages) + ';'
print 'totalMinTime = ' + str(totalMinTime) + ';'
print 'totalMaxTime = ' + str(totalMaxTime) + ';'
for key, val in nodesPerCluster.iteritems():
    print 'nodesPerCluster[' + str(key) + '] = ' + str(val) + ';'
