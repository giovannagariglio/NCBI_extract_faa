from ftplib import FTP, error_perm
import requests
import sys, os, shutil
#import gzip

"""
This program downloads FASTA aminoacid (faa) files for user specified bacteria from NCBI's FTP server.
"""

if len(sys.argv) > 1: # checks if the user has called the species name as a system argument
	bacteria = sys.argv[1] # sets the name as the argument if true
else:
	bacteria = input("Species name: ") # asks for user input if the name hasn't been passed as an argument

while " " in bacteria: # checks if the argument was properly passed
	print("Species name should be written with '_' used as spaces, i.e. 'Treponema pallidum' becomes 'Treponema_pallidum'.")
	bacteria = input("Species name: ")

os_cwd = os.getcwd() # get os current working directory

print("Connecting to NCBI's FTP server...")
ftp = FTP('ftp.ncbi.nlm.nih.gov', timeout=900) # connect to host, default port; the high timeout allows for the code to run even if connection is poor
ftp.login() # user anonymous, passwd anonymous@

print("Connected.")
print("Changing to bacteria refseq directory...")

while True: # allows the user to try different species names until they succeed in finding one available on ncbi's database
	try:
		ftp.cwd("genomes/refseq/bacteria/" + bacteria + "/all_assembly_versions") # change working directory to Treponema pallidum's refseq directory with all available assembly versions
		break
	except:
		print("The specified bacteria was not found on NCBI's FTP server.") 
		bacteria = input("Species name: ")
ftp_origin = ftp.pwd() # here, ftp_origin means the folder in which all available strains can be found


print("Success. Getting strains...")
list_of_strains = ftp.nlst() # creates a list with all available strains in the directory
print("Strain list retrieved.")

# the following code creates an OS directory to store downloaded faa files 
protein_folder = bacteria + "_faa"
print("Creating bacteria faa directory (" + protein_folder +") in current OS directory...")
protein_dir = protein_folder
ftp.close()

attempts = 0
while True:
	try:
		os.mkdir(protein_dir)
		break
	except FileExistsError:
		attempts = attempts + 1
		protein_dir = protein_folder + "_" + str(attempts)

print("Folder successfully created. Starting downloads...")
print()
os.chdir(protein_dir)

for dir_name in list_of_strains:
	# some directories might have other files or directories other than the strain directories, which inevitably appear on the created list 
	if "GCF" not in dir_name: # allows for only strain directories to be considered
		list_of_strains.remove(dir_name)

for counter, strain in enumerate(list_of_strains):
	try:
		print("Downloading " + strain + " faa file...")
		ftp.cwd(ftp_origin + "/" + strain) # changes to strain's directory
		filename = strain + "_protein.faa.gz" # sets target file name
		with open(filename, "wb") as f: # opens and closes target file
			ftp.retrbinary('RETR '+ filename, f.write) # downloads target file while open
		print("File " + str(counter + 1) + " out of " + str(len(list_of_strains)) + " successfully downloaded.")
		print()
	except error_perm as e: # ensures the code keeps running even if a strain doesn't have an available faa file
		if "No such file or directory" in str(e):
			print("There are no available faa files for " + strain)
		else:
			print("File for " + strain + " not extracted: an error occurred. Reason:")
			print(str(e))
		print()
	except EOFError:
		print("Disconnected from the server.")

print("Downloads completed.")
