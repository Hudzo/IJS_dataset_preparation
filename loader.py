import os
from subprocess import call


def load_unzip(dataset_info):
    
    print("")
    
    #Load
    print("Downloading...")
    if not os.path.exists(dataset_info[0] + '/' + dataset_info[0] + '.zip'):
        call(
            'wget "'+ dataset_info[1] + '" -P "' + dataset_info[0] + '/"',
            shell=True
        )
        print("Downloading done.\n")
    else:
        print("Dataset already downloaded. Did not download twice.\n")
      
        
    #Unzip
    print("Extracting...")
    extract_directory = os.path.abspath(dataset_info[0] + '/' + dataset_info[0])
    if(dataset_info[0] == "WARD1"):
        extract_directory = extract_directory + '.0'
    if not os.path.exists(extract_directory):
        call(
            'unzip -nq "' + dataset_info[0] + '/' + dataset_info[0] + '.zip"',
            shell=True
        )
        print("Extracting successfully done to {}.".format(extract_directory))
    else:
        print("Dataset already extracted. Did not extract twice.\n")
    
        
        
def dataset_loader(dataset_name):
    
    #get index from name
    names = {"ward1":0, "opportunityucidataset":1 }
    
    #name of the dataset and the download link
    info = [["WARD1", "https://people.eecs.berkeley.edu/~yang/software/WAR/WARD1.zip"],
            ["OpportunityUCIDataset","https://archive.ics.uci.edu/ml/machine-learning-databases/00226/OpportunityUCIDataset.zip"]]
    
    load_unzip(info[names[dataset_name.lower()]])
    
    
    
    
    
    
    
    
    