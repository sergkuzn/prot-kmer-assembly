# Info
This work was created by several people as a university course project. I was mainly in charge of the protein assembly algorithm ([scs.py](https://github.com/sergkuzn/prot-kmer-assembly/blob/main/group3_package/src/scs.py), [scs_utils.py](https://github.com/sergkuzn/prot-kmer-assembly/blob/main/group3_package/src/scs_utils.py), [heap_utils](https://github.com/sergkuzn/prot-kmer-assembly/blob/main/group3_package/src/heap_utils.py)). Additionally, I implemented interaction with the website of a service using Selenium since its officia API was working pourly ([blast.py](https://github.com/sergkuzn/prot-kmer-assembly/blob/main/group3_package/src/blast.py)). The project remains unaltered since its submission and is published here in the same state without being polished.

----- End of Info -----

# To start the backend server and frontend server:
- first check that the ports specified in docker-compose.yml are available on your machine.
- For production (Bruce): ```docker-compose up --build``` 
- For development: ```docker-compose up```
- If changes are made to any Dockerfiles, rebuild:  ```docker-compose up --build```
## The frontend website is currently running at: ```http://localhost:8080/```

# For testing the Backend CLI from inside of the Docker container:
1. Launch the Backend Server: ```docker-compose up```
2. While the container is running (look above^ on how to run the container):
```docker exec -it group3_api_1 sh -c "exec bash"``` 
This will start an interactive bash shell inside of the backend's running docker container. There you can run any python commands, including click cli commands.
# For testing the Backend CLI from your terminal
Just install our python package in an empty virtual environment with python3.6 or higher, 
from the root directory of the project:```pip install -e group3_package```

## CLI commands:
Example: src run-parser --fastq-file path_to_my_file
1. run_parser:
Arguments: fastq-file (required)
Functionality: parse the fastq
output: DNA sequence

2. quick_assemble:
Arguments: input-list DNA (required)
Functionality: parse the list of DNA
output: assembled DNA sequence


3. slow_assemble:
Arguments: input-list DNA (required)
Functionality: parse given list of DNA
output: assembled DNA sequence


4. transcribe_dna:
Arguments: input-dna (required)
Functionality: transcribe the given DNA sequence
output: mRNA sequence

5. translate_rna:
Arguments: input-mrna (required)
Functionality: translate given mRNA
output: amino-acids

6. run:
Arguments: file (required), algo, chrome
Functionality: find proteins for given file with reads
output: protein list
```
# "run" command example (for --chrome Chrome needs to be installed, otherwise it is slow)
cd group3
src run --chrome --file group3_package/tests/data/Homo_sapiens_CXCR5_sequence_len100_cov10.fa
```

# What our package does:
Our package allows you to upload a dna file, and as an end result see a list of amino acids and their predicted proteins. To accomplish this, we
take an uploaded dna file, parse the file for the dna sequences, and perform de novo sequence assembly using an optimized greedy scs + max heap approach.
For larger fastq files, we have also implemented a parallelized version of the sequence assembly which has been observed to offer up to 30% speed increase.
After the de novo sequence assembly has been performed, we perform transcription of the DNA sequence into mRNA, and then translation of the mRNA into
amino acids. We then make a query to the NCBI BLAST REST API ```https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=DeveloperInfo```
to obtain a list of predicted proteins for our amino acids.

# System Design
- Frontend: Vue.js (Javascript framework)
- API: FastAPI
- Backend: Python Package
- Containerization: Docker
- Because the Vue.js runs on a separate server from our backend python code, we decided we would need to build an API for communication between our python
package and our frontend. To do this we chose to use FastAPI, and built this API into our python package. For containerization, we built a docker-compose file
which has 2 services:
1. A backend service, which has our python package installed, and runs the FastAPI server.
2. A frontend service, which runs our Vue.js server
- Due to observed stability issues while allocating more cpu's Docker (when the Docker kernel detects that the host machine has run out of memory, it starts killing its containers)
we left out the option to parallelize Greedy SCS initial pairwise calculations in the Full Stack Application. 


