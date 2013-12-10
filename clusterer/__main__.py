#!/usr/bin/env python
import numpy as np
from clusterer import extract_feature_vectors, cluster

if __name__ == '__main__':
    fvs_by_node, all_log_types = extract_feature_vectors('./parsedData/')
    fvs_np = np.array(fvs_by_node.values())
    print 'Nodes:', fvs_by_node.keys()
    print 'Feature vectors (node x feature):', fvs_np

    print cluster(fvs_np, 3)
    print cluster(fvs_np, 2)
