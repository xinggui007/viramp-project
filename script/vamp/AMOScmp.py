## AUTHOR: Yinan Wan ##
## DATE: 2013/09/25 ##
# Description: Run the AMOScmp pipeline #

## Demo ##
#  #

import os, re, shutil
import argparse
import subprocess
import string
import random

def run_cmds(cmds, getval=True):
	DEVNULL = open(os.devnull, 'wb')
	p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
	out, err = p.communicate()
	if getval:
		return out

def purge(dir, pattern):
	for f in os.listdir(dir):
		if re.search(pattern, f):
			try:
				os.remove(os.path.join(dir,f))
			except:
				shutil.rmtree(os.path.join(dir,f))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

def wrap():
	parser = argparse.ArgumentParser(description='Running the AMOScmp pipeline')
	parser.add_argument('-c', metavar='contigs.fa', help='Contigs file, fasta format')
	parser.add_argument('-p', metavar='reads.pe.fa',help='(optional) Paired-end reads file, fasta or fastq format')
	parser.add_argument('-f', metavar='refseq.fa', help='Reference sequence, fasta format')
	parser.add_argument('-o', metavar='AMOSoutput', default='AMOSouput', help='Output prefix, by default is AMOSoutput')

	def AMOSpipeline():
		PREFIX = id_generator()
		INPUT = 'combined_seq.fa'
		AFG = '.'.join([PREFIX,'afg'])

		shutil.copyfile(args.c, INPUT)
		if args.p:
			preads = open(args.p, 'rb')
			cbd = open(INPUT,'a')
			cbd.write(preads.read())
			cbd.close()
			preads.close()

		def formatting():
			commands = ['toAmos', '-s', INPUT, '-o', AFG]
			run_cmds(commands, getval=False)

		def go_AMOScmp():
			commands = ['AMOScmp', '-D', '='.join(['TGT', AFG]), '-D', '='.join(['REF', args.f]), PREFIX]
			run_cmds(commands)
	
		def clean():
			formatting()
			go_AMOScmp()
			fasta = '.'.join([PREFIX, 'fasta']) 
			FOUTPUT = '.'.join([args.o, 'fasta'])	
			os.rename(fasta, FOUTPUT)
			os.remove('combined_seq.fa')
			purge('./', PREFIX)	
		clean()

	parser.set_defaults(func=AMOSpipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()	
