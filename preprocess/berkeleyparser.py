import os, sys
import subprocess


class Parser:
    def __init__(self):
        self.jobs = {}
        self.parsed = {}

    def clear(self):
        self.jobs = {}
        self.parsed = {}

    def add_job(self, id, sentence):
        self.jobs[id] = sentence

    def run(self):
        abstract()

    def get_job(self, id):
        return self.jobs[id]

    def parse(self, sentence):
        self.clear()
        self.add_job(0, sentence)
        self.run()
        return self.get_job(0)

class CommandLineParser(Parser):
    def __init__(self, command):
        Parser.__init__(self)
        self.command = command

    def run(self):
        if not self.jobs:
            return
        proc=subprocess.Popen([self.command],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE)
        #output, input = popen2.popen2(self.command)
        for id in self.jobs:
            proc.stdin.write(self.jobs[id] + "\n")
        out,err=proc.communicate()
        out = [l.strip() for l in out.split("\n")]
        for i, id in enumerate(self.jobs):
            self.parsed[id] = out[i]
        #output.close()

if __name__ == "__main__":
    #parser = CommandLineParser("parser_bin/berkeleyParser+Postagger.sh")
    parser = CommandLineParser("parser_bin/distribute.sh parser_bin/berkeleyParser+Postagger.sh")
    id = 0
    for line in sys.stdin.readlines():
        line = line.rstrip()
        parser.add_job(id, line)
        id += 1
    parser.run()
    for id in parser.parsed:
        print(id, parser.parsed[id])
