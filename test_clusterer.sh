#!/bin/sh

time python clusterer 2 0 `date +%s` "^Elapsed" || exit
time python clusterer 2 1381274519 1381276355 "^Elapsed" || exit
time python clusterer 2 1381274519 `date +%s` "^Elapsed" || exit
time python clusterer 2 `date +%s` `date +%s` "^Elapsed" || exit
