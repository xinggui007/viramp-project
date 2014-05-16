## demo ##
# sh velvet.sh -k 21,25,29 -p paired_end.fa -s single_end.fa -o outfile -f fasta

## AUTHOR: Yinan Wan ##
## DATE: 2013/08/19 ##
## DESCRIPTION: This script runs velvet with a series of kmers and output a combined fasta files containing all the assembled contigs ##

print_help()
{
echo "This script runs velvet with a series of kmers and output a combined fasta files containing all the assembled contigs"
echo "-h help"
echo "-k k-mer(s) used in velvet e.x 23,25,29"
echo "-p paired-end reads file"
echo "-s single-end reads file"
echo "-f [fasta, fastq] input files format"
echo "-o output file, by default 'velvet_contigs.fa'"
}

if [ $# -lt 3 ];then
print_help
exit 1
fi

while getopts "hk:p:s:o:f:" opt
do
case "$opt" in 
h) print_help; exit 1
;;
k) khmer=$OPTARG
;;
p) pfile="-shortPaired $OPTARG"
;;
s) sfile="-short $OPTARG"
;;
o) outfile=$OPTARG
;;
f) fmt=$OPTARG
;;
\?) print_help; exit 1
;;
	esac
done

if [ ! $outfile ];then
 outfile=velvet_contigs.fa
fi

kkmer=(`echo $khmer|tr ',' ' '`)
for i in "${kkmer[@]}"; do
	velveth hsv.beforedigipe.$i $i -${fmt} $pfile $sfile  
	velvetg hsv.beforedigipe.$i -exp_cov auto -cov_cutoff auto -scaffolding no 
done

## concatenate the contigs in all the kmers
cat hsv.beforedigipe.*/contigs.fa >> all_contigs.fa
cat all_contigs.fa|awk -v OFS='' 'BEGIN{ctg=0}{if($0~/^>/){ctg++;print ">contig"ctg} else print $0}' > ${outfile}
rm -f all_contigs.fa
rm -r -f hsv.beforedigipe.*
