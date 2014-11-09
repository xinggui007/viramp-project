## AUTHOR: Yinan Wan ##
## DATE: 2013/09/19 ##
## DESCRIPTION: This script detect snps in the draft genome by comparing to reference genome ##
## NOTE: This only detect SNPs in unique region ##

## Demo ##
# python snp_detection.py -t draft_genome.fa -r refseq.fa -o snps.vcf #

import sys, os, re
import subprocess
import argparse

def run_cmd(cmds, getval=True):
	# DEVNULL = open(os.devnull, 'wb')
	p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	if getval:
		return out

def wrap():
	parser = argparse.ArgumentParser(description='Detecting snps in the draft genome by comparing to reference genome')
	parser.add_argument('-r', metavar='refseq.fa', help='Reference genome')
	parser.add_argument('-t', metavar='draft_genome.fa', help='Newly assembled genome for snp detection')
	parser.add_argument('-o', metavar='snps.vcf', default='snps.vcf', help='Output file, by default snps.vcf')
	
	def MUMmer_snp():
		commands_1 = ['nucmer', '--prefix=snp_det', args.r, args.t ]
		run_cmd(commands_1, getval=False)
		
		commands_2 = ['show-snps', '-CHTlr', 'snp_det.delta' ]
		msnps = run_cmd(commands_2)
		
		return msnps

	def vcformat(msnp):
		## create reference string
		refseq = str()
		gname = str()
		for line in file(args.r):
			line = line.strip()
			if re.match('^>', line):
				elem = line.split()
				gname = elem[0][1:]
			else:
				refseq = refseq + line

		otf = open(args.o, 'w')
		otf.write("##fileformat=VCFv4.1\n")
		otf.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

                def read_snps(nsnps, refpos, refvar,tgvar, tgpos):
                        if len(nsnps) == 0: 
				nsnps = [refpos, tgpos, refvar, tgvar]
			elif refvar !='.' and tgvar != '.':
                                otf.write('\t'.join([gname, nsnps[0], 'nucmer', nsnps[2], nsnps[3], '0', 'PASS', '.']))
				otf.write('\n')
				nsnps = [refpos, tgpos, refvar, tgvar]
			elif refvar == '.':
				if int(refpos) == int(nsnps[0]) + 1:
					nsnps[3] = nsnps[3] + tgvar
				else:
					otf.write('\t'.join([gname, nsnps[0], 'nucmer', nsnps[2], nsnps[3], '0', 'PASS', '.']))
                                	otf.write('\n')
					newrefpos = int(refpos) - 1
					nsnps = [str(newrefpos), str(int(tgpos)-1), refseq[newrefpos-1], refseq[newrefpos-1]+tgvar]
					
			elif tgvar == '.':
					if int(tgpos) == int(nsnps[1]) + 1:
                                        	nsnps[2] = nsnps[2] + refvar
                                	else:
						otf.write('\t'.join([gname, nsnps[0], 'nucmer', nsnps[2], nsnps[3], '0', 'PASS', '.']))
                                		otf.write('\n')
                                        	newrefpos = int(refpos) - 1
                                        	nsnps = [str(newrefpos), str(int(tgpos)-1), refseq[newrefpos-1]+refvar, refseq[newrefpos-1]]
			return nsnps

		snps = list()
		for line in msnp.split('\n'):
			if not re.match('^#', line) and len(line)>0:
				elem = line.split('\t')
				snps = read_snps(snps, elem[0],elem[1],elem[2],elem[3])
		if len(snps)==4:
			otf.write('\t'.join([gname, snps[0], 'nucmer', snps[2], snps[3], '0', 'PASS', '.']))
		otf.write('\n')	
		otf.close()

	def pipeline():
		msnps = MUMmer_snp()
		vcformat(msnps)

	parser.set_defaults(func=pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap()

	
