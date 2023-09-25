"""Tests for the TRANSLATION and protein prediction."""

from src import translation

class TestTranslation:

    def test_transcribe(self):
        """check if rna is correct"""
        dna = "AAGGCCCTCT"
        rna_comp = "UUCCGGGAGA"
        rna = "AAGGCCCUCU"
        check_rna_comp, check_rna = translation.transcribe(dna)
        assert (rna_comp == check_rna_comp) is True
        assert (rna == check_rna) is True

    def test_translate(self):
        """check if protein is correct"""
        rna = "UAUGAAUAUCAAUGCUUGAAUCUGAGAAUUGA"
        protein = ["NINA","LESEN"]
        check_protein = translation.translate(rna)
        assert (protein == check_protein) is True

   # we decided to remove this test, because it depends on the BLAST API and not code that we wrote
    #def test_blast(self):
   #     """check if blast predicts protein"""
   #     sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
     #   prediction = translation.request_blastp(sequence)
     #   assert (prediction == 'insulin isoform UB [Homo sapiens]') is True
