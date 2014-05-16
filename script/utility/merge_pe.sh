#!/bin/bash

print_help()
{
 echo "-h help"
 echo "-l read_1 file, fastq format"
 echo "-e read_2 file, fastq format"
}

if [ $# -lt 3 ];then
 print_help
exit
fi

while getopts "hl:e:" opt
do
 case "$opt" in
 h) print_help; exit 1
 ;;
 l) read_1=$OPTARG
 ;;
 e) read_2=$OPTARG
 ;;
 \?) print_help;exit 2
 ;;
	esac
done

## paste <(cat $read_1|bioawk -c fastx -v OFS='\t' 'BEGIN{num=0}{num+=1;print "VIRAMP"num"\/1", $2, $3}') <(cat $read_2|bioawk -c fastx -v OFS='\t' 'BEGIN{num=0}{num+=1; print "VIRAMP"num"\/2", $2, $3}') | awk -v OFS='\n' '{if(NF==2) {print ">"$1,$2,">"$3,$4} else print "@"$1,$2,"+",$3,"@"$4,$5,"+",$6}'

paste <(cat $read_1|bioawk -c fastx -v OFS='\t' '{print $1"\/1", $2, $3}') <(cat $read_2|bioawk -c fastx -v OFS='\t' '{print $1"\/2", $2, $3}') | awk -v OFS='\n' '{if(NF==2) {print ">"$1,$2,">"$3,$4} else print "@"$1,$2,"+",$3,"@"$4,$5,"+",$6}'
## paste <(cat $read_1|bioawk -c fastx -v OFS="\t" '{if($3) {print "@"$1" "$4, $2, "+", $3} else {print ">"$1" "$4, $2}}') <(cat $read_2|bioawk -c fastx -v OFS="\t" '{if($3) {print "@"$1" "$4, $2, "+", $3} else {print ">"$1" "$4, $2}}')|sed 's/\t/\n/g'
