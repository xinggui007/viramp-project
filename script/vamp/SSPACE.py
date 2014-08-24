## AUTHOR: Yinan Wan ##
## DATE: 2013/11/25 ##
## Description: using SSPACE to check and extend contigs ##

## Demo ##
# python SSPACE.py -c contigs.fa -l left.fastq -e right.fastq -f fastq -i 350  #

import re, os
import argparse
import shutil, errno

def run_cmd(cmds):
	command = ' '.join(cmds)
	os.system(command)

SRC_DIR = '/mnt/src'
SSPACE_DIR = os.path.join(SRC_DIR,'SSPACE-BASIC-2.0_linux-x86_64', 'SSPACE_Basic_v2.0.pl') 

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: 
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def purge(dir, pattern):
        for f in os.listdir(dir):
                if re.search(pattern, f):
                        try:
                                os.remove(os.path.join(dir,f))
                        except:
                                shutil.rmtree(os.path.join(dir,f))

def wrap():
	parser = argparse.ArgumentParser(description="Using SSPACE to extend contigs and close gaps")
	parser.add_argument('-c', metavar='contigs.fa', help='contigs to be extended')
	parser.add_argument('-l', metavar='left.fastq', help='paired end reads set-1')
	parser.add_argument('-e', metavar='right.fastq', help='paired end reads set-2')
	parser.add_argument('-f', choices=['fasta', 'fastq'], default='fasta', help='format of reads set, by default "fasta"')
	parser.add_argument('-i', metavar='INT', default='350', help='inserstion size of the paired end reads, by default 350')
	parser.add_argument('-r', metavar='FLOAT', default=0.25, help='error rate between expected and observed insertion size, by default 0.25')
	parser.add_argument('-t', choices=['FF', 'FR', 'RF', 'RR'], default='FR', help='Orientation of the paired-reads, F indicates forward; R indicates reverse; by default FR')
	parser.add_argument('-o', metavar='sspace_out', default='sspace_out', help='prefix of the output, by default sspace_out')

	parser.add_argument('-x', choices=['0','1'], default='1', help='whether to execute extension mode (yes=1, np=0), ignoring extension will be much faster, but may miss some information; by default is 1')
	parser.add_argument('-m', metavar='INT', default='32', help='Minimum number of overlapping bases with the seed/contig during overhang consensus build up (default -m 32)')
	parser.add_argument('-b', metavar='INT', default='20', help='Minimum number of reads needed to call a base during an extension (default -o 20)')
	parser.add_argument('-z', metavar='INT', default='0', help='Minimum contig length used for scaffolding. Filters out contigs that are below -z, default is 0')
	parser.add_argument('-k', metavar='INT', default='5', help='Minimum number of read pairs to compute scaffold, default is 5')
	parser.add_argument('-s', metavar='INT', default='15', help='Minimum overlap required between contigs to merge adjacent contigs in a scaffold; default is 15')

	def libfile():
		ORIENT = args.t 
		ERR = args.r
		fleft = '.'.join([PREFIX, 'left', args.f])
		fright = '.'.join([PREFIX, 'right', args.f])
		shutil.copyfile(RD1, fleft)
		shutil.copyfile(RD2, fright)
		f = open('library.txt', 'wb')
		f.write(' '.join(['Lib1', fleft, fright, str(args.i), str(ERR), ORIENT]))
		f.close()

	def run_SSPACE():
		commands = [SSPACE_DIR, '-l', 'library.txt', '-s', CTG, '-x', args.x, '-b', PREFIX, '-m', args.m, '-o', args.b, '-z', args.z, '-k', args.k, '-n', args.s]
		run_cmd(commands)

	def clean():
		maindir = os.getcwd()
		workdir = 'tmpsspace'
		newdir = os.path.join(maindir, workdir)
		mkdir_p(newdir)
		os.chdir(newdir)
		libfile()
		run_SSPACE()
		os.chdir(maindir)
		
		orgout = '.'.join([args.o, 'tmp', 'final.scaffolds.fasta'])
		finout = '.'.join([args.o, 'fasta'])

		orgpath = os.path.join(newdir, orgout)
		finpath = os.path.join(maindir, finout)

		os.rename(orgpath, finpath)
		purge('./', workdir)

	parser.set_defaults(func=clean)
	args = parser.parse_args()

	PREFIX = '.'.join([args.o, 'tmp'])
	RD1 = os.path.abspath(args.l)
	RD2 = os.path.abspath(args.e)
	CTG = os.path.abspath(args.c)

	args.func()

if __name__ == '__main__':
	wrap()	
