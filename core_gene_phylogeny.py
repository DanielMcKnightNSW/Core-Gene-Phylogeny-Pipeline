# This script takes GFF3 files from Bakta and produces a maximum likelihood core gene tree with 100 
# boostrap replciates called clonalframeml_out.labelled_tree.newick
import os
import subprocess
import sys

#How many cores do you want to utilise 
num_cores = sys.argv[1]

bakta_out = "bakta_out"
os.makedirs(bakta_out, exist_ok=True)

#1. Creates a list of GFFs for panaroo. GFFs must be in a subdirectory within the bakta_out directory
gff_files = []
for sample in os.listdir(bakta_out):
    gff_path = os.path.join(bakta_out, sample, f"{sample}.gff3")
    if os.path.exists(gff_path):
        gff_files.append(gff_path)

#2. Run Panaroo using GFFs from Bakta
panaroo_out = "results"
os.makedirs(panaroo_out, exist_ok=True)
core_gene_alignment = os.path.join(panaroo_out, "core_gene_alignment.aln")
if not os.path.exists(core_gene_alignment):
    subprocess.run(["panaroo", "-i"] + gff_files + ["-o", panaroo_out,"--clean-mode", "strict","-a", 
    "core","--core_threshold", "0.9999","--aligner", "mafft","-t", num_cores])

#3. Trim Panaroo core gene alignment with trimal
trimmed_aln = os.path.join(panaroo_out, "core_gene_alignment.trimmed.aln")
if not os.path.exists(trimmed_aln):
    subprocess.run(["trimal", "-in", core_gene_alignment, "-out", trimmed_aln, "-automated1"])

#4. Generate a phylogeny using the panaroo core gene alignment using iqtree
iqtree_prefix = os.path.join(panaroo_out, "core_gene_alignment.trimmed.aln")
treefile = iqtree_prefix + ".treefile"
if not os.path.exists(treefile):
    subprocess.run(["iqtree", "-b 100", "-s", trimmed_aln, "-m", "GTR+G", "-nt", num_cores])

#5. Run clonalframeML to filter recombination
clonalframeml_out = os.path.join(panaroo_out, "clonalframeml_out")
if not os.path.exists(clonalframeml_out):
    subprocess.run(["ClonalFrameML", treefile, trimmed_aln, clonalframeml_out])

print("\nAnalysis complete. The final phylogeny is:",clonalframeml_out)