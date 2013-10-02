## AUTHOR: Yinan Wan ##
## Date: 2013/09/30 ##
## Description: Run the SPAdes assembler ##

## Demo ##
#python SPAdes.py -p paired.fa -s single.fa -k 31,41,51,61 -o spades_sc.fa  #

import sys, os, re
import argparse
import subprocess
import shutil

CPATH = os.path.abspath('./')
PRD = 'spades_paired.fa'
SRD = 'spades_single.fa'
def run_cmd(cmds, getval=True):
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = p.communicate()
        if getval:
                return out

def wrap():
	parser = argparse.ArgumentParser(description='de novo assembling by SPAdes')
	parser.add_argument('-p', metavar='paired.fa', help='paired-end reads file')
	parser.add_argument('-s', metavar='single.fa', help='single-end reads file')
	parser.add_argument('-k', metavar='khmers', help='k-mers used in SPAdes de novo assembling, multiple khmers allowed')
	parser.add_argument('-o', metavar='spades_sc.fa', default='spades_sc.fa', help='output file name, by default sapdes_sc.fa')

	def run_spades():
		paired_rd = str()
		single_rd = str()
		new_prd = str()
		new_srd = str()

		if args.p:
			paired_rd = '--12'
			new_prd = PRD
			shutil.copyfile(args.p, new_prd) 
		if args.s:
			single_rd = '-s'
			new_srd = SRD
			shutil.copyfile(args.s, new_srd)

		commands = ['spades.py', '-k', args.k, '--careful', '--only-assembler', paired_rd, new_prd, single_rd, new_srd, '-o', 'spades_out']
		print ' '.join(commands)
		run_cmd(commands, getval=False)
		shutil.copyfile('spades_out/scaffolds.fasta', args.o)

	parser.set_defaults(func=run_spades)
	args = parser.parse_args()
	args.func()

if __name__ == "__main__":
	wrap()	

