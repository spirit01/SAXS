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
"""ENSAMBLE, -d directory -n number of models """
"""-k number of selected structure"""
"""-r repet of program"""

files = []
pdb_files = []
exp_file = []
list_of_random_items_modified = []
list_of_random_items = []
selected_files_for_ensamble = []

def argument():
    parser = ArgumentParser()
    parser.add_argument("-d", "--dir", dest="myDirVariable",
                        help="Choose dir", metavar="DIR", required=True)

    parser.add_argument("-n", metavar='N', type=int,
                        dest="number_of_selected_files",
                        help="Number of selected structure",
                        required=True)

    parser.add_argument("-k", metavar='K', type=int,
                        dest="k_number_of_options",
                        help="Number of possibility structure, less then selected files",
                        required=True)

    parser.add_argument("-q", metavar='Q', type=int,
                        dest="mixing_koeficient", help="Mixing koeficient",
                        default=1)
    parser.add_argument("-r", metavar='R', type=int,
                        dest="repeat", help="Number of repetitions",
                        default=1)
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()

    global files
    global list_of_random_items_modified
    files = listdir(args.myDirVariable)
    list_of_random_items_modified = [None]*1
    return(args)

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
    #part for home:out_pymol = subprocess.check_output(" pymol -c file_for_pymol.pml | grep Executive:", shell=True)
    #part for META:out_pymol = subprocess.check_output("module add pymol-1.8.2.1-gcc; pymol -c file_for_pymol.pml | grep Executive:;module rm pymol-1.8.2.1-gcc", shell=True)
    rmsd = float(out_pymol[out_pymol.index(b'=')+1:out_pymol.index(b'(')-1])
    print('RMSD ', structure_1, ' and ', structure_2, ' = ', rmsd)
    return rmsd

def searching_pdb():
    for line in files:
        line = line.rstrip()
        if re.search('.pdb$', line):
            #if re.search('.pdb.dat', line):
            pdb_files.append(line)
        #if re.search('exp.dat', line):
            #print('experimental file', line)
        #    exp_file.append(line)
    total_number_of_pdb_files = len(pdb_files)
    return(total_number_of_pdb_files)

def argument_processing(args, total_number_of_pdb_files):
    #print(args)
    print('Parametrs ')
    print('Total number of pdb files', total_number_of_pdb_files)

    if total_number_of_pdb_files < args.number_of_selected_files:
        print("Number od pdb files is ", total_number_of_pdb_files)
        sys.exit(0)

    if args.k_number_of_options > args.number_of_selected_files:
        print("Number of selected structure is only", args.number_of_selected_files)
        sys.exit(0)

    if args.mixing_koeficient != 1:
        print ("For q>1 is not implemented now \n")
        sys.exit(0)

    print('Files from directory', args.myDirVariable)
    print('The number of the selected files',
          args.number_of_selected_files)
    print('The number of selected options', args.k_number_of_options)
    print('All pdb.dat files \n', pdb_files)

    global selected_files_for_ensamble
    selected_files_for_ensamble = random.sample(pdb_files,
                                                args.number_of_selected_files)
    print('Randomly selected files: \n', selected_files_for_ensamble)

    global list_of_random_items
    list_of_random_items = random.sample(selected_files_for_ensamble,
                                         args.k_number_of_options)
    print('Randomly selected files: \n', list_of_random_items)

def using_adderror():
    list_of_random_items_modified[0] = adderror("exp.dat",list_of_random_items[0]+'.dat')
    str1 = ''.join(str(e)+"\n" for e in list_of_random_items_modified)
    str2 = ''.join(str(e)+"\n" for e in list_of_random_items)
    print(str1)
    print(str2)

    return(str1, str2)

def find_index(strings):
    for e in list_of_random_items:
        value_of_index = selected_files_for_ensamble.index(e)
        print(selected_files_for_ensamble.index(e))

    with open("input_for_ensamble_fit", "w") as f:
        f.write(strings[0])

def ensamble_fit():
    command = "/storage/brno3-cerit/home/krab1k/saxs-ensamble-fit/core/ensamble-fit -L -p /storage/brno2/home/petrahrozkova/SAXS/mod -n " +  str(args.number_of_selected_files) + " -m /storage/brno2/home/petrahrozkova/SAXS/" +list_of_random_items_modified[0]+".dat"

    subprocess.call(command,shell=True)

def result_rmsd():
    with open('result', 'r') as f:
        (f.readline())
        result = f.readline()
        values_of_index_result = result.split(',')[4:]
        return(values_of_index_result)

def pymol_processing():
    sum_rmsd = 0
    values_of_index_result = result_rmsd()
    dictionary_index_and_structure = dict()
    for i, j in enumerate(selected_files_for_ensamble):
        dictionary_index_and_structure[i] = j

    for i, j in enumerate(values_of_index_result):
        f = float(j)
        if f != 0:
            computed_rmsd = rmsd_pymol(selected_files_for_ensamble[i],
                                       list_of_random_items[0])
            print('Adjusted rmsd ', f*computed_rmsd, '\n')
            sum_rmsd += f*computed_rmsd

    print('Sum of RMSD', sum_rmsd)


if __name__ == '__main__':
    args = argument()
    total_number_of_pdb_files = searching_pdb()
    for i in range(args.repeat):
        argument_processing(args, total_number_of_pdb_files)
        strings = using_adderror()
        find_index(strings)
        #ensamble-fit()
        pymol_processing()
