## AUTHOR: Yinan Wan ##
## DATE: 2013/09/23 ##
## Description: This script use MUMmer toolkit to find tandem repeats in draft genome ##

## Demo ##
# python tendam_repeats.py -s target_genome.fa -l 50 #

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
	parser = argparse.ArgumentParser(description='Find tendam repeats in draft genome')
	parser.add_argument('-s', metavar='genome.fa', help='Genome sequence for analysis, FASTA format')
	parser.add_argument('-l', metavar='INT', default='50', help='Minimum tandem repeat length, by default is 50')
	parser.add_argument('-o', metavar='output.txt', default='output.txt', help='Output file name, by default is output.txt')

	def break_contigs():
		ctg_name=str()
		ctg = dict()
		for line in file(args.s):
			line = line.strip()
			if re.match('^>', line):
				ctg_name=line.split('>')[1]
				ctg.update({ctg_name:str()})
			else:
				ctg[ctg_name] = ctg[ctg_name] + line

		return ctg

	def show_tandem(ctg):
		fnew = open(args.o, 'wb')
		fheader = '\t'.join(['Start','Extent', 'UnitLen', 'Copies', 'Ctg#'])
		fnew.write(fheader+'\n')

		for ct in sorted(ctg.keys()):
			f = open('tmp.fa','wb')
			f.write(''.join(['>',ct]))
			f.write('\n')
			f.write(ctg[ct])
			f.write('\n')
			f.close()

			commands = ['exact-tandems','tmp.fa', args.l]
			result = run_cmd(commands)
			for line in result.split('\n'):
				line = line.strip()
				if re.match('^[0-9]', line):
					elem = line.split()
					nline = '\t'.join(elem+[ct])
					fnew.write(nline+'\n')		
		fnew.close()				

	def pipeline():
		ctg = break_contigs()
		show_tandem(ctg)

	parser.set_defaults(func=pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
