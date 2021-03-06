#!/usr/bin/env python
from collections import defaultdict
from difflib import SequenceMatcher as sm
from itertools import groupby
import csv
import glob
import os

from parser import LogParser


def parse_num(num):
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            pass
    return num


def get_common_str(log_msgs):
    common_str = None
    for i in log_msgs:
        if common_str is None:
            common_str = i
            continue

        y = sm(None, a=common_str, b=i)
        matched = y.get_matching_blocks()

        common_str = ''
        for m in matched[:-1]:
            if m.b == 0 or m.b + m.size == len(i) or m.size > 1:
                beg_idx = m.b
                end_idx = beg_idx + m.size
                # A heuristic for decimal fractions such as 0.xxx
                if i[end_idx - 2:end_idx] == '0.':
                    end_idx -= 2
                assert(end_idx >= beg_idx)
                common_str += i[beg_idx:end_idx]
    return common_str


def get_variable_str(common_str, log_msg):
    y = sm(None, a=common_str, b=log_msg)
    matched = y.get_matching_blocks()

    variables = []
    end_of_prev_block = 0
    for m in matched:
        if end_of_prev_block != m.b:
            variables.append(parse_num(log_msg[end_of_prev_block:m.b]))
        end_of_prev_block = m.b + m.size
    return variables


if __name__ == '__main__':
    output_dir = './parsedData/%s'

    log_fnames_by_node = defaultdict(list)
    log_fnames = glob.glob('./data/*.log.*')
    for log_fname in log_fnames:
        fext = os.path.splitext(log_fname)[1][1:]
        log_fnames_by_node[fext].append(log_fname)

    for node_id, log_fnames in log_fnames_by_node.iteritems():
        parser = LogParser()
        all_logs = []
        for log_fname in log_fnames:
            all_logs.extend(parser.parse_file(log_fname))
        print 'Done parsing log files of node %s.' % node_id

        sorted(all_logs, lambda x, y: x.date < y.date)

        # To extract common strings
        logs_by_type = defaultdict(list)  # log_type: (fname, lnum)
        for log in all_logs:
            logs_by_type[log.log_type].append(log)

        common_strs = {}
        for key, logs in logs_by_type.iteritems():
            common_strs[key] = get_common_str(frozenset([l.log_msg for l in logs]))
        print 'Done extracting common strings.'

        variables = {}
        for log in all_logs:
            variables[log] = get_variable_str(common_strs[log.log_type], log.log_msg)
        print 'Done extracting variable strings.'

        if False:
            # Print out logs and their variable parts
            for log_type, logs in logs_by_type.iteritems():
                print log_type
                for log in logs:
                    print variables[log], log.log_msg
                print 'Done.'

        for log_type, logs in logs_by_type.iteritems():
            # Check the maximum length of variable parts
            max_var_len = 1
            for log in logs:
                max_var_len = max(max_var_len, len(variables[log]))

            try:
                os.makedirs(output_dir % node_id)
            except OSError:
                pass

            # Remove cache files
            try:
                os.remove(output_dir % node_id + '/log_%s_%s.npz' % log_type)
            except OSError:
                pass

            with open(output_dir % node_id + '/log_%s_%s.txt' % log_type, 'w') as txtfile:
                txtfile.write(common_strs[log_type])

            with open(output_dir % node_id + '/log_%s_%s.csv' % log_type, 'wb') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['filename', 'line_num', 'date']
                        + ['log_msg']
                        + ['v%d' % i for i in range(max_var_len)])
                for log in logs:
                    var_str = variables[log]
                    while len(var_str) < max_var_len:
                        var_str.append('')
                    writer.writerow(list(log_type) + [log.date] + [log.log_msg] + var_str)
        print 'Done writing to CSV files.'
