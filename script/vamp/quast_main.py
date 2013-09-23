## AUTHOR: Yinan Wan ##
## DATE: 2013/09/03 ##
## Description: This script runs the quast to evaluate the assemblings and generate variation file ##

## Demo ##
# python quast_main.py -r refseq.fa -t amos_assemblings.fa -o quast_out#

import os, re
import argparse

GALAXY_DIR = '/mnt/galaxy/galaxy-dist'
TOOL_DIR= os.path.join(GALAXY_DIR, 'tools')
VAMP_DIR=os.path.join(TOOL_DIR,'vamp')
QUAST_DIR='/mnt/src/quast-2.2'

def run_cmd(cmds):
	command = ' '.join(cmds)
	os.system(command)

def wrap():

	parser = argparse.ArgumentParser(description='Quast report')
	parser.add_argument('-r', metavar='reference-genme', help='reference genome')
	parser.add_argument('-t', metavar='target files', help='files for assessment, if more than one, separated by commas without spaces, e.x seq1.fa,seq2.fa,seq3.fa')
	parser.add_argument('-o', metavar='output', default='quast_out', help='output directory, by default write to quast_out')

	def main_quast():
		targets = args.t.split(',')
		quast_path = os.path.join(QUAST_DIR, 'quast.py')	
		commands = [quast_path, '-R', args.r, '-o', args.o, ' '.join(targets) ]
		run_cmd(commands)

	def simple_html():
		html_path = os.path.join(VAMP_DIR, 'quast_html.py')
		commands = ['python', html_path, args.o ]
		run_cmd(commands)

	def all_cmd():
		main_quast()
		simple_html()

	parser.set_defaults(func=all_cmd)
	args = parser.parse_args()
	args.func()

if __name__ == "__main__":
	wrap()
