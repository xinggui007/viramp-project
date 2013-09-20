## produce a simple html quast used for galaxy display
from htmltag import h1, p,td,b
import sys,re

def report(rname,qdir):
	f = open(rname,'wb')
	f.write('<!DOCTYPE html>\n')
	f.write('<html>\n')
	f.write('<body>\n')

	hd = h1('Assembly Statistics')
	f.write(hd)
	f.write('<table>\n')
	reportdir=qdir+'/report.txt'
	for line in file(reportdir):
		line = line.strip()
		if re.match('All statistics are based on contigs', line):
			f.write(p(line)+'\n')
		elif len(line)>0 :
			f.write('<tr>'+'\n')
			elem = re.split('\s{2,}',line)	
			for el in elem:
				f.write(td(el))
			f.write('</tr>'+'\n')

	f.write('</table>')
	f.write(p(b('Please download the whole quast report data for details'))+'\n')
	f.write('</body>')
	f.write('</html>')

def main(rname,qdir):
	report(rname,qdir)

if __name__ == '__main__':
	main('quast2show.html',sys.argv[1])
