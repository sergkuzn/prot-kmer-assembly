import click

from src.parser import parse
from src.scs import greedy_scs_heap, scs
from src import scs as dna_assembly
from src.translation import transcribe, translate, request_blastp
from src import blast


@click.group()
def cli():
    pass


@cli.command()
@click.option('-f', '--fastq-file', default=None, required=True, help="fastq-file path")
def run_parser(fastq_file):
    print(parse(fastq_file))
    parse(fastq_file)


@cli.command()
@click.option('-l', '--input-list', default=None, required=True, help="fastq file")
def quick_assemble(input_list):
    """Takes reasonable time"""
    print(greedy_scs_heap(parse(input_list)))
    greedy_scs_heap(parse(input_list))


@cli.command()
@click.option('-l', '--input-list', default=None, required=True, help="fastq file")
def slow_assemble(input_list):
    """solution guaranteed"""
    print(scs(parse(input_list)))
    scs(parse(input_list))


@cli.command()
@click.option('-d', '--input-dna', default=None, required=True, help="list of dna string")
@click.option('-o', '--output', default='transcribed_dna_output.txt', help='Name of the output file')
def transcribe_dna(input_dna: str, output: str):
    """transcibe given dna into mrna
    input = merged sequence
    dna = 'AAAGGCCCTCTCTTTGAGAACCTCTCTAGCCCCATTTCGC'
    """
    mrna, rna = transcribe(input_dna)
    print(mrna)
    with open(output, "w") as file:
        file.write(mrna)


# ------------------

@cli.command()
@click.option('-m', '--input-mrna', default=None, required=True, help="list of mrna string")
@click.option('-o', '--output', default='translated_mrna_output.txt', help='Name of the output file')
def translate_rna(input_mrna: str, output: str):
    """translate from mrna into sequence of amino-acids
    translate mrna to protein (open reading frame)
    input: mrna str
    output: list of amino acid strs
"""
    print(translate(input_mrna))
    result = translate(input_mrna)
    with open(output, "w") as file:
        file.write(result)


@cli.command()
@click.option('-s', '--sequence', default=None, required=True, help="sequence of amino acid string")
def blast_request(sequence: str):
    """Requests results in BLAST from sequence of possible amino-acid to get Predicted Protein
    time requests to once every 10 second, as per blast API documentation
    :param
    Input: amino acid sequence:str
    Output: Predicted Protein:str
    """
    print(request_blastp(sequence))


@cli.command()
@click.option('--file', required=True, help="FASTA/FASTQ file")
@click.option('--algo', default='heap', help="heap, dict, matrix, scs")
@click.option('--chrome', is_flag=True, default=False, help="Use selenium + Chrome browser for BLAST (otherwise API)")
def run(file: str, algo: str, chrome: bool):
    """
    Determine the list of proteins from dna reads.
    """
    if algo == 'heap':
        algo = dna_assembly.greedy_scs_heap
    elif algo == 'dict':
        algo = dna_assembly.greedy_scs_dict
    elif algo == 'matrix':
        algo = dna_assembly.greedy_scs_matrix
    elif algo == 'scs':
        algo = dna_assembly.scs
    else:
        raise RuntimeError(f'Wrong algo value {algo}')

    dna_seqs = parse(file)
    one_dna = algo(dna_seqs)
    rna_mrna_seqs = transcribe(one_dna)

    amino_seqs = []
    for rna_mrna_seq in rna_mrna_seqs:
        amino_seqs += translate(rna_mrna_seq)

    amino_seqs = [s for s in amino_seqs if len(s) >= 20]

    if chrome:
        proteins = blast.blast_website(amino_seqs, docker=False)
        print(f'Found {len(proteins)}')
        print('Top 10:')
        for p in proteins[:10]:
            print(p)
    else:
        print('Warning: Chrome not used, might be slow.')
        for amino_seq in amino_seqs:
            print(request_blastp(amino_seq))


if __name__ == '__main__':
    # cd group3
    # src run --chrome --file group3_package/tests/data/Homo_sapiens_CXCR5_sequence_len100_cov10.fa

    cli()
