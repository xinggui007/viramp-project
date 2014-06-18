## demo ##
# sh diginorm.sh -i paired-end.fastq -o afterdiginorm -C 10 -N 4 -x 1e9 -p #

## AUTHOR: Yinan Wan ##
## DATE: 2013/08/16 ##
## DESCRIPTION: This script runs the diginorm program to reduce the sequencing coverage ##

print_help()
{
 echo "this script runs the diginorm"
 echo "-i input file "
 echo "-o output file"
 echo "-h help"
 echo "-C INT coverage cutoff"
 echo "-N INT Number of hash table to use"
 echo "-x lower_bound on hashsize to use"
 echo "-p paired end reads"

}

if [ $# -lt 3 ];then
print_help
exit 1
fi

while getopts "hi:o:C:N:x:p" opt
do
case "$opt" in
h) print_help;exit 1
;;
i) reads=$OPTARG
;;
o) outfile=$OPTARG
;;
C) cutoff=$OPTARG
;;
N) hashnum=$OPTARG
;; 
x) hashsize=$OPTARG
;;
p) pairedflag="-p"
;;
\?) print_help; exit 1
;;
	esac
done

if [ ! $outfile ];then
 outfile=diginorm_out
fi


digdir='/mnt/src/python-module/khmer'
dig_script_dir=${digdir}/scripts
dig_sandbox_dir=${digdir}/sandbox

${dig_script_dir}/normalize-by-median.py -C $((cutoff*5)) -k 20 -N $hashnum -x $hashsize --savehash ${outfile}.kh $pairedflag $reads 2>&1
mv *.keep ${outfile}.keepnew
${dig_script_dir}/filter-abund.py ${outfile}.kh ${outfile}.keepnew 2>&1

## seperate the se and pe reads from result of filter-abund (this step does not have the option to keep paired, but results are mostly paired, with a few to have one end filtered out)
python ${dig_sandbox_dir}/strip-and-split-for-assembly.py ${outfile}.keepnew.abundfilt 2>&1

for endlb in se pe;do
case "endlb" in
pe) pflag="-p"
;;
se) pflag=""
;;
	esac

${dig_script_dir}/normalize-by-median.py -C $cutoff -k 20 -N $hashnum -x $hashsize $pflag ${outfile}.keepnew.abundfilt.${endlb} 2>&1
rm ${outfile}.keepnew.abundfilt.${endlb}
mv ${outfile}.keepnew.abundfilt.${endlb}.keep $outfile.${endlb}.fasta
done

rm ${outfile}.kh
rm ${outfile}.keepnew
rm ${outfile}.keepnew.abundfilt

