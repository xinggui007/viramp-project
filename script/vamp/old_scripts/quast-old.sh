## demo ##
# sh quast.sh -r refseq.fa -o pipeline_quast -i amoscmp_result.fa,amoscmp_result2.fa

## AUTHOR: Yinan Wan ##
## DATE: 2013/08/19 ##
## DESCRIPTION: This script runs the QUAST program for assembling assessment and snp generation ##

print_help()
{
 echo "-h Help"
 echo "-r Reference genome"
 echo "-i Sequences for assessment" 
 echo "-o outputdir, required for galaxy integration"
 echo "-v whether to generating variation file (vcf format)"
}

if [ $# -lt 3 ];then
print_help
exit 1
fi

while getopts "hr:i:o:v" opt
do
 case "$opt" in
h) print_help; exit 1
;;
r) refseq=$OPTARG
;;
i) fname=$OPTARG
;;
o) outfile=$OPTARG
;;
\?) print_help; exit 1
;;
v) varfile="true"
;;
	esac
done

vampdir='/mnt/galaxy/galaxy-dist/tools/vamp'
quastdir='/mnt/src/quast-2.2'
infile=(`echo $fname|tr ',' ' '`)

if [ ! $outfile ];then
 outfile=quast_out
fi

## quast ##
$quastdir/quast.py -R $refseq -o $outfile ${infile[@]} $refseq

## produce simple html for galaxy display
python ${vampdir}/quast_html.py $outfile

## convert .used_snps into vcf format ##
if [ $varfile ];then

 for fn in ${infile[@]}
  do
  inputf_1=${fn##*/}
  inputf=${inputf_1%.*}
  python /home/yinan/local/galaxy/galaxy-dist/tools/utility/snp2vcf.py -f ${outfile}/contigs_reports/nucmer_output/${inputf}.used_snps -r $refseq > variation.vcf
  done
fi

