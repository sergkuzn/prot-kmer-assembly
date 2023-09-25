import uvicorn
from fastapi import FastAPI, UploadFile
import aiofiles
from pathlib import Path
import models
import os
from src.parser import parse
from src.translation import transcribe, translate, request_blastp
from src.scs import greedy_scs_heap
from src.blast import blast_website
import sys
from fastapi.middleware.cors import CORSMiddleware
import argparse
import logging


apiapp = FastAPI(title="Group 3's API",
                 description="This API is used for group3 in Programming Lab 2. It will be used to serve as communcation between the python package and Vue.js front end server.",
                 contact={"email": "lmichael96@gmail.com"})

apiapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8888, help="port number for the API")
parser.add_argument("--num_cores", type=int, default=1, help="number of cores to use")
args = parser.parse_args()

PORT = args.port
NUM_CORES=args.num_cores

class DNASequenceTracker:
    def __init__(self):
        self.file_uploaded = False
        self.dna_sequences = None
        self.assembled_dna = None
        self.mRNA_sequence = None
        self.amino_acids = None
        self.amino_acids_and_proteins = None
    
    def reset(self):
        self.__init__()

    def get_dna_sequence(self):
        if self.file_uploaded:
            if self.assembled_dna:
                return {'dna_file_uploaded': True, 'assembled_dna':self.assembled_dna}
            else:
                self.assembled_dna = greedy_scs_heap(strings=self.dna_sequences, num_cpu=NUM_CORES)
                return {'dna_file_uploaded': True, 'assembled_dna':self.assembled_dna}
        else:
            return {'dna_file_uploaded': False}
    
    def get_mRNA_sequence(self):
        if self.file_uploaded:
            if self.assembled_dna:
                if self.mRNA_sequence:
                    return {'dna_file_uploaded': True, 'dna_sequence_assembled': True, 'mRNA': self.mRNA_sequence}
                else:
                    self.mRNA_sequence = transcribe(self.assembled_dna)[1]
                    return {'dna_file_uploaded': True, 'dna_sequence_assembled': True, 'mRNA': self.mRNA_sequence}
            else:
                return {'dna_file_uploaded': True, 'dna_sequence_assembled': False}
        else:
            return {'dna_file_uploaded': False}
    
    def get_amino_acids(self):
        if self.file_uploaded:
            if self.assembled_dna:
                if self.mRNA_sequence:
                    if self.amino_acids_and_proteins:
                        return {'dna_file_uploaded': True, 'dna_sequence_assembled': True, 'mRNA_assembled': True, 'amino_acids_and_proteins': self.amino_acids_and_proteins}
                    else:
                        self.amino_acids = translate(self.mRNA_sequence)
                        try:
                            # loop through the amino acids and get the result from blast. Only save a a result is returned from blat
                            self.amino_acids_and_proteins = {}
                            amino_acids = ""
                            for amino_acid in self.amino_acids:
                                # define a minimum amino acid length:
                                if len(amino_acid) > 105:
                                    #------------------------------
                                    # amino_acids = amino_acids + f"\n{amino_acid}"
                                    self.amino_acids_and_proteins[amino_acid] = request_blastp(amino_acid)
                                else:
                                    continue
                                    #--------------------------------
                            # self.amino_acids_and_proteins = blast_website(self.amino_acids)
                            return {'dna_file_uploaded': True, 'dna_sequence_assembled': True, 'mRNA_assembled': True, 'amino_acids_and_proteins': self.amino_acids_and_proteins}
   
                        except Exception as e:
                            return {'dna_file_uploaded': True, 'dna_sequence_assembled': True, 'mRNA_assembled': True, 'error': "BLAST API Error"}
                else:
                    return {'dna_file_uploaded': True, 'dna_sequence_assembled': True, 'mRNA_assembled': False}

            else:
                return {'dna_file_uploaded': True, 'dna_sequence_assembled': False}
        else:
            return {'dna_file_uploaded': False}

            

    async def upload_file(self, dnaFile: UploadFile):
        try:
            # clear stored sequences when a new file is uploaded
            self.dna_sequences = None
            self.assembled_dna = None
            self.mRNA_sequence = None
            self.amino_acids = None
            tmp_dir = os.path.join(os.getcwd(), 'tmp')
            Path(tmp_dir).mkdir(parents=True, exist_ok=True)
            tmp_file_location = os.path.join(tmp_dir, dnaFile.filename)
            async with aiofiles.open(tmp_file_location, 'w') as out_file:
                raw_content = await dnaFile.read()
                content = raw_content.decode("utf-8")
                await out_file.write(content)
            parsed_seqs = parse(tmp_file_location)
            os.remove(tmp_file_location)
            self.dna_sequences = parsed_seqs
            self.file_uploaded = True
            return {'successfully_uploaded': True}
        except Exception as e:
            return {'successfully_uploaded': False, 'error': e}

# for now we only expect 1 user, just use this object to keep track of the data
# if we wanted to scale to multiple users, we would need to keep track in a database, or data structure stored in memory (risky)
dna_sequence_tracker = DNASequenceTracker()


@apiapp.get("/reset", response_model=models.Reset)
def reset_data():
    # For now we only expect 1 user. This endpoint will be called to reset the data whenever the user refreshes the website.
    dna_sequence_tracker.reset()
    return {"data_reset": True}

@apiapp.get("/amino_acids", response_model=models.AminoAcids)
def get_amino_acids():
    """Get the list of amino acids"""
    return dna_sequence_tracker.get_amino_acids()

@apiapp.get("/mRNA", response_model=models.MRNA)
def get_mrna():
    """Get the transcribed mRNA sequence"""
    return dna_sequence_tracker.get_mRNA_sequence()

@apiapp.get("/dnaSequence", response_model=models.DNASequence)
def get_dna_sequence():
    """Get the aligned DNA sequence from the uploaded dna strand files."""
    return dna_sequence_tracker.get_dna_sequence()

@apiapp.post("/upload", response_model=models.Upload)
async def upload_file(dnaFile: UploadFile):
    """handle uploaded file from user and parse the sequences and store them into dna_sequence_tracker"""
    return await dna_sequence_tracker.upload_file(dnaFile)



if __name__ == '__main__':
    uvicorn.run('app:apiapp', host="0.0.0.0", port=PORT)
