import os, shutil

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

path = "~/databases/protein_faa_reps"
namesFile = "~/databases/protein_faa_reps/list_of_hit_proteins_codes.txt"

#Reads each line and adds it to a list

with open(namesFile, "r") as f:
    data = f.read().splitlines()

#Trys to make the directory if it does not already exist

try:

    os.mkdir(path + "/new_seqs_directory")
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

    
for fileName in data:
    print("Looking for: " + fileName + "_protein.faa ...")
    x = find(fileName + "_protein.faa", path + "/bacteria")
    if x != None:
        print(x + " found!")
        shutil.copy(x, path + "/new_seqs_directory" )
    else:
        print("Not found")

