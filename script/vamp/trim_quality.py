## AUTHOR: Yinan Wan ##
## DATE: 2013/09/04 ##
## Description: quality trimming with seqtk ##

## Demo ##
# python trim_quality.py -i input.fq -o L -l 30 #

import argparse
import os

def wrap():
	parser = argparse.ArgumentParser(description='Quality trimming with seqtk')
	parser.add_argument('-i', metavar='input.fastq', help='fastq file for quality trimming')
	parser.add_argument('-o', choices=['L','R','S'], help='Assigning read orient (left,right for paired-end, or single-end) to read name')
	parser.add_argument('-l', metavar='30', help='Maximumly trim down to INT bp')

	SUFFIX = {
		'L':'#0/1',
		'R':'#0/2',
		'S':'',
	}

	def trimming():
		seqtk_cmds = ['seqtk','trimfq', '-l', args.l, args.i]
		seqtk_cmd = ' '.join(seqtk_cmds)

		bioawk_cmds = ['bioawk', '-c', 'fastx', "'{print $0}'"]
		bioawk_cmd = ' '.join(bioawk_cmds)

		awk_cmds = ['awk', '-v', 'var='+SUFFIX[args.o], "'BEGIN{OFS=\"\\n\"}{print \"@\"$1var,$2,\"+\",$3}'"]
		awk_cmd = ' '.join(awk_cmds)

		command = '|'.join([seqtk_cmd, bioawk_cmd, awk_cmd])	
		os.system(command)

	parser.set_defaults(func=trimming)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
