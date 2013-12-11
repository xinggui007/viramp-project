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
	# parser.add_argument('-o', choices=['L','R','S'], help='Assigning read orient (left,right for paired-end, or single-end) to read name')
	parser.add_argument('-l', metavar='30', default='30', help='Maximumly trim down to INT bp')

	SUFFIX = {
		'L':'/1',
		'R':'/2',
		'S':'',
	}

	def trimming():
		seqtk_cmds = ['seqtk','trimfq', '-l', args.l, args.i]
		seqtk_cmd = ' '.join(seqtk_cmds)

		os.system(seqtk_cmd)

	parser.set_defaults(func=trimming)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
