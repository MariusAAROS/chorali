import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default=None, help="Input directory of source files")
parser.add_argument("-o", "--output", type=str, default=None, help="ouput file path")
args = parser.parse_args()


listd = os.listdir(args.input)
directories = [os.path.join(args.input,o) for o in listd if os.path.isdir(os.path.join(args.input,o))]
topicsf=open(args.output,"w")
for dir_index,_dir in enumerate(directories):
	topicsf.write("<topic>\n<num> "+os.path.basename(_dir)+" </num>\n<title> </title>\n\n<narr>\n</narr>\n\n<docs>\n")
	files = os.listdir(_dir)
	for file in files:
		topicsf.write(file+"\n")
	topicsf.write("</docs>\n\n</topic>\n\n")
