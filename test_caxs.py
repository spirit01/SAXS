#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""testovaci program pro ENSAMBLE, -d adresař -n počet modelů -k počet vybranných
vybraných molekul, -r počet opakování"""
from os import listdir
import re
import sys
from argparse import ArgumentParser
import random
pocet_pdb_souboru=0
parser = ArgumentParser()
pdb_soubory=[]

parser.add_argument("-d", "--dir", dest="myDirVariable",
                    help="choose dir", metavar="DIR",required=True)

parser.add_argument("-n", metavar='N', type=int, dest="pocet_vybranych",
                        help="pocet zvolenych srtuktur")

parser.add_argument("-k", metavar='K', type=int, dest="pocet_vybranych_z_n",
                        help="pocet vybranych molekul ze souboru n")


args = parser.parse_args() #zpacuje argumenty skriptu

files = listdir(args.myDirVariable)

for line in files:
        #print line
        line = line.rstrip()
        if re.search('pdb.dat', line):
            pocet_pdb_souboru=pocet_pdb_souboru+1
            pdb_soubory.append(line)
            #print line
number_of_pdb_files = len(pdb_soubory)
print ('počet', number_of_pdb_files)

print (pocet_pdb_souboru)

print (args.myDirVariable)
print (args.pocet_vybranych)
print (args.pocet_vybranych_z_n)
print (pdb_soubory)


if pocet_pdb_souboru<args.pocet_vybranych:
    print ("Souborů je pouze ", pocet_pdb_souboru)

if args.pocet_vybranych_z_n>args.pocet_vybranych:
    print ("Pocet vybranych souboru je pouze", args.pocet_vybranych)

#list_of_random_items = random.sample(pdb_soubory, args.pocet_vybranych)
#print (list_of_random_items)
