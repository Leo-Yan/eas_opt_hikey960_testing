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

class result_comparison:

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

    sections = []

    def __init__(self, infile, outfile):
        self.infile = infile

    def __del__(self):
        self.fr.close()

    def parse_file(self):
        for s in self.scenarios:
            self.parse_scene(s)

    def parse_sections(self):

        sec = []

        self.fr = open(self.infile, "r")
        in_line = csv.reader(self.fr)
        next(in_line, None)

        p = re.compile(r'(.*)_\d', re.I)

        for row in in_line:
            m = re.match(p, row[0])
            section = m.group(1)

            if not section in sec:
                sec.append(section)

        return sec

    def parse_scene(self, scene):

        l1_Value = dict()

        self.sections = self.parse_sections()

        p = re.compile(r'(.*)_\d', re.I)

        for kern in self.sections:

            l2_Value = defaultdict(list)

            self.fr = open(self.infile, "r")
            in_line = csv.reader(self.fr)
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

                if condition not in self.scenarios[scene]:
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

    #for s in scenarios:
    #    parse_file(s, sys.argv[1])
    parser = result_comparison(sys.argv[1], sys.argv[2])
    parser.parse_file()

if __name__ == "__main__":
    main(sys.argv[1:])
