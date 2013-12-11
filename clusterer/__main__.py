#!/usr/bin/env python
import datetime
import numpy as np
import os
import sys

from clusterer import extract_feature_vectors, cluster, get_all_log_types

if __name__ == '__main__':
    data_dir = './parsedData/'
    node_dirs = [os.path.join(data_dir, node_dir) for node_dir in os.listdir(data_dir)]

    n_clusters = int(sys.argv[1])
    assert n_clusters > 0
    start_time = int(sys.argv[2])
    end_time = int(sys.argv[3])
    assert start_time >= 0 and end_time >= 0
    regex_pattern = sys.argv[4]

    fvs_by_node, all_log_types = extract_feature_vectors(node_dirs, start_time, end_time)
    fvs_np = np.array(fvs_by_node.values(), dtype=np.float)

    km = cluster(fvs_np, n_clusters)
    km.predict(fvs_np)

    dists = km.transform(fvs_np)
    closest_nodes = np.argmin(dists, axis=0)
    print len(closest_nodes)
    for node in closest_nodes:
        print fvs_by_node.keys()[node]

    matched_log_types = get_all_log_types(node_dirs, regex_pattern)[1]
    print len(matched_log_types)
    print os.linesep.join(matched_log_types)
