## AUTHOR: Yinan Wan ##
## DATE: 2013/09/04 ##
## Descriptor: This script runs the diginorm program to reduce the sequencing coverage ##

## Demo ##
# python diginorm.py -i input.fq -o diginorm_out -p #

import os, re
import argparse

DIGI_DIR = '/mnt/src/python-module/khmer'
DIGI_SCRIPT_DIR = os.path.join(DIGI_DIR, 'scripts')
DIGI_SANDBOX_DIR = os.path.join(DIGI_DIR, 'sandbox')

def run_cmd(cmd):
	command = ' '.join(cmd)
	os.system(command)

def wrap():
	parser = argparse.ArgumentParser(description='Diginorm process in virus assembling')
	parser.add_argument('-i', metavar='input.fq', help='reads file for dignorm')
	parser.add_argument('-o', metavar='diginorm_out', default='diginorm_out', help='prefix for output files, default is diginorm_out')
	parser.add_argument('-C', metavar='INT', default='10', help='coverage cutoff, by default is 10')
	parser.add_argument('-N', metavar='INT', default='4', help='Number of hashtable to use, by default is 4')
	parser.add_argument('-x', metavar='INT', default='1e8', help='lower_bound of hashsize to use, by default is 1e8')
	parser.add_argument('-p', action='store_true', help='using paired-end reads')

	def normalize(cutoff, normfile, savehash=True, paired=True):
		norm_dir = os.path.join(DIGI_SCRIPT_DIR,'normalize-by-median.py')
		if savehash:
			hashfile = '.'.join([args.o, 'kh'])
			svhs = ' '.join(['--savehash',hashfile])
		else:
			svhs = ''

		if paired:
			pd='-p'
		else:
			pd=''

		commands = [norm_dir, '-C', str(cutoff), '-k', '20', '-N', args.N, '-x', args.x, pd, svhs, normfile, '2>&1']
		run_cmd(commands)

	def filter_abund():
		filter_dir = os.path.join(DIGI_SCRIPT_DIR, 'filter-abund.py')
		hashfile = '.'.join([args.o, 'kh'])
		filter_file = '.'.join([prefn, 'keep'])
		commands = [filter_dir, hashfile, filter_file, '2>&1']
		run_cmd(commands)

	def split_pe():
		split_dir = os.path.join(DIGI_SANDBOX_DIR, 'strip-and-split-for-assembly.py')
		infile = '.'.join([prefn, 'keep', 'abundfilt'])
		commands = ['python', split_dir, infile, '2>&1']
		run_cmd(commands)

	def diginorm_all():
		normalize(int(args.C)*5, args.i)
		filter_abund()
		split_pe()

		psuffix = {
			'pe':True,
			'se':False,
		}

		for endlb in ['pe', 'se']:
			normfile = '.'.join([prefn,'keep','abundfilt',endlb])
			normalize(int(args.C), normfile, paired=psuffix[endlb])

			newout = '.'.join([args.o,endlb,'fasta'])
			tmpout = '.'.join([normfile, 'keep'])
			os.rename(tmpout, newout)

		for sfx in ['kh','keep']:
			commands = ['rm', ''.join(['*.',sfx,'*'])]
			run_cmd(commands)

	parser.set_defaults(func=diginorm_all)
	args = parser.parse_args()
	prefn = os.path.split(args.i)[1]
	args.func()

if __name__ == '__main__':
	wrap()

