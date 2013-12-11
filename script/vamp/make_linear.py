import sys, re, os
import argparse
import subprocess
import shutil

def run_cmd(cmds, getval=True):
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
	parser = argparse.ArgumentParser(description='closing the gaps from the draft to provide a final linear genome')
	parser.add_argument('-c', metavar='contigs.fa', help='draft genome containing multiple contigs')	
	parser.add_argument('-r', metavar='refseq.fa', help='reference genome for contig orientation')
	parser.add_argument('-o', metavar='output', default='final_linear', help='output prefix, by default is "final_linear"')

	def gcmp():
		commands = ['nucmer', '='.join(['--prefix', PREFIX]), args.r, args.c]
                run_cmd(commands, getval=False)

	def coords():
		commands = ['show-coords', '-rclHT', '.'.join([PREFIX, 'delta'])]
		result = run_cmd(commands)
		f = open('.'.join([PREFIX, 'coords']), 'w')
		f.write(result)
		f.close()

	def getfasta(fasta):
		nflag = 0
		seqname=str()
		ndict = dict()
		for line in file(fasta):
			if nflag == 0 and re.match('^>', line.strip()):
				seqname = line.strip().replace('>','')
				nflag = 1
			elif nflag and len(seqname)>0:
				ndict.update({seqname:line.strip()})
				nflag = 0
		return ndict

	def nconst(coords):
		ndict = dict()
		for line in file(coords):
			if re.match('^\d+', line):
				elem = line.strip().split('\t')
				if elem[12] not in ndict:
					ndict[elem[12]] = {'ref_st':int(elem[0]), 'ref_ed':int(elem[1]), 't_st':int(elem[2]), 't_ed':int(elem[3])}
				else:
					ndict[elem[12]]['ref_st']=min(int(elem[0]), ndict[elem[12]]['ref_st'])
					ndict[elem[12]]['ref_ed']=max(int(elem[1]), ndict[elem[12]]['ref_ed'])
					ndict[elem[12]]['t_st']=min(int(elem[2]), ndict[elem[12]]['t_st'])
					ndict[elem[12]]['t_ed']=max(int(elem[3]), ndict[elem[12]]['t_ed'])

		ctgseq = getfasta(args.c)
		ncoord = 0
		nseq = str()
		for ctg in sorted(ndict, key=lambda x:int(ndict[x]['ref_st'])):
			if ncoord == 0:
				nseq=ctgseq[ctg][0:ndict[ctg]['t_ed']]	
				ncoord = ndict[ctg]['ref_ed']
			else:
				nadd = ndict[ctg]['ref_st']-ncoord-1
				#print ctg, str(nadd), ndict[ctg]['ref_st']
				tmpseq = ctgseq[ctg][(ndict[ctg]['t_st']-1):ndict[ctg]['t_ed']]
				nseq = ''.join([nseq, 'N'*nadd, tmpseq])
				ncoord = ndict[ctg]['ref_ed']
		tmpseq = ctgseq[ctg][ndict[ctg]['t_ed']:]
		nseq = ''.join([nseq, tmpseq])

		f = open('.'.join([args.o, 'fasta']), 'w')
		nheader=''.join(['>', 'linear_genome'])
		f.write('\n'.join([nheader, nseq]))
		f.close()	

	def main():
		gcmp()
		coords()
		fcoords = '.'.join([PREFIX, 'coords'])	
		nconst(fcoords)
		purge('./', PREFIX)

	parser.set_defaults(func=main)
	args = parser.parse_args()

	PREFIX = '_'.join([args.o, 'tmp'])	
	args.func()

if __name__ == '__main__':
	wrap()
