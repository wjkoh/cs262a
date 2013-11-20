from datetime import datetime
from itertools import groupby
import json
import re


__all__ = ['LogParser']


class LogParser(object):
    """Log line format: [IWEF]mmdd hh:mm:ss.uuuuuu threadid file:line] msg"""
    LOG_TYPES = 'IWEF'

    def __init__(self): pass

    def parse_file(self, log_fname):
        with open(log_fname, 'r') as f:
            raw_str = f.read()
        return self.parse_str(raw_str)

    def parse_str(self, raw_str):
        parsed_logs = []
        pattern = '(^[%s])' % self.LOG_TYPES
        l = re.split(pattern, raw_str, flags=re.MULTILINE)

        logs = [i for i in zip(l, l[1:]) if i[0] in self.LOG_TYPES]

        for log_type, contents in logs:
            tokens = str.split(contents)

            parsed = {}
            parsed['type'] = log_type
            date_str = tokens[0] + ' ' + tokens[1]
            parsed['date'] = datetime.strptime(date_str, '%m%d %H:%M:%S.%f')
            parsed['thread_id'] = int(tokens[2])
            parsed['filename'], line_num = str.split(tokens[3], ':')
            if not line_num[-1].isdigit():  # Remove ']'
                line_num = line_num[:-1]
            parsed['line_num'] = int(line_num)
            parsed['log_msg'] = tokens[4:]
            parsed_logs.append(parsed)

            # debug
            print 'Raw'
            print log_type, contents.strip()
            print 'Parsed'
            print parsed
            print
        return parsed_logs
