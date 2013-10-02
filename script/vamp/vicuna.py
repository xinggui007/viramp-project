## AUTHOR: Yinan Wan ##
## DATE: 2013/09/30 ##
## Description: Run the VICUNA de novo assembler ##

## DEMO ##
# python vicuna.py -p paired.fa -s single.fa -f fasta -o outfile.fa #

import sys, os, re
import shutil
import argparse
import subprocess

VAMP_DIR = os.path.split(os.path.abspath(__file__))[0]
VICUNA_CONF = os.path.join(VAMP_DIR, 'vicuna_conf')

PFOLDER = 'paired'
SFOLDER='single'
CPATH = os.path.abspath('./')
PFPATH = os.path.join(CPATH, PFOLDER)
SFPATH = os.path.join(CPATH, SFOLDER)

def run_cmd(cmds, getval=True):
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if getval:
                return out


def p_mkdir(ndir):
	if not os.path.exists(ndir):
		os.makedirs(ndir)

def wrap():
	parser = argparse.ArgumentParser(description='Running the vicuna')
	parser.add_argument('-p', metavar='paired.fa', help='paired-end read file')
	parser.add_argument('-s', metavar='single.fa', help='single-end read file')
	parser.add_argument('-f', choices=['fasta', 'fastq'], default='fasta', help='read file format')
	parser.add_argument('-o', metavar='outfile.fa', default='outfile.fa', help='output file name')

	def vicuna():
		if args.f == 'fasta':
			dst_p = os.path.join(PFPATH, 'reads.fa')
			dst_s = os.path.join(SFPATH, 'sreads.fa')
			confile = 'fa_vicuna_conf.txt' 
		elif args.f == 'fastq':
			dst_p = os.path.join(PFPATH, 'reads.fq')
			dst_s = os.path.join(SFPATH, 'sreads.fq')
			confile = 'fq_vicuna_conf.txt'

		p_mkdir(PFPATH)
		p_mkdir(SFPATH)

		shutil.copyfile(args.p, dst_p)
		shutil.copyfile(args.s, dst_s)
		config_f = os.path.join(VICUNA_CONF, confile)

		commands_1 = ['vicuna-omp-v1.0', config_f]
		run_cmd(commands_1, getval=False)

		os.rename('contig.lfv.fasta', args.o)

	parser.set_defaults(func=vicuna)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
			
