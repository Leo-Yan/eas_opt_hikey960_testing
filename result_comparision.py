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
        'idle'                                      : [ 'Power' ],
        'audio'                                     : [ 'Power' ],
        'video'                                     : [ 'Power' ],
        'hackbench'                                 : [ 'Power' ],
        'geekbench'                                 : [ 'Power' ],
        'linpack'                                   : [ 'Power' ],
        'quadrant'                                  : [ 'Power' ],
        'smartbench'                                : [ 'Power' ],
        'nenamark'                                  : [ 'Power' ],
        'recentfling'                               : [ 'Power' ],
        'galleryfling'                              : [ 'Power' ],
        'browserfling'                              : [ 'Power' ],
        'uibench'                                   : [ 'Power' ],
        'uibench_InflatingListActivity'             : [ 'Power' ],
        'uibench_TextCacheHighHitrateActivity'      : [ 'Power' ],
        'uibench_FullscreenOverdrawActivity'        : [ 'Power' ],
        'uibench_EditTextTypeActivity'              : [ 'Power' ],
        'uibench_TrivialRecyclerViewActivity'       : [ 'Power' ],
        'uibench_InvalidateActivity'                : [ 'Power' ],
        'uibench_DialogListActivity'                : [ 'Power' ],
        'uibench_ActivityTransition'                : [ 'Power' ],
        'uibench_TextCacheLowHitrateActivity'       : [ 'Power' ],
        'uibench_ScrollableWebViewActivity'         : [ 'Power' ],
        'uibench_BitmapUploadActivity'              : [ 'Power' ],
        'uibench_TrivialListActivity'               : [ 'Power' ],
        'uibench_SlowBindRecyclerViewActivity'      : [ 'Power' ],
        'uibench_TrivialAnimationActivity'          : [ 'Power' ],
        'uibench_GlTextureViewActivity'             : [ 'Power' ],
        'uibench_ActivityTransitionDetails'         : [ 'Power' ],
        'uibench_ShadowGridActivity'                : [ 'Power' ]
    }

    perf_scenarios = {
        'hackbench'    : [ 'test_time' ],
        'geekbench'    : [ 'score',
                           'multicore_score' ],
        'linpack'      : [ 'Linpack ST',
                           'Linpack MT' ],
        'quadrant'     : [ 'benchmark_score' ],
        'smartbench'   : [ 'Smartbench: valueProd',
                           'Smartbench: valueGame' ],
        'nenamark'     : [ 'nenamark score' ],
        'recentfling'  : [ 'Average 90th Percentile',
                           'Average 95th Percentile',
                           'Average 99th Percentile',
                           'Average Jank',
                           'Average Jank%' ],
        'galleryfling' : [ 'Average 90th Percentile',
                           'Average 95th Percentile',
                           'Average 99th Percentile',
                           'Average Jank',
                           'Average Jank%' ],
        'browserfling' : [ 'Average 90th Percentile',
                           'Average 95th Percentile',
                           'Average 99th Percentile',
                           'Average Jank',
                           'Average Jank%' ],
        'emailfling'   : [ 'Average 90th Percentile',
                           'Average 95th Percentile',
                           'Average 99th Percentile',
                           'Average Jank',
                           'Average Jank%' ],
        'uibench'                              : [ 'janks%' ],
        'uibench_InflatingListActivity'        : [ 'janks%' ],
        'uibench_TextCacheHighHitrateActivity' : [ 'janks%' ],
        'uibench_FullscreenOverdrawActivity'   : [ 'janks%' ],
        'uibench_EditTextTypeActivity'         : [ 'janks%' ],
        'uibench_TrivialRecyclerViewActivity'  : [ 'janks%' ],
        'uibench_InvalidateActivity'           : [ 'janks%' ],
        'uibench_DialogListActivity'           : [ 'janks%' ],
        'uibench_ActivityTransition'           : [ 'janks%' ],
        'uibench_TextCacheLowHitrateActivity'  : [ 'janks%' ],
        'uibench_ScrollableWebViewActivity'    : [ 'janks%' ],
        'uibench_BitmapUploadActivity'         : [ 'janks%' ],
        'uibench_TrivialListActivity'          : [ 'janks%' ],
        'uibench_SlowBindRecyclerViewActivity' : [ 'janks%' ],
        'uibench_TrivialAnimationActivity'     : [ 'janks%' ],
        'uibench_GlTextureViewActivity'        : [ 'janks%' ],
        'uibench_ActivityTransitionDetails'    : [ 'janks%' ],
        'uibench_ShadowGridActivity'           : [ 'janks%' ],
    }

    # Parse the testing sections, every section is corresponding to one
    # kernel image or one set configurations
    sections = []

    baseline = None

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

            if m is None:
                section = 'general_section'
            else:
                section = m.group(1)

            if not section in sec:
                sec.append(section)

        sec.sort()

        self.baseline = sec[0]
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
        temp_f.write("set style line 1 lc rgb 'orange'\n")
        temp_f.write("set style line 2 lc rgb 'pink'\n")
        temp_f.write("set style line 3 lc rgb 'blue'\n")
        temp_f.write("set style line 4 lc rgb 'cyan'\n")
        temp_f.write("set style line 5 lc rgb 'seagreen'\n")
        temp_f.write("set style line 6 lc rgb 'green'\n")
        temp_f.write("set style line 7 lc rgb 'brown'\n")
        temp_f.write("set style line 8 lc rgb 'yellow'\n")
        temp_f.write("set style line 9 lc rgb 'red'\n")
        temp_f.write("plot for [i=2:"+str(sec_num)+"] filename using i:xtic(1) ti col ls i-1;\n")
        temp_f.write("set terminal wxt noenhanced font 'Ubuntu,9'\n")
        temp_f.close()

        os.system('gnuplot -e "filename=\'' + comp_type + '_plot.txt' + '\''+'" /tmp/plot_template')

    def write_scenario(self, scene, metric, value, baseline=None):

        self.fo.write(scene.replace(" ", "_") + '_' + metric.replace(" ", "_"))

        if not baseline is None:
            for m, values in sorted(value[baseline].items()):
                if m == metric:
                    base = sum(values) / len(values)
                    break
        else:
            base = 0

        for kern in self.sections:
            collectValue = sorted(value[kern].items())
            for m, values in collectValue:
                if m == metric:
                    self.fo.write(' ' + str(sum(values) / len(values) - base))

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

                if m is not None:
                    section = m.group(1)
                else:
                    section = 'general_section'

                condition = row[3]
                value     = row[4]

                if condition not in scenarios[scene]:
                    continue

                if section != kern:
                    continue

                l2_Value[condition].append(float(value))
                l1_Value[section] = l2_Value

        return l1_Value

    def parse_scenarios(self, scenarios, comp_str, baseline=None):

        self.fo = open(comp_str + '_plot.txt', "w+")
        self.fo.write('test')

        for kern in self.sections:
            self.fo.write(' ' + kern)
        self.fo.write('\n')

        filled_data = False

        for s in scenarios:
            value = self.parse_scenario(s, scenarios)
            if bool(value) == False:
                continue
            filled_data = True

            for metric in scenarios[s]:
                print 'condition = {}'.format(metric)
                self.write_scenario(s, metric, value, baseline)
        self.fo.close()

        if filled_data is False:
            print comp_str + ": data is empty"
            return

        self.plot_comparison(comp_str)

    def parse_power(self):
        self.parse_scenarios(self.power_scenarios, 'power')
        self.parse_scenarios(self.power_scenarios, 'power_delta', self.baseline)

    def parse_perf(self):
        self.parse_scenarios(self.perf_scenarios, 'performance')
        self.parse_scenarios(self.perf_scenarios, 'performance_delta', self.baseline)

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
