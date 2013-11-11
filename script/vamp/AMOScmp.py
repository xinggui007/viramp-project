## AUTHOR: Yinan Wan ##
## DATE: 2013/09/25 ##
# Description: Run the AMOScmp pipeline #

## Demo ##
#  #

import os, re, shutil
import argparse
import subprocess

def run_cmds(cmds, getval=True):
	DEVNULL = open(os.devnull, 'wb')
	p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
	out, err = p.communicate()
	if getval:
		return out

def wrap():
	parser = argparse.ArgumentParser(description='Running the AMOScmp pipeline')
	parser.add_argument('-r', action="store_true", help='Randomly place repetitive reads into one of their copy locations if they cannot be placed via mate-pair info')
	parser.add_argument('-c', metavar='contigs.fa', help='Contigs file, fasta format')
	parser.add_argument('-p', metavar='reads.pe.fa',help='Paired-end reads file, fasta or fastw format')
	parser.add_argument('-f', metavar='refseq.fa', help='Reference sequence, fasta format')
	parser.add_argument('-o', metavar='AMOSoutput', default='AMOSouput', help='Output prefix, by default is AMOSoutput')

	def AMOSpipeline():
		PREFIX='_'.join([args.o, 'tmp'])
		INPUT = 'combined_seq.fa'
		AFG = '.'.join([PREFIX,'afg'])
		BANK = '.'.join([PREFIX,'bnk'])
		SEQ='.'.join([PREFIX, 'seq'])
		ALIGN='.'.join([PREFIX, 'delta'])
		LAYOUT='.'.join([PREFIX, 'layout'])
		CONFLICT = '.'.join([PREFIX, 'conflict'])
		CONTIG = '.'.join([PREFIX, 'contig'])
		FASTA = '.'.join([PREFIX, 'fasta'])
		FOUTPUT = '.'.join([args.o, 'fasta'])

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
	
		def banks():
			commands = ['bank-transact','-c','-z','-b',BANK, '-m', AFG]
			run_cmds(commands, getval=False)

		def dump():
			commands = ['dumpreads', BANK]
			seqs = run_cmds(commands)
			nseq = open(SEQ,'wb')
			nseq.write(seqs)
			nseq.close()

		def rnucmer():
			commands = ['nucmer', '--maxmatch', '-p', PREFIX, args.f, SEQ]
			run_cmds(commands, getval=False)

		def layout():
			if args.r:
				rep='-r'
			else:
				rep=''
			commands = ['casm-layout',rep, '-U', LAYOUT, '-C', CONFLICT, '-b', BANK, ALIGN]
			run_cmds(commands, getval=False)

		def consensus():
			commands = ['make-consensus', '-f', '-o', '10', '-b', BANK]
			fasta = run_cmds(commands)
			f = open(FASTA, 'wb')
                        f.write(fasta)
                        f.close()

		def mcontigs():
			commands = ['bank2contig', BANK]
			CONTIG = run_cmds(commands)
	
		def tfasta():
			commands = ['bank2fasta', '-b', BANK]
			fasta = run_cmds(commands)
			f = open(FASTA, 'wb')
			f.write(fasta)
			f.close()

		def clean():
			formatting()
			banks()
			dump()
			rnucmer()
			layout()
			consensus()
			mcontigs()
			
			os.rename(FASTA, FOUTPUT)
			os.remove(INPUT)
		
		clean()

	parser.set_defaults(func=AMOSpipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()	
