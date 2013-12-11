## AUTHOR: Yinan Wan ##
## DATE: 2013/11/25 ##
## Description: using SSPACE to check and extend contigs ##

## Demo ##
#  #

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
	parser.add_argument('-i', metavar='INT', default='350', help='inserstion size of the paired end reads, by default 250')
	parser.add_argument('-o', metavar='sspace_out', default='sspace_out', help='prefix of the output, by default sspace_out')

	def libfile():
		ORIENT = 'FR'
		ERR = '0.25'
		fleft = '.'.join([PREFIX, 'left', args.f])
		fright = '.'.join([PREFIX, 'right', args.f])
		shutil.copyfile(RD1, fleft)
		shutil.copyfile(RD2, fright)
		f = open('library.txt', 'wb')
		f.write(' '.join(['Lib1', fleft, fright, args.i, ERR, ORIENT]))
		f.close()

	def run_SSPACE():
		commands = [SSPACE_DIR, '-l', 'library.txt', '-s', CTG, '-x', '1', '-b', PREFIX]
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
