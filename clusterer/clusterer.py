from collections import defaultdict
import csv
import datetime
import glob
import os
import re

import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans


__all__ = ['get_all_log_types', 'extract_feature_vectors', 'cluster']


def get_all_log_types(node_dirs, regex_pattern='.'):
    prog = re.compile(regex_pattern, flags=re.DOTALL | re.MULTILINE)

    # Find all the log types
    #print 'Find all the log types...'
    all_log_types = set()
    matched_log_types = set()
    for node_dir in node_dirs:
        log_files = glob.glob(os.path.join(node_dir, '*.csv'))

        for log_file in log_files:
            log_type_str = os.path.splitext(os.path.basename(log_file))[0]
            if log_type_str in all_log_types:
                continue

            all_log_types.add(log_type_str)

            matched = True
            with open(log_file, 'rb') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if prog.search(row['log_msg']) is None:
                        matched = False
            if matched:
                matched_log_types.add(log_type_str)
    all_log_types = frozenset(all_log_types)
    matched_log_types = frozenset(matched_log_types)
    return all_log_types, matched_log_types


def extract_feature_vectors(node_dirs, start_time=0, end_time=float('inf')):
    all_log_types, _ = get_all_log_types(node_dirs)

    # Extract feature vectors
    #print 'Extract feature vectors...'
    fvs_by_node = defaultdict(lambda: np.zeros(len(all_log_types), dtype=np.int))
    for node_dir in node_dirs:
        #print 'Node', node_dir
        for i, log_type in enumerate(all_log_types):
            with open(os.path.join(node_dir, '%s.csv' % log_type), 'rb') as f:
                reader = csv.DictReader(f)
                rows = list(reader)  # A header is not included.

                # Get the date column
                n_matched = 0
                dates = []
                for row in rows:
                    try:
                        date = datetime.datetime.strptime(row['date'],
                                '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        date = datetime.datetime.strptime(row['date'],
                                '%Y-%m-%d %H:%M:%S')
                    if start_time <= date <= end_time:
                        n_matched += 1
                    dates.append(date)

                # Might need to filter by timestamps
                assert n_matched <= len(rows)
                fvs_by_node[node_dir][i] = n_matched
    return fvs_by_node, all_log_types


def cluster(fvs, n_clusters):
    #print 'Start clustering for %d clusters...' % n_clusters
    fvs = np.asarray(fvs)
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters)
    return kmeans.fit(fvs)
