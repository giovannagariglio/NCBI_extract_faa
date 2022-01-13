# NCBI_extract_faa
Python script to download FASTA protein files from NCBI genome datasets.

Within the folder, 4 different scripts can be found. The species should be written as the following example for all of them: Neisseria_gonorrhoeae.

All of the scripts, except for NCBI_extract_faa.py, accept the species name as an optional argument (ie. NCBI_download_extract.py Neisseria_gonorrhoeae).

For NCBI_extract_faa.py, the folder which the files will be extracted from is an obligatory argument (ie. NCBI_extract_faa.py file.zip).

## NCBI_download_extract.py 
This is the most up-to-date script so far. It allows for the user to download refseq faa files for bacteria from the NCBI FTP server.

After downloading the files into a directory (Genus_species_faa), it proceeds to decompress them.

## NCBI_download_faa.py 
This script downloads refseq faa files for bacteria from the NCBI FTP server, without decompressing them.

## NCBI_download_faa_ftplib.py 
After a few tests, it was clear to me that NCBI's server has limits for either connection time or amount of files downloaded, 
after which it proceeds to disconnect the user, making it hard to download large amounts of files.

For that reason, this first version of the script, which downloads faa files within the FTP server, should be used only for small amounts of files (<100).

## NCBI_extract_faa.py 
NCBI currently has a beta version of a new way to download files from their database called "NCBI Datasets". 
This script allows for users to extract faa files from the folder provided by NCBI Datasets.
