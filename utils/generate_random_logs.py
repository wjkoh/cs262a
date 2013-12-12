#!/usr/bin/env python
import csv
import glob
import os
import random
import sys

if __name__ == '__main__':
    data_dir = './parsedData/'
    random_log_msg = 'RANDOM'

    probability = 0.10
    if len(sys.argv) > 1:
        probability = float(sys.argv[1])
    assert 0.0 <= probability <= 1.0

    node_dirs = [os.path.join(data_dir, node) for node in os.listdir(data_dir)]
    for node_dir in node_dirs:
        csv_files = glob.glob(os.path.join(node_dir, 'log_*.csv'))
        for csv_file in csv_files:
            with open(csv_file, 'rb') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames

                first_row = reader.next()
                random_log_type = first_row['filename'], '-' + first_row['line_num']
                f.seek(0)  # To read from the beginning again

                with open(os.path.join(node_dir, 'rand_%s_%s.txt' % random_log_type), 'w') as f:
                    f.write(random_log_msg)

                with open(os.path.join(node_dir, 'rand_%s_%s.csv' % random_log_type), 'wb') as f:
                    writer = csv.DictWriter(f, fieldnames)
                    writer.writeheader()
                    for row in reader:
                        if random.random() <= probability:
                            row['filename'], row['line_num'] = random_log_type
                            row['log_msg'] = random_log_msg
                            writer.writerow(row)
