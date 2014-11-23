## AUTHOR: Yinan Wan ##
## DATE: 11/22/2014 ##
## DESCRIPTION BWA Wrapper for alignment ##

## DEMO python bwa_wrapper.py -p -1 left.fastq -2 right.fastq -r refseq.fa -m normal##


import sys, os, re, shutil
import argparse
import subprocess
import string
import random

def run_cmds(cmds, getval=False):
        DEVNULL = open(os.devnull, 'wb')
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
        out, err = p.communicate()
        if getval:
                return out
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: 
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def wrap():
	if len(sys.argv)<2:
                print "Try '-h' option for more information"
                exit(1)

        parser = argparse.ArgumentParser(description="This script run genome alignment using bwa")
	parser.add_argument('-l', metavar='read_1.fq', help='read-1 from paired-end sequencing, fastq format')
	parser.add_argument('-r', metavar='read_2.fq', help='read-2 from paired-end sequencing, fastq format, if paired-end')
	parser.add_argument('-p', action="store_true", help="Paired-end reads")
	parser.add_argument('-g', metavar="refseq.fa", help='reference genome in fasta format')	
	parser.add_argument('-m', choices=['normal', 'mem'],default='normal', help="bwa alignment mode, 'normal' is using aln+sampe/samse, 'mem' is using bwa-mem")
	parser.add_argument('-d', metavar="bamfiles", help="result directory, for galaxy usage")
	prfx = '_'.join([id_generator(), 'genome'])
	maindir = os.getcwd()
	genome_idx = os.path.join(maindir, prfx)
	def bwa_index():

		command = ['bwa', 'index', '-p', genome_idx, args.g]	
		run_cmds(command)

	def bwa_normal():
		command_1 = ['bwa', 'aln', genome_idx, args.l]
		sai_1 = run_cmds(command_1, getval=True)
		f = open('rd_1.sai', 'wb')
		f.write(sai_1)
		f.close()

		if args.p:
			command_2 = ['bwa', 'aln', genome_idx, args.r]
			sai_2 = run_cmds(command_2, getval=True)
			f = open('rd_2.sai', 'wb')
			f.write(sai_2)
			f.close()

			command_sam = ['bwa', 'sampe', genome_idx, 'rd_1.sai', 'rd_2.sai', args.l, args.r]
			sam_p = run_cmds(command_sam, getval=True)
			f = open('aligned.sam', 'wb')
			f.write(sam_p)
			f.close()

		else:
			command_sam = ['bwa', 'samse', '-f', 'aligned.sam', genome_idx, 'rd_1.sai', args.l]
			sam_s = run_cmds(command_sam, getval=True)

	def bwa_mem():
		if args.p:
			command_p = ['bwa', 'mem', genome_idx, args.l, args.r]
		else:
			command_p = ['bwa', 'mem', genome_idx, args.l]

		fsam = run_cmds(command_p, getval=True)
		f = open('aligned.sam', 'wb')	
		f.write(fsam)
		f.close()


	def sam2bam():
		command = ['samtools', 'view', '-Sb', 'aligned.sam']
		fbam = run_cmds(command, getval=True)
		f = open('aligned.bam', 'wb')
		f.write(fbam)
		f.close()

		command_sort=['samtools', 'sort', 'aligned.bam', 'aligned.sorted']
		run_cmds(command_sort)
		
		command_index = ['samtools', 'index', 'aligned.sorted.bam']
		run_cmds(command_index)
		
	
	def all_proc():
		bwa_index()
		if args.m == 'normal':
			bwa_normal()
		else:
			bwa_mem()
		sam2bam()

	parser.set_defaults(func=all_proc)
        args = parser.parse_args()	
	args.func()

if __name__ == '__main__':
	wrap()
