## demo ##
# sh quick_start.sh -l read_1.fastq -e read_2.fastq -r reference.fa -o output #

## AUTHOR: Yinan Wan ##
## DATE: 2013/08/19 ##
## DESCRIPTION: An overall pipeline for VAMP(virus assembly pipeline)##

print_help()
{
 echo "This script runs the whole pipeline"
 echo "-h help"
 echo "-l read_1 file from paired-end sequencing"
 echo "-e read_2 file from paired-end sequencing"
 echo "-r reference genome"
 echo "-d (optional)output_dir for quash.sh, only necessary for Galaxy integration"
 echo "-v indicate whether need variation file"
} 

#if [$# -lt 3 ];then
# print_help
# exit 1
#fi

while getopts "hl:e:r:d:v" opt
do
 case "$opt" in
h) print_help;exit 1
;;
l) read_1=$OPTARG
;;
e) read_2=$OPTARG
;;
r) refseq=$OPTARG
;;
d) quastdir=$OPTARG
;;
v) varfile="-v"
;;
\?) print_help; exit 1
;;
	esac
done

tooldir=/home/ubuntu/galaxy/galaxy-dist/tools
vampdir=${tooldir}/vamp

####### quality trimming #######
seqtk trimfq $read_1|hawk -c fastx '{print $0}'|awk 'BEGIN{OFS="\n"}{print "@"$1"#0/1",$2,"+",$3}' > left.fastq
 if [ "$read_2" ];then
seqtk trimfq $read_2|hawk -c fastx '{print $0}'|awk 'BEGIN{OFS="\n"}{print "@"$1"#0/2",$2,"+",$3}' > right.fastq

## merging paired-end reads scripts needs further rewrite !!!
  python ${tooldir}/utility/merge_pe.py -l left.fastq -e right.fastq > after_merge.fastq
else
  mv $read_1 after_merge.fastq
 fi
#######################


###### diginorm process ######
 sh ${vampdir}/diginorm.sh -i after_merge.fastq -C 10 -N 4 -x 1e9 -p
## result in two files: diginorm_reads.pe.fasta and diginorm_reads.se.fasta
#######################


######## velvet #######

## concatenate the kmer numbers ##
for i in {1..8}
do
  nk=31+$((i))*4
  kmer[$i]=$((nk))
done
kkmer=`echo ${kmer[@]}|tr ' ' ','`

sh ${vampdir}/velvet.sh -k $kkmer -p diginorm_out.pe.fasta -s diginorm_out.se.fasta -o velvet_contigs.fa -f fasta
## this result in one file containing all the assembled contigs: velvet_contigs.fa
######################


###### AMOScmp: AMOS reference-guided assembling of the contigs  ######

## combine contig and paired-end reads file and convert into AMOS message file (.afg) // integrated into AMOScmp.sh## 
# cat velvet_contigs.fa > combined_seq.fa
# cat diginorm_reads.pe.fasta >> combined_seq.fa
# toAmos -s combined_seq.fa -o combined_seq.afg
# rm -f combined_seq.fa

sh ${vampdir}/AMOScmp.sh -r -c velvet_contigs.fa -p diginorm_out.pe.fasta -f $refseq -o amoscmp_result
######################


####### Quast assessment ######
# ~/tools/quast-2.1/quast.py -R $refseq -o pipeline_quast amoscmp_result.fa $refseq 
sh ${vampdir}/quast.sh -r $refseq -i amoscmp_result.fasta -d $quastdir $varfile
## This result in a quast.html report and amoscmp_result.vcf/$refseq.vcf snp files 
##############################


######## snpEff ##########
## build up snpEff annotation database 
## sh snpEff_buildDB.sh -r $refseq -f $afmt -a $anf -v customized_genome 
# this result in a snpEff_customized_genome.config and a customized_genome database

## running snpEff
## java -Xmx4g -jar /home/yinan/tools/snpEff/snpEff.jar -c snpEff_customized_genome.config customized_genome -v amoscmp_result.vcf
####### completed ##########	
