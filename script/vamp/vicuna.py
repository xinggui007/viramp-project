## AUTHOR: Yinan Wan ##
## DATE: 2013/09/30 ##
## Description: Run the VICUNA de novo assembler ##

## DEMO ##
# python vicuna.py -p paired.fa -s single.fa -f fasta -o outfile.fa #

import sys, os, re
import shutil
import argparse
import subprocess

VAMP_DIR = os.path.split(os.path.abspath(__file__))[0]
VICUNA_CONF = os.path.join(VAMP_DIR, 'vicuna_conf')

PFOLDER = 'paired'
SFOLDER='single'
CPATH = os.path.abspath('./')
PFPATH = os.path.join(CPATH, PFOLDER)
SFPATH = os.path.join(CPATH, SFOLDER)

def run_cmd(cmds, getval=True):
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if getval:
                return out


def p_mkdir(ndir):
	if not os.path.exists(ndir):
		os.makedirs(ndir)

def wrap():
	parser = argparse.ArgumentParser(description='Running the vicuna')
	parser.add_argument('-p', metavar='paired.fa', help='paired-end read file')
	parser.add_argument('-s', metavar='single.fa', help='(optional) single-end read file')
	parser.add_argument('-o', metavar='outfile.fa', default='outfile.fa', help='output file name')

	def vicuna():
		awk_cmd1 = '{if(NR%2==1) {if(length($qual)==0){s=""; while(length(s)<length($seq)) s=s"I"}else{s=$qual;} print "@"$1; print $2; print "+"; print s}}'
		awk_cmd2 = '{if(NR%2==0) {if(length($qual)==0){s=""; while(length(s)<length($seq)) s=s"I"}else{s=$qual;} print "@"$1; print $2; print "+"; print s}}'

		dst_p1 = os.path.join(PFPATH, 'reads.1.fq')
                dst_p2 = os.path.join(PFPATH, 'reads.2.fq')
		dst_s = os.path.join(SFPATH, 'sreads.fq')
		confile = 'fq_vicuna_conf.txt'

		p_mkdir(PFPATH)
		p_mkdir(SFPATH)
		
		if args.p is not None:
			cmd_p1 = ['bioawk', '-c', 'fastx', awk_cmd1, args.p] 
			f_p1 = open(dst_p1, 'wb')
			f_p1.write(run_cmd(cmd_p1, getval=True))
			f_p1.close()

			cmd_p2 = ['bioawk', '-c', 'fastx', awk_cmd2, args.p]
			f_p2 = open(dst_p2, 'wb')
			f_p2.write(run_cmd(cmd_p2, getval=True))
			f_p2.close()

		if args.s is not None:
			single_cmd = ['bioawk', '-c', 'fastx', '{if(length($qual)==0){s=""; while(length(s)<length($seq)) s=s"I";}else{s=$qual;} print "@"$1; print $2; print "+"; print s;}']
			s_rd = open(dst_s, 'wb')
			s_rd.write(run_cmd(single_cmd, getval=True))
			s_rd.close()

		config_f = os.path.join(VICUNA_CONF, confile)

		commands_1 = ['vicuna-omp-v1.0', config_f]
		run_cmd(commands_1, getval=False)

		os.rename('contig.lfv.fasta', args.o)

	parser.set_defaults(func=vicuna)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
			
