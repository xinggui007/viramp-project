## AUTHOR: Yinan Wan ##
## DATE: 2013/09/09 ##
## DESCRIPTION: This script compares the draft genome to the reference genome ##

## Demo: python genomeCMP.py -r refseq.fa -d target.fa -o output -s target -c ##

import sys, os, re
import subprocess
import argparse

def run_cmd(cmds, getval=True):
	DEVNULL = open(os.devnull, 'wb')
	p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
	out, err = p.communicate()
	if getval:
		return out

def wrap():
	parser = argparse.ArgumentParser(description='Compare the draft genome and reference genome assembling')
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome sequence for comparison')
	parser.add_argument('-d', metavar='target.fa', help='target draft genome for comparison')
	parser.add_argument('-o', metavar='output', default='comparison', help='output prefix')
	parser.add_argument('-s', choices=['ref','target'], default='ref', help='result sorted by reference genome position or grouped by target contigs')
	parser.add_argument('-c', action='store_true', help='output data files for circos visualization input')

	def gcmp():
		commands = ['nucmer', '='.join(['--prefix', args.o]), args.r, args.d]
		run_cmd(commands, getval=False)

	def coords():
		commands = ['show-coords', '-rclHT', '.'.join([args.o, 'delta'])]
		result = run_cmd(commands)
		f = open('.'.join([args.o, 'coords']), 'w')
		f.write(result)
		f.close()

	def reformat(target=True):

		f=open('.'.join([args.o,'final','coords']),'w')
		beginline = '\t'.join(['[R_St]','[R_Ed]','[T_St]','[T_Ed]','[% IDY]','[LEN_R]','[LEN_T]','[COV_R]','[COV_T]','[REF_ID]','[CGT_ID]'])

		f.write(beginline+'\n')
		if target:
			commands_group = ['cut','-f13', '.'.join([args.o, 'coords'])]
			out = run_cmd(commands_group)
			cgroup = set(out.split())
			for i in sorted(cgroup, key=int):
				command_grep = ['awk', '-v', '='.join(['var',i]),'BEGIN{OFS=\"\\t\"}{if ($13==var) print $1, $2, $3,$4,$7,$8,$9,$10,$11,$12,$13}', '.'.join([args.o,'coords'])]
				newline = run_cmd(command_grep)
				f.write(newline)
				f.write(''.join(['='*len(beginline),'\n']))
		else:
			command_grep = ['cut','-f1-4,7-13','.'.join([args.o,'coords'])]
			newline = run_cmd(command_grep)
			f.write(newline)
		f.close()

## circos data file and link file
	def circos_input():

		f = open('_'.join([args.o,'circos','input.txt']), 'w')
		fl = open('_'.join([args.o,'circos','links.txt']), 'w')

		def write_data(dtid, value,label,ctcolor):
                        data = ['chr','-',dtid, label, '0', value, ctcolor]     
                        output = ' '.join(data)         
                        f.write(output+'\n')                    

		def write_links(linkid, chrm, st,end,color):
			data = [linkid, chrm, st, end,'='.join(['color',color])]
			output = ' '.join(data)
			fl.write(output+'\n')

		cdfile = '.'.join([args.o, 'coords'])
		contigs = dict()
		refseq = dict() 
		refNum = dict()
		segdup = 0 ## linkid
		links = dict()

		for line in file(cdfile):
			line = line.strip()
			elem = line.split('\t')
			## write link file
			segdup = segdup + 1
			linkid = ''.join(['segdup',str(segdup)])
	
			links.update({linkid:[elem[12], elem[2], elem[3], elem[11], elem[0], elem[1]]}) ## linkid:[contig_num, contig_start, contig_end, refseq_num, refseq_start, refseq_end]	
				
			## record data file
			if elem[11] not in refseq.keys():
				refseq.update({elem[11]:elem[7]})
				# write_data('refseq',elem[7],'reference-genome','chrY')
			if elem[12] not in contigs.keys():
				contigs.update({elem[12]:elem[8]})

		## deal with color
		cdiv = 360/len(contigs)

		## write data file
		if None in [re.match('^\d+$', a) for a in refseq.keys()]:
			sortsb = str
		else:
			sortsb=int

		for rf in sorted(refseq.keys(), key=sortsb):
			write_data(''.join(['refseq', rf]), refseq[rf], rf, 'chrY')	
		for ct in sorted(contigs.keys(),key=int, reverse=True):	
			color = str(int(ct)*cdiv)
			cdigit = '0'*(3-len(color))+color
			write_data(''.join(['hs',ct]), contigs[ct], ct, ''.join(['hue',cdigit]))

		## write link file
		for lid in links.keys():
			color = str(int(links[lid][0])*cdiv)
			cdigit = '0'*(3-len(color))+color
			chrm = ''.join(['hs',links[lid][0]])
			fcolor = ''.join(['hue',cdigit])
			write_links(lid, chrm, links[lid][1], links[lid][2], fcolor)
			write_links(lid, ''.join(['refseq',links[lid][3]]), links[lid][4],links[lid][5], fcolor)

		f.close()
		fl.close()

	def all_pipeline():
		gcmp()
		coords()
		if args.s == 'target':
			reformat()
		else:
			reformat(target=False)

		if args.c:
			circos_input()

	parser.set_defaults(func=all_pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()
