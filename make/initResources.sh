#!/usr/bin/env bash

RESOURCES_DIR=${1:-"../Resources"};
HUMAN="HomoSapiens"
MURINE="MusMusculus"

GENOME_DIR="Genomes"
HUMAN_GENOME_DIR="${RESOURCES_DIR}/${GENOME_DIR}/${HUMAN}"
MURINE_GENOME_DIR="${RESOURCES_DIR}/${GENOME_DIR}/${MURINE}"
mkdir -p "${HUMAN_GENOME_DIR}"
mkdir -p "${MURINE_GENOME_DIR}"

REGIONS_DIR="Regions"
HUMAN_REGIONS_DIR="${RESOURCES_DIR}/${REGIONS_DIR}/${HUMAN}"
MURINE_REGIONS_DIR="${RESOURCES_DIR}/${REGIONS_DIR}/${MURINE}"
mkdir -p "${HUMAN_REGIONS_DIR}"
mkdir -p "${MURINE_REGIONS_DIR}"

SNPS_DIR="SNPs"
HUMAN_SNPS_DIR="${RESOURCES_DIR}/${SNPS_DIR}/${HUMAN}"
MURINE_SNPS_DIR="${RESOURCES_DIR}/${SNPS_DIR}/${MURINE}"
mkdir -p "${HUMAN_SNPS_DIR}"
mkdir -p "${MURINE_SNPS_DIR}"

REFSEQ_DIR="RefSeqAnnotations"
HUMAN_REFSEQ_DIR="${RESOURCES_DIR}/${REFSEQ_DIR}/${HUMAN}"
MURINE_REFSEQ_DIR="${RESOURCES_DIR}/${REFSEQ_DIR}/${MURINE}"
mkdir -p "${HUMAN_REFSEQ_DIR}"
mkdir -p "${MURINE_REFSEQ_DIR}"

GENES_EXPRESSION_DIR="GenesExpression"
HUMAN_GENES_EXPRESSION_DIR="${RESOURCES_DIR}/${GENES_EXPRESSION_DIR}/${HUMAN}"
MURINE_GENES_EXPRESSION_DIR="${RESOURCES_DIR}/${GENES_EXPRESSION_DIR}/${MURINE}"
mkdir -p "${HUMAN_GENES_EXPRESSION_DIR}"
mkdir -p "${MURINE_GENES_EXPRESSION_DIR}"

echo "Started Downloading UCSC Resources.
"
#---------------------------------------------------------------------------
# HG38
#---------------------------------------------------------------------------
HG38_FTP_URL="http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/"

echo "Started Downloading Hg38 Files:"

# Genome
HG38_FTP_GENOME_URL="http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/"
HG38_GENOME_FASTA_FILE="hg38.fa.gz"
HG38_GENOME_FASTA="ucscHg38Genome.fa.gz"
echo "Downloading Hg38 Genome: ${HG38_FTP_GENOME_URL}${HG38_GENOME_FASTA_FILE}"
wget "${HG38_FTP_GENOME_URL}${HG38_GENOME_FASTA_FILE}"  --directory-prefix="${HUMAN_GENOME_DIR}"
echo "Saving Gzipped Hg38 Genome Under: ${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA}"
gunzip -c "${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA_FILE}" > "${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA}"
rm "${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA_FILE}"
echo "Done Processing Hg38 Genome"

# Repeats Regions
HG38_REGIONS_FILE="ucscHg38Alu.bed.gz"
HG38_REGIONS_TABLE_FILE="rmsk.txt.gz"
echo "Downloading Hg38 Alu Repeats Table ${HG38_FTP_URL}${HG38_REGIONS_TABLE_FILE}"
wget "${HG38_FTP_URL}${HG38_REGIONS_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing Hg38 RefSeq Curated Table ${HG38_REGIONS_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG38_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($13 ~/Alu/ && $6 !~/_/) {print $6,$7,$8}' | gzip > "${HUMAN_REGIONS_DIR}/${HG38_REGIONS_FILE}"
rm "${HUMAN_REFSEQ_DIR}/${HG38_REGIONS_TABLE_FILE}"
echo "Done Processing Hg38 Alu Repeats Table ${HG38_REGIONS_TABLE_FILE}"

# SNPs
HG38_SNPS_FILE="ucscHg38CommonGenomicSNPs150.bed.gz"
HG38_SNPS_TABLE_FILE="snp150Common.txt.gz"
echo "Downloading Hg38 Common Genomic SNPs Table ${HG38_FTP_URL}${HG38_SNPS_TABLE_FILE}"
wget "${HG38_FTP_URL}${HG38_SNPS_TABLE_FILE}"  --directory-prefix="${HUMAN_SNPS_DIR}"
echo "Processing Hg38 RefSeq Curated Table ${HG38_SNPS_TABLE_FILE}"
zcat "${HUMAN_SNPS_DIR}/${HG38_SNPS_TABLE_FILE}" | awk '{OFS ="\t"}($11=="genomic") {print $2,$3,$4,$7,$9,$10,$16,$25}'| gzip > "${HUMAN_SNPS_DIR}/${HG38_SNPS_FILE}"
rm "${HUMAN_SNPS_DIR}/${HG38_SNPS_TABLE_FILE}"
echo "Done Processing Hg38 Common Genomic SNPs Table ${HG38_SNPS_TABLE_FILE}"

# RefSeq
HG38_REFSEQ_TABLE_FILE="ncbiRefSeqCurated.txt.gz"
HG38_REFSEQ_FILE="ucscHg38RefSeqCurated.bed.gz"
echo "Downloading Hg38 RefSeq Curated Table ${HG38_FTP_URL}${HG38_REFSEQ_TABLE_FILE}"
wget "${HG38_FTP_URL}${HG38_REFSEQ_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing Hg38 RefSeq Curated Table ${HG38_REFSEQ_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG38_REFSEQ_TABLE_FILE}"| awk '{OFS ="\t"} {print $3,$5,$6,$2,$13,$4,$10,$11}' |gzip > "${HUMAN_REFSEQ_DIR}/${HG38_REFSEQ_FILE}"
rm "${HUMAN_REFSEQ_DIR}/${HG38_REFSEQ_TABLE_FILE}"
echo "Done Processing Hg38 RefSeq Curated Table ${HG38_REFSEQ_TABLE_FILE}"

# Genes Expression
HG38_GENES_EXPRESSION_FILE="ucscHg38GTExGeneExpression.bed.gz"
HG38_GENES_EXPRESSION_TABLE_FILE="gtexGene.txt.gz"
echo "Downloading Hg38 Genes Expression Table ${HG38_FTP_URL}${HG38_GENES_EXPRESSION_TABLE_FILE}"
wget "${HG38_FTP_URL}${HG38_GENES_EXPRESSION_TABLE_FILE}"  --directory-prefix="${HUMAN_GENES_EXPRESSION_DIR}"
echo "Processing Hg38 RefSeq Curated Table ${HG38_GENES_EXPRESSION_TABLE_FILE}"
zcat "${HUMAN_GENES_EXPRESSION_DIR}/${HG38_GENES_EXPRESSION_TABLE_FILE}" | awk '{OFS ="\t"} {print $1,$2,$3,$4,$10,$6}'| gzip > "${HUMAN_GENES_EXPRESSION_DIR}/${HG38_GENES_EXPRESSION_FILE}"
rm "${HUMAN_GENES_EXPRESSION_DIR}/${HG38_GENES_EXPRESSION_TABLE_FILE}"
echo "Done Processing Hg38 Genes Expression Table ${HG38_GENES_EXPRESSION_TABLE_FILE}"


#---------------------------------------------------------------------------
# HG19
#---------------------------------------------------------------------------
HG19_FTP_URL="http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/"

echo "Started Downloading Hg19 Files:"

# Genome
HG19_FTP_GENOME_URL="http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/"
HG19_GENOME_FASTA_FILE="chromFa.tar.gz"
echo "Downloading Hg38 Genome: ${HG19_FTP_GENOME_URL}${HG19_GENOME_FASTA_FILE}"
HG19_GENOME_FASTA="ucscHg19Genome.fa.gz"
wget "${HG19_FTP_GENOME_URL}${HG19_GENOME_FASTA_FILE}"  --directory-prefix="${HUMAN_GENOME_DIR}"
echo "Saving Gzipped Hg38 Genome Under: ${HUMAN_GENOME_DIR}/${HG19_GENOME_FASTA}"
tar -xOzf "${HUMAN_GENOME_DIR}/${HG19_GENOME_FASTA_FILE}" | cat > "${HUMAN_GENOME_DIR}/${HG19_GENOME_FASTA}"
echo "Done Processing Hg38 Genome"

# Repeats Regions
HG19_REGIONS_FILE="ucscHg19Alu.bed.gz"
HG19_REGIONS_TABLE_FILE="rmsk.txt.gz"
echo "Downloading HG19 Alu Repeats Table ${HG19_FTP_URL}${HG19_REGIONS_TABLE_FILE}"
wget "${HG19_FTP_URL}${HG19_REGIONS_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing HG19 RefSeq Curated Table ${HG19_REGIONS_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG19_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($13 ~/Alu/ && $6 !~/_/) {print $6,$7,$8}' | gzip > "${HUMAN_REGIONS_DIR}/${HG19_REGIONS_FILE}"
rm "${HUMAN_REFSEQ_DIR}/${HG19_REGIONS_TABLE_FILE}"
echo "Done Processing HG19 Alu Repeats Table ${HG19_REGIONS_TABLE_FILE}"

# SNPs
HG19_SNPS_FILE="ucscHg19CommonGenomicSNPs150.bed.gz"
HG19_SNPS_TABLE_FILE="snp150Common.txt.gz"
echo "Downloading HG19 Common Genomic SNPs Table ${HG19_FTP_URL}${HG19_SNPS_TABLE_FILE}"
wget "${HG19_FTP_URL}${HG19_SNPS_TABLE_FILE}"  --directory-prefix="${HUMAN_SNPS_DIR}"
echo "Processing HG19 RefSeq Curated Table ${HG19_SNPS_TABLE_FILE}"
zcat "${HUMAN_SNPS_DIR}/${HG19_SNPS_TABLE_FILE}" | awk '{OFS ="\t"}($11=="genomic") {print $2,$3,$4,$7,$9,$10,$16,$25}'| gzip > "${HUMAN_SNPS_DIR}/${HG19_SNPS_FILE}"
rm "${HUMAN_SNPS_DIR}/${HG19_SNPS_TABLE_FILE}"
echo "Done Processing HG19 Common Genomic SNPs Table ${HG19_SNPS_TABLE_FILE}"

# RefSeq
HG19_REFSEQ_TABLE_FILE="ncbiRefSeqCurated.txt.gz"
HG19_REFSEQ_FILE="ucscHg19RefSeqCurated.bed.gz"
echo "Downloading HG19 RefSeq Curated Table ${HG19_FTP_URL}${HG19_REFSEQ_TABLE_FILE}"
wget "${HG19_FTP_URL}${HG19_REFSEQ_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing HG19 RefSeq Curated Table ${HG19_REFSEQ_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG19_REFSEQ_TABLE_FILE}"| awk '{OFS ="\t"} {print $3,$5,$6,$2,$13,$4,$10,$11}' |gzip > "${HUMAN_REFSEQ_DIR}/${HG19_REFSEQ_FILE}"
rm "${HUMAN_REFSEQ_DIR}/${HG19_REFSEQ_TABLE_FILE}"
echo "Done Processing HG19 RefSeq Curated Table ${HG19_REFSEQ_TABLE_FILE}"

# Genes Expression
HG19_GENES_EXPRESSION_FILE="ucscHg19GTExGeneExpression.bed.gz"
HG19_GENES_EXPRESSION_TABLE_FILE="gtexGene.txt.gz"
echo "Downloading Hg19 Genes Expression Table ${HG19_FTP_URL}${HG19_GENES_EXPRESSION_TABLE_FILE}"
wget "${HG19_FTP_URL}${HG19_GENES_EXPRESSION_TABLE_FILE}"  --directory-prefix="${HUMAN_GENES_EXPRESSION_DIR}"
echo "Processing Hg19 RefSeq Curated Table ${HG19_GENES_EXPRESSION_TABLE_FILE}"
zcat "${HUMAN_GENES_EXPRESSION_DIR}/${HG19_GENES_EXPRESSION_TABLE_FILE}" | awk '{OFS ="\t"} {print $1,$2,$3,$4,$10,$6}'| gzip > "${HUMAN_GENES_EXPRESSION_DIR}/${HG19_GENES_EXPRESSION_FILE}"
rm "${HUMAN_GENES_EXPRESSION_DIR}/${HG19_GENES_EXPRESSION_TABLE_FILE}"
echo "Done Processing Hg19 Genes Expression Table ${HG19_GENES_EXPRESSION_TABLE_FILE}"

#---------------------------------------------------------------------------
# MM10
#---------------------------------------------------------------------------
MM10_FTP_URL="http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/"

echo "Started Downloading MM10 Files:"

# Genome
MM10_FTP_GENOME_URL="http://hgdownload.soe.ucsc.edu/goldenPath/MM10/bigZips/"
MM10_GENOME_FASTA_FILE="chromFa.tar.gz"
echo "Downloading Hg38 Genome: ${MM10_FTP_GENOME_URL}${MM10_GENOME_FASTA_FILE}"
MM10_GENOME_FASTA="ucscMm10Genome.fa.gz"
wget "${MM10_FTP_GENOME_URL}${MM10_GENOME_FASTA_FILE}"  --directory-prefix="${HUMAN_GENOME_DIR}"
echo "Saving Gzipped Hg38 Genome Under: ${HUMAN_GENOME_DIR}/${MM10_GENOME_FASTA}"
tar -xOzf "${HUMAN_GENOME_DIR}/${MM10_GENOME_FASTA_FILE}" | cat > "${HUMAN_GENOME_DIR}/${MM10_GENOME_FASTA}"
echo "Done Processing Hg38 Genome"

# Repeats Regions
MM10_REGIONS_FILE="ucscMM10Alu.bed.gz"
MM10_REGIONS_TABLE_FILE="rmsk.txt.gz"
echo "Downloading MM10 Alu Repeats Table ${MM10_FTP_URL}${MM10_REGIONS_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_REGIONS_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_REGIONS_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($13 ~/Alu/) {print $6,$7,$8}' | gzip > "${HUMAN_REGIONS_DIR}/${MM10_REGIONS_FILE}"
rm "${HUMAN_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"
echo "Done Processing MM10 Alu Repeats Table ${MM10_REGIONS_TABLE_FILE}"

# SNPs
MM10_SNPS_FILE="ucscMM10CommonGenomicSNPs150.bed.gz"
MM10_SNPS_TABLE_FILE="snp150Common.txt.gz"
echo "Downloading MM10 Common Genomic SNPs Table ${MM10_FTP_URL}${MM10_SNPS_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_SNPS_TABLE_FILE}"  --directory-prefix="${HUMAN_SNPS_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_SNPS_TABLE_FILE}"
zcat "${HUMAN_SNPS_DIR}/${MM10_SNPS_TABLE_FILE}" | awk '{OFS ="\t"}($11=="genomic") {print $2,$3,$4,$7,$9,$10,$16,$25}'| gzip > "${HUMAN_SNPS_DIR}/${MM10_SNPS_FILE}"
rm "${HUMAN_SNPS_DIR}/${MM10_SNPS_TABLE_FILE}"
echo "Done Processing MM10 Common Genomic SNPs Table ${MM10_SNPS_TABLE_FILE}"

# RefSeq
MM10_REFSEQ_TABLE_FILE="ncbiRefSeqCurated.txt.gz"
MM10_REFSEQ_FILE="ucscMM10RefSeqCurated.bed.gz"
echo "Downloading MM10 RefSeq Curated Table ${MM10_FTP_URL}${MM10_REFSEQ_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_REFSEQ_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_REFSEQ_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${MM10_REFSEQ_TABLE_FILE}"| awk '{OFS ="\t"} {print $3,$5,$6,$2,$13,$4,$10,$11}' |gzip > "${HUMAN_REFSEQ_DIR}/${MM10_REFSEQ_FILE}"
rm "${HUMAN_REFSEQ_DIR}/${MM10_REFSEQ_TABLE_FILE}"
echo "Done Processing MM10 RefSeq Curated Table ${MM10_REFSEQ_TABLE_FILE}"

# Genes Expression
MM10_GENES_EXPRESSION_FILE="ucscMM10GTExGeneExpression.bed.gz"
MM10_GENES_EXPRESSION_TABLE_FILE="gtexGene.txt.gz"
echo "Downloading MM10 Genes Expression Table ${MM10_FTP_URL}${MM10_GENES_EXPRESSION_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_GENES_EXPRESSION_TABLE_FILE}"  --directory-prefix="${HUMAN_GENES_EXPRESSION_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_GENES_EXPRESSION_TABLE_FILE}"
zcat "${HUMAN_GENES_EXPRESSION_DIR}/${MM10_GENES_EXPRESSION_TABLE_FILE}" | awk '{OFS ="\t"} {print $1,$2,$3,$4,$10,$6}'| gzip > "${HUMAN_GENES_EXPRESSION_DIR}/${MM10_GENES_EXPRESSION_FILE}"
rm "${HUMAN_GENES_EXPRESSION_DIR}/${MM10_GENES_EXPRESSION_TABLE_FILE}"
echo "Done Processing MM10 Genes Expression Table ${MM10_GENES_EXPRESSION_TABLE_FILE}"
