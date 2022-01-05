import sys, os, shutil
from zipfile import ZipFile

file = sys.argv[1]

print(f"Extracting dataset files from {sys.argv[1]}.")

with ZipFile(str(file), 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()
   print("NCBI dataset files successfully extracted.")

cwd = os.getcwd()

data_path = os.path.join(cwd, "ncbi_dataset", "data")

final_path = os.path.join(cwd, "ncbi_dataset")

FASTA_counter = 0 # Used to count extracted protein FASTA files.
NA_list = [] # Used to 

for counter, file in enumerate(os.listdir(data_path)): # Gets each of the available files and directories on the data folder from a list.
	file_path = os.path.join(data_path, file) # Determines the path of each file and directory.
	print(f"Analysing {counter + 1} out of {len(os.listdir(data_path))} files...") 
	if os.path.isdir(file_path): # Checks if the path leads to a directory.
		FASTA_counter += 1
		try:
			faa_original = os.path.join(file_path, "protein.faa") # Determines the original path of the FASTA file.
			faa_path = os.path.join(final_path, f'{file}.faa') # Determines the final path of the FASTA file, located on "ncbi_dataset" directory.
			os.rename(faa_original, faa_path) # Moves the FASTA file to its final location.
			print(f'FASTA file for {file} strain proteins moved to "ncbi_dataset" directory.')
		except Exception as e:
			NA_list.append(file)
			print(f'FASTA file for {file} strain not extracted: an error occurred. Reason: {e}')
			continue	

print(f'Analysis completed. Protein FASTA files for {FASTA_counter - len(NA_list)} strains extracted.')
if len(NA_list) != 0:
	print(f'{len(NA_list)} FASTA files were missing or corrupted. The following strains were compromised:')
	print(NA_list)

shutil.rmtree(data_path)