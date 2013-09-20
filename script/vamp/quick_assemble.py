
## AUTHOR: Yinan Wan ##
## DATE: 2013/09/04 ##
## Description: Complete pipeline for virus assembling ##

## Demo ##
# #
import os,re
import argparse
import shutil

def run_cmd(cmds):
	command = ' '.join(cmds)
	os.system(command)

TOOL_DIR='/mnt/galaxy/galaxy-dist/tools/'
VAMP_DIR=os.path.join(TOOL_DIR, 'vamp')
UTIL_DIR=os.path.join(TOOL_DIR, 'utility')
READ_1 = 'left.fastq'
READ_2 = 'right.fastq'
MERGE_FILE = 'after_merge.fq'
VELVET_FILE = 'velvet_contigs.fa'
DIGINORM_PREFIX = 'afterdiginorm'
AMOS_PREFIX = 'draft_genome'
QUAST_FOLDER = 'quast_out'
CMP_PREFIX='comparison'

def wrap():

	parser = argparse.ArgumentParser(description="This script runs the whole pipeline")
	parser.add_argument('-l', metavar='read_1.fq', help='read-1 from paired-end sequencing, fastq format')
	parser.add_argument('-e', metavar='read_2.fq', help='read-2 from paired-end sequencing, fastq format')
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome, fasta format')
	parser.add_argument('-d', metavar='quast_out', default='quast_out', help='(optional), output directory for quast report, only necessary for Galaxy integration')

	def quality_trim(infile, outfile, ort_label):
		qual_dir = os.path.join(VAMP_DIR, 'trim_quality.py')
		commands = ['python', qual_dir, '-i', infile, '-o', ort_label, '-l', '30', '>', outfile]
		print 'Trimming', infile, '...'
		run_cmd(commands)

	def merge_pair():
		merge_dir = os.path.join(UTIL_DIR, 'merge_pe.sh')
		commands = [merge_dir, '-l', READ_1, '-e', READ_2, '>', MERGE_FILE ]
		print 'Merging', READ_1, 'and', READ_2, '...' 
		run_cmd(commands)

	def diginorm():
		diginorm_dir = os.path.join(VAMP_DIR, 'diginorm.py')
		commands = ['python', diginorm_dir, '-i', MERGE_FILE, '-o', DIGINORM_PREFIX, '-C', '10', '-x', '1e8', '-p']	
		run_cmd(commands)

	def velvet():
		velvet_dir = os.path.join(VAMP_DIR, 'velvet.py')
		khmers = ','.join(str(x) for x in range(31,72,5))
		paired_rd = '.'.join([DIGINORM_PREFIX,'pe','fasta'])
		single_rd = '.'.join([DIGINORM_PREFIX, 'se', 'fasta'])
		commands = ['python', velvet_dir, '-k', khmers, '-p', paired_rd, '-s', single_rd, '-o', VELVET_FILE, '-f', 'fasta']
		run_cmd(commands)

	def AMOScmp():
		AMOScmp_dir = os.path.join(VAMP_DIR, 'AMOScmp.sh')
		paired_rd = '.'.join([DIGINORM_PREFIX, 'pe', 'fasta'])
		commands = [AMOScmp_dir, '-r', '-c', VELVET_FILE, '-p', paired_rd, '-f', args.r, '-o', AMOS_PREFIX]
		run_cmd(commands)	
		
	def Quast():
		quast_dir = os.path.join(VAMP_DIR, 'quast_main.py')
		target = '.'.join([AMOS_PREFIX,'fasta'])
		commands = ['python', quast_dir, '-r', args.r, '-t', target, '-o', QUAST_FOLDER]
		run_cmd(commands)

	def SNP_det():
		snp_dir = os.path.join(VAMP_DIR, 'snp_detection.py')
		target = '.'.join([AMOS_PREFIX,'fasta'])
		commands = ['python', snp_dir, '-r', args.r, '-t', target, '-o', 'variation.vcf']
		run_cmd(commands)
	
	def genomeCMP():
		CMP_dir = os.path.join(VAMP_DIR, 'genomeCMP.py')
		target = '.'.join([AMOS_PREFIX, 'fasta'])
		commands = ['python', CMP_dir, '-r', args.r, '-d', target, '-s', 'target', '-o', CMP_PREFIX, '-c']
		run_cmd(commands)

	def Circos():
		circos_dir = os.path.join(VAMP_DIR,'circos.py')	
		cinput = '_'.join([CMP_PREFIX,'circos_input.txt'])
		linput = '_'.join([CMP_PREFIX, 'circos_links.txt'])
		commands = ['python', circos_dir, '-i', cinput, '-l', linput, '-o', CMP_PREFIX]
		run_cmd(commands) 

	def pipeline():
		quality_trim(args.l, READ_1, 'L')
		quality_trim(args.e, READ_2, 'R')
		merge_pair()
		diginorm()
		velvet()
		AMOScmp()
		Quast()
		SNP_det()
		genomeCMP()
		Circos()

	parser.set_defaults(func=pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()	
