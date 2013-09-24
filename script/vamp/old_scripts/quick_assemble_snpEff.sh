## demo ##
## sh quick_assemble_snpEff.sh -r refseq.fa -f annotation_format -a annotation_file -v variation_file##

## AUTHOR: Yinan Wan ##
## DATE: 2013/08/20 ##
## Description: This script run a quick snpEff assessment under galaxy/entire pipeline ##

print_help()
{
 echo "-h help"
 echo "-r reference genome"
 echo "-a annotation file"
 echo "-f [gff, gtf, genbank] Annotation file format"
 echo "-v variation file, vcf format"
}

if [ $# -lt 3 ];then
 print_help
 exit 1
fi

while getopts "hr:a:f:" opt
do
 case "$opt" in
h) print_help; exit 1
;;
r) refseq=$OPTARG
;;
a) ant=$OPTARG
;;
f) fmt=$OPTARG
;;
v) varfile=$OPTARG
;;
\?) print_help;exit 1
;;
	esac
done

## build up databases
genversion=`date +%y%m%d%H%M%S` 
sh snpEff_buildDB.sh -r $refseq -a $ant -f $fmt -v $genversion

## run the snpEff
$snpEffdir=/home/yinan/local/galaxy/galaxy-dist/tools/snpEff/data

sh snpEff_main.sh -c ${snpEffdir}/${genversion}/snpEff_${genversion}.config ${genversion} -v $varfile

