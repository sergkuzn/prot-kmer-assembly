from src.translation import translate, transcribe

dna='CTCTGAGTTGCTATGTGACTGGGAACAGGATACTTCACCTCTCCATTCTTTCTCTCCTTT'
cdna,rna=transcribe(dna)
print(translate(cdna))
print(cdna)
