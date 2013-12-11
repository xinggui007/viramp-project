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
 \?) print_help;exit 1
 ;;
	esac
done

 paste <(cat $read_1|bioawk -c fastx -v OFS='\t' '{print $1"\/1", $2, $3}') <(cat $read_2|bioawk -c fastx -v OFS='\t' '{print $1"\/2", $2, $3}') | awk -v OFS='\n' '{print "@"$1,$2,"+",$3,"@"$4,$5,"+",$6}'
