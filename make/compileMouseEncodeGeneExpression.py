import gzip
import os
import sys
from csv import reader


def compile_mouse_endoce_gene_expression(base_dir, outfile, refseq_file):
    res = dict()
    refseq = dict()
    with gzip.open(refseq_file) as ref:
        data = [l for l in reader(ref, delimiter="\t")]
        gene_id_i = 1
        chr_i = 2
        strand_i = 3
        start_i = 4
        end_i = 5
        name_i = 12
        for l in data:
            gene = l[gene_id_i].split(".")[0]
            chrom = l[chr_i]
            start = l[start_i]
            end = l[end_i]
            strand = l[strand_i]
            name = l[name_i]
            gene_d = dict(chrom=chrom, start=start, end=end, strand=strand, name=name)
            refseq[gene] = gene_d

    for root, dirs, files in os.walk(base_dir):
        for ifile in files:
            with open(os.path.join(root, ifile)) as ge:
                data = [l for l in reader(ge, delimiter="\t")]
                headers = data[0]
                gene_id_i = headers.index("gene_id")
                counts = headers.index("FPKM")
                data = data[1:]

                for rec in data:
                    res.setdefault(rec[gene_id_i],list()).append(rec[counts])

    with gzip.open(outfile, 'wb') as out:
        output = list()
        for gene, counts in res.iteritems():
            rec = refseq.get(gene, None)
            if None is rec:
                continue
            output.append("\t".join([rec["chrom"], rec["start"], rec["end"], rec["name"], ",".join(counts), rec["strand"]]))


        out.write("\n".join(output))


if __name__ == "__main__":
    compile_mouse_endoce_gene_expression(sys.argv[1], sys.argv[2], sys.argv[3])
