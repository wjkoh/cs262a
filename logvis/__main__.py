#!/usr/bin/env python
from parser import LogParser

if __name__ == '__main__':
    error_fname = '../data/training_slave.aion.sarietta.log.ERROR.20131008-233011.10204'
    warning_fname = '../data/training_slave.aion.sarietta.log.WARNING.20131008-233011.10204'
    info_fname = '../data/training_slave.aion.sarietta.log.INFO.20131008-232039.10206'

    parser = LogParser()
    parser.parse_file(error_fname)
    parser.parse_file(warning_fname)
    parser.parse_file(info_fname)
