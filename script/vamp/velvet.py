## AUTHOR: Yinan Wan ##
## DATE: 2013/08/30 ##
## Description: Velvet wrap in Galaxy ##
## Demo ##
# python velvet.py -k 31,41,51 -p pair.fq -s single.fq -f fastq -o velvet_contigs.fa#

import os, re
import shutil
import argparse

def run_cmd(cmds):
	command = ' '.join(cmds)
	os.system(command)

def wrap():
	parser = argparse.ArgumentParser(description='This script runs velvet with a series of kmers and output a combined fasta files containing all the assembled contigs')
	parser.add_argument('-k', metavar='khmers', help='k-mers used in velvet assembling, multiple k-mers should be separated by commas, e.x 21,31,41,51')
	parser.add_argument('-p', metavar='paired-end file', default=str(), help='file with paired-end reads')
	parser.add_argument('-s', metavar='single-end file', default=str(), help='file with single-end reads')
	parser.add_argument('-f', choices=['fasta', 'fastq'], default='fasta', help="file format of input")	
	parser.add_argument('-o', metavar='output', default='velvet_contigs.fa', help='output file name, by default velvet-contigs.fa')

	def run_velvet():
		allfasta = open('all_contigs.fa','a')
		khmer_ary = args.k.split(',')
		khmer = ' '.join(khmer_ary)
		
		sd = str()
		pd = str()

		if len(args.p) > 0:
			pd = ' '.join(['-shortPaired', args.p])
		if len(args.s) > 0:
			sd = ' '.join(['-short', args.s])

		for i in khmer_ary:

			dirname = '.'.join(['hsv','beforedigipe',i])
			commands_1 = ['velveth', dirname, i, '-'+args.f, pd, sd ]
			run_cmd(commands_1)

			commands_2 = ['velvetg', dirname, '-exp_cov', 'auto', '-ins_length', '250', '-cov_cutoff', 'auto', '-scaffolding', 'yes' ]
			run_cmd(commands_2)

			## append to bigfa
			ctg_path = os.path.join(dirname, 'contigs.fa')
			ctg = open(ctg_path, 'rb')
			allfasta.write(ctg.read())
			ctg.close()

			shutil.rmtree(dirname)
	
		allfasta.close()		
		## rename contigs
		allfasta = open('all_contigs.fa','rb')
		ctgNum=0
		rename_fa = open(args.o, 'w')
		for line in allfasta.readlines():
			if re.match('^>', line):
				ctgNum = ctgNum+1
				rename_fa.write('>contig'+str(ctgNum)+'\n')
			else:
				rename_fa.write(line)
		rename_fa.close()

		os.remove('all_contigs.fa')	

		
	parser.set_defaults(func=run_velvet)
	args = parser.parse_args()
	args.func()

if __name__ == "__main__":
	wrap()	
