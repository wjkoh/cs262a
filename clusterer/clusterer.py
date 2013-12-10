from collections import defaultdict
import csv
import datetime
import glob
import os

import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans


__all__ = ['extract_feature_vectors', 'cluster']


def extract_feature_vectors(data_dir):
    node_dirs = os.listdir(data_dir)

    # Find all the log types
    print 'Find all the log types...'
    all_log_types = set()
    for node_dir in node_dirs:
        log_files = glob.glob(os.path.join(data_dir, node_dir, '*.csv'))

        all_log_types.update([
            os.path.splitext(os.path.basename(log_file))[0]
            for log_file in log_files])
    all_log_types = frozenset(all_log_types)

    # Extract feature vectors
    print 'Extract feature vectors...'
    fvs_by_node = defaultdict(lambda: np.zeros(len(all_log_types), dtype=np.int))
    for node_dir in node_dirs:
        print 'Node', node_dir
        for i, log_type in enumerate(all_log_types):
            with open(os.path.join(data_dir, node_dir, '%s.csv' % log_type), 'rb') as f:
                reader = csv.DictReader(f)
                rows = list(reader)  # A header is not included.

                # Get the date column
                dates = []
                for row in rows:
                    try:
                        date = datetime.datetime.strptime(row['date'],
                                '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        date = datetime.datetime.strptime(row['date'],
                                '%Y-%m-%d %H:%M:%S')
                    dates.append(date)

                # Might need to filter by timestamps
                fvs_by_node[node_dir][i] = len(rows)
    return fvs_by_node, all_log_types


def cluster(fvs, n_clusters):
    print 'Start clustering for %d clusters...' % n_clusters
    fvs = np.asarray(fvs)
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters)
    return kmeans.fit_predict(fvs)
