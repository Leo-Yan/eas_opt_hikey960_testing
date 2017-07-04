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

    power_scenarios = {
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
            'Power',
        ],
    }

    perf_scenarios = {
        'hackbench' : [
            'test_time'
        ],
        'geekbench' : [
            'score',
            'multicore_score',
        ],
    }

    sections = []
    write_tag = 0

    def __init__(self, infile, outfile):
        self.infile  = infile
        self.outfile = outfile

    def parse_file(self):

        self.sections = self.parse_sections()
        self.parse_power()
        self.parse_perf()

    def parse_power(self):

        self.fo = open(self.outfile, "w+")
        self.fo.write('test')

        for kern in self.sections:
            self.fo.write(' ' + kern)
        self.fo.write('\n')

        for s in self.power_scenarios:
            value = self.parse_scene(s, self.power_scenarios)
            if bool(value) == False:
                continue
            self.write_scene(s, value)

        self.fo.close()
        self.plot_comparison('Power')

    def parse_perf(self):

        self.fo = open(self.outfile, "w+")
        self.fo.write('test')

        for kern in self.sections:
            self.fo.write(' ' + kern)
        self.fo.write('\n')

        for s in self.perf_scenarios:
            value = self.parse_scene(s, self.perf_scenarios)
            if bool(value) == False:
                continue
            self.write_scene(s, value)

        self.fo.close()
        self.plot_comparison('Performance')

    def plot_comparison(self, comp_type):

        sec_num = len(self.sections)
        sec_num += 1

        temp_f = open('/tmp/plot_template', "w+")
        temp_f.write("set terminal pngcairo noenhanced size 1024,600 font 'Ubuntu,9'\n")
        temp_f.write("set output '"+ comp_type + "_comparison.png'\n")
        temp_f.write("set grid\n")
        temp_f.write("set title " + "'" + comp_type + " Comparision'\n")
        temp_f.write("set ylabel " + "'" + comp_type + " Result'\n")
        temp_f.write("set boxwidth 0.9 absolute\n")
        temp_f.write("set style fill solid 1.00 border lt -1\n")
        temp_f.write("set key outside right\n")
        temp_f.write("set style histogram clustered gap 1 title  offset character 0, 0, 0\n")
        temp_f.write("set datafile missing '-'\n")
        temp_f.write("set style data histograms\n")
        temp_f.write("set xtics rotate by -45\n")
        temp_f.write("set xtics ()\n")
        temp_f.write("plot for [i=2:"+str(sec_num)+"] filename using i:xtic(1) ti col ls i-1;\n")
        temp_f.write("set terminal wxt noenhanced font 'Ubuntu,9'\n")
        temp_f.close()

        os.system('gnuplot -e "filename=\''+self.outfile+'\''+'" /tmp/plot_template')

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

        sec.sort()

        print sec

        return sec

    def parse_scene(self, scene, scenarios):

        l1_Value = dict()

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

                if condition not in scenarios[scene]:
                    continue

                #print section
                #print kern
                if section != kern:
                    continue

                l2_Value[condition].append(float(value))
                l1_Value[section] = l2_Value

        print l1_Value

        return l1_Value


    def write_scene(self, scene, value):

        self.fo.write(scene)

        for kern in self.sections:
            collectValue = sorted(value[kern].items())

            print collectValue

            for condition, values in collectValue:
                print condition
                print values
                self.fo.write(' ' + str(sum(values) / len(values)))

        self.fo.write('\n')


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
