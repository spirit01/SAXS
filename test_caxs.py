#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""testovaci program pro ENSAMBLE, -d adresař -n počet modelů -k počet vybranných
vybraných molekul, -r počet opakování"""
from os import listdir
import re
import sys
from argparse import ArgumentParser
import random
import subprocess
from math import sqrt
import ast


parser = ArgumentParser()
pdb_files=[]

parser.add_argument("-d", "--dir", dest="myDirVariable",
                    help="Choose dir", metavar="DIR",required=True)

parser.add_argument("-n", metavar='N', type=int, dest="number_of_selected_files",
                        help="Number of selected structure")

parser.add_argument("-k", metavar='K', type=int, dest="k_number_of_options",
                        help="Number of possibility structure, less then selected files")

parser.add_argument ("-q",metavar='Q', type=int, dest="mixing_koeficient",
                        help="Mixing koeficient" )


args = parser.parse_args() #zpacuje argumenty skriptu
files = listdir(args.myDirVariable)

def rmsd_pymol(structure_1, structure_2):
    file_for_pymol=open('script_for_pymol.pml', 'w')
    file_for_pymol.write('run fitting.py \n')
    file_for_pymol.write('load '+  structure_1[:len(structure_1)-4]+'\n' )
    file_for_pymol.write('load '+  structure_2[:len(structure_2)-4]+'\n' )
    file_for_pymol.write('fitting '+ structure_1[:len(structure_1)-8] + ', c. a, ')
    file_for_pymol.write(structure_2[:len(structure_2)-8] + ', c. a \n')
    file_for_pymol.write('quit \n')
    file_for_pymol.close()

    out_pymol=subprocess.check_output("pymol -c script_for_pymol.pml | grep selection", shell=True)
    rmsd = float (out_pymol[out_pymol.index(b'=')+1:len(out_pymol)-1])
    print ('RMSD ', structure_1, ' and ', structure_2 , ' = ',rmsd)
    return rmsd

for line in files:
        #print line
        line = line.rstrip()
        if re.search('pdb.dat', line):
            pdb_files.append(line)
            #print line
total_number_of_pdb_files = len(pdb_files)
print ('Parametrs ')
print ('Total number of pdb.dat files', total_number_of_pdb_files)

if total_number_of_pdb_files<args.number_of_selected_files:
    print ("Number od pdb.dat files is ", total_number_of_pdb_files)
    sys.exit(0)

if args.k_number_of_options>args.number_of_selected_files:
    print ("Pocet vybranych souboru je pouze", args.number_of_selected_files)
    sys.exit(0)

if args.mixing_koeficient != 1:
    print ("For q>1 is not implemented now \n")
    sys.exit(0)

print ('Files from directory', args.myDirVariable)
print ('The number of the selected files',args.number_of_selected_files)
print ('The number of selected options', args.k_number_of_options)
print ('All pdb.dat files \n',pdb_files)

selected_files_for_ensamble = random.sample(pdb_files, args.number_of_selected_files)
print ('Randomly selected files: \n',selected_files_for_ensamble)

list_of_random_items = random.sample(selected_files_for_ensamble,args.k_number_of_options)
print ('Randomly selected files: \n',list_of_random_items)


str1 = ''.join(str(e)+"\n"  for e in list_of_random_items)

#hodnoty indexů vybraných stukrur
for e in list_of_random_items:
    value_of_index=selected_files_for_ensamble.index(e)
    print(selected_files_for_ensamble.index(e))

f = open('input_for_ensamble_fit', 'w')
f.write(str1)
f.close()

#subprocess.call("/storage/brno3-cerit/home/krab1k/saxs-ensamble-fit/core/ensamble-fit -L -p /storage/brno2/home/petrahrozkova/SAXS/mod -n 10 -m /storage/brno2/home/petrahrozkova/SAXS/mod08.pdb.dat",shell=True)

#RMSD in PyMol
f = open('result','r')
(f.readline())
result=f.readline()
values_of_index_result=result.split(',')[4:]
str2 = ''.join(str(e)+"\n"  for e in values_of_index_result)
print (str2)

for i in values_of_index_result:
    f = float(i)
    if f != 0:
        print (i)
        selected_index=values_of_index_result.index(i)
        print (selected_index)
        rmsd_pymol(selected_files_for_ensamble[selected_index],list_of_random_items[0])

#print (str2)
