
## AUTHOR: Yinan Wan ##
## DATE: 2013/09/04 ##
## Description: Complete pipeline for virus assembling ##

## Demo ##
# python quick_assemble.py -l read_1.fq -e read_2.fq -r refseq.fa -d output_dir#
import os,re
import argparse
import shutil

def run_cmd(cmds):
	command = ' '.join(cmds)
	os.system(command)

VAMP_DIR=os.path.split(os.path.abspath(__file__))[0]
TOOL_DIR=os.path.split(VAMP_DIR)[0]
UTIL_DIR=os.path.join(TOOL_DIR, 'utility')
SRC_DIR = '/mnt/src'

READ_1 = 'left.fastq'
READ_2 = 'right.fastq'
MERGE_FILE = 'after_merge.fq'
CTG_FILE = 'contigs.fa'
DIGINORM_PREFIX = 'afterdiginorm'
SSPACE_PREFIX = 'sspace'
AMOS_PREFIX = 'draft_genome'
QUAST_FOLDER = 'quast_out'
CMP_PREFIX='comparison'

def wrap():

	parser = argparse.ArgumentParser(description="This script runs the whole pipeline")
	parser.add_argument('-l', metavar='read_1.fq', help='read-1 from paired-end sequencing, fastq format')
	parser.add_argument('-e', metavar='read_2.fq', help='read-2 from paired-end sequencing, fastq format')
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome, fasta format')
	parser.add_argument('-d', metavar='quast_out', default='quast_out', help='(optional), output directory for quast report, only necessary for Galaxy integration')
	parser.add_argument('-a', choices=['velvet', 'vicuna', 'spades'], default='velvet', help='choose the de novo assembler, by default velvet')	
	parser.add_argument('-s', action='store_true', help='use SSPACE to do de novo schaffolding and quality control')

	def quality_trim(infile, outfile, ort_label):
		qual_dir = os.path.join(VAMP_DIR, 'trim_quality.py')
		commands = ['python', qual_dir, '-i', infile, '-o', ort_label, '-l', '30', '>', outfile]
		print 'Trimming', infile, '...'
		run_cmd(commands)

	def merge_pair(rd1, rd2, fmerged):
		merge_dir = os.path.join(UTIL_DIR, 'merge_pe.sh')
		commands = [merge_dir, '-l', rd1, '-e', rd2, '>', fmerged ]
		print 'Merging', rd1, 'and', rd2, '...' 
		run_cmd(commands)

	def diginorm(fmerged, predig):
		diginorm_dir = os.path.join(VAMP_DIR, 'diginorm.py')
		commands = ['python', diginorm_dir, '-i', fmerged, '-o', predig, '-C', '10', '-x', '1e8', '-p']	
		run_cmd(commands)

	def velvet(paired_rd, single_rd, fvelvet):
		velvet_dir = os.path.join(VAMP_DIR, 'velvet.py')
		khmers = ','.join(str(x) for x in range(31,72,5))
		# paired_rd = '.'.join([predig,'pe','fasta'])
		# single_rd = '.'.join([predig, 'se', 'fasta'])
		commands = ['python', velvet_dir, '-k', khmers, '-p', paired_rd, '-s', single_rd, '-o', fvelvet, '-f', 'fasta']
		run_cmd(commands)

	def vicuna(paired_rd, single_rd, fvicuna):
		vicuna_dir = os.path.join(VAMP_DIR, 'vicuna.py')
		# paired_rd = '.'.join([predig,'pe','fasta'])
                # single_rd = '.'.join([predig, 'se', 'fasta'])

		commands = ['python', vicuna_dir, '-p', paired_rd, '-s', single_rd, '-f', 'fasta', '-o', fvicuna]
		run_cmd(commands)

	def spades(paired_rd, single_rd, fspades):
		spades_dir = os.path.join(VAMP_DIR, 'spades.py')
		khmers = ','.join(str(x) for x in range(31,72,5))
		# paired_rd = '.'.join([predig,'pe','fasta'])
                # single_rd = '.'.join([predig, 'se', 'fasta'])
	
		commands = ['python', spades_dir, '-k', khmers, '-p', paired_rd, '-s', single_rd, '-o', fspades]
		run_cmd(commands)	

	def SSPACE(fctg, presspace):
		sspace_dir = os.path.join(SRC_DIR,'SSPACE-BASIC-2.0_linux-x86_64', 'SSPACE_Basic_v2.0.pl')
		commands = [sspace_dir, '-l', 'library.txt', '-s', fctg, '-b', presspace]	
		run_cmd(commands)

	def AMOScmp(fctg, preamos, paired_rd):
		AMOScmp_dir = os.path.join(VAMP_DIR, 'AMOScmp.py')
		# paired_rd = '.'.join([predig, 'pe', 'fasta'])
#		ctg_file = '.'.join([SSPACE_PREFIX, 'final.scaffolds.fasta'])
		commands = ['python', AMOScmp_dir, '-r', '-c', fctg, '-p', paired_rd, '-f', args.r, '-o', preamos]
		run_cmd(commands)	
		
	def Quast(target, quast_folder):
		quast_dir = os.path.join(VAMP_DIR, 'quast_main.py')
		# target = '.'.join([AMOS_PREFIX,'fasta'])
		commands = ['python', quast_dir, '-r', args.r, '-t', target, '-o', quast_folder]
		run_cmd(commands)

	def SNP_det(target):
		snp_dir = os.path.join(VAMP_DIR, 'snp_detection.py')
		# target = '.'.join([AMOS_PREFIX,'fasta'])
		commands = ['python', snp_dir, '-r', args.r, '-t', target, '-o', 'variation.vcf']
		run_cmd(commands)
	
	def genomeCMP(target, cmp_prefix):
		CMP_dir = os.path.join(VAMP_DIR, 'genomeCMP.py')
		# target = '.'.join([AMOS_PREFIX, 'fasta'])
		commands = ['python', CMP_dir, '-r', args.r, '-d', target, '-s', 'target', '-o', cmp_prefix, '-c']
		run_cmd(commands)

	def Circos(cinput, linput, cpref):
		circos_dir = os.path.join(VAMP_DIR,'circos.py')	
		# cinput = '_'.join([CMP_PREFIX,'circos_input.txt'])
		# linput = '_'.join([CMP_PREFIX, 'circos_links.txt'])
		commands = ['python', circos_dir, '-i', cinput, '-l', linput, '-o', cpref]
		run_cmd(commands) 

	def pipeline():
		quality_trim(args.l, READ_1, 'L')
		quality_trim(args.e, READ_2, 'R')
		merge_pair(READ_1, READ_2, MERGE_FILE)
		diginorm(MERGE_FILE, DIGINORM_PREFIX)

		single_rd = '.'.join([DIGINORM_PREFIX, 'se', 'fasta'])
		paired_rd = '.'.join([DIGINORM_PREFIX,'pe','fasta'])

		if args.a == 'velvet':
			velvet(paired_rd, single_rd, CTG_FILE)
		elif args.a == 'vicuna':
			vicuna(paired_rd, single_rd, CTG_FILE)
		elif args.a == 'spades':
			spades(paired_rd, single_rd, CTG_FILE)

		if args.s:
			SSPACE(CTG_FILE, SSPACE_PREFIX)
			fctg = '.'.join([SSPACE_PREFIX, 'final.scaffolds.fasta'])
		else:
			fctg = CTG_FILE

		AMOScmp(fctg, AMOS_PREFIX, paired_rd)

		target = '.'.join([AMOS_PREFIX,'fasta'])

		Quast(target, QUAST_FOLDER)
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
