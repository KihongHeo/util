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
        items = sorted(list(data.items()), key=lambda x: x[1])

    xs = [0]
    ys = [0]
    x = 0
    y = 0
    solved = set()
    for (name, time) in items:
        if time >= 3600:
            break
        x += 1
        y += time
        xs.append(x)
        ys.append(y)
        solved.add(name)
    ys = list(map(lambda x: x/60, ys))
    return (names, solved, xs, ys)

title_font = {'size':'20', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'}
axis_font = {'size':'18'}
def plot(problem):
#    plt.figure(figsize=(4,4), dpi=100)
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)

    # format for yaxis
#    ax = matplotlib.pyplot.gca()
#    mkfunc = lambda x, pos: '%1.0fM' % (x * 1e-6) if x >= 1e6 else '%1.0fK' % (x * 1e-3) if x >= 1e3 else '%1.0f' % x
#    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
#    ax.yaxis.set_major_formatter(mkformatter)
    if problem == "BV":
        markevery = 6
    else:
        markevery = 1

    (testset, solved_phog, xs_phog, ys_phog) = line("expr/sphog/" + problem + "/running_time_info")
    print("Problem: " + problem)
    plt.plot(xs_phog, ys_phog, 'b', label="Euphony", markevery=markevery)
    print("\tEuphony solved " + str(len(xs_phog) - 1) + "/ " + str(len(testset)))

    (names_eusolver, solved_eusolver, xs_eusolver, ys_eusolver) = line("expr/baseline/eusolver/" + problem + "/running_time_info", testset=testset)
    plt.plot(xs_eusolver, ys_eusolver, 'g--', label="EUSolver", markevery=markevery)
    print("\tEUSolver solved " + str(len(xs_eusolver) - 1) + "/" + str(len(names_eusolver)))
    
#    (names_cvc, solved_cvc, xs_cvc, ys_cvc) = line("expr/baseline/cvc/" + problem + "/running_time_info", testset=testset)
#    plt.plot(xs_cvc, ys_cvc, 'r', marker='s', label="CVC", markevery=markevery)
#    print("\tCVC solved " + str(len(xs_cvc) - 1) + "/" + str(len(names_cvc)))
   
#    solved = solved_phog.union(solved_pcfg).union(solved_eusolver).union(solved_cvc)
#    print("\tALL solved " + str(len(solved)) + "/" + str(len(testset)))
#    diff = set(testset).difference(solved)
#    print("\tDiff " + str(len(diff)))
#    print(diff)
#    print(solved)
    if problem == "BV":
        plt.xlabel('# Solved Instances (total = ' + str(len(testset) + 4) + ')', **axis_font)
        plt.ylabel('Time (m)',labelpad=-1, **axis_font)
    else:
        plt.xlabel('# Solved Instances (total = ' + str(len(testset)) + ')', **axis_font)
        plt.ylabel('Time (m)', **axis_font)
    plt.legend(fontsize=14)
    if problem == "BV":
        title = "BITVEC"
    elif problem == "STR":
        title = "STRING"
    elif problem == "LIA":
        title = "CIRCUIT"
    x0, x1, y0, y1 = plt.axis()
    plt.axis((x0+0.25, x1, y0, y1))
    plt.title(title, **title_font)
    plt.tight_layout()
    plt.savefig(problem + '.pdf')
    plt.close()

def plot2():
#    plt.figure(figsize=(4,4), dpi=100)
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams['axes.ymargin'] = 0
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)
    plt.tight_layout()
    # format for yaxis
#    ax = matplotlib.pyplot.gca()
#    mkfunc = lambda x, pos: '%1.0fM' % (x * 1e-6) if x >= 1e6 else '%1.0fK' % (x * 1e-3) if x >= 1e3 else '%1.0f' % x
#    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
#    ax.yaxis.set_major_formatter(mkformatter)
#    if problem == "BV":
#        markevery = 6
#    else:
    markevery = 10

    (testset1, solved_phog1, xs_phog1, ys_phog1) = line("expr/sphog/LIA/running_time_info")
    (testset2, solved_phog2, xs_phog2, ys_phog2) = line("expr/sphog/STR/running_time_info")
    (testset3, solved_phog3, xs_phog3, ys_phog3) = line("expr/sphog/BV/running_time_info")
    ys_phog = [0] + sorted(ys_phog1[1:] + ys_phog2[1:] + ys_phog3[1:])
    xs_phog = range(0, len(ys_phog))
    plt.plot(xs_phog, ys_phog, 'b', marker='o', label="A$^{*}$+PHOG", markevery=markevery)
    print(len(solved_phog1)+len(solved_phog2)+len(solved_phog3))
    (testset1, solved_phog1, xs_phog1, ys_phog1) = line("expr/sphog/LIA_uniform/running_time_info")
    (testset2, solved_phog2, xs_phog2, ys_phog2) = line("expr/sphog/STR_uniform/running_time_info")
    (testset3, solved_phog3, xs_phog3, ys_phog3) = line("expr/sphog/BV_uniform/running_time_info")
    ys_phog = [0] + sorted(ys_phog1[1:] + ys_phog2[1:] + ys_phog3[1:])
    xs_phog = range(0, len(ys_phog))
    plt.plot(xs_phog, ys_phog, 'g', marker='^', label="Uniform+PHOG", markevery=markevery)
    print(len(solved_phog1)+len(solved_phog2)+len(solved_phog3))

    (testset1, solved_phog1, xs_phog1, ys_phog1) = line("expr/sphog/LIA_pcfg/running_time_info")
    (testset2, solved_phog2, xs_phog2, ys_phog2) = line("expr/sphog/STR_pcfg/running_time_info")
    (testset3, solved_phog3, xs_phog3, ys_phog3) = line("expr/sphog/BV_pcfg/running_time_info")
    ys_phog = [0] + sorted(ys_phog1[1:] + ys_phog2[1:] + ys_phog3[1:])
    xs_phog = range(0, len(ys_phog))
    plt.plot(xs_phog, ys_phog, 'r', marker='s', label="A$^{*}$+PCFG", markevery=markevery)
    print(len(solved_phog1)+len(solved_phog2)+len(solved_phog3))

    (testset1, solved_phog1, xs_phog1, ys_phog1) = line("expr/sphog/LIA_pcfg_uniform/running_time_info")
    (testset2, solved_phog2, xs_phog2, ys_phog2) = line("expr/sphog/STR_pcfg_uniform/running_time_info")
    (testset3, solved_phog3, xs_phog3, ys_phog3) = line("expr/sphog/BV_pcfg_uniform/running_time_info")
    ys_phog = sorted(ys_phog1 + ys_phog2 + ys_phog3)
    xs_phog = range(0, len(ys_phog))
    plt.plot(xs_phog, ys_phog, 'gray', marker='D', label="Uniform+PCFG", markevery=markevery)
    print(len(solved_phog1)+len(solved_phog2)+len(solved_phog3))


#    print("\tEuphony solved " + str(len(xs_phog) - 1) + "/ " + str(len(testset)))

#    (names_eusolver, solved_eusolver, xs_eusolver, ys_eusolver) = line("expr/baseline/eusolver/LIA/running_time_info", testset=testset)
#    plt.plot(xs_eusolver, ys_eusolver, 'g', marker='^', label="EUSolver", markevery=markevery)
#    print("\tEUSolver solved " + str(len(xs_eusolver) - 1) + "/" + str(len(names_eusolver)))
    
#    (names_cvc, solved_cvc, xs_cvc, ys_cvc) = line("expr/baseline/cvc/LIA/running_time_info", testset=testset)
#    plt.plot(xs_cvc, ys_cvc, 'r', marker='s', label="CVC", markevery=markevery)
#    print("\tCVC solved " + str(len(xs_cvc) - 1) + "/" + str(len(names_cvc)))
   
#    solved = solved_phog.union(solved_pcfg).union(solved_eusolver).union(solved_cvc)
#    print("\tALL solved " + str(len(solved)) + "/" + str(len(testset)))
 #   diff = set(testset).difference(solved)
  #  print("\tDiff " + str(len(diff)))
#    print(diff)
#    print(solved)
#    if problem == "BV":
    plt.xlabel('# Solved Instances (total=405)', **axis_font)
    plt.ylabel('Time (m)',labelpad=-1, **axis_font)
#    else:
#        plt.xlabel('# Solved Instances (total = ' + str(len(testset)) + ')', **axis_font)
#        plt.ylabel('Time(s)', **axis_font)
    plt.legend(fontsize=14)
#    if problem == "BV":
#        title = "BITVEC"
#    elif problem == "STR":
#        title = "STRING"
#    elif problem == "LIA":
    title = "Efficacy of A$^{*}$ and PHOG"
    x0, x1, y0, y1 = plt.axis()
    plt.axis((x0+0.5, x1, y0, y1))
    plt.title(title, **title_font)
    plt.tight_layout()
    plt.savefig('efficacy.pdf')
    plt.close()


if __name__ == "__main__":
#    plot("LIA")
#    plot("STR")
#    plot("BV")
    plot2()
