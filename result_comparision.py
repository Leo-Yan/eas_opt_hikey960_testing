#!/usr/bin/python

import array
import argparse
import csv
import os
import sys
import sys, getopt
import collections
import re
from os import system, remove
from collections import defaultdict

scenarios = {

    'idle' : [
        'Power',
    ],

    'audio' : [
        'Power',
    ],

    'video' : [
        'Power',
    ],

    'hackbench' : [
        'Power',
    ],

    'geekbench' : [
        'score',
        'multicore_score',
        'Power',
    ],
}

#def tree():
#    return collections.defaultdict(tree)


def parse_file(scene, file_name):

    #print file_name
    #print file_name.split(os.path.sep)[0]

    in_file = open(file_name, "r")
    in_line = csv.reader(in_file)
    next(in_line, None)

    l1_Value = dict()
    #l2_Value = defaultdict(list)
    sections = []

    p = re.compile(r'(.*)_\d', re.I)

    for row in in_line:
        m = re.match(p, row[0])

        if row[1] not in scene:
            continue

        section = m.group(1)
        #print section

        if not section in sections:
            sections.append(section)

        #print sections

    for kern in sections:

        l2_Value = defaultdict(list)

        in_file = open(file_name, "r")
        in_line = csv.reader(in_file)
        next(in_line, None)

        for row in in_line:
            #print row[0]
            #print row[1]
            #print row[3]
            #print row[4]

            m = re.match(p, row[0])
            #print m.group(1)

            if row[1] not in scene:
                continue

            section    = m.group(1)
            condition = row[3]
            value     = row[4]

            if condition not in scenarios[scene]:
                continue

            #print section
            #print kern
            if section != kern:
                continue

            l2_Value[condition].append(float(value))
            l1_Value[section] = l2_Value

    print l1_Value


def main(argv):

    if not os.path.isfile(sys.argv[1]):
        print "file don't exists:"
        sys.exit(1)

    for s in scenarios:
        parse_file(s, sys.argv[1])

if __name__ == "__main__":
    main(sys.argv[1:])
