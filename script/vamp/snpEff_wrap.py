## demo ##


## AUTHOR: Yinan Wan ##
## DATE: 2013/08/28 ##
## DESCRIPTION: ##

import argparse
import re,sys,os,shutil


SNPEFF_DIR = '/home/yinan/local/galaxy/galaxy-dist/tools/snpEff'

def buildDB(ref,ant,fmt,gversion):
	ref = os.path.abspath(ref)
	ant = os.path.abspath(ant)

	## create data/ folder and prepare files for database built
	def build_ant_dir():
		anodir = os.path.join(SNPEFF_DIR, 'data', gversion)

		if not os.path.exists(anodir):
			os.makedirs(anodir)
		else:
			print "database exists!!!"
			sys.exit(1)
		
		## copy reference sequence
		refdst = os.path.join(anodir, 'sequences.fa')
                shutil.copy(ref, refdst)
	
		## Annotation format parameter check, copy annotation file
		def ant_format():

			def gff():
				antdst = os.path.join(anodir, 'genes.gff')
				shutil.copy(ant, antdst)
				with open(antdst,'a') as antw:
					antw.write('##FASTA')
					antw.write(file(refdst).read())	## be careful!!! the chromosome name must be exactly the same as antdst (annotation file)
					dbfmt='-gff3'
				return dbfmt

			def gtf(): 
				antdst = os.path.join(anodir, 'genes.gtf')
				shutil.copy(ant, antdst)
				dbfmt = '-gtf22'
				return dbfmt

			def genbank():
				antdst = os.path.join(anodir, 'genes.gb')
				shutil.copy(ant, antdst)
				dbfmt = '-genbank'
				return db

			ANT_FORMAT = {
                                'gff':gff,
                                'gtf':gtf,
                                'genbank':genbank,
                        }

			return ANT_FORMAT[fmt]()		
	
		format_par = ant_format()
		return format_par

	## customize the config file
	def config_file():
		configsrc = os.path.join(SNPEFF_DIR, 'snpEff.config')
		configdst = os.path.join(SNPEFF_DIR, 'data',gversion, 'snpEff_' + gversion + '.config')
		shutil.copy(configsrc, configdst)

		with open(configdst,'a') as newconfig:
			newgme = gversion + '.genome: ' + gversion
			newconfig.write('##' + gversion+'\n')
			newconfig.write(newgme)

		return configdst

	## copy and adjust annotation file 
	dbformat = build_ant_dir()
	configdst = config_file()	

	jardir = os.path.join(SNPEFF_DIR, 'snpEff.jar')
	command_para = ['java', '-jar', jardir, 'build', '-c', configdst, dbformat, '-v', gversion] 
	command = ' '.join(command_para)
	os.system(command)

def run_snpEff(gversion, varfile, outputvcf):
	varfile = os.path.abspath(varfile)

	jardir = os.path.join(SNPEFF_DIR, 'snpEff.jar')
	configf = 'snpEff_' + gversion + '.config' 
	configdir = os.path.join(SNPEFF_DIR, 'data', configf)
	commands = ['java', '-Xmx4g', '-jar', jardir, '-c' + configdir, gversion, '-v','>',outputvcf]
	
	command = ' '.join(commands)
	os.system(command)

def wrap():
	parser = argparse.ArgumentParser(description='Annotating the variation about its effect in genome')
	subparsers = parser.add_subparsers(dest='action')

	parser_build = subparsers.add_parser('build', help='build the annotation database')
	parser_build.add_argument('-r',  metavar='reference.fa', help='reference sequence')
        parser_build.add_argument('-a',  metavar='annotation.gff', help='annotation file')
        parser_build.add_argument('-f',  choices=['gff', 'gtf', 'genbank'],help='annotation file format, only gff tested')
	parser_build.add_argument('-g', metavar='customized-genome', help='Customized genome name')
	
	def build():
		print "Building database", args.g, '...'
		buildDB(args.r,args.a,args.f,args.g)

	## set build mode
	parser_build.set_defaults(func=build)	

	parser_main = subparsers.add_parser('main', help='run the snpEff main function')
	parser_main.add_argument('-v', metavar='variation.vcf', help='variation file to be annotated')
        parser_main.add_argument('-o', metavar='output.vcf', help='output vcf file')
	parser_main.add_argument('-g', metavar='customized-genome', help='Customized genome name')

	def snpEff_main():
		run_snpEff(args.g, args.v, args.o)
		print 'Annotating', args.v, '...'

	## set main_function mode
	parser_main.set_defaults(func=snpEff_main)

	parser_all = subparsers.add_parser('all', help='run build/main function together')
	parser_all.add_argument('-r',  metavar='reference.fa', help='reference sequence')
        parser_all.add_argument('-a',  metavar='annotation.gff', help='annotation file')
        parser_all.add_argument('-f',  choices=['gff', 'gtf', 'genbank'],help='nnotation file format, only gff tested')	
        parser_all.add_argument('-v', metavar='variation.vcf', help='variation file to be annotated')
        parser_all.add_argument('-o', metavar='output.vcf', help='output vcf file')
	parser_all.add_argument('-g', metavar='customized-genome', help='Customized genome name')

	def snpEff_all():
		build()
		snpEff_main()

	## set all mode
	parser_all.set_defaults(func=snpEff_all)

	args = parser.parse_args()
	args.func()


if __name__ == "__main__":
	wrap()	
