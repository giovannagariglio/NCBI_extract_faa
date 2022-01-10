from ftplib import FTP
import sys, os

os_cwd = os.getcwd() # get os current working directory

bacteria = "Treponema_pallidum"

print("Connecting to NCBI's FTP server...")
ftp = FTP('ftp.ncbi.nlm.nih.gov') # connect to host, default port

print("Connected. Logging in as anonymous...")
ftp.login() # user anonymous, passwd anonymous@

print("Logged in. Changing to bacteria refseq directory.")
ftp.cwd("genomes/refseq/bacteria/" + bacteria + "/all_assembly_versions") # change working directory to Treponema pallidum's refseq directory with all available assembly versions
ftp_origin = ftp.pwd()

print("Success. Getting strains...")
list_of_strains = ftp.nlst() # creates a list with all available strains in the directory

protein_folder = bacteria + "_faa"
print("Creating bacteria faa folder (" + protein_folder +") in current OS directory...")
os.mkdir(protein_folder)
print("Folder successfully created. Starting downloads...")
os.chdir(protein_folder)

for strain in list_of_strains:
	if "GCF" in strain:
		try:
			print("Downloading " + strain + " faa file...")
			ftp.cwd(ftp_origin + "/" + strain) # changes to strain's directory
			filename = strain + "_protein.faa.gz" # sets target file name
			with open(filename, "wb") as f:
				ftp.retrbinary('RETR '+ filename, f.write)
			print("File successfully downloaded.")
		except Exception as e:
			print("FASTA file for " + strain + " not extracted: an error occurred. Reason:")
			print(e)
print("Downloads completed.")

'''
print("Testing " + list_of_strains[0])
ftp.cwd(ftp_origin + "/" + list_of_strains[0]) # changes to first strain directory
filename = list_of_strains[0] + "_protein.faa.gz"

print("Downloading protein (faa) file...")
with open(filename, "wb") as f:
	ftp.retrbinary('RETR '+ filename, f.write)
print("File successfully downloaded.")
'''