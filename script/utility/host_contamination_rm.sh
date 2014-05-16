#!/bin/bash

INDEX_DIR='/mnt/galaxy/galaxy-dist/vamp-data/host-index'
print_help(){
echo 'This script remove the host contamination reads'
echo '-h print help'
echo '-d pre-built genome index'
echo '-g customized host genome, if this option is specified, "-d" will be ignored'
echo '-i input read_1 file'
echo '-j input read_2 file, if paired-end'
echo '-o output prefix'
}

if [ $# -lt 3 ]; then
 print_help
 exit 1
fi

while getopts "hd:g:i:j:o:" opt
do
case "$opt" in
h) print_help;exit 1
;;
d) ind=${INDEX_DIR}/$OPTARG
;;
g) cgenome=$OPTARG
;;
i) input_p1=$OPTARG
;;
j) input_p2=$OPTARG
;;
o) fout=$OPTARG
;;
\?) print_help; exit 1
;;
	esac
done

if [ ${#cgenome} -gt 0 ]; then
 bowtie2-build $cgenome custgnm
 ind=custgnm
fi

if [ ${#input_p2} -gt 0 ]; then
 bowtie2 -x $ind -1 $input_p1 -2 $input_p2 -S aligned.sam 2>&1
 samtools view -Sb aligned.sam -o aligned.bam 2>&1
 samtools sort aligned.bam aligned.sort
 samtools index aligned.sort.bam

 samtools view -f 4 -b aligned.sort.bam > host_unmapped.bam
 samtools view -F 4 -f 8 -b aligned.sort.bam > host_one_read_mapped.bam
 samtools merge -f merged_clean_reads.bam host_unmapped.bam host_one_read_mapped.bam
 samtools sort -n merged_clean_reads.bam merged_clean_reads.sort

 bedtools bamtofastq -i merged_clean_reads.sort.bam -fq ${fout}_R1.fastq -fq2 ${fout}_R2.fastq

else
 bowtie2 -x $ind -U $input_p1 -S aligned.sam
 samtools view -Sb aligned.sam > aligned.bam
 samtools sort aligned.bam aligned.sort
 samtools index aligned.sort.bam

 samtools view -f 4 -b aligned.sort.bam > host_unmapped.bam
 bedtools bamtofastq -i host_unmapped.bam -fq ${fout}_R1.fastq
fi
