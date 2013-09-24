## demo ##
# sh trim_quality.sh -i input.fastq -o orient #

## AUTHOR: Yinan Wan ##
## DATE: 2013/08/22 ##
## DESCRIPTION: Quality trimming for fastq file, using seqtk toolkit ##

print_help()
{
 echo "-h help"
 echo "-i input fastq file"
 echo "-o [L,R,S]read orient, L for read_1, R for read_2, S for single-end reads"
 echo "-l INT maximumly trim down to INT bp"
}

if [ $# -lt 3 ];then
 print_help
 exit 1
fi

while getopts "hi:o:l:" opt
do
 case "$opt" in
h) print_help; exit 1
;;
i) fname=$OPTARG
;;
o) forient=$OPTARG
;;
l) maxlen="$OPTARG"
;;
\?) print_help; exit 1
	esac
done

case $forient in 
L) fsuffix='#0/1'
;;
R) fsuffix='#0/2'
;;
S) fsuffix=''
;;
	esac

seqtk trimfq -l $maxlen $fname |bioawk -c fastx '{print $0}'|awk -v var=$fsuffix 'BEGIN{OFS="\n"}{print "@"$1var,$2,"+",$3}' 
