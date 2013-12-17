from shutil import copytree, ignore_patterns
import glob
import os
import sys


if __name__ == '__main__':
    data_dir = './parsedData/'
    use_symlink = True

    orig_nodes = os.listdir(data_dir)
    orig_nodes = [os.path.basename(i) for i in glob.glob(os.path.join(data_dir, '1*'))]

    for dup_cnt in range(100):
        for orig_node in orig_nodes:
            src = os.path.join(data_dir, orig_node)
            dst = os.path.join(data_dir, 'd%s_%04d' % (orig_node, dup_cnt))
            if use_symlink:
                src = os.path.relpath(src, data_dir)
                os.symlink(src, dst)
            else:
                copytree(src, dst)
