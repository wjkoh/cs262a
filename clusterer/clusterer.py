from collections import Counter
from collections import defaultdict
import bisect
import calendar
import csv
import datetime
import glob
import os
import re

import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans


__all__ = ['get_all_log_types', 'extract_feature_vectors', 'cluster', 'run_clustering']


def get_all_log_types(node_dirs, regex_pattern='.'):
    prog = re.compile(regex_pattern, flags=re.DOTALL | re.MULTILINE)

    # Find all the log types
    print 'Find all the log types...'
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


def read_dates_from_csv_file(fname):
    with open(fname, 'rb') as f:
        reader = csv.DictReader(f)

        # Get the date column
        dates = []
        timestamps = []
        for row in reader:
            try:
                date = datetime.datetime.strptime(row['date'],
                        '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                date = datetime.datetime.strptime(row['date'],
                        '%Y-%m-%d %H:%M:%S')
            dates.append(date)
            timestamps.append(calendar.timegm(date.utctimetuple()))
    return dates, timestamps


def extract_feature_vectors(node_dirs, start_time=0, end_time=float('inf')):
    start_dt = datetime.datetime.utcfromtimestamp(start_time)
    end_dt = datetime.datetime.utcfromtimestamp(end_time)

    all_log_types, _ = get_all_log_types(node_dirs)

    # Extract feature vectors
    print 'Extract feature vectors...'
    fvs_by_node = defaultdict(lambda: np.zeros(len(all_log_types), dtype=np.int))
    for node_dir in node_dirs:
        print 'Node', node_dir
        for i, log_type in enumerate(all_log_types):
            out_file = os.path.join(node_dir, '%s.npz' % log_type)

            try:
                npz_file = np.load(out_file)
                timestamps = npz_file['timestamps']
                cumulative_cnts = npz_file['cumulative_cnts']
            except IOError:
                print 'No .npz file exists.', 'Rebuilding from CSV file...'
                csv_file = os.path.join(node_dir, '%s.csv' % log_type)
                dates, timestamps = read_dates_from_csv_file(csv_file)

                # Build data structures for fast range queries
                c = Counter(timestamps)
                timestamps, counts = zip(*sorted(c.items()))

                # I used reverse prefix sums because it was easier to think.
                cumulative_cnts = []
                total_cnt = 0
                for count in reversed(counts):
                    total_cnt += count
                    cumulative_cnts.append(total_cnt)
                cumulative_cnts.reverse()

                # Convert to NumPy arrays
                timestamps = np.asarray(timestamps, dtype=np.uint)
                cumulative_cnts = np.asarray(cumulative_cnts, dtype=np.uint)

                # Save
                np.savez(out_file, timestamps=timestamps, cumulative_cnts=cumulative_cnts)

            # Binary search
            n_matched = 0
            beg_idx = bisect.bisect_left(timestamps, start_time)  # GTEQ
            if beg_idx != len(timestamps):
                n_matched =  cumulative_cnts[beg_idx]

                end_idx = bisect.bisect_left(timestamps, end_time) # GTEQ
                if end_idx != len(timestamps):
                    n_matched -= cumulative_cnts[end_idx]
            fvs_by_node[node_dir][i] = n_matched

    return fvs_by_node, all_log_types


def cluster(fvs, n_clusters):
    print 'Start clustering for %d clusters...' % n_clusters
    fvs = np.asarray(fvs)
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters)
    return kmeans.fit(fvs)

def run_clustering(data_dir, n_clusters, start_time, end_time, regex_pattern):
    node_dirs = [os.path.join(data_dir, node_dir) for node_dir in os.listdir(data_dir)]

    #start_time = datetime.datetime.fromtimestamp(start_time)
    #end_time = datetime.datetime.fromtimestamp(end_time)

    #fvs_by_node, all_log_types = extract_feature_vectors(node_dirs, start_time, end_time)
    #fvs_np = np.array(fvs_by_node.values(), dtype=np.float)

    #km = cluster(fvs_np, n_clusters)
    #km.predict(fvs_np)

    #dists = km.transform(fvs_np)
    #closest_nodes = np.argmin(dists, axis=0)
    matched_log_types = get_all_log_types(node_dirs, regex_pattern)[1]
    return {'closest_nodes': node_dirs, 'matched_log_types': matched_log_types};
