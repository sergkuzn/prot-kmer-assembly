import os


def parse(path):
    """Open and return given fastq or fasta file
    :param
    Input: path to fastq or/fasta file
    Output: list of sequences"""

    ext = path.split(".")[-1]

    if ext == "fastq":
        with open(path, 'r') as file:
            file = file.read().split("\n")
            parsed_seqs = file[1::4]

    elif ext in ["fasta", "fa"]:
        with open(path, 'r') as file:
            file = file.read().split(">")
            parsed_seqs = [seq.split("\n", 1)[1].replace("\n", "") for seq in file[1:]]

    return parsed_seqs
