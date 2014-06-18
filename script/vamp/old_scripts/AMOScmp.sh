## demo ##
# sh AMOScmp.sh -r -c contig.fa -p paired.fa -f reference.fa -o outfile #

## AUTHOR:Yinan Wan ##
## DATE: 2013/08/19 ##
## DESCRIPTION: This script runs the whole AMOScmp pipeline, modified from AMOScmp script of AMOS ##

#!/bin/bash 
print_help()
{
 echo "-h help"
 echo "-r Randomly place repetitive reads into one of their copy locations if they cannot be placed via mate-pair info"
 echo "-c Contig file, fasta format"
 echo "-p Paired-end reads file, fasta format"
 echo "-f Reference file, fasta format"
 echo "-o Output prefix"
}

if [ $# -lt 3 ];then
print_help
exit
fi

while getopts "hrt:c:p:f:o:" opt
do
case "$opt" in
h) print_help; exit 1
;;
r) rep=-r
;;
t) tgt=$OPTARG
;;
c) ctg=$OPTARG
;;
p) perds="$OPTARG"
;;
f) ref=$OPTARG
;;
o) outpref=$OPTARG
;;
\?) print_help; exit 1
;;
	esac
done

if [ ! $outpref ];then
 outpref=amosresult
fi

PREFIX=${outpref}_tmp
BANK=${PREFIX}.bnk
SEQ=${PREFIX}.seq
## SEQ='combined_seq.fa'
ALIGN=${PREFIX}.delta
LAYOUT=${PREFIX}.layout
CONFLICT=${PREFIX}.conflict
CONTIG=${PREFIX}.contig
FASTA=${PREFIX}.fasta

if [ $perds ];then
 cat $perds > combined_seq.fa
fi

cat $ctg >> combined_seq.fa
toAmos -s combined_seq.fa -o ${PREFIX}.afg 2>&1

## building AMOS bank
bank-transact -c -z -b $BANK -m ${PREFIX}.afg 2>&1

## Collecting clear range sequences
 dumpreads $BANK > $SEQ 2>&1

## Running nucmer
nucmer --maxmatch -p ${PREFIX} $ref $SEQ 2>&1

## Running layout
casm-layout $rep -U $LAYOUT -C $CONFLICT -b $BANK $ALIGN 2>&1

## Running consensus
make-consensus -f -b $BANK 2>&1

## Outputting contigs
# bank2contig $BANK > $CONTIG 2>&1

## Outputting fasta
bank2fasta -b $BANK > $FASTA 2>&1

## remove unrelated stuff
# mv ${FASTA} ${outpref}.fasta 
# rm -r -f ${PREFIX}.*
# rm combined_seq.fa
