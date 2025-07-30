import os
import subprocess
import sys

# Input your [1] location to directory of fasta files [2] number of cores for bakta to use [3] location to your bakta database
input_dir = sys.argv[1].strip()
num_cores = sys.argv[2].strip()
bakta_db = sys.argv[3].strip()

bakta_out = "bakta_out"
os.makedirs(bakta_out, exist_ok=True)


#Annotate with Bakta 
for fasta in os.listdir(input_dir):
    if fasta.endswith(".fasta") or fasta.endswith(".fa"):
        sample = os.path.splitext(fasta)[0]
        outdir = os.path.join(bakta_out, sample)
        os.makedirs(outdir, exist_ok=True)
        subprocess.run([
            "bakta","--force","--output", outdir,
            "--prefix", sample,
            "--threads", num_cores,
            "--db", bakta_db,
            os.path.join(input_dir, fasta)
        ], check=True)