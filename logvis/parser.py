from collections import namedtuple
from datetime import datetime
from itertools import groupby
import json
import re


__all__ = ['Log', 'LogParser']


Log = namedtuple('Log',
        ['log_type', 'log_level', 'date', 'thread_id', 'filename', 'line_num', 'log_msg',
            'variables'])


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
        pattern = '^([%s])' % self.LOG_TYPES
        l = re.split(pattern, raw_str, flags=re.MULTILINE)
        logs = [i for i in zip(l, l[1:]) if i[0] in self.LOG_TYPES]

        parsed = {}
        for log_level, contents in logs:
            tokens = contents.split()

            parsed['variables'] = None
            parsed['log_level'] = log_level
            date_str = '%s %s' % (tokens[0], tokens[1])
            parsed['date'] = datetime.strptime(date_str, '%m%d %H:%M:%S.%f')
            parsed['thread_id'] = int(tokens[2])
            parsed['filename'], line_num = tokens[3].split(':')
            if not line_num[-1].isdigit():  # Remove ']'
                line_num = line_num[:-1]
            parsed['line_num'] = int(line_num)
            parsed['log_msg'] = ' '.join(tokens[4:])
            parsed['log_type'] = (parsed['filename'], parsed['line_num'])
            parsed_logs.append(Log(**parsed))
        return parsed_logs
