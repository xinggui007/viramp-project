import sys, re, argparse

parser = argparse.ArgumentParser('SNP file conversion')
parser.add_argument('-f', dest='fname', help='.snp file to be converted')
parser.add_argument('-r', dest='refseq', help='reference genome, fasta format')
parser.add_argument('-n', dest='gname', default='', help='customized genome name; if empty, using the header in reference genome')
parser.add_argument('-o', dest='output', help='output file name')

args = parser.parse_args()
fname = args.fname
refile = args.refseq
output = args.output
gname = args.gname

ref=''
alt=''
refpos='0'
altpos=''
refseq=''

seqfile = open(refile)
otf = open(output, 'w')
for line in seqfile.readlines():
	if re.match('^>', line) and len(gname) == 0:
		elem=line.strip().split()
		gname=elem[0][1:]
	else:
		refseq = refseq+line.strip()

otf.write("##fileformat=VCFv4.1\n")
otf.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

for line in file(fname):
	line = line.strip()
	if not re.match('^#',line):
		elem = line.split('\t')
		if elem[2] == refpos:
			ref = elem[3]
			alt = alt + elem[4]
		elif elem[5] == altpos:
			ref = ref + elem[3]
			alt = elem[4]
		else:
			if ref == '.':
				ref = refseq[int(refpos)-1]
				alt = ref + alt
			elif alt == '.':
				refpos = int(refpos)-len(ref)
				ref = refseq[refpos-1] + ref
				alt = refseq[refpos-1]
			otf.write(gname+'\t'+str(refpos)+'\tnucmer\t'+ref+'\t'+alt+'\t0\tPASS\t.\n')
			ref = elem[3]
			alt = elem[4]
			
	refpos = elem[2]
	altpos = elem[5]

otf.close()
