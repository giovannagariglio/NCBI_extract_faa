from ftplib import FTP
import sys, os

"""
This program downloads FASTA aminoacid (faa) files for user specified bacteria from NCBI's FTP server.

When trying to download large amounts of files, a connection error has been ocurring.
For this reason, I expect to make an updated version using rsync on Unix, currently recommended by NCBI 
(https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/#symlinks) for large data sets, which could solve the problem.
I intend to do it by getting the names from the list of strains and closing the FTP connection to avoid having the host computer kill it.
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
ftp = FTP('ftp.ncbi.nlm.nih.gov') # connect to host, default port
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

# the following code creates an OS directory to store downloaded faa files 
protein_folder = bacteria + "_faa"
print("Creating bacteria faa directory (" + protein_folder +") in current OS directory...")
os.mkdir(protein_folder)
print("Folder successfully created. Starting downloads...")
os.chdir(protein_folder)

for strain in list_of_strains:
	# some directories might have other files or directories other than the strain directories, which inevitably appear on the created list 
	if "GCF" in strain: # allows only strain directories to be considered
		try:
			print("Downloading " + strain + " faa file...")
			ftp.cwd(ftp_origin + "/" + strain) # changes to strain's directory
			filename = strain + "_protein.faa.gz" # sets target file name
			with open(filename, "wb") as f: # opens and closes target file
				ftp.retrbinary('RETR '+ filename, f.write) # downloads target file while open
			print("File successfully downloaded.")
		except Exception as e: # ensures the code keeps running even if a strain doesn't have an available faa file
			print("FASTA file for " + strain + " not extracted: an error occurred. Reason:")
			"""
			print(e)
print("Downloads completed.")