#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import listdir
import os
import re
import sys
from argparse import ArgumentParser
import random
import subprocess
from math import sqrt
import ast
from adderror import adderror
import numpy as np, numpy.random
import tempfile
import shutil

"""ENSAMBLE, -d directory -n number of models """
"""-k number of selected structure"""
"""-r repet of program"""

def get_argument():
    parser = ArgumentParser()
    parser.add_argument("-d", "--dir", dest="myDirVariable",
                        help="Choose dir", metavar="DIR", required=True)

    parser.add_argument("-n", metavar='N', type=int,
                        dest="n_files",
                        help="Number of selected structure",
                        required=True)

    parser.add_argument("-k", metavar='K', type=int,
                        dest="k_options",
                        help="Number of possibility structure, less then selected files",
                        required=True)

    parser.add_argument("-r", metavar='R', type=int,
                        dest="repeat", help="Number of repetitions",
                        default=1)
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")

    parser.add_argument("-result", type=float, dest="result", help="pesimist(0) or optimist(<0) result",
                        default = 0)

    args = parser.parse_args()
    return(args)

def find_pdb_file(args):
    pdb_files=[]
    files = listdir(args.myDirVariable)
    for line in files:
        line = line.rstrip()
        if re.search('.pdb$', line):
            pdb_files.append(line)
    total_number_of_pdb_files = int(len(pdb_files))
    return(pdb_files)

def test_argument(args):
    if int(len(find_pdb_file(args))) < args.n_files:
        print("Number od pdb files is ONLY", find_pdb_file(args))
        sys.exit(0)
    if args.k_options > args.n_files:
        print("Number of selected structure is ONLY", args.n_files)
        sys.exit(0)

def print_parametrs_verbose(args):
    print('Parametrs ')
    print('Total number of pdb files is', int(len(find_pdb_file(args))))
    print('Files from directory', args.myDirVariable)
    print('The number of the selected files',
          args.n_files)
    print('The number of selected options', args.k_options)
    print('All pdb.dat files \n', find_pdb_file(args))

def select_n(args):
    find_pdb_file(args)
    print("test")
    selected_files_for_ensamble = random.sample(find_pdb_file(args),args.n_files)
    if args.verbose:
        print('Randomly selected files: \n', selected_files_for_ensamble)

    return(selected_files_for_ensamble)

def select_k(args,  select_random_files_for_experiment):
    list_of_random_items = []
    list_of_random_items = random.sample(select_random_files_for_experiment,
                                         args.k_options)
    if args.verbose:
        print('Randomly selected files: \n', list_of_random_items)

    return(list_of_random_items)

def ensamble_fit(args, selected_files_for_ensamble, data_for_experiment_modified):
    with tempfile.TemporaryDirectory(dir = '.') as tmpdirname:
        print('created temporary directory', tmpdirname)
        for files in selected_files_for_ensamble:
            shutil.copy(files+'.dat', tmpdirname)
        #name = input("Enter your name: ")   # Python 3
        curve_for_ensamble = make_curve_for_experiment(data_for_experiment_modified, args)

    #    command = "/storage/brno3-cerit/home/krab1k/saxs-ensamble-fit/core/ensamble-fit -L -p /storage/brno2/home/petrahrozkova/SAXS/tmpdirname/ -n " +  str(args.n_files) + " -m /storage/brno2/home/petrahrozkova/SAXS/" + curve_for_ensamble
    #    subprocess.call(command,shell=True)
    return()

def work_with_result_from_ensamble():
    value_of_chi2 = []
    values_of_index_result =[]
    result_q_and_value = []
    with open('result', 'r') as f:
        next(f)
        #print (f.readline[2:4])
        for line in f:
            line = line.rstrip()
            value_of_chi2 =line.split(',')[3]
            values_of_index_result = line.split(',')[4:]
            result_q_and_value.append((value_of_chi2, values_of_index_result))

    #print(value_of_chi2)
    #print(values_of_index_result)
    print(result_q_and_value)

    return(result_q_and_value)

def do_result(args):
    result_q_and_value = work_with_result_from_ensamble()
    if args.result == 0:
        tolerance = 0
    else:
        tolerance = float(args.result)
        if tolerance > 1:
            print('Less then 1')
            sys.exit(0)
    maximum = float(max(result_q_and_value)[0])
    print(maximum)
    minimum = maximum - maximum*tolerance
    print(maximum, minimum)
    list_of_tuples = []
    #print(maximum)
    #for i in range(len(maximum[1])):
    #    if float(maximum[1][i]) != 0:
    #        list_of_tuples.append((i , maximum[1][i]))
    #print(list_of_tuples)




    print(tolerance)
"""
def be_pessimist(result_q_and_value):
    #print(value_of_chi2)
    maximum = max(result_q_and_value)
    list_of_tuples = []
    #print(maximum)
    for i in range(len(maximum[1])):
        if float(maximum[1][i]) != 0:
            list_of_tuples.append((i , maximum[1][i]))
    print(list_of_tuples)

    return(list_of_tuples)


def be_optimist(result_q_and_value):
    tolerance = 0.1
    maximum = max(result_q_and_value)
    #for i in result_q_and_value:
    #return(list_of_tuples)
"""
def make_curve_for_experiment(data_for_experiment_modified, args):
    print('data',data_for_experiment_modified)
    file_for_ensamble = []
    i = 0
    file_and_wight = []
    tmp = []
    k = args.k_options
    tmp = np.random.dirichlet(np.ones(args.k_options),size=1).transpose()
    for files in data_for_experiment_modified:
        file_and_wight.append((files, float(tmp[i])))
        i += 1
    print(file_and_wight)
    #result = []
    files = [open(file, 'r') for file in data_for_experiment_modified]
    with open('result.pdb.dat', 'w') as f:
        run = True
        while run:
            sum_result = 0
            i = 0
            for file in files:
                line = file.readline()
                if line == '':
                    run = False
                    break
                if not line.startswith('#'):
                    result = float(line.split(' ')[4])*file_and_wight[i][1]
                    sum_result = sum_result + result

            if sum_result != 0:
                print(sum_result)
                f.write(str(0) + '\t' +str(sum_result) + '\t' + str(0) + '\n')
    for file in files:
        file.close()
    curve_for_ensamble = adderror("exp.dat", 'result.pdb.dat')
    print(curve_for_ensamble)
    return(curve_for_ensamble)

def rmsd_pymol(structure_1, structure_2):
    with open("file_for_pymol.pml", "w") as file_for_pymol:
        file_for_pymol.write("""
        load  {s1}
        load  {s2}
        align {s3}, {s4}
        quit
        """.format(s1=structure_1, s2=structure_2,
                   s3=os.path.splitext(structure_1)[0],
                   s4=os.path.splitext(structure_2)[0]))
    out_pymol = subprocess.check_output(" pymol -c file_for_pymol.pml | grep Executive:", shell=True)
    #part for home:
    out_pymol = subprocess.check_output(" pymol -c file_for_pymol.pml | grep Executive:", shell=True)
    #part for META:out_pymol = subprocess.check_output("module add pymol-1.8.2.1-gcc; pymol -c file_for_pymol.pml | grep Executive:;module rm pymol-1.8.2.1-gcc", shell=True)
    rmsd = float(out_pymol[out_pymol.index(b'=')+1:out_pymol.index(b'(')-1])
    print('RMSD ', structure_1, ' and ', structure_2, ' = ', rmsd)
    return(rmsd)



if __name__ == '__main__':
    args = get_argument()
    modified_data = []
    data_for_experiment = []
    find_pdb_file(args)
    test_argument(args)
    result_q_and_value = []
    select_random_files_for_experiment = []
    if args.verbose:
        print_parametrs_verbose(args)

    for i in range(args.repeat):
        select_random_files_for_experiment = select_n(args)
        data_for_experiment = select_k(args, select_random_files_for_experiment)
        data_for_experiment_modified = [None]*args.k_options
        for i in range(args.k_options):
            data_for_experiment_modified [i] = str(data_for_experiment[i])+".dat"
        ensamble_fit(args, select_random_files_for_experiment, data_for_experiment_modified)
        #work_with_result_from_ensamble()
        do_result(args)
