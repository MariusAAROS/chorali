#!/usr/bin/env python2

import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default=None,
                    help="Input directory of files to summarize")
parser.add_argument("-o", "--output", type=str,
                    help="Summaries output directory")
args = parser.parse_args()

for pfile in os.listdir(args.input):
    with open(args.input+pfile) as file:
        print(pfile)
        filename = pfile.split(".")[0]
        sourcefile = args.output+filename+".sent.tok"
        print(sourcefile)
        nsent = sum(1 for line in open(sourcefile))
        print("sourcefile sentences number is "+str(nsent))
        with open(args.output+filename+".sent.clus", "w") as ofile:
            print(args.output+filename+".sent.clus")
            lines = file.readlines()
            lines = [str.strip(line) for line in lines]
            for n in range(nsent):
                found = False
                print(n)
                for num, line in enumerate(lines):
                    if str(n) in line:
                        ofile.write(str(num)+"\n")
                        found = True
                        # print(num)
                if not found:
                    sys.exit("Missing sentence!!!")
