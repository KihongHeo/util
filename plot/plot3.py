#!/usr/local/bin/python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys
import os
import re
import math

def line(filename, testset=None):
    data = {}
    names = set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            tokens = re.split('[ \t]+', line)
            if testset == None or tokens[0] in testset:
                names.add(tokens[0])
                data[tokens[0]] = float(tokens[1])

    return data

title_font = {'fontname':'Arial', 'size':'18', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'}
axis_font = {'fontname':'Arial', 'size':'13'}
def plot(problem):
    if problem == "BV":
        markevery = 6
    else:
        markevery = 1

    data_phog = line("expr/sphog/" + problem + "/running_time_info")
    data_pcfg = line("expr/sphog/" + problem + "_pcfg/running_time_info")
    count = 0
    xs = []
    ys = []
    for (name, time) in data_phog.items():
        if time >= 3600:
            continue
        try:
            pcfg_time = data_pcfg[name]
        except:
            pcfg_time = 3600
        xs.append(float(pcfg_time))
        ys.append(float(time))
        count += 1
    
    plt.scatter(xs, ys, facecolors='none', edgecolors='b')
    return count
   
if __name__ == "__main__":
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.tight_layout()
    plt.xlim([0,3600])
    plt.ylim([0,3600])
    count_lia = plot("LIA")
    count_str = plot("STR")
    count_bv = plot("BV")
    plt.plot([0, 3600], [0, 3600], 'r--', linewidth=1)
    print("LIA:" + str(count_lia))
    print("STR:" + str(count_str))
    print("BV:" + str(count_bv))
    title ="Running Time (total=" + str(count_lia + count_str + count_bv) + ")"
    plt.title(title, **title_font)
    plt.xlabel("$EUPHONY_{PCFG}$ (s)", **axis_font)
    plt.ylabel("$EUPHONY_{PHOG}$ (s)", **axis_font)
    plt.savefig('efficacy.pdf')
    plt.close()
