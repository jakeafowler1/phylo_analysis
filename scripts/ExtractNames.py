#This script is to find the taxonomic labels ie. species, class, order (s__, c__,o__) etc. from the bac120 file downloaded from GTDB and insert them in place of the existing
from re import *
import time
import os

#Change these file locations as desired
fNameTree = '//nobackup//cm16jf//databases//protein_faa_reps//group3_seqs//group3_hits_2.aln.nwk' #file you would like to alter
fNameBac = '//nobackup//cm16jf//databases//taxonomy//bac120_taxonomy.tsv' # bac120 taxonomy file
fNameGeneral = '//nobackup//cm16jf//databases//protein_faa_reps//bacteria//' # GTDB database of protein_faa_reps
extension = "_protein.faa" # Extension of the protein files

# Open tree file and read contents, then close
f = open(fNameTree, "r")
contents = f.read()
f.close()

# Extracts the codes based on the fact it starts with any number of char from a-z or A-Z or any number from 0-9,
# then any numbr of numbers from 0-9, then a '_', before finaly any number of numbers from 0-9. Gives them all in
# a list format.
ExtractedStrings = findall("[a-zA-Z0-9]*\.[0-9]*\_{1}[0-9]*", contents)

# These are the codes that need to be replaced!
print("Extracted " + str(len(ExtractedStrings)) + " codes from file.")
#print(ExtractedStrings)

# Open bacteria file and read contents, then close.
f = open(fNameBac, "r")
contentsBac = f.read()
f.close()

# Extract all the filenames that need to be read and the name you want to change it too
code = findall("[a-zA-Z0-9]*\_[a-zA-Z0-9]*\_[0-9]*\.[0-9]*", contentsBac)

#Change the inital letter here to give a differnt name
name = findall("p\_\_[a-zA-Z0-9\- ]*", contentsBac) #search for phylum
name2 = findall("s\_\_[a-zA-Z0-9\- ]*", contentsBac) #search for species

# These two lengths must be the same in order for it to work
print(len(code))
print(len(name))

# Make a copy of the tree contents to be changed and define some counters
newContents = contents
found = 0 
notfound = 0
counter = 0 #Counters overall iterations

for c in code:

    # Generates the file name to attemempt to open
    fNameSeach = str(fNameGeneral+c+extension)
    try:
        # Trys to open the file
        currFile = open(fNameSeach, "r")
        # Notifies the user if it has been found
        print("Found " + fNameSeach)
        # Outputs whole file into variable
        contentsCurr = currFile.read()

        # Loops through every extracted string from the tree file
        for extStr in ExtractedStrings:
            # If the extracted string is contained in the bacteria current file being read, then replace the code name with the bacteria name of choice
            if extStr in contentsCurr:
                print("Replace " + extStr + " with " + name[counter] + "_" + name2[counter])
                # This replaces the name, customise as you wish. Will replace each iteration.
                newContents = newContents.replace(extStr, extStr + name[counter] + "_" + name2[counter]) #replace GTDB protein >code with >code_phylum_species
                found += 1 #Tallys the number of found hits

        #Close the file
        currFile.close()
    except:
        # If the file does not exisit then add one to the not found counter
        notfound += 1
    
    counter += 1 # overall counter is increments, needed to obtain the name index in the try loop.

# Print the results and the tree
print(found)
print(notfound)
print(newContents)

#Writes it to a new file
file = open("/nobackup/cm16jf/databases/protein_faa_reps/treefiles/.aln", "w") #the name of the new file
file.write(newContents)
file.close()
