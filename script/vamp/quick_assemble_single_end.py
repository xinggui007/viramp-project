## AUTHOR: Yinan Wan ##
## DATE: 2013/12/11 ##
## Description: Complete pipeline for virus assembly with single-end reads ##

## Demo:  ##
##  ##

import os, re, shutil
import subprocess
import argparse

VAMP_DIR=os.path.split(os.path.abspath(__file__))[0]
TOOL_DIR=os.path.split(VAMP_DIR)[0]
UTIL_DIR=os.path.join(TOOL_DIR, 'utility')
SRC_DIR = '/mnt/src'

TRIM_RD = 'trimed_rd.fastq'
DIGINORM_PREFIX = 'afterdiginorm'
CTG_FILE = 'contigs.fa'
AMOS_PREFIX = 'draft_genome'
LINEAR_PREFIX = 'linear'
## QUAST_FOLDER = 'quast_out'
CMP_PREFIX = 'comparison'

def run_cmd(cmds, getval=True):
	DEVNULL = open(os.devnull, 'wb')
	p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
	out, err = p.communicate()
	if getval:
		return out
	
def wrap():
	
	parser = argparse.ArgumentParser(description='This script runs the whole pipeline with single-end reads')
	parser.add_argument('-l', metavar='reads.fq', help='single-end read dataset, fastq format')
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome, fasta format')
	parser.add_argument('-d', metavar='quast_out', default='quast_out', help='(optional) output directory of quast report, only need to specify when integrated into galaxy')
	parser.add_argument('-a', choices=['velvet', 'spades'], default='velvet', help='choose the de novo assembler, by default velvet') 
	parser.add_argument('-m', action='store_true', help='create one linear genome sequence')
	parser.add_argument('-c', action='store_true', help='Do not perform digital normalization')

	def quality_trim(infile, outfile):
                qual_dir = os.path.join(VAMP_DIR, 'trim_quality.py')
                commands = ['python', qual_dir, '-i', infile, '-l', '30']
                nfile = run_cmd(commands)
		f = open(outfile, 'w')
		f.write(nfile)
		f.close()	

	def diginorm(infile, predig):
                diginorm_dir = os.path.join(VAMP_DIR, 'diginorm.py')
                commands = ['python', diginorm_dir, '-i', infile, '-o', predig] 
                run_cmd(commands)

	def velvet(single_rd, fvelvet):
                velvet_dir = os.path.join(VAMP_DIR, 'velvet.py')
                khmers = ','.join(str(x) for x in range(31,72,8))
                commands = ['python', velvet_dir, '-k', khmers, '-s', single_rd, '-o', fvelvet]
                run_cmd(commands)

#	def vicuna(single_rd, fvicuna):
#                vicuna_dir = os.path.join(VAMP_DIR, 'vicuna.py')

#                commands = ['python', vicuna_dir, '-s', single_rd, '-f', 'fasta', '-o', fvicuna]
#                run_cmd(commands)

        def spades(single_rd, fspades, fmt='fasta'):
                spades_dir = os.path.join(VAMP_DIR, 'SPAdes.py')
                khmers = ','.join(str(x) for x in range(31,52,10))
        
                commands = ['python', spades_dir, '-k', khmers, '-s', single_rd, '-o', fspades, '-f', fmt]
		print ' '.join(commands)
                run_cmd(commands)      

	def AMOScmp(fctg, preamos):
                AMOScmp_dir = os.path.join(VAMP_DIR, 'AMOScmp.py')
                commands = ['python', AMOScmp_dir, '-c', fctg, '-f', args.r, '-o', preamos]
                run_cmd(commands)       

	def Quast(target, quast_folder):
                quast_dir = os.path.join(VAMP_DIR, 'quast_main.py')
                commands = ['python', quast_dir, '-r', args.r, '-t', target, '-o', quast_folder]
                run_cmd(commands)

        def SNP_det(target):
                snp_dir = os.path.join(VAMP_DIR, 'snp_detection.py')
                commands = ['python', snp_dir, '-r', args.r, '-t', target, '-o', 'variation.vcf']
                run_cmd(commands)
        
        def genomeCMP(target, cmp_prefix):
                CMP_dir = os.path.join(VAMP_DIR, 'genomeCMP.py')
                commands = ['python', CMP_dir, '-r', args.r, '-d', target, '-o', cmp_prefix, '-c']
                run_cmd(commands)

        def Circos(cinput, linput, cpref):
                circos_dir = os.path.join(VAMP_DIR,'circos.py') 
                commands = ['python', circos_dir, '-i', cinput, '-l', linput, '-o', cpref]
                run_cmd(commands) 

        def make_linear(contigs):
                linear_dir = os.path.join(VAMP_DIR, 'make_linear.py')
                commands = ['python', linear_dir, '-c', contigs, '-r', args.r, '-o', LINEAR_PREFIX]
                run_cmd(commands)


	def pipeline():
		quality_trim(args.l, TRIM_RD)	
		diginorm(TRIM_RD, DIGINORM_PREFIX)

		if args.c:
			single_rd = TRIM_RD
			fmt = 'fastq'
		else:	
			single_rd = '.'.join([DIGINORM_PREFIX, 'se', 'fasta'])	
			fmt = 'fasta'

		if args.a == 'velvet':
			velvet(single_rd, CTG_FILE)
#		elif args.a == 'vicuna':
#			vicuna(single_rd, CTG_FILE)
		elif args.a == 'spades':
			spades(single_rd, CTG_FILE, fmt)

		AMOScmp(CTG_FILE, AMOS_PREFIX)
		pretarget = '.'.join([AMOS_PREFIX, 'fasta'])

		if args.m:
			make_linear(pretarget)
#			target = '.'.join([LINEAR_PREFIX, 'fasta'])
#		else:
#			target = pretarget

		target = pretarget

		Quast(target, args.d)
                SNP_det(target)
                genomeCMP(target, CMP_PREFIX)

                cinput = '_'.join([CMP_PREFIX,'circos_input.txt'])
                linput = '_'.join([CMP_PREFIX, 'circos_links.txt'])
                Circos(cinput, linput, CMP_PREFIX)

        parser.set_defaults(func=pipeline)
        args = parser.parse_args()
        args.func()

if __name__ == '__main__':
        wrap()  

