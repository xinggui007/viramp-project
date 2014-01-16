import os, re, sys
import subprocess
import argparse

def run_cmd(cmds, getval=True):
        DEVNULL = open(os.devnull, 'wb')
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
        out, err = p.communicate()
        if getval:
                return out
def purge(dir, pattern):
        for f in os.listdir(dir):
                if re.search(pattern, f):
                        try:
                                os.remove(os.path.join(dir,f))
                        except:
                                shutil.rmtree(os.path.join(dir,f))

def wrap():
	parser = argparse.ArgumentParser(description="Run BWA for mapping")
	parser.add_argument('-r', metavar="refseq.fa", help='reference sequence for mapping')
	parser.add_argument('-l', metavar="read file_1")
	parser.add_argument('-e', metavar="read file_2, optional, only needed for a paired-end mapping with two separate files")
	parser.add_argument('-p', action="store_true", help="indicating the paired-end reads are interleaved in one file (-e is not needed here)")
	
	subparsers = parser.add_subparsers(dest="action")
	
	parser_normal = subparsers.add_parser('basic', help="Running the basic BWA algorithm")
	parser_normal.add_argument('-o', metavar="INT", default='5', help='maximum number of gap opens')


	parser_mem = subparsers.add_parser()
