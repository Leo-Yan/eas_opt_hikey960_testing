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

    # Parse the testing sections, every section is corresponding to one
    # kernel image or one set configurations
    sections = []

    def __init__(self, infile):
        self.infile  = infile

    def parse_sections(self):

        sec = []

        self.fr = open(self.infile, "r")
        in_line = csv.reader(self.fr)
        next(in_line, None)

        # Abstract the section id
        p = re.compile(r'(.*)_\d', re.I)

        for row in in_line:
            m = re.match(p, row[0])
            section = m.group(1)

            if not section in sec:
                sec.append(section)

        sec.sort()
        return sec

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

        os.system('gnuplot -e "filename=\'' + comp_type + '_plot.txt' + '\''+'" /tmp/plot_template')

    def write_scenario(self, scene, value):

        self.fo.write(scene)

        for kern in self.sections:
            collectValue = sorted(value[kern].items())

            print collectValue

            for condition, values in collectValue:
                print condition
                print values
                self.fo.write(' ' + str(sum(values) / len(values)))

        self.fo.write('\n')

    def parse_scenario(self, scene, scenarios):

        l1_Value = dict()

        p = re.compile(r'(.*)_\d', re.I)

        for kern in self.sections:

            l2_Value = defaultdict(list)

            self.fr = open(self.infile, "r")
            in_line = csv.reader(self.fr)
            next(in_line, None)

            for row in in_line:

                m = re.match(p, row[0])

                if row[1] not in scene:
                    continue

                section   = m.group(1)
                condition = row[3]
                value     = row[4]

                if condition not in scenarios[scene]:
                    continue

                if section != kern:
                    continue

                l2_Value[condition].append(float(value))
                l1_Value[section] = l2_Value

        return l1_Value

    def parse_scenarios(self, scenarios, comp_str):

        self.fo = open(comp_str + '_plot.txt', "w+")
        self.fo.write('test')

        for kern in self.sections:
            self.fo.write(' ' + kern)
        self.fo.write('\n')

        for s in scenarios:
            value = self.parse_scenario(s, scenarios)
            if bool(value) == False:
                continue
            self.write_scenario(s, value)

        self.fo.close()
        self.plot_comparison(comp_str)

    def parse_power(self):
        self.parse_scenarios(self.power_scenarios, 'power')

    def parse_perf(self):
        self.parse_scenarios(self.perf_scenarios, 'performance')

    def parse_file(self):
        self.sections = self.parse_sections()
        self.parse_power()
        self.parse_perf()


if __name__ == "__main__":

    if not os.path.isfile(sys.argv[1]):
        print "file don't exists:"
        sys.exit(1)

    parser = result_comparison(sys.argv[1])
    parser.parse_file()
