## AUTHOR: Yinan Wan ##
## DATE: 2013/09/09 ##
## DESCRIPTION: This script compares the draft genome to the reference genome ##

## Demo: python genomeCMP.py -r refseq.fa -d target.fa -o output -s target -c ##

import sys, os, re
import subprocess
import argparse
import shutil
import csv

def run_cmd(cmds, getval=True):
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

def wrap():
	parser = argparse.ArgumentParser(description='Compare the draft genome and reference genome assembling')
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome sequence for comparison')
	parser.add_argument('-d', metavar='target.fa', help='target draft genome for comparison')
	parser.add_argument('-o', metavar='output', default='comparison', help='output prefix')
	parser.add_argument('-s', choices=['ref','target'], default='ref', help='result sorted by reference genome position or grouped by target contigs')
	parser.add_argument('-c', action='store_true', help='output data files for circos visualization input')

	def gcmp():
		commands = ['nucmer', '--maxmatch', '='.join(['--prefix', PREFIX]), args.r, args.d]
		run_cmd(commands, getval=False)

	def coords():
		commands = ['show-coords', '-rclHT', '.'.join([PREFIX, 'delta'])]
		result = run_cmd(commands)
		f = open('.'.join([PREFIX, 'coords']), 'w')
		f.write(result)
		f.close()

        def sortbytarget(x, y, contigcol=-1, targetstartcol=2, targetendcol=3):
                minx = min(int(x[targetstartcol], x[targetendcol]))
                miny = min(int(y[targetstartcol], y[targetendcol]))

                return (x[contigcol] > y[contigcol]) and (minx > miny)

        _input_colnames = ['[R_St]','[R_Ed]','[T_St]','[T_Ed]','col5', 'col6', '[% IDY]','[LEN_R]','[LEN_T]','[COV_R]','[COV_T]','[REF_ID]','[CGT_ID]']
        _output_colnames = ['[R_St]','[R_Ed]','[T_St]','[T_Ed]','[% IDY]','[LEN_R]','[LEN_T]','[COV_R]','[COV_T]','[REF_ID]','[CGT_ID]']

        _contigcol = '[CGT_ID]'
        _targetstartcol = '[T_St]'
        _targetendcol = '[T_Ed]'

        def reformat(outprefix, target=True):
                """Reformat the output of nucmer, removing columns 5 and 6.

                If target=True, the rows are resorted by the target genome,
                first by contig name, then by the minimum start/end position.

                """

		f = open('.'.join([outprefix, 'final', 'coords']), 'w')
                ow = csv.DictWriter(f, delimiter="\t", fieldnames=_output_colnames, extrasaction='ignore')
                ow.writerow(dict(zip(_output_colnames, _output_colnames)))

                infile = open('.'.join([PREFIX, 'coords']))
                data = map(lambda s: dict(zip(_input_colnames, s.strip().split("\t"))), list(infile))

                # Resort by target genome, otherwise do nothing
                if target:
                        data = sorted(data, key=lambda x: (x[_contigcol], min(int(x[_targetstartcol]), int(x[_targetendcol]))))

                ow.writerows(data)

                f.close()

        ## circos data file and link file
	def circos_input(outprefix):

		f = open('_'.join([outprefix, 'circos','input.txt']), 'w')
		fl = open('_'.join([outprefix, 'circos','links.txt']), 'w')

		def write_data(dtid, value,label,ctcolor):
                        data = ['chr','-',dtid, label, '0', value, ctcolor]     
                        output = ' '.join(data)         
                        f.write(output+'\n')                    

		def write_links(linkid, chrm, st,end,color):
			data = [linkid, chrm, st, end,'='.join(['color',color])]
			output = ' '.join(data)
			fl.write(output+'\n')

		cdfile = '.'.join([outprefix, 'final','coords']) 
		contigs = dict()
		refseq = dict() 
		refNum = dict()
		segdup = 0 ## linkid
		links = dict()

		for line in file(cdfile):
			line = line.strip()
			if re.match('^\d+', line):
				elem = line.split('\t')
				## write link file
				segdup = segdup + 1
				linkid = ''.join(['segdup',str(segdup)])
				ctgname = elem[10].replace('|','_')	
				refname = elem[9].replace('|', '_')	
				links.update({linkid:[ctgname, elem[2], elem[3], refname, elem[0], elem[1]]}) ## linkid:[contig_num, contig_start, contig_end, refseq_num, refseq_start, refseq_end]	
					
				## record data file
				if elem[9] not in refseq.keys():
					refseq.update({refname:elem[5]})
				if elem[10] not in contigs.keys():
					contigs.update({ctgname:[elem[6], int(elem[0])]}) # [contig len, ref_st]

		## deal with color
		cdiv = 360/len(contigs)

		## write data file
		if None in [re.match('^\d+$', a) for a in refseq.keys()]:
			sortsb = str
		else:
			sortsb=int

		for rf in sorted(refseq.keys(), key=sortsb):
			write_data(''.join(['refseq', rf]), refseq[rf], rf, 'chrY')
	
		ctcolor = 0
		coldict = dict()	
		for ct in sorted(contigs,key=lambda x:contigs[x][1], reverse=True): ## only reverse the tick, but not the order	
			ctnum = len(contigs)-ctcolor
			ctcolor += 1
			color = str(ctcolor*cdiv)
			cdigit = '0'*(3-len(color))+color
			fcolor = ''.join(['hue',cdigit])
			coldict.update({ct:fcolor})
			write_data(''.join(['hs',ct]), contigs[ct][0], '_'.join(['ctg',str(ctnum)]), fcolor)

		## write link file
		for lid in links.keys():
			chrm = ''.join(['hs',links[lid][0]])
			fcolor = coldict[links[lid][0]]  
			write_links(lid, chrm, links[lid][1], links[lid][2], fcolor)
			write_links(lid, ''.join(['refseq',links[lid][3]]), links[lid][4],links[lid][5], fcolor)

		f.close()
		fl.close()

	def all_pipeline():
		gcmp()
		coords()

		if args.s == 'target':
			reformat(outprefix=args.o)
		else:
			reformat(outprefix=args.o, target=False)
		purge('./', PREFIX)

		if args.c:
			circos_input(outprefix=args.o)

	parser.set_defaults(func=all_pipeline)
	args = parser.parse_args()

	PREFIX = '_'.join([args.o, 'tmp'])

	args.func()

if __name__ == '__main__':
	wrap()
