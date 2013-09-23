## AUTHOR: Yinan Wan ##
## DATE: 2013/09/23 ##
## Description: This script use MUMmer toolkit to find inexact repeats in draft genome ##

## Demo ##
# Python inexact_repeats.py -g draft_genome.py -o output.txt #

import sys, os, re
import subprocess
import argparse

def run_cmd(cmds, getval=True):
	DEVNULL = open(os.devnull, 'wb')
	p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
	out, err = p.communicate()
	if getval:
		return out

def wrap():
	parser = argparse.ArgumentParser(description='Find inexact repeats in draft genome')
	parser.add_argument('-g', metavar='draft_genome.fa', help='Genome sequence for repeat analysis')
	parser.add_argument('-o', metavar='output.txt', default='output.txt', help='Output file name, by default is "output.txt"')

	def vnucmer():
		commands = ['nucmer', '--maxmatch', '--nosimplify', '='.join(['--prefix', 'draft_nucmer']), args.g, args.g]
		run_cmd(commands, getval=False)

	def coords():
		commands = ['show-coords', '-rTH', 'draft_nucmer.delta']
		rawrep = run_cmd(commands)

		f = open(args.o, 'wb')
		rheader = '\t'.join(['st1','end1','st2','end2','len1', 'len2','%idy','ctg1#', 'ctg2#'])
		f.write(rheader+'\n')

		for line in rawrep.split('\n'):
			if len(line)>0:
				elem = line.split('\t')
				seq1 = [elem[0], elem[1], elem[7]]
				seq2 = [elem[2], elem[3], elem[8]] ## start, end, contig

				if seq1 != seq2:
					# rline = '\t'.join([elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]])
					f.write(line+'\n')

		f.close()

	def pipeline():
		vnucmer()
		coords()

	parser.set_defaults(func=pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
