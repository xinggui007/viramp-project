## AUTHOR: Yinan Wan ##
## DATE: 2013/09/12 ##
## Description: This script create circos graph for assembling evaluation #

## Demo ##
# python  circos.py -i circos_input.txt -l circos_links.txt -o output#
import re,os
import argparse

CIRCOS_DIR = '/mnt/src/circos-0.64'
VAMP_DIR = os.path.split(os.path.abspath(__file__))[0] 

CIRCOS_CMD_DIR = os.path.join(CIRCOS_DIR,'bin')
CIRCOS_ETC_DIR = os.path.join(CIRCOS_DIR, 'etc')
CIRCOS_VAMP_DIR = os.path.join(VAMP_DIR, 'circos_conf')

def run_command(cmd):
	command = ' '.join(cmd)
	os.system(command)

def wrap():
	parser = argparse.ArgumentParser(description='This script create circos')
	parser.add_argument('-i', metavar='circos_input.txt', help='circos data file')
	parser.add_argument('-l', metavar='circos_links.txt', help='circos link file')
	parser.add_argument('-r', metavar='(disable -i/l)refseq.fa', help='Input is fasta format reference sequence;if this option, target genome(-t) is required, and circos data/link file is not needed')
	parser.add_argument('-t', metavar='(disable -i/l)draft_genome.fa', help='Target Genome; if this option, reference genome(-r) is required, and circos data/link file is not needed')
	parser.add_argument('-c', action='store_true', help='Input reference sequence is multi-fasta')
	parser.add_argument('-o', metavar='output_circos',default='output', help='output prefix')

	def input_files(): 
		cmp_dir = os.path.join(VAMP_DIR, 'genomeCMP.py')
		prfx = '_'.join([args.o, 'cmp'])
		commands = ['python', cmp_dir, '-r', args.r, '-d', args.t, '-o', prfx, '-c']
		run_command(commands)	
		fdata = '_'.join([prfx,'circos','input.txt'])
		flink = '_'.join([prfx, 'circos','links.txt'])
		return fdata, flink

	def draw_circos(fdata, flink):

		CONFILE = '_'.join([args.o,'circos.conf'])
	        graphName = '_'.join([args.o, 'circos.svg'])
		graphPDF = '_'.join([args.o, 'circos.pdf'])			
	
		f = open(CONFILE, 'w')

		def write_include(conf_dir, confile):
			conf_dir = os.path.join(conf_dir, confile)
			conf_include = ''.join(['<<','include',' ',conf_dir, '>>', '\n'])

			f.write(conf_include)
		
		### writing circos configuration file ##					

		input_line = ' '.join(['karyotype','=',fdata])
		f.write(input_line+'\n')
		write_include(CIRCOS_VAMP_DIR,'general.conf')
		if not args.c:
			f.write('chromosome_scale = /refseq/=0.5rn\n')
	
		f.write('<image>\n')
		image_line = ' '.join(['file','=',graphName])
		f.write(image_line+'\n')
		write_include(CIRCOS_VAMP_DIR, 'image.generic.conf')
		f.write('</image>\n')

		f.write('<links>\n')
		f.write('<link>\n')
		link_line = ' '.join(['file','=',flink])
		f.write(link_line+'\n')
		write_include(CIRCOS_VAMP_DIR, 'link.generic.conf')
		f.write('</link>'+'\n')
		f.write('</links>'+'\n')

		write_include(CIRCOS_VAMP_DIR, 'ideogram.conf')
		write_include(CIRCOS_VAMP_DIR, 'ticks.conf')
		write_include(CIRCOS_ETC_DIR, 'housekeeping.conf')
		write_include(CIRCOS_ETC_DIR, 'colors_fonts_patterns.conf')
	
		f.close() 
		######### FINISH CONF ############
		
		circos_cmd = os.path.join(CIRCOS_CMD_DIR, 'circos')
		commands = [circos_cmd, '-conf', CONFILE]
		run_command(commands)

		## convert svg to png
		commands = ['rsvg-convert', '-d', '300', '-p', '300', '-f', 'pdf','-a', graphName, '-o', graphPDF]		
		run_command(commands)

	def pipeline():
		if args.r and args.t:
			fdata, flink = input_files()
		else:
			fdata, flink = args.i, args.l
		draw_circos(fdata, flink)
				
	parser.set_defaults(func=pipeline)
	args = parser.parse_args()
	args.func()

if __name__ == '__main__':
	wrap() 
