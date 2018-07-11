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
HG38_GENOME_FASTA="ucscHg38Genome.fa"
echo "Downloading Hg38 Genome: ${HG38_FTP_GENOME_URL}${HG38_GENOME_FASTA_FILE}"
wget "${HG38_FTP_GENOME_URL}${HG38_GENOME_FASTA_FILE}"  --directory-prefix="${HUMAN_GENOME_DIR}"
echo "Saving Gzipped Hg38 Genome Under: ${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA}"
gunzip -c "${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA_FILE}" > "${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA}"
rm "${HUMAN_GENOME_DIR}/${HG38_GENOME_FASTA_FILE}"
echo "Done Processing Hg38 Genome"

# Repeats Regions
HG38_REGIONS_FILE="ucscHg38Alu.bed.gz"
HG38_SINE_FILE="ucscHg38SINE.bed.gz"
HG38_RE_FILE="ucscHg38AllRE.bed.gz"
HG38_REGIONS_TABLE_FILE="rmsk.txt.gz"
echo "Downloading Hg38 Alu Repeats Table ${HG38_FTP_URL}${HG38_REGIONS_TABLE_FILE}"
wget "${HG38_FTP_URL}${HG38_REGIONS_TABLE_FILE}"  --directory-prefix="${HUMAN_REFSEQ_DIR}"
echo "Processing Hg38 RefSeq Curated Table ${HG38_REGIONS_TABLE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG38_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($13 ~/Alu/ && $6 !~/_/) {print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin| gzip > "${HUMAN_REGIONS_DIR}/${HG38_REGIONS_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG38_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($12 ~/Alu/ && $6 !~/_/) {print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin|  gzip > "${HUMAN_REGIONS_DIR}/${HG38_SINE_FILE}"
zcat "${HUMAN_REFSEQ_DIR}/${HG38_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($6 !~/_/) {print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin|  gzip > "${HUMAN_REGIONS_DIR}/${HG38_RE_FILE}"
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
HG19_GENOME_FASTA="ucscHg19Genome.fa"
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
zcat "${HUMAN_REFSEQ_DIR}/${HG19_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"}($13 ~/Alu/ && $6 !~/_/) {print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin|  gzip > "${HUMAN_REGIONS_DIR}/${HG19_REGIONS_FILE}"
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
MM10_FTP_GENOME_URL="http://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/"
MM10_GENOME_FASTA_FILE="chromFa.tar.gz"
echo "Downloading MM10 Genome: ${MM10_FTP_GENOME_URL}${MM10_GENOME_FASTA_FILE}"
MM10_GENOME_FASTA="ucscMm10Genome.fa"
wget "${MM10_FTP_GENOME_URL}${MM10_GENOME_FASTA_FILE}"  --directory-prefix="${MURINE_GENOME_DIR}"
echo "Saving Gzipped Hg38 Genome Under: ${MURINE_GENOME_DIR}/${MM10_GENOME_FASTA}"
tar -xOzf "${MURINE_GENOME_DIR}/${MM10_GENOME_FASTA_FILE}" | cat > "${MURINE_GENOME_DIR}/${MM10_GENOME_FASTA}"
echo "Done Processing Hg38 Genome"

# Repeats Regions
MM10_REGIONS_FILE="ucscMM10SINE_B1_B2.bed.gz"
MM10_SINE_FILE="ucscMM10AllSINE.bed.gz"
MM10_RE_FILE="ucscMM10AllRE.bed.gz"
MM10_REGIONS_TABLE_FILE="rmsk.txt.gz"
echo "Downloading MM10 Alu Repeats Table ${MM10_FTP_URL}${MM10_REGIONS_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_REGIONS_TABLE_FILE}"  --directory-prefix="${MURINE_REFSEQ_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_REGIONS_TABLE_FILE}"
zcat "${MURINE_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"} (($11 ~/^B1/||$13 ~/^B2/) && $12 == "SINE"){print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin|  gzip > "${MURINE_REGIONS_DIR}/${MM10_REGIONS_FILE}"
zcat "${MURINE_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"} ($12 == "SINE"){print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin|  gzip > "${MURINE_REGIONS_DIR}/${MM10_SINE_FILE}"
zcat "${MURINE_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"} {print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin| gzip > "${MURINE_REGIONS_DIR}/${MM10_RE_FILE}"
rm "${MURINE_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"
echo "Done Processing MM10 Alu Repeats Table ${MM10_REGIONS_TABLE_FILE}"

# SNPs
MM10_SNPS_FILE="ucscMM10CommonGenomicSNPs150.bed.gz"
MM10_SNPS_TABLE_FILE="snp150Common.txt.gz"
echo "Downloading MM10 Common Genomic SNPs Table ${MM10_FTP_URL}${MM10_SNPS_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_SNPS_TABLE_FILE}"  --directory-prefix="${MURINE_SNPS_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_SNPS_TABLE_FILE}"
zcat "${MURINE_SNPS_DIR}/${MM10_SNPS_TABLE_FILE}" | awk '{OFS ="\t"}($11=="genomic") {print $2,$3,$4,$7,$9,$10,$16,$25}'| gzip > "${MURINE_SNPS_DIR}/${MM10_SNPS_FILE}"
rm "${MURINE_SNPS_DIR}/${MM10_SNPS_TABLE_FILE}"
echo "Done Processing MM10 Common Genomic SNPs Table ${MM10_SNPS_TABLE_FILE}"

# RefSeq
MM10_REFSEQ_TABLE_FILE="ncbiRefSeqCurated.txt.gz"
MM10_REFSEQ_FILE="ucscMM10RefSeqCurated.bed.gz"
echo "Downloading MM10 RefSeq Curated Table ${MM10_FTP_URL}${MM10_REFSEQ_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_REFSEQ_TABLE_FILE}"  --directory-prefix="${MURINE_REFSEQ_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_REFSEQ_TABLE_FILE}"
zcat "${MURINE_REFSEQ_DIR}/${MM10_REFSEQ_TABLE_FILE}"| awk '{OFS ="\t"} {print $3,$5,$6,$2,$13,$4,$10,$11}' |gzip > "${MURINE_REFSEQ_DIR}/${MM10_REFSEQ_FILE}"
rm "${MURINE_REFSEQ_DIR}/${MM10_REFSEQ_TABLE_FILE}"
echo "Done Processing MM10 RefSeq Curated Table ${MM10_REFSEQ_TABLE_FILE}"

# Genes Expression
MM10_GENES_EXPRESSION_FILE="ucscMM10GTExGeneExpression.bed.gz"
MM10_GENES_EXPRESSION_TABLE_FILE="gtexGene.txt.gz"
echo "Downloading MM10 Genes Expression Table ${MM10_FTP_URL}${MM10_GENES_EXPRESSION_TABLE_FILE}"
wget "${MM10_FTP_URL}${MM10_GENES_EXPRESSION_TABLE_FILE}"  --directory-prefix="${MURINE_GENES_EXPRESSION_DIR}"
echo "Processing MM10 RefSeq Curated Table ${MM10_GENES_EXPRESSION_TABLE_FILE}"
zcat "${MURINE_GENES_EXPRESSION_DIR}/${MM10_GENES_EXPRESSION_TABLE_FILE}" | awk '{OFS ="\t"} {print $1,$2,$3,$4,$10,$6}'| gzip > "${MURINE_GENES_EXPRESSION_DIR}/${MM10_GENES_EXPRESSION_FILE}"
rm "${MURINE_GENES_EXPRESSION_DIR}/${MM10_GENES_EXPRESSION_TABLE_FILE}"
echo "Done Processing MM10 Genes Expression Table ${MM10_GENES_EXPRESSION_TABLE_FILE}"


#---------------------------------------------------------------------------
# MM9
#---------------------------------------------------------------------------
MM9_FTP_URL="http://hgdownload.soe.ucsc.edu/goldenPath/mm9/database/"

echo "Started Downloading MM9 Files:"

# Genome
MM9_FTP_GENOME_URL="http://hgdownload.soe.ucsc.edu/goldenPath/MM9/bigZips/"
MM9_GENOME_FASTA_FILE="chromFa.tar.gz"
echo "Downloading MM9 Genome: ${MM9_FTP_GENOME_URL}${MM9_GENOME_FASTA_FILE}"
MM9_GENOME_FASTA="ucscMM9Genome.fa"
wget "${MM9_FTP_GENOME_URL}${MM9_GENOME_FASTA_FILE}"  --directory-prefix="${MURINE_GENOME_DIR}"
echo "Saving Gzipped Hg38 Genome Under: ${MURINE_GENOME_DIR}/${MM9_GENOME_FASTA}"
tar -xOzf "${MURINE_GENOME_DIR}/${MM9_GENOME_FASTA_FILE}" | cat > "${MURINE_GENOME_DIR}/${MM9_GENOME_FASTA}"
echo "Done Processing Hg38 Genome"

# Repeats Regions
MM9_REGIONS_FILE="ucscMM9SINE_B1_B2.bed.gz"
MM9_SINE_FILE="ucscMM9AllSINE.bed.gz"
MM9_RE_FILE="ucscMM9AllRE.bed.gz"
MM9_REGIONS_TABLE_FILE="rmsk.txt.gz"
echo "Downloading MM9 Alu Repeats Table ${MM9_FTP_URL}${MM9_REGIONS_TABLE_FILE}"
wget "${MM9_FTP_URL}${MM9_REGIONS_TABLE_FILE}"  --directory-prefix="${MURINE_REFSEQ_DIR}"
echo "Processing MM9 RefSeq Curated Table ${MM9_REGIONS_TABLE_FILE}"
zcat "${MURINE_REFSEQ_DIR}/${MM10_REGIONS_TABLE_FILE}"| awk '{OFS ="\t"} (($11 ~/^B1/||$13 ~/^B2/) && $12 == "SINE"){print $6,$7,$8}' | ${BEDTOOLS_PATH} sort -i stdin| ${BEDTOOLS_PATH} merge -i stdin| gzip > "${MURINE_REGIONS_DIR}/${MM9_REGIONS_FILE}"
rm "${MURINE_REFSEQ_DIR}/${MM9_REGIONS_TABLE_FILE}"
echo "Done Processing MM9 Alu Repeats Table ${MM9_REGIONS_TABLE_FILE}"

# SNPs
MM9_SNPS_FILE="ucscMM9CommonGenomicSNPs150.bed.gz"
MM9_SNPS_TABLE_FILE="snp150Common.txt.gz"
echo "Downloading MM9 Common Genomic SNPs Table ${MM9_FTP_URL}${MM9_SNPS_TABLE_FILE}"
wget "${MM9_FTP_URL}${MM9_SNPS_TABLE_FILE}"  --directory-prefix="${MURINE_SNPS_DIR}"
echo "Processing MM9 RefSeq Curated Table ${MM9_SNPS_TABLE_FILE}"
zcat "${MURINE_SNPS_DIR}/${MM9_SNPS_TABLE_FILE}" | awk '{OFS ="\t"}($11=="genomic") {print $2,$3,$4,$7,$9,$10,$16,$25}'| gzip > "${MURINE_SNPS_DIR}/${MM9_SNPS_FILE}"
rm "${MURINE_SNPS_DIR}/${MM9_SNPS_TABLE_FILE}"
echo "Done Processing MM9 Common Genomic SNPs Table ${MM9_SNPS_TABLE_FILE}"

# RefSeq
MM9_REFSEQ_TABLE_FILE="ncbiRefSeqCurated.txt.gz"
MM9_REFSEQ_FILE="ucscMM9RefSeqCurated.bed.gz"
echo "Downloading MM9 RefSeq Curated Table ${MM9_FTP_URL}${MM9_REFSEQ_TABLE_FILE}"
wget "${MM9_FTP_URL}${MM9_REFSEQ_TABLE_FILE}"  --directory-prefix="${MURINE_REFSEQ_DIR}"
echo "Processing MM9 RefSeq Curated Table ${MM9_REFSEQ_TABLE_FILE}"
zcat "${MURINE_REFSEQ_DIR}/${MM9_REFSEQ_TABLE_FILE}"| awk '{OFS ="\t"} {print $3,$5,$6,$2,$13,$4,$10,$11}' |gzip > "${MURINE_REFSEQ_DIR}/${MM9_REFSEQ_FILE}"
rm "${MURINE_REFSEQ_DIR}/${MM9_REFSEQ_TABLE_FILE}"
echo "Done Processing MM9 RefSeq Curated Table ${MM9_REFSEQ_TABLE_FILE}"

# Genes Expression
MM9_GENES_EXPRESSION_FILE="ucscMM9GTExGeneExpression.bed.gz"
MM9_GENES_EXPRESSION_TABLE_FILE="gtexGene.txt.gz"
echo "Downloading MM9 Genes Expression Table ${MM9_FTP_URL}${MM9_GENES_EXPRESSION_TABLE_FILE}"
wget "${MM9_FTP_URL}${MM9_GENES_EXPRESSION_TABLE_FILE}"  --directory-prefix="${MURINE_GENES_EXPRESSION_DIR}"
echo "Processing MM9 RefSeq Curated Table ${MM9_GENES_EXPRESSION_TABLE_FILE}"
zcat "${MURINE_GENES_EXPRESSION_DIR}/${MM9_GENES_EXPRESSION_TABLE_FILE}" | awk '{OFS ="\t"} {print $1,$2,$3,$4,$10,$6}'| gzip > "${MURINE_GENES_EXPRESSION_DIR}/${MM9_GENES_EXPRESSION_FILE}"
rm "${MURINE_GENES_EXPRESSION_DIR}/${MM9_GENES_EXPRESSION_TABLE_FILE}"
echo "Done Processing MM9 Genes Expression Table ${MM9_GENES_EXPRESSION_TABLE_FILE}"

#---------------------------------------------------------------------------
# Create INI File
#---------------------------------------------------------------------------
DBS_PATHS_INI="${RESOURCES_DIR}/ResourcesPaths.ini"
echo "[DEFAULTS]" >> ${DBS_PATHS_INI}
echo "ResourcesDir = ${RESOURCES_DIR}" >> ${DBS_PATHS_INI}
echo "bedtools_path = ${BEDTOOLS_PATH}" >> ${DBS_PATHS_INI}
echo "samtools_path = ${SAMTOOLS_PATH}" >> ${DBS_PATHS_INI}

echo "[hg38]" >> ${DBS_PATHS_INI}
echo "Genome = ${HG38_GENOME_FASTA}" >> ${DBS_PATHS_INI}
echo "RERegion = ${HG38_REGIONS_FILE}" >> ${DBS_PATHS_INI}
echo "SNPs = ${HG38_SNPS_FILE}" >> ${DBS_PATHS_INI}
echo "RefSeq = ${HG38_REFSEQ_FILE}" >> ${DBS_PATHS_INI}
echo "GeneExpression = ${HG38_GENES_EXPRESSION_FILE}" >> ${DBS_PATHS_INI}
echo "" >> ${DBS_PATHS_INI}

echo "[hg19]" >> ${DBS_PATHS_INI}
echo "Genome = ${HG19_GENOME_FASTA}" >> ${DBS_PATHS_INI}
echo "RERegion = ${HG19_REGIONS_FILE}" >> ${DBS_PATHS_INI}
echo "SNPs = ${HG19_SNPS_FILE}" >> ${DBS_PATHS_INI}
echo "RefSeq = ${HG19_REFSEQ_FILE}" >> ${DBS_PATHS_INI}
echo "GeneExpression = ${HG19_GENES_EXPRESSION_FILE}" >> ${DBS_PATHS_INI}
echo "" >> ${DBS_PATHS_INI}

echo "[mm10]" >> ${DBS_PATHS_INI}
echo "Genome = ${MM10_GENOME_FASTA}" >> ${DBS_PATHS_INI}
echo "RERegion = ${MM10_REGIONS_FILE}" >> ${DBS_PATHS_INI}
echo "SNPs = ${MM10_SNPS_FILE}" >> ${DBS_PATHS_INI}
echo "RefSeq = ${MM10_REFSEQ_FILE}" >> ${DBS_PATHS_INI}
echo "GeneExpression = ${MM10_GENES_EXPRESSION_FILE}" >> ${DBS_PATHS_INI}
echo "" >> ${DBS_PATHS_INI}

echo "[mm9]" >> ${DBS_PATHS_INI}
echo "Genome = ${MM9_GENOME_FASTA}" >> ${DBS_PATHS_INI}
echo "RERegion = ${MM9_REGIONS_FILE}" >> ${DBS_PATHS_INI}
echo "SNPs = ${MM9_SNPS_FILE}" >> ${DBS_PATHS_INI}
echo "RefSeq = ${MM9_REFSEQ_FILE}" >> ${DBS_PATHS_INI}
echo "GeneExpression = ${MM9_GENES_EXPRESSION_FILE}" >> ${DBS_PATHS_INI}
echo "" >> ${DBS_PATHS_INI}

