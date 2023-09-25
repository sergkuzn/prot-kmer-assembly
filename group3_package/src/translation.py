#!/usr/bin/env python

import re
from Bio.Blast import NCBIWWW
import time

#input = merged sequence
#dna = "AAAGGCCCTCTCTTTGAGAACCTCTCTAGCCCCATTTCGC"

def transcribe(dna):
    #transcribe dna to rna
    #input: dna as str
    #output: two str

    to_rna = {"A": "U", "T": "A", "C": "G", "G": "C"}  # for complimentary strand
    rna_comp = ""  # empty string
    for base in dna:  # for each base find complimentary base and add to rna string
        rna_comp = rna_comp + to_rna[base]

    rna = dna.replace("T", "U")  # for same strand

    return rna_comp, rna


def translate(mrna):
    #translate mrna to protein (open reading frame)
    #input: mrna str
    #output: list of amino acid strs

    to_protein = {'AUA': 'I', 'AUC': 'I', 'AUU': 'I', 'AUG': 'M', 'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',
                  'AAC': 'N', 'AAU': 'N',
                  'AAA': 'K', 'AAG': 'K', 'AGC': 'S', 'AGU': 'S', 'AGA': 'R', 'AGG': 'R', 'CUA': 'L', 'CUC': 'L',
                  'CUG': 'L', 'CUU': 'L',
                  'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P', 'CAC': 'H', 'CAU': 'H', 'CAA': 'Q', 'CAG': 'Q',
                  'CGA': 'R', 'CGC': 'R',
                  'CGG': 'R', 'CGU': 'R', 'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V', 'GCA': 'A', 'GCC': 'A',
                  'GCG': 'A', 'GCU': 'A',
                  'GAC': 'D', 'GAU': 'D', 'GAA': 'E', 'GAG': 'E', 'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G',
                  'UCA': 'S', 'UCC': 'S',
                  'UCG': 'S', 'UCU': 'S', 'UUC': 'F', 'UUU': 'F', 'UUA': 'L', 'UUG': 'L', 'UAC': 'Y', 'UAU': 'Y',
                  'UAA': 'STOP',
                  'UAG': 'STOP', 'UGC': 'C', 'UGU': 'C', 'UGA': 'STOP', 'UGG': 'W'}

    proteins = []

    for start in re.finditer('AUG', mrna):  # find start position
        seq = mrna[start.span()[0]:]  # mrna starting at start position

        protein = ""  # for each codon append the aminoacid string with the corresponding aminoacid
        for pos in range(0, len(seq) - 3, 3):  # reading frame/codon positions
            codon = seq[pos:pos + 3]
            if len(codon) < 3:
                break
            if to_protein[codon] != 'STOP':
                aminoacid = to_protein[codon]
                protein = protein + aminoacid
            else:  # stop appending aminoacids once a stop-codon is reached
                break

        proteins.append(protein[1:])
    return proteins


# amino acid sequence
# sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
# 'insulin isoform UB [Homo sapiens]'

def request_blastp(sequence):
    # input: amino acid sequence: str
    # output: predicted protein: str
    # this function requests results in BLAST

    # limit requests to once every 10 seconds, because in the blast API documentation: "Do not contact the server more often than once every 10 seconds."
    time.sleep(11)
    result_handle = NCBIWWW.qblast("blastp", "nr", sequence)
    blast_results = result_handle.read()
    try:
        data = blast_results.split("<Hit_def>")[1].split("</Hit_def>")[0]
        return data
    except:
        return -1

