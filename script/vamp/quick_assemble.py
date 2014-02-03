
## AUTHOR: Yinan Wan ##
## DATE: 2013/09/04 ##
## Description: Complete pipeline for virus assembling ##

## Demo ##
# python quick_assemble.py -l read_1.fq -e read_2.fq -r refseq.fa -d output_dir#
import os,re,sys
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
LINEAR_PREFIX = 'linear'
QUAST_FOLDER = 'quast_out'
CMP_PREFIX='comparison'

def wrap():
	if len(sys.argv)<2:
		print "Try '-h' option for more information"
		exit(1)

	parser = argparse.ArgumentParser(description="This script runs the whole pipeline")
	parser.add_argument('-l', metavar='read_1.fq', help='read-1 from paired-end sequencing, fastq format')
	parser.add_argument('-e', metavar='read_2.fq', help='read-2 from paired-end sequencing, fastq format')
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome, fasta format')
	parser.add_argument('-d', metavar='quast_out', default='quast_out', help='(optional), output directory for quast report, only necessary for Galaxy integration')
	parser.add_argument('-a', choices=['velvet', 'vicuna', 'spades'], default='velvet', help='choose the de novo assembler, by default velvet')	
	parser.add_argument('-i', metavar='INT', default='350', help='inserstion size of paired end reads, by default is 350')
	parser.add_argument('-k', metavar='35,45,55,65', default='35,45,55,65', help='k-mer set used in de novo assembly')
	parser.add_argument('-c', action='store_true', help='Do not perform digital normalization')
	parser.add_argument('-g', action='store_true', help='Do not create Circos graph for contig alignment visualization')
	parser.add_argument('-m', action='store_true', help='create one linear genome sequence')

	def quality_trim(infile, outfile):
		qual_dir = os.path.join(VAMP_DIR, 'trim_quality.py')
		commands = ['python', qual_dir, '-i', infile, '-l', '30', '>', outfile]
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

	def velvet(fvelvet, paired_rd, single_rd=None):
		velvet_dir = os.path.join(VAMP_DIR, 'velvet.py')
		khmers = args.k
		if single_rd: 
			commands = ['python', velvet_dir, '-k', khmers, '-p', paired_rd, '-s', single_rd, '-o', fvelvet, '-f', 'fasta']
		else:
			commands = ['python', velvet_dir, '-k', khmers, '-p', paired_rd, '-o', fvelvet, '-f', 'fasta']
		run_cmd(commands)

	def vicuna(fvicuna, paired_rd, single_rd=None):
		vicuna_dir = os.path.join(VAMP_DIR, 'vicuna.py')

		if single_rd:
			commands = ['python', vicuna_dir, '-p', paired_rd, '-s', single_rd, '-f', 'fasta', '-o', fvicuna]
		else:
			commands = ['python', vicuna_dir, '-p', paired_rd, '-f', 'fasta', '-o', fvicuna]	
		run_cmd(commands)

	def spades(fspades, paired_rd, single_rd=None):
		spades_dir = os.path.join(VAMP_DIR, 'spades.py')
		khmers = ','.join(str(x) for x in range(31,72,5))
		if single_rd:	
			commands = ['python', spades_dir, '-k', khmers, '-p', paired_rd, '-s', single_rd, '-o', fspades]
		else:
			commands = ['python', spades_dir, '-k', khmers, '-p', paired_rd, '-o', fspades]
		run_cmd(commands)	

	def AMOScmp(fctg, preamos, paired_rd):
		AMOScmp_dir = os.path.join(VAMP_DIR, 'AMOScmp.py')
		commands = ['python', AMOScmp_dir, '-c', fctg, '-p', paired_rd, '-f', args.r, '-o', preamos]
		run_cmd(commands)	
	
	def SSPACE(fctg, RD1, RD2, INS, FMT, PREFIX):
		sspace_dir = os.path.join(VAMP_DIR, 'SSPACE.py')
		commands = ['python', sspace_dir, '-c', fctg, '-l', RD1, '-e', RD2, '-i', INS, '-f', FMT, '-o', PREFIX]
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
		quality_trim(args.l, READ_1)
		quality_trim(args.e, READ_2)
		merge_pair(READ_1, READ_2, MERGE_FILE)


		if args.c:
			paired_rd = MERGE_FILE
                        single_rd = None
		else:
			diginorm(MERGE_FILE, DIGINORM_PREFIX)
			single_rd = '.'.join([DIGINORM_PREFIX, 'se', 'fasta'])
			paired_rd = '.'.join([DIGINORM_PREFIX,'pe','fasta'])

		if args.a == 'velvet':
			velvet(CTG_FILE, paired_rd, single_rd)
		elif args.a == 'vicuna':
			vicuna(CTG_FILE, paired_rd, single_rd)
		elif args.a == 'spades':
			spades(CTG_FILE, paired_rd, single_rd)

		AMOScmp(CTG_FILE, AMOS_PREFIX, paired_rd)

		AMOS_CTG = '.'.join([AMOS_PREFIX,'fa'])

		SSPACE(AMOS_CTG, READ_1, READ_2, args.i, 'fastq', SSPACE_PREFIX)

		pretarget = '.'.join([SSPACE_PREFIX,'fasta'])
		if args.m:
			make_linear(pretarget)
			target = '.'.join([LINEAR_PREFIX, 'fasta'])
		else:
			target = pretarget

		Quast(target, QUAST_FOLDER)
		SNP_det(target)
		genomeCMP(target, CMP_PREFIX)

		cinput = '_'.join([CMP_PREFIX,'circos_input.txt'])
		linput = '_'.join([CMP_PREFIX, 'circos_links.txt'])
	
		if not args.g:	
			Circos(cinput, linput, CMP_PREFIX)

	parser.set_defaults(func=pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()	
