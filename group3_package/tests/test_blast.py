from src import blast
from src import parser
from src.translation import transcribe, translate


def get_Homo_sapiens_CXCR5_aa_seqs():
    # one_dna = parser.parse('data/Homo_sapiens_CXCR5_sequence.fa')[0]
    # rna_mrna_seqs = transcribe(one_dna)
    # amino_seqs = []
    # for rna_mrna_seq in rna_mrna_seqs:
    #     amino_seqs += translate(rna_mrna_seq)

    with open('data/Homo_sapiens_CXCR5_amino_acids.txt', 'r') as f:
        amino_seqs = f.read().split('\n')
    return amino_seqs


def create_reads_dataset_from_real_dna(one_dna, seq_len=100, coverage=10):
    import numpy as np

    start_indexes = np.random.randint(0, len(one_dna) - seq_len, seq_len * coverage)
    reads = [one_dna[start: start + seq_len] for start in start_indexes]

    with open(f'Homo_sapiens_CXCR5_sequence_len{seq_len}_cov{coverage}.fa', 'w') as f:
        for i, read in enumerate(reads):
            f.write(f'> seq{i}\n')
            f.write(read)
            f.write('\n')


class TestBlast:
    def test_blast_website(self):
        amino_seqs = get_Homo_sapiens_CXCR5_aa_seqs()
        amino_seqs = [s for s in amino_seqs if len(s) > 50]

        proteins = blast.blast_website(amino_seqs, docker=False)

        assert len(proteins) > 0
        assert 'C-X-C chemokine receptor type 5 isoform 1 [Homo sapiens]' in proteins
