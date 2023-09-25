from pydantic import BaseModel
from pydantic.schema import Optional

class Reset(BaseModel):
    data_reset: bool

class AminoAcids(BaseModel):
    dna_file_uploaded: bool
    dna_sequence_assembled: Optional[bool]
    mRNA_assembled: Optional[bool]
    amino_acids_and_proteins: Optional[dict]

class MRNA(BaseModel):
    dna_file_uploaded: bool
    dna_sequence_assembled: Optional[bool]
    mRNA: Optional[str]

class DNASequence(BaseModel):
    dna_file_uploaded: bool
    assembled_dna: Optional[str]

class Upload(BaseModel):
    successfully_uploaded: bool
    error: Optional[str]
