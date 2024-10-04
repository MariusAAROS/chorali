from __future__ import unicode_literals
import os,sys
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default=None, help="similarities files directory")
parser.add_argument("-m", "--minsim", type=float, default=0.0, help="minimum similarity value under which similarity is considered as null")
parser.add_argument("-o", "--output", type=str, help="output directory")
args = parser.parse_args()

if os.path.exists(args.output):
    shutil.rmtree(args.output)
os.mkdir(args.output)

print("starting")
files = [os.path.join(args.input,o) for o in os.listdir(args.input)]
for file in files:
    with open(file,"r") as infile:
        filename=os.path.basename(file)
        outputfile=os.path.join(args.output,filename)
        lines=infile.read().splitlines()
        with open(outputfile,"w") as outfile:
            for line in lines:
                splittedline=line.split()
                sim=float(splittedline[2])
                if sim < args.minsim:
                    newline=splittedline[0]+" "+splittedline[1]+" 0.0\n"
                else:
                    newline=line+"\n"
                outfile.write(newline)
print("file has been filtered")
